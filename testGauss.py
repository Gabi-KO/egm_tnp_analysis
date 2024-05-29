import os
import ROOT
from ROOT import TCanvas, TFile, gBenchmark, gStyle

# Make sure ROOT.TFile.Open(fileURL) does not seg fault when $ is in sys.argv (e.g. $ passed in as argument)
ROOT.PyConfig.IgnoreCommandLineOptions = True
# Make plots faster without displaying them
ROOT.gROOT.SetBatch(ROOT.kTRUE)
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

    # Get list of primitives from canvas
    primitives = list(c.GetListOfPrimitives())

    # Print primitives
    print("Primitives:")
    for p in primitives:
        print(" - {0}: {1}".format(type(p), p))

    # Load histogram
    hist_name = "htemp"
    h = c.GetPrimitive(hist_name)
    print("h: {0}".format(h))

    # Declare observable x
    x = ROOT.RooRealVar("x", "mass", 43, 137)

    # Import the histogram into a RooDataHist
    data = ROOT.RooDataHist("data", "dataset with x", ROOT.RooArgList(x), h)

    # Define the parameters for the Gaussian signal
    mean  = ROOT.RooRealVar("mean", "mean", 91.4, 43, 137)
    sigma = ROOT.RooRealVar("sigma", "sigma", 6.6, 0.1, 43)
    gauss = ROOT.RooGaussian("gauss", "Gaussian Signal", x, mean, sigma)

    # Define the parameters for the linear background
    a1 = ROOT.RooRealVar("a1", "a1", 0, -1, 1)
    linear_bkg = ROOT.RooPolynomial("linear_bkg", "Linear Background", x, ROOT.RooArgList(a1))

    # Define the yields for signal and background
    nsig = ROOT.RooRealVar("nsig", "number of signal events", 5000, 0, 10000)
    nbkg = ROOT.RooRealVar("nbkg", "number of background events", 5000, 0, 10000)

    # Construct the total model as a sum of the Gaussian signal and the linear background
    model = ROOT.RooAddPdf("model", "Gaussian Signal + Linear Background", ROOT.RooArgList(gauss, linear_bkg), ROOT.RooArgList(nsig, nbkg))

    # Fit the model to the data
    model.fitTo(data)

    # Create a canvas to display the results
    new_c = TCanvas("c", "Gaussian Fit with Linear Background", 1744, 800)

    # Set the statistics box options
    gStyle.SetOptStat("emr")  # Show entries, mean, and RMS

    # Draw the histogram with statistics box
    h.Draw()

    # Create a RooPlot to visualize the fit results
    xframe = x.frame(ROOT.RooFit.Title("Gaussian Fit with Linear Background"))

    # Plot the data and the fit result on the RooPlot
    data.plotOn(xframe)
    model.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Components("linear_bkg"), ROOT.RooFit.LineStyle(ROOT.kDashed))
    model.plotOn(xframe, ROOT.RooFit.Components("gauss"), ROOT.RooFit.LineStyle(ROOT.kDotted))

    # Draw the RooPlot on the canvas
    xframe.Draw("same")

    # Define plot name
    if cuts:
        plot_name = "{0}/{1}_{2}.pdf".format(plot_dir, variable, cuts)
    else:
        plot_name = "{0}/{1}_{2}.pdf".format(plot_dir, variable, cuts)

    new_c.Update()

    # Save the canvas as an image file
    plot_name = "{0}/gaussian_fit_with_background.pdf".format(plot_dir)
    new_c.SaveAs(plot_name)

    gBenchmark.Show('gaussfit')

    # Delete objects
    del f
    del c
    del new_c

if __name__ == "__main__":
    filename = "mass_hist.root"
    fit_gaussian_with_background(filename, "mass")
