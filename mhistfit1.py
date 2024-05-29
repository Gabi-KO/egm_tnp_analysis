import os
import ROOT
from ROOT import TCanvas, TFile, gBenchmark, gStyle, gROOT, RooRealVar, RooDataHist, RooArgList, RooGaussian, RooPolynomial, RooAddPdf, RooFit

# Make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# Make plots faster without displaying them
gROOT.SetBatch(ROOT.kTRUE)
# Tell ROOT not to be in charge of memory, fix issue of histograms being deleted when ROOT file is closed:
ROOT.TH1.AddDirectory(False)

# Create directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
       os.makedirs(dir_name)

# Fit gaussian with background
def fit_gaussian_with_background(file_name, variable, cuts = ""):
    plot_dir = "plots"
    makeDir(plot_dir)

    # Load canvas from root file
    canvas_name = "Canvas_1"
    f = TFile(file_name)
    c = f.Get(canvas_name)

    # Check for errors when loading canvas
    if not c:
        print("ERROR: Unable to load this canvas: {0}".format(canvas_name))
        f.Close()
        return

    # Load histogram
    hist_name = "htemp"
    h = c.GetPrimitive(hist_name)
    #print(h)
    if not h:
        print("ERROR: Unable to load histogram: {0}".format(hist_name))
        f.Close()
        return

    #print("Histogram entries: {0}".format(h.GetEntries()))

    # Declare observable x with the histogram's range
    x = RooRealVar("x", "invariant mass (GeV)", 50, 130) #43, 137

    # Import the histogram into a RooDataHist
    data = RooDataHist("data", "dataset with x", RooArgList(x), h)

    # Define the parameters for the Gaussian signal
    mean  = RooRealVar("mean", "mean", 91.4, 60, 115) #49.58, 130.42
    sigma = RooRealVar("sigma", "sigma", 6.6, 0.1, 49.58)
    gauss = RooGaussian("gauss", "Gaussian Signal", x, mean, sigma)


    # define parameters for 2nd  gaussian
    mean2 = RooRealVar("mean2", "mean2", 91, 75, 105)
    sigma2 = RooRealVar("sigma2", "sigma2", 6.6, 0.1, 50)
    gauss2 = RooGaussian("gauss2", "Gaussian Signal 2", x, mean2, sigma2)

    # Define the parameters for the linear background
    a1 = RooRealVar("a1", "a1", 0, -1, 1)
    linear_bkg = RooPolynomial("linear_bkg", "Linear Background", x, RooArgList(a1))

    # Define the yields for signal and background
    nsig = RooRealVar("nsig", "number of signal events", 5000, 0, 10000)
    nsig2 = RooRealVar("nsig2", "number of signal events", 5000, 0, 10000)
    nbkg = RooRealVar("nbkg", "number of background events", 5000, 0, 10000)
   

    # Construct the total model as a sum of the Gaussian signal and the linear background
    model = RooAddPdf("model", "Double Gaussian Signal + Linear Background", RooArgList(gauss, gauss2, linear_bkg), RooArgList(nsig, nsig2, nbkg))

    # Fit the model to the data
    model.fitTo(data)

    # Create a canvas to display the results
    new_c = TCanvas("new_c", "Gaussian Fit with Linear Background", 1744, 800)
    new_c.cd()

    # Set the statistics box options
    gStyle.SetOptStat("emr")  # Show entries, mean, and RMS

    # Draw the histogram with statistics box
    h.Draw()

    # Create a RooPlot to visualize the fit results
    xframe = x.frame(RooFit.Title("Gaussian Fit with Linear Background"))

    # Plot the data and the fit result on the RooPlot
    data.plotOn(xframe)
    model.plotOn(xframe) #double gaussian
    model.plotOn(xframe, RooFit.Components("linear_bkg"), RooFit.LineStyle(ROOT.kDashed), RooFit.LineColor(ROOT.kBlack)) #linear background
    model.plotOn(xframe, RooFit.Components("gauss"), RooFit.LineStyle(ROOT.kDotted), RooFit.LineColor(ROOT.kGreen)) #first gaussian
    model.plotOn(xframe, RooFit.Components("gauss2"), RooFit.LineStyle(ROOT.kDotted), RooFit.LineColor(ROOT.kRed)) #second gaussian


    # Draw the RooPlot on the canvas, overlaying it on the histogram
    xframe.Draw("same")

    #set up weird extra frame for chi2 calculation
    xframe_gauss = x.frame(ROOT.RooFit.Title("Combined Gaussian Fit"))
    data.plotOn(xframe_gauss)
    model.plotOn(xframe_gauss, ROOT.RooFit.Components("gauss,gauss2"), ROOT.RooFit.LineStyle(ROOT.kSolid))
    chi2_gauss = xframe_gauss.chiSquare()
    

    # add parameters box
    stats_box = ROOT.TPaveText(0.7, 0.7, 0.9, 0.4, "NDC")
    stats_box.SetFillColor(0)
    stats_box.AddText("Parameter Stats")
    stats_box.AddText(f"Mean: {mean.getValV():.2f} +/- {mean.getError():.2f}")
    stats_box.AddText(f"Sigma: {sigma.getValV():.2f} +/- {sigma.getError():.2f}")
    stats_box.AddText(f"nsig: {nsig.getValV():.0f} +/- {nsig.getError():.0f}")
    stats_box.AddText(f"nbkg: {nbkg.getValV():.0f} +/- {nbkg.getError():.0f}")
    stats_box.AddText(f"Mean 2: {mean2.getValV():.2f} +/- {mean2.getError():.2f}")
    stats_box.AddText(f"Sigma 2: {sigma2.getValV():.2f} +/- {sigma2.getError():.2f}")
    chi2 = xframe.chiSquare()
    stats_box.AddText(f"Chi2/NDF: {chi2:.2f}")
    stats_box.AddText(f"Chi2/NDF (Gaussians): {chi2_gauss:.2f}")
    stats_box.Draw()

    # Update canvas to show statistics box
    new_c.Update()

    # Print entries in the histogram to verify
    #print("Updated Histogram entries: {0}".format(h.GetEntries()))

    # Define plot name
    if cuts:
        plot_name = "{0}/{1}_{2}.pdf".format(plot_dir, variable, cuts)
    else:
        plot_name = "{0}/{1}.pdf".format(plot_dir, variable)

    # Save the canvas as an image file
    new_c.SaveAs(plot_name)

    #activate stats box
    gBenchmark.Show('gaussfit')

    # Delete objects
    del f
    del c
    del new_c

if __name__ == "__main__":
    filename = "mass_hist.root"
    fit_gaussian_with_background(filename, "Z_Mass_GaussFit")

