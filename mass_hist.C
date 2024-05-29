#ifdef __CLING__
#pragma cling optimize(0)
#endif
void Canvas()
{
//=========Macro generated from canvas: tcanvas1/tcanvas1
//=========  (Fri May 24 16:48:22 2024) by ROOT version 6.26/06
   TCanvas *tcanvas1 = new TCanvas("tcanvas1", "tcanvas1",0,0,4,28);
   tcanvas1->Range(0,0,1,1);
   tcanvas1->SetBorderMode(0);
   tcanvas1->SetBorderSize(0);
   tcanvas1->SetFrameFillColor(0);
   tcanvas1->SetFrameBorderMode(0);
   
   TH1F *mass__1 = new TH1F("mass__1","mass",100,43,137);
   mass__1->SetBinContent(8,11);
   mass__1->SetBinContent(9,25);
   mass__1->SetBinContent(10,26);
   mass__1->SetBinContent(11,28);
   mass__1->SetBinContent(12,26);
   mass__1->SetBinContent(13,17);
   mass__1->SetBinContent(14,23);
   mass__1->SetBinContent(15,22);
   mass__1->SetBinContent(16,20);
   mass__1->SetBinContent(17,27);
   mass__1->SetBinContent(18,20);
   mass__1->SetBinContent(19,25);
   mass__1->SetBinContent(20,23);
   mass__1->SetBinContent(21,27);
   mass__1->SetBinContent(22,24);
   mass__1->SetBinContent(23,26);
   mass__1->SetBinContent(24,11);
   mass__1->SetBinContent(25,14);
   mass__1->SetBinContent(26,24);
   mass__1->SetBinContent(27,15);
   mass__1->SetBinContent(28,24);
   mass__1->SetBinContent(29,20);
   mass__1->SetBinContent(30,23);
   mass__1->SetBinContent(31,23);
   mass__1->SetBinContent(32,18);
   mass__1->SetBinContent(33,20);
   mass__1->SetBinContent(34,15);
   mass__1->SetBinContent(35,22);
   mass__1->SetBinContent(36,19);
   mass__1->SetBinContent(37,16);
   mass__1->SetBinContent(38,15);
   mass__1->SetBinContent(39,24);
   mass__1->SetBinContent(40,24);
   mass__1->SetBinContent(41,25);
   mass__1->SetBinContent(42,32);
   mass__1->SetBinContent(43,41);
   mass__1->SetBinContent(44,72);
   mass__1->SetBinContent(45,67);
   mass__1->SetBinContent(46,88);
   mass__1->SetBinContent(47,115);
   mass__1->SetBinContent(48,151);
   mass__1->SetBinContent(49,153);
   mass__1->SetBinContent(50,174);
   mass__1->SetBinContent(51,226);
   mass__1->SetBinContent(52,247);
   mass__1->SetBinContent(53,172);
   mass__1->SetBinContent(54,137);
   mass__1->SetBinContent(55,95);
   mass__1->SetBinContent(56,77);
   mass__1->SetBinContent(57,44);
   mass__1->SetBinContent(58,32);
   mass__1->SetBinContent(59,25);
   mass__1->SetBinContent(60,24);
   mass__1->SetBinContent(61,15);
   mass__1->SetBinContent(62,12);
   mass__1->SetBinContent(63,25);
   mass__1->SetBinContent(64,16);
   mass__1->SetBinContent(65,14);
   mass__1->SetBinContent(66,17);
   mass__1->SetBinContent(67,16);
   mass__1->SetBinContent(68,9);
   mass__1->SetBinContent(69,6);
   mass__1->SetBinContent(70,17);
   mass__1->SetBinContent(71,10);
   mass__1->SetBinContent(72,8);
   mass__1->SetBinContent(73,7);
   mass__1->SetBinContent(74,10);
   mass__1->SetBinContent(75,6);
   mass__1->SetBinContent(76,10);
   mass__1->SetBinContent(77,8);
   mass__1->SetBinContent(78,10);
   mass__1->SetBinContent(79,8);
   mass__1->SetBinContent(80,6);
   mass__1->SetBinContent(81,6);
   mass__1->SetBinContent(82,6);
   mass__1->SetBinContent(83,3);
   mass__1->SetBinContent(84,6);
   mass__1->SetBinContent(85,5);
   mass__1->SetBinContent(86,8);
   mass__1->SetBinContent(87,3);
   mass__1->SetBinContent(88,7);
   mass__1->SetBinContent(89,3);
   mass__1->SetBinContent(90,5);
   mass__1->SetBinContent(91,4);
   mass__1->SetBinContent(92,6);
   mass__1->SetBinContent(93,5);
   mass__1->SetEntries(2991);
   mass__1->SetDirectory(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   mass__1->SetLineColor(ci);
   mass__1->GetXaxis()->SetRange(1,100);
   mass__1->GetXaxis()->SetLabelFont(42);
   mass__1->GetXaxis()->SetTitleOffset(1);
   mass__1->GetXaxis()->SetTitleFont(42);
   mass__1->GetYaxis()->SetLabelFont(42);
   mass__1->GetYaxis()->SetTitleFont(42);
   mass__1->GetZaxis()->SetLabelFont(42);
   mass__1->GetZaxis()->SetTitleOffset(1);
   mass__1->GetZaxis()->SetTitleFont(42);
   mass__1->Draw("");
   tcanvas1->Modified();
   tcanvas1->cd();
   tcanvas1->SetSelected(tcanvas1);
}
