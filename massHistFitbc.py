import os
import ROOT
from ROOT import TCanvas, TFile, gBenchmark, gStyle, gROOT, RooRealVar, RooDataHist, RooArgList, RooGaussian, RooPolynomial, RooAddPdf, RooFit


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

def analyze(file_name, variable, cuts = ""):
    print("file name: {0}".format(file_name))

    plot_dir = "plots"
    makeDir(plot_dir)

    # Load canvas from root file
    canvas_name = "Canvas_1"
    f = ROOT.TFile(file_name)
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


    hist_name = "htemp"
    h = c.GetPrimitive(hist_name)
    print("h: {0}".format(h))
    
    x = ROOT.RooRealVar("x", "invarent mass [GeV]", 49.58, 130.42)
    
    data = ROOT.RooDataHist("data", "dataset with x", ROOT.RooArgList(x), h)

    #  mean = ROOT.RooRealVar("mean", "mean", 91, 49.58, 130.42)
    # sigma = ROOT.RooRealVar("sigma", "width", 6.6, 0.1, 50)
    # gauss = ROOT.RooGaussian("gauss", "gaussian PDF", x, mean, sigma)
    mean = ROOT.RooRealVar("mean", "mean", 91, 49.58, 130.42)
    sigma = ROOT.RooRealVar("sigma", "width", 6.6, 0.1, 50)
    gauss1 = ROOT.RooGaussian("gauss1", "gaussian1 PDF", x, mean, sigma)

    mean2 = ROOT.RooRealVar("mean2", "mean2", 91, 70, 110)
    sigma2 = ROOT.RooRealVar("sigma2", "width2", 6.6, 0.1, 50)
    gauss2 = ROOT.RooGaussian("gauss2", "gaussian2 PDF", x, mean2, sigma2)


    a0 = ROOT.RooRealVar("a1","a1",0,-1,1)
    a1 = ROOT.RooRealVar("a1","a1",0, -1, 1)
    linear_bkg = ROOT.RooPolynomial("linear_bkg", "Linear Background", x, ROOT.RooArgList(a1))

    nsig = ROOT.RooRealVar("nsig", "number of signal events", 5000, 0, 10000)
    nsig2 = ROOT.RooRealVar("nsig2", "number of signal events 2", 5000, 0, 10000)
    nbkg = ROOT.RooRealVar("nbkg", "number of background events", 5000, 0, 10000)

    model = ROOT.RooAddPdf("model", "Two Gaussian Signal + Linear Background", ROOT.RooArgList(gauss1,gauss2, linear_bkg),ROOT.RooArgList(nsig, nsig2, nbkg))
    # model2 = ROOT.RooAddPDF("model2", "Second Gaussian", ROOT.RooArgList(gauss2))

    model.fitTo(data)
    # model2.fitTo(data)

    new_c = ROOT.TCanvas("c", "Gaussian Fit with Linear Background", 800, 600)
    new_c.cd()


    xframe = x.frame(ROOT.RooFit.Title("Gaussian Fit with Linear Background to Invariant Mass"))

  

    data.plotOn(xframe)
    model.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Components("linear_bkg"), ROOT.RooFit.LineStyle(ROOT.kDashed))
    model.plotOn(xframe, ROOT.RooFit.Components("gauss1"), ROOT.RooFit.LineStyle(ROOT.kDotted))
    #model2.plotOn(xframe, ROOT.RooFit.Components("gauss2"), ROOT.RooFit.LineStyle(ROOT.kSolid))


    gStyle.SetOptStat("emr")
    h.Draw()

    xframe.Draw("same")
    
    stats_box = ROOT.TPaveText(0.7, 0.6, 1.0, 0.4, "NDC")
    stats_box.SetFillColor(0)
    stats_box.AddText(f"Mean: {mean.getValV():.2f} +/- {mean.getError():.2f}")
    stats_box.AddText(f"Sigma: {sigma.getValV():.2f} +/- {sigma.getError():.2f}")
    stats_box.AddText(f"nsig: {nsig.getValV():.0f} +/- {nsig.getError():.0f}")
    stats_box.AddText(f"nbkg: {nbkg.getValV():.0f} +/- {nbkg.getError():.0f}")

    chi2 = xframe.chiSquare()
    stats_box.AddText(f"Chi2/NDF: {chi2:.2f}")
    stats_box.Draw() 

    
    if cuts:
        plot_name = "{0}/{1}_{2}.pdf".format(plot_dir, variable, cuts)
    else:
        plot_name = "{0}/{1}.pdf".format(plot_dir, variable)

    new_c.Update()
    new_c.SaveAs(plot_name)

    gBenchmark.Show('gaussfit')

    del f
    del c
    del new_c





def main():
    file_name = "massHist.root"
    analyze(file_name, "mass")

if __name__ == "__main__":
    main()
