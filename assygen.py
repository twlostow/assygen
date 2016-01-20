#!/usr/bin/python

from gerber2pdf import *
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import csv

class PPComponent:
    def __init__(self,xc, yc, w, h, name, desc, ref):
        self.xc = xc
        self.yc = yc
        self.w = w
        self.h = h
        if(self.w == 0):
            self.w = 0.8 * mm

        if(self.h == 0):
            self.h = 0.8 * mm

        self.name = name
        self.desc = desc
        self.ref = ref



class PickAndPlaceFile:
    def split_parts(self, layer, index, n_comps):
        parts = [];
        n=0
        for i in sorted(self.layers[layer].iterkeys()):
            if(n >= index and n < index+n_comps):
                parts.append(self.layers[layer][i])
            n=n+1
        return parts

    def num_groups(self, layer):
        return len(self.split_parts(layer, 0, 10000))

    def draw(self, layer, index, n_comps, canv):
        parts = self.split_parts(layer, index, n_comps)
        n=0
        for i in parts:
            canv.setStrokeColor(self.col_map[n])
            canv.setFillColor(self.col_map[n])
            n=n+1
            for j in i:
                canv.rect(j.xc - j.w/2, j.yc-j.h/2, j.w, j.h, 1, 1)
    
    def gen_table(self, layer, index, n_comps,canv):
        parts = self.split_parts(layer, index, n_comps)

        yt = 260 * mm
        canv.setFont("Helvetica",10)
        canv.setStrokeGray(0)
        canv.setFillGray(0)
        canv.drawString(20 * mm, yt, "Color");
        canv.drawString(40 * mm, yt, "Lib.Reference");
        canv.drawString(80 * mm, yt, "Comment");
        canv.drawString(120 * mm, yt, "Designators");
        n=0
        for group in parts:
            dsgn = ""
            yt = yt - 6 * mm
            canv.setFillColor(self.col_map[n])
            canv.rect(20 *mm, yt, 10 * mm, 3 * mm, 1, 1)
            canv.setFillGray(0)
            n=n+1
            for part in group:
                dsgn = dsgn + " " + part.name
            canv.drawString(120 * mm, yt, dsgn);
            canv.drawString(40 * mm, yt, group[0].ref[0:20]);
            canv.drawString(80 * mm, yt, group[0].desc[0:20]);

#            table.append(["", dsgn, group[0].desc, group[0].ref])

   
    

class PickAndPlaceFileKicad(PickAndPlaceFile):
    def __init__(self, fname):
	print("Load")
	f= open(fname,'r')
	rows=[]
	for line in f:
	    rows.append(line.split())
	    

        self.col_map = [colors.Color(1,0,0), 
                  colors.Color(1,1,0), 
                  colors.Color(0,1,0), 
                  colors.Color(0,1,1), 
                  colors.Color(1,0,1), 
                  colors.Color(0,0,1)]

#	Ref    Val                  Package         PosX       PosY        Rot     Side


        i_dsg = rows[0].index("Ref")
        i_desc = rows[0].index("Val")
        i_cx = rows[0].index("PosX")
        i_cy = rows[0].index("PosY")
        i_layer = rows[0].index("Side")

        self.layers = {};
        self.layers["Top"] = {};        
        self.layers["Bottom"] = {};
       
	print(i_dsg, i_desc, i_cx, i_cy);
        for i in rows[1:]:
            if(len(i)>0):
		print(i[i_dsg], i[i_cx])
                cx = float(i[i_cx]) * mm
                cy = float(i[i_cy]) * mm

                w = 1 * mm
                h = 1 * mm
                l = i[i_layer]
		if l == "F.Cu":
		    layer = "Top"
		else:
		    layer = "Bottom"
                ref = i[i_desc]
#                print(ref,cy, py)
                if(not ref in self.layers[layer]):
                    self.layers[layer][ref] = []
                self.layers[layer][ref].append(PPComponent(cx, cy, w, h, i[i_dsg], i[i_desc], ref))


#class PickAndPlaceFileKicad(PickAndPlaceFile):
#    def __init__(self, fname):
#	print("Load")
#        reader = csv.reader(open(fname,'rb') ,delimiter=' ')
#        rows = []
#        for row in reader:
#            rows.append(row)
#
#        self.col_map = [colors.Color(1,0,0), 
#                  colors.Color(1,1,0), 
#                  colors.Color(0,1,0), 
#                  colors.Color(0,1,1), 
#                  colors.Color(1,0,1), 
#                  colors.Color(0,0,1)]
#
#        i_dsg = rows[0].index("Designator")
#        i_desc = rows[0].index("Description")
#        i_cx = rows[0].index("Center-X(mm)")
#        i_cy = rows[0].index("Center-Y(mm)")
#        i_px = rows[0].index("Pad-X(mm)")
#        i_py = rows[0].index("Pad-Y(mm)")
#        i_layer = rows[0].index("Layer")
#        i_ref = rows[0].index("LibRef")
#
#        self.layers = {};
#        self.layers["Top"] = {};        
#        self.layers["Bottom"] = {};
#       
#        for i in rows[1:]:
#            if(len(i)>0):
#                cx = float(i[i_cx]) * mm
#                cy = float(i[i_cy]) * mm
#                px = float(i[i_px]) * mm
#                py = float(i[i_py]) * mm
#                w = abs(cx-px) * 2
#                h = abs(cy-py) * 2
#                layer = i[i_layer]
#                ref = i[i_ref]
#                print(ref,cy, py)
#                if(not ref in self.layers[layer]):
#                    self.layers[layer][ref] = []
#                self.layers[layer][ref].append(PPComponent(cx, cy, w, h, i[i_dsg], i[i_desc], ref))

def renderGerber(base_name, layer, canv):
    global gerberExtents
    if(layer == "Bottom"):
        f_copper = base_name+".GBL"
        f_overlay = base_name+".GBO"
    else:
        f_copper = base_name+".GTL"
        f_overlay = base_name+".GTO"

    canv.setLineWidth(0.0)
    gm = GerberMachine( "", canv )
    gm.Initialize()
    ResetExtents()
    gm.setColors(colors.Color(0.85,0.85,0.85), colors.Color(0,0,0))
    gm.ProcessFile( f_copper )
    gm.setColors(colors.Color(0.5,0.5,0.5), colors.Color(0,0,0))
    return gm.ProcessFile( f_overlay )


def producePrintoutsForLayer(base_name, layer, canv):


    ctmp = canvas.Canvas(base_name + "_assy.pdf")
    ext = renderGerber(base_name, layer, ctmp);

    scale1 = (gerberPageSize[0]-2*gerberMargin)/((ext[2]-ext[0]))
    scale2 = (gerberPageSize[1]-2*gerberMargin)/((ext[3]-ext[1]))
    scale = min(scale1, scale2)
    gerberScale = (scale,scale)
#    print("PS" , gerberPageSize[0], gerberMargin, gerberScale)
    gerberOffset = (-ext[0]*scale + gerberMargin, -ext[1]*scale + gerberMargin)
#    print "Offset (in.): (%4.2f, %4.2f)" % (gerberOffset[0]/inch,gerberOffset[1]/inch)
#    print "Scale (in.):  (%4.2f, %4.2f)" % gerberScale



    pf = PickAndPlaceFileKicad(base_name+".CSV")
    ngrp =  pf.num_groups(layer)

    for page in range(0, (ngrp+5)/6):
        n_comps = min(6, ngrp - page*6)

        canv.saveState()
        canv.translate( gerberOffset[0], gerberOffset[1] )
        if(layer == "Bottom"):
            canv.scale( gerberScale[0], gerberScale[1] )
#            canv.scale( -1, 1 )
#            canv.translate(-0.5*gerberPageSize[0],0)
        else:
            canv.scale( gerberScale[0], gerberScale[1] )

        renderGerber(base_name, layer, canv);

        pf.draw(layer, page*6, n_comps, canv);

        canv.restoreState()
        pf.gen_table(layer, page*6, n_comps, canv);
        canv.showPage()

import sys
canv = canvas.Canvas(sys.argv[1]+"_assy.pdf")
#producePrintoutsForLayer(sys.argv[1], "Top", canv)
producePrintoutsForLayer(sys.argv[1], "Bottom", canv)
canv.save()