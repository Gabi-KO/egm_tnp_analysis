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
    if not h:
        print("ERROR: Unable to load histogram: {0}".format(hist_name))
        f.Close()
        return

    print("Histogram entries: {0}".format(h.GetEntries()))

    # Declare observable x
    x = RooRealVar("x", "mass", 43, 137)

    # Import the histogram into a RooDataHist
    data = RooDataHist("data", "dataset with x", RooArgList(x), h)

    # Define the parameters for the Gaussian signal
    mean  = RooRealVar("mean", "mean", 91.4, 43, 137)
    sigma = RooRealVar("sigma", "sigma", 6.6, 0.1, 43)
    gauss = RooGaussian("gauss", "Gaussian Signal", x, mean, sigma)

    # Define the parameters for the linear background
    a1 = RooRealVar("a1", "a1", 0, -1, 1)
    linear_bkg = RooPolynomial("linear_bkg", "Linear Background", x, RooArgList(a1))

    # Define the yields for signal and background
    nsig = RooRealVar("nsig", "number of signal events", 5000, 0, 10000)
    nbkg = RooRealVar("nbkg", "number of background events", 5000, 0, 10000)

    # Construct the total model as a sum of the Gaussian signal and the linear background
    model = RooAddPdf("model", "Gaussian Signal + Linear Background", RooArgList(gauss, linear_bkg), RooArgList(nsig, nbkg))

    # Fit the model to the data
    model.fitTo(data)

    # Create a canvas to display the results
    new_c = TCanvas("new_c", "Gaussian Fit with Linear Background", 1744, 800)

    # Set the statistics box options
    gStyle.SetOptStat("emr")  # Show entries, mean, and RMS

    # Draw the histogram with statistics box
    h.Draw()

    # Create a RooPlot to visualize the fit results
    xframe = x.frame(RooFit.Title("Gaussian Fit with Linear Background"))

    # Plot the data and the fit result on the RooPlot
    data.plotOn(xframe)
    model.plotOn(xframe)
    model.plotOn(xframe, RooFit.Components("linear_bkg"), RooFit.LineStyle(ROOT.kDashed))
    model.plotOn(xframe, RooFit.Components("gauss"), RooFit.LineStyle(ROOT.kDotted))

    # Draw the RooPlot on the canvas, overlaying it on the histogram
    xframe.Draw("same")

    # Update canvas to show statistics box
    new_c.Update()

    # Print entries in the histogram to verify
    print("Updated Histogram entries: {0}".format(h.GetEntries()))

    # Define plot name
    if cuts:
        plot_name = "{0}/{1}_{2}.pdf".format(plot_dir, variable, cuts)
    else:
        plot_name = "{0}/{1}.pdf".format(plot_dir, variable)

    # Save the canvas as an image file
    new_c.SaveAs(plot_name)

    gBenchmark.Show('gaussfit')

    # Delete objects
    del f
    del c
    del new_c

if __name__ == "__main__":
    filename = "mass_hist.root"
    fit_gaussian_with_background(filename, "mass")
