#!/usr/bin/env python
# {{{ Top

# {{{ Docs

"""
Copyright (c) 2011 Joseph C Chavez <jchavez@swcp.com>

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.

Introduction:

    This program converts Gerber files (used to fabricate printed circuit boards) 
    into a PDF document that can be viewed and printed with the freely available 
    Acrobat viewer.  Gerber files must conform to the RS-274X specification.  My 
    intention is to provide complete support for the full RS-274X specification.  
    However, this early version has seen only limited testing so far.  If you 
    find an example Gerber file that is not handled correctly, or discover bugs 
    in the program, please e-mail me at jchavez@swcp.com.

Dependencies:

    Python (Tested with version 2.6)      : http://www.python.org
    plex (Tested with version 2.0.0)      : http://pypi.python.org/pypi/plex/
    reportlab (Tested with release 2.5)   : http://www.reportlab.org
    
Usage:

    This program can be run as a stand-alone routine or imported as an external 
    module. Invoking the program stand-alone with no command line arguments 
    launches an interactive session that lets you specify the list of Gerber 
    files to be converted (wildcards are supported), and also the page size, 
    the scale, and the offset.  You also have the option of fitting the plot so 
    it fills the page, in which case the scale and offset are computed 
    automatically.  The files are converted to a single multi-page PDF document 
    named "gerber.pdf" (by default), which is placed in the same directory as 
    your Gerber files, with one page for each Gerber file.

    
    If command line arguments are provided, they are interpreted as Gerber 
    file path names (wildcards are supported).  The specified files are 
    converted to a single PDF document (one page per file) using the following 
    module variables:
    
          Variable         Default Value          Comment
        -----------        -------------------    -------
        gerberPageSize     8.5*inch, 11.0*inch    Width, Height
        
        gerberOutputFile   "gerber.pdf"           Default output file name
        
        gerberFitPage      0                      If true, automatically fit 
                                                  plot to page
                                                  
        gerberMargin       0.75*inch              Margin used if gerberFitPage
                                                  is true
                                                  
        gerberScale        1.0, 1.0               X scale, Y scale
        
        gerberOffset       0.0*inch, 0.0*inch     X offset, Y offset
        
    If a file named "gerber2pdf.cfg" exists in the same directory as the Gerber 
    files, its contents are executed as Python statements before translation 
    begins.  Therefore, you can use this file as a configuration file to change 
    the value of any of the above module variables. For example, this file could 
    contain something like this:
    
    gerberPageSize = (6.0*inch, 6.0*inch)
    gerberOffset = (1.0*inch, 1.0*inch)
    gerberOutputFile = "myGerberFileName.pdf"
    gerberScale = (1.0,1.0)
    
    Alternatively, if you wish to automatically fill the page with the plot, this
    file could contain something like this:
    
    gerberPageSize = (11.0*inch,8.5*inch)
    gerberFitPage = 1
    gerberMargin = 0.5*inch
    gerberOutputFile = "yourFileName.pdf"
    
    If you would prefer not to include all the Gerber file path names in the
    command line arguments, you can supply them in the configuration file by 
    including a command like this:
    
    fileList = [ file1.gbr, file2.gbr, file3.gbr ]
    
    If you import this program as an external module, you have access to the above 
    mentioned module variables and to the function Interact(), which launches the 
    interactive session described above.  You also have access to the function 
    Translate( gerberFileNameList ), which translates the specified list of Gerber 
    files into a PDF document using the current values of the module variables.
    
Home Directory:

    http://www.osmondpcb.com/gerber2pdf.html
   
Version History:
    Version 1.7 - January 14, 2011
    
       1) the latest version of plex (2.0.0) uses a lowercase 'p' for the module name
       2) exec on line 336 fails if the aperture macro contains dos newlines (\r\n)
       3) HandleLineCenter computes the coordinates incorrectly (cx and cy
          should not be multiplied by costheta/sintheta)
       Thanks to Igor Izyumin
        
	Version 1.6 - September 17, 2006
	
		Lines made with rectangular apertures are now handled correctly.  Polygon
		aperture definitions are now handled correctly.
		
    Version 1.5 - March 3, 2006
    
        Allow terminating M02 token without final asterisk.

    Version 1.4 - October 31, 2004
    
        Allow G74 and G75 blocks prior to aperture selection.

    Version 1.3 - March 29, 2004
    
        Fixed a problem with Python 2.3 by removing line termination characters from
        strings supplied to the eval function.

    Version 1.2 - March 28, 2004
    
        Outline macros and multi-line macros are now handled correctly.
        
        Macro primitives with trailing commas in their variable lists are now 
        handled correctly.
        
        Comment blocks beginning with "G4" are now handled correctly.

    Version 1.1 - October 7, 2003
    
        Thanks to Martin Thompson, macro definitions containing assignment
        operators now work correctly.

        Calculated extents and offsets are now expressed in inches.

    Version 1.0 - September 1, 2003
    
        Martin Thompson added the ability to automatically scale and offset the 
        plot to fill a given page size.
        
        Fixed a circular interpolation bug.
        
    Version 0.9 - July 26, 2003
    
        Fixed several problems with Polygon apertures.

    Version 0.8 - July 13, 2003
    
        Now handles the Mode command correctly.  Fixed a problem with some 
        polygon fills containing circular interpolation entities.  Now permits 
        value string lengths to extend beyond the strict limits set by the 
        Format Statement.
        
    Version 0.7 - July 12, 2003
        
        Now accepts negative numbers for aperture definition modifiers.

    Version 0.6 - March 10, 2003
    
        Handles zero width aperture.

    Version 0.5 - March 7, 2003
    
        Paths can now use rectangular apertures.
        
        D-codes with leading zeros are now handled correctly in aperture 
        definitions.
        
    Version 0.4 - February 22, 2003

        Fixed bugs within the AD block.  The program now correctly handles an
        aperture type that consists of a macro that requires no modifiers.
        Also, leading spaces are now permitted in aperture type modifiers.

        Fixed a bug with the circle aperture macro primitive.  The program now 
        correctly handles the exposure off condition.

        The program now correctly interprets the M2 code.

    Version 0.3 - January 11, 2003
    
        Within an FS block, if the L/T designator is not present, L is assumed;
        if the A/T designator is not present, A is assumed.
        
        During an interactive session, the configuration file (if present) is now 
        read correctly immediately after the Gerber file list is determined.
        
        Fixed a problem with the incorrect interpretation of the X operator in an
        Aperture Macro.
        
        Fixed a bug with outline and polygon macro elements.

    Version 0.2 - December 10, 2002
    
        Bug fix:  Initial G36 area fill block handled incorrectly.

    Version 0.1 - December 9, 2002
    
        Initial Release

"""

# }}}
# {{{ Imports
try:
    from plex import *
except:
    from Plex import *
import re
import math
import exceptions
import glob
import os.path
from reportlab.lib.units import inch, mm
# }}}
# {{{ Globals
gerberScale      = (1.0,1.0)
gerberOffset     = (0.0*inch,0.0*inch)
gerberPageSize   = (8.5*inch,11.0*inch)
gerberOutputFile = "gerber.pdf"
gerberFitPage = 0
gerberMargin = 0.75*inch
gerberExtents = [1e6,1e6,-1e6,-1e6] # xmin, ymin, xmax, ymax
# if you add things here don't forget to add them to the
# global lines in ReadConfiguration, Translate and Interact!!!

# }}}
# {{{ UpdateExtents
def UpdateCircleExtents(xc, yc, radius, thickness):
    UpdateExtents(xc-radius-thickness/2, yc-radius-thickness/2,
                  xc+radius+thickness/2, yc+radius+thickness/2)
def UpdateLineExtents(x1, y1, x2, y2, thickness):
    # xxx overcompensates for thickness
    if x1 > x2:
        t = x2
        x2 = x1
        x1 = t
    if y1 > y2:
        t = y2
        y2 = y1
        y1 = t
    UpdateExtents(x1-thickness,y1-thickness,x2+thickness,y2+thickness)
def UpdateArcExtents( x1, y1, x2, y2, startAngle, extent, thickness):
    # xxx doesn't do the arc bit right, pretends its a straight line! :-(
    UpdateLineExtents(x1, y1, x2, y2, thickness)
def ResetExtents():
    global gerberExtents
    gerberExtents = [1e6,1e6,-1e6,-1e6] # xmin, ymin, xmax, ymax

def UpdatePointExtents( x1, y1 ):
    global gerberExtents
    if x1 < gerberExtents[0]:
        gerberExtents[0] = x1
    if y1 < gerberExtents[1]:
        gerberExtents[1] = y1
    if x1 > gerberExtents[2]:
        gerberExtents[2] = x1
    if y1 > gerberExtents[3]:
        gerberExtents[3] = y1

def UpdateExtents(x1, y1, x2, y2):
    global gerberExtents
    if x1 > x2:
        t = x2
        x2 = x1
        x1 = t
    if y1 > y2:
        t = y2
        y2 = y1
        y1 = t
    if x1 < gerberExtents[0]:
        gerberExtents[0] = x1
    if y1 < gerberExtents[1]:
        gerberExtents[1] = y1
    if x2 > gerberExtents[2]:
        gerberExtents[2] = x2
    if y2 > gerberExtents[3]:
        gerberExtents[3] = y2
# }}}
# {{{ gerberError
class GerberError(exceptions.Exception):
    pass
# }}}
# {{{ GerberScanner
class GerberScanner(Scanner):

    macroDelim = Str("%AM")
    paramDelim = Str("%")
    comment = Seq( Str("G04") | Str("G4"), Rep(AnyBut("*\n\r")), Any( "*\n\r" ) )
    block = Seq( Rep(AnyBut("*%\n\r")), Str("*") ) | Str("M02") | Str("M2")
    mblock = Seq( Rep(AnyBut("*%")), Str("*") )
    lineEnd = Str("\n\r") | Str("\n") | Str("\r")

    lexicon = Lexicon( [
        ( comment, IGNORE ),
        ( macroDelim, Begin('macro') ),
        ( paramDelim, Begin('param') ),
        ( block, "block" ),
        ( lineEnd, IGNORE ),
        State('macro', [
            ( paramDelim, Begin( '' ) ),
            ( mblock, "mblock" ),
            ( lineEnd, IGNORE )
        ]),
        State('param', [
            ( paramDelim, Begin( '' ) ),
            ( block, "pblock" ),
            ( lineEnd, IGNORE )
        ])
    ])

    def __init__(self, file, name):
        Scanner.__init__(self, self.lexicon, file, name )
# }}}
# {{{ Stump
class Stump:
    pass
# }}}
# {{{ MacroEquation
class MacroEquation:

    def __init__( self, str ):
        str=str.replace("*", "")
        str = str.replace("$","stump._Star_")
        str = str.replace("x","*")
        self.equation = str.replace("X","*")
        
    def Doit( self, stump ):
        exec( self.equation.strip() )
# }}}
# {{{ PrimitiveDefinition
class PrimitiveDefinition:

    def __init__( self, str ):
        str = str.strip()
        params = str.split(",")
        self.items = []
        for str in params:
            str = str.replace("*","")
            str = str.replace("x","*")
            str = str.replace("X","*")
            str = str.replace("$","stump._Star_")
            if str:
                self.items.append( str )
    
    def Doit( self, stump ):
        return map( eval, self.items )                
# }}}
# {{{ MacroDefinition
class MacroDefinition:

    def __init__( self ):
        self.items = []
        
    def NewMacro( self, params ):
        stump = Stump()
        macro = Macro()
        for i in range(len(params)):
            attr = "_Star_%d" % (i+1)
            setattr( stump, attr, eval(params[i]) )
            
        for item in self.items:
            result = item.Doit( stump )
            if result:
                macro.items.append( result )
        return macro
# }}}
# {{{ Macro

class Macro:
    # {{{ __INIT__
    def __init__( self ):
        self.items = []
        self.rectangular = False
    # }}}
    # {{{ HandleCircle

    def HandleCircle( self, gm, parameters ):
        c,x,y,unit = gm.canv,gm.x,gm.y,gm.unit
        
        c.saveState()
        expose = parameters[0]
        if expose == 0:
            c.setFillColor(gm.curBgColor);
        radius = 0.5 * parameters[1] * unit
        cx = x + parameters[2] * unit
        cy = y + parameters[3] * unit
        c.circle( cx, cy, radius, stroke=0, fill=1 )
        UpdateCircleExtents(cx,cy,radius, 0)
        c.restoreState()

    # }}}
    # {{{ HandleLineCenter    

    def HandleLineCenter( self, gm, parameters ):
        c,x,y,unit = gm.canv,gm.x,gm.y,gm.unit

        c.saveState()
        c.setLineCap( 0 )
        expose = parameters[0]
        if expose == 0:
            c.setStrokeColor(gm.curBgColor)
        width = parameters[1] * unit
        height = parameters[2] * unit
        cx = parameters[3] * unit
        cy = parameters[4] * unit
        rotation = parameters[5]
        sintheta = math.sin( rotation * math.pi / 180.0 )
        costheta = math.cos( rotation * math.pi / 180.0 )
        
        c.setLineWidth( height )
        x1 = x + cx + costheta * (-0.5 * width)
        y1 = y + cy + sintheta * (-0.5 * width)
        x2 = x + cx + costheta * (0.5 * width)
        y2 = y + cy + sintheta * (0.5 * width)
        UpdateLineExtents(x1,y1,x2,y2, c._lineWidth)
        c.line( x1, y1, x2, y2 )
        c.restoreState()

    # }}}
    # {{{ HandleLineVector

    def HandleLineVector( self, gm, parameters ):
        c,x,y,unit = gm.canv, gm.x, gm.y, gm.unit

        c.saveState()
        c.setLineCap( 0 )
        expose = parameters[0]
        if expose == 0:
            c.setStrokeColor(gm.curBgColor)
        width = parameters[1] * unit
        xa = parameters[2] * unit
        ya = parameters[3] * unit
        xb = parameters[4] * unit
        yb = parameters[5] * unit
        rotation = parameters[6]
        sintheta = math.sin( rotation * math.pi / 180.0 )
        costheta = math.cos( rotation * math.pi / 180.0 )

        c.setLineWidth( width )
        x1 = x + xa * costheta - ya * sintheta
        y1 = y + xa * sintheta + ya * costheta

        x2 = x + xb * costheta - yb * sintheta
        y2 = y + xb * sintheta + yb * costheta
        UpdateLineExtents(x1,y1,x2,y2, c._lineWidth)
        c.line( x1, y1, x2, y2 )
        c.restoreState()

    # }}}
    # {{{ HandleLineLowerLeft

    def HandleLineLowerLeft( self, gm, parameters ):
        c,x,y,unit = gm.canv, gm.x, gm.y, gm.unit
 
        c.saveState()
        c.setLineCap( 0 )
        expose = parameters[0]
        if expose == 0:
            c.setStrokeColor(gm.curBgColor)
        width = parameters[1] * unit
        height = parameters[2] * unit
        xll = parameters[3] * unit
        yll = parameters[4] * unit
        xa = xll
        ya = yll + 0.5 * height
        xb = xa + width
        yb = ya
        rotation = parameters[5]
        sintheta = math.sin( rotation * math.pi / 180.0 )
        costheta = math.cos( rotation * math.pi / 180.0 )
       
        c.setLineWidth( height )
        x1 = x + xa * costheta - ya * sintheta
        y1 = y + xa * sintheta + ya * costheta

        x2 = x + xb * costheta - yb * sintheta
        y2 = y + xb * sintheta + yb * costheta

        UpdateLineExtents(x1,y1,x2,y2, c._lineWidth)
        c.line( x1, y1, x2, y2 )
        c.restoreState()

    # }}}
    # {{{ HandleOutline

    def HandleOutline( self, gm, parameters ):
        c,x,y,unit = gm.canv, gm.x, gm.y, gm.unit
 
        c.saveState()
        expose = parameters[0]
        if expose == 0:
            c.setStrokeColor(gm.curBgColor)

        npoints = parameters[1]
        points = []
        for i in range(npoints+1):
            points.append( (parameters[2*i+2]*unit, parameters[2*i+3]*unit) )
        rotation = parameters[-1]
        sintheta = math.sin( rotation * math.pi / 180.0 )
        costheta = math.cos( rotation * math.pi / 180.0 )

        path = None
        for xa,ya in points:
            x1 = x + xa * costheta - ya * sintheta
            y1 = y + xa * sintheta + ya * costheta
            if path is None:
                path = c.beginPath()
                path.moveTo(x1,y1)
            else:
                path.lineTo(x1,y1)
        if path:
            c.drawPath(path, stroke=0, fill=1 )
        UpdateLineExtents(x1,y1,x1,y1, 0.0)
        c.restoreState()

    # }}}
    # {{{ HandlePolygon

    def HandlePolygon( self, gm, parameters ):
        c,x,y,unit = gm.canv, gm.x, gm.y, gm.unit
 
        c.saveState()
        expose = parameters[0]
        if expose == 0:
            c.setStrokeColor(gm.curBgColor)

        nvertices = parameters[1]
        cx = parameters[2]*unit
        cy = parameters[3]*unit
        diameter = parameters[4]*unit
        rotation = parameters[5]
        sintheta = math.sin( rotation * math.pi / 180.0 )
        costheta = math.cos( rotation * math.pi / 180.0 )

        angleStep = 2.0 * math.pi / nvertices
        path = None
        for i in range(nvertices):
            xa = cx + 0.5 * diameter * math.cos( i * angleStep )
            ya = cy + 0.5 * diameter * math.sin( i * angleStep )
            x1 = x + xa * costheta - ya * sintheta
            y1 = y + xa * sintheta + ya * costheta
            if path is None:
                path = c.beginPath()
                path.moveTo(x1,y1)
            else:
                path.lineTo(x1,y1)
        if path:
            path.close()
            c.drawPath(path, stroke=0, fill=1 )
        UpdateExtents(x1,y1,x1,y1)
        c.restoreState()

    # }}}
    # {{{ HandleMoire

    def HandleMoire( self, gm, parameters ):        
        c,x,y,unit = gm.canv, gm.x, gm.y, gm.unit
 
        c.saveState()
        cx = parameters[0]*unit
        cy = parameters[1]*unit
        outsideDiameter = parameters[2]*unit
        lineThickness = parameters[3]*unit
        gap = parameters[4]*unit
        nCircles = parameters[5]
        crossHairThickness = parameters[6]*unit
        crossHairLength = parameters[7]*unit
        rotation = parameters[8]
        sintheta = math.sin( rotation * math.pi / 180.0 )
        costheta = math.cos( rotation * math.pi / 180.0 )

        c.setLineWidth( lineThickness )
        for i in range(nCircles):
            radius = 0.5 * outsideDiameter - 0.5 * lineThickness - i * ( gap + lineThickness )
            UpdateCircleExtents(x+cx,y+cy,radius, lineThickness)
            c.circle(x+cx,y+cy,radius,stroke=1,fill=0)

        c.setLineCap(0)
        c.setLineWidth( crossHairThickness )

        xa = cx - 0.5*crossHairLength
        ya = cy
        xb = cx + 0.5*crossHairLength
        yb = cy
        
        x1 = x + xa * costheta - ya * sintheta
        y1 = y + xa * sintheta + ya * costheta
        x2 = x + xb * costheta - yb * sintheta
        y2 = y + xb * sintheta + yb * costheta
        UpdateLineExtents(x1,y1,x2,y2,c._lineWidth)
        c.line(x1,y1,x2,y2)        
        
        xa = cx
        ya = cy - 0.5*crossHairLength
        xb = cx
        yb = cy + 0.5*crossHairLength
        
        x1 = x + xa * costheta - ya * sintheta
        y1 = y + xa * sintheta + ya * costheta
        x2 = x + xb * costheta - yb * sintheta
        y2 = y + xb * sintheta + yb * costheta
        UpdateLineExtents(x1,y1,x2,y2,c._lineWidth)
        c.line(x1,y1,x2,y2)        

        c.restoreState()

    # }}}
    # {{{ HandleThermal

    def HandleThermal( self, gm, parameters ):
        c,x,y,unit = gm.canv, gm.x, gm.y, gm.unit
 
        c.saveState()

        cx = parameters[0]*unit
        cy = parameters[1]*unit
        outsideDiameter = parameters[2]*unit
        insideDiameter = parameters[3]*unit
        crossHairThickness = parameters[4]*unit
        rotation = parameters[5]
        sintheta = math.sin( rotation * math.pi / 180.0 )
        costheta = math.cos( rotation * math.pi / 180.0 )

        radius = 0.25 * (outsideDiameter + insideDiameter)
        c.setLineWidth( 0.5 * (outsideDiameter - insideDiameter) )
        UpdateCircleExtents(x+cx,y+cy,radius, c._lineWidth)
        c.circle(x+cx,y+cy,radius,stroke=1,fill=0)

        c.setLineCap(2)
        c.setStrokeColor(gm.curBgColor)
        c.setLineWidth( crossHairThickness )

        xa = cx - 0.5*outsideDiameter
        ya = cy
        xb = cx + 0.5*outsideDiameter
        yb = cy
        
        x1 = x + xa * costheta - ya * sintheta
        y1 = y + xa * sintheta + ya * costheta
        x2 = x + xb * costheta - yb * sintheta
        y2 = y + xb * sintheta + yb * costheta
        UpdateLineExtents(x1,y1,x2,y2, c._lineWidth)
        c.line(x1,y1,x2,y2)        
        
        xa = cx
        ya = cy - 0.5*outsideDiameter
        xb = cx
        yb = cy + 0.5*outsideDiameter
        
        x1 = x + xa * costheta - ya * sintheta
        y1 = y + xa * sintheta + ya * costheta
        x2 = x + xb * costheta - yb * sintheta
        y2 = y + xb * sintheta + yb * costheta
        UpdateLineExtents(x1,y1,x2,y2, c._lineWidth)
        c.line(x1,y1,x2,y2)        
        c.restoreState()        

    # }}}
    # {{{ Flash
    def Flash( self, gm ):
        for primitive in self.items:
            id = primitive[0]
            if id == 1:
                self.HandleCircle( gm, primitive[1:] )
            elif id == 2 or id == 20:
                self.HandleLineVector( gm, primitive[1:] )
            elif id == 21:
                self.HandleLineCenter( gm, primitive[1:] )
            elif id == 22:
                self.HandleLineLowerLeft( gm, primitive[1:] )
            elif id == 4:
                self.HandleOutline( gm, primitive[1:] )
            elif id == 5:
                self.HandlePolygon( gm, primitive[1:] )
            elif id == 6:
                self.HandleMoire( gm, primitive[1:] )
            elif id == 7:
                self.HandleThermal( gm, primitive[1:] )
    # }}}

# }}}            
# {{{ CircleAperture

class CircleAperture:

    def __init__( self, parameters ):
        self.od = float(parameters[0])
        self.pathWidth = self.od
        self.rectangular = False
        self.lineCap = 1
        if len(parameters) == 1:
            self.hole = None
        elif len(parameters) == 2:
            self.hole = 'round'
            self.holeDiam = float(parameters[1])
        elif len(parameters) == 3:
            self.hole = 'rect'
            self.holeDiamX = float(paramters[1])
            self.holeDiamY = float(parameter[2])
        else:
            raise GerberError("Malformed circle aperture definition")
            
    def Flash( self, gm ):
        c = gm.canv
        UpdateCircleExtents(gm.x, gm.y, 0.5*self.od*gm.unit,0)
        c.circle( gm.x, gm.y, 0.5*self.od*gm.unit, stroke=0, fill=1 )
        if self.hole == 'round':
            c.setFillColor( gm.curBgColor )
            c.circle( gm.x, gm.y, 0.5*self.holeDiam*gm.unit, stroke=0, fill=1)
            c.setFillColor (gm.curFgColor)
        elif self.hole == 'rect':
            c.setFillColor( gm.curBgColor )
            width  = self.holeDiamX*gm.unit
            height = self.holeDiamY*gm.unit
            x = gm.x - 0.5*width
            y = gm.y - 0.5*height
            c.rect( x, y, width, height, stroke=0, fill=1 )
            c.setFillColor (gm.curFgColor)

# }}}        
# {{{ RectAperture

class RectAperture:

    def __init__( self, parameters ):
        if len(parameters) < 2:
            raise GerberError("No Y dimension in rectangle aperture definition")
        
        self.xdimension = float(parameters[0])
        self.ydimension = float(parameters[1])
        self.rectangular = True
        self.pathWidth = None
        self.lineCap = 2
        
        if len(parameters) == 2:
            self.hole = None
        elif len(parameters) == 3:
            self.hole = 'round'
            self.holeDiam = float(parameters[2])
        elif len(parameters) == 4:
            self.hole = 'rect'
            self.holeDiamX = float(parameters[2])
            self.holeDiamY = float(parameters[3])
        else:
            raise GerberError("Malformed rectangle aperture definition")    

    def Flash( self, gm ):
        c = gm.canv
        width  = self.xdimension*gm.unit
        height = self.ydimension*gm.unit
        x = gm.x - 0.5*width
        y = gm.y - 0.5*height
        UpdateExtents(x,y,x+width,y+height)
        c.rect( x, y, width, height, stroke=0, fill=1 )
        if self.hole == 'round':
            c.setFillColor( gm.curBgColor )
            c.circle( gm.x, gm.y, 0.5*self.holeDiam*gm.unit, stroke=0, fill=1)
            c.setFillColor (gm.curFgColor)
        elif self.hole == 'rect':
            c.setFillColor( gm.curBgColor )
            width  = self.holeDiamX*gm.unit
            height = self.holeDiamY*gm.unit
            x = gm.x - 0.5*width
            y = gm.y - 0.5*height
            c.rect( x, y, width, height, stroke=0, fill=1 )
            c.setFillColor (gm.curFgColor)

# }}}
# {{{ OvalAperture

class OvalAperture:

    def __init__( self, parameters ):
        if len(parameters) < 2:
            raise GerberError("No Y dimension in oval aperture definition")
        
        self.pathWidth = None   
        self.xdimension = float(parameters[0])
        self.ydimension = float(parameters[1])
        
        if len(parameters) == 2:
            self.hole = None
        elif len(parameters) == 3:
            self.hole = 'round'
            self.holeDiam = float(parameters[2])
        elif len(parameters) == 4:
            self.hole = 'rect'
            self.holeDiamX = float(parameters[2])
            self.holeDiamY = float(parameters[3])
        else:
            raise GerberError("Malformed oval aperture definition")    

    def Flash( self, gm ):
        c = gm.canv
        width  = self.xdimension*gm.unit
        height = self.ydimension*gm.unit
        radius = 0.5*min(width,height)
        x = gm.x - 0.5*width
        y = gm.y - 0.5*height
        UpdateExtents(x,y,x+width,y+height)
        c.roundRect( x, y, width, height, radius, stroke=0, fill=1 )
        if self.hole == 'round':
            c.setFillColor( gm.curBgColor )
            c.circle( gm.x, gm.y, 0.5*self.holeDiam*gm.unit, stroke=0, fill=1)
            c.setFillColor (gm.curFgColor)
        elif self.hole == 'rect':
            c.setFillColor( gm.curBgColor )
            width  = self.holeDiamX*gm.unit
            height = self.holeDiamY*gm.unit
            x = gm.x - 0.5*width
            y = gm.y - 0.5*height
            c.rect( x, y, width, height, stroke=0, fill=1 )
            c.setFillColor (gm.curFgColor)

# }}}
# {{{ PolyAperture
class PolyAperture:

    def __init__( self, parameters ):
        if len(parameters) < 2:
            raise GerberError("Malformed aperture definition for regular polygon")

        self.rectangular = False
        self.pathWidth = None
        self.diameter = float(parameters[0])
        self.nSides = int(parameters[1])

        self.rotation = 0.0
        self.hole = None
        
        if len(parameters) >= 3:
            self.rotation = float(parameters[2]) * math.pi / 180.0
            
        if len(parameters) == 4:
            self.hole = 'round'
            self.holeDiam = float(parameters[3])
        elif len(parameters) == 5:
            self.hole = 'rect'
            self.holeDiamX = float(parameters[3])
            self.holeDiamY = float(parameters[4])
                
        if len(parameters) > 5:
            raise GerberError("Malformed polygon aperture definition")    

    def Flash( self, gm ):
        c = gm.canv
        angleStep = 2.0 * math.pi / self.nSides

        path = None
        for i in range(self.nSides):
            x = 0.5 * self.diameter * math.cos( i * angleStep + self.rotation )
            y = 0.5 * self.diameter * math.sin( i * angleStep + self.rotation )
            UpdatePointExtents(x,y)
            if path is None:
                path = c.beginPath()
                path.moveTo( x, y )
            else:
                path.lineTo( x, y )
        path.close()
        c.drawPath( path, stroke=0, fill=1 )
        if self.hole == 'round':
            c.setFillColor( gm.curBgColor )
            c.circle( gm.x, gm.y, 0.5*self.holeDiam*gm.unit, stroke=0, fill=1)
            c.setFillColor (gm.curFgColor)
        elif self.hole == 'rect':
            c.setFillColor( gm.curBgColor )
            width  = self.holeDiamX*gm.unit
            height = self.holeDiamY*gm.unit
            x = gm.x - 0.5*width
            y = gm.y - 0.5*height
            c.rect( x, y, width, height, stroke=0, fill=1 )
            c.setFillColor (gm.curFgColor)
# }}}
# {{{ GerberMachine
class GerberMachine: 

    rb   = re.compile( r'(N\d+)?(G\d+)?(X-?\d*)?(Y-?\d*)?(I-?\d*)?(J-?\d*)?(D\d+)?(M\d+)?\*' )
    rfs  = re.compile( r'(FS)([LT])?([AI])?(N\d)?(G\d)?(X\d\d)(Y\d\d)(D\d)?(M\d)?\*' )
    rad0 = re.compile( r'(AD)(D\d\d\d?)([^,]+)\*' )
    rad1 = re.compile( r'(AD)(D\d\d\d?)([^,]+),([. 0-9]+)' )
    rad2 = re.compile( r'X(-?[. 0-9]+)' )
    # {{{ __init__

    def __init__(self, fileName, canv=None):
        from reportlab.pdfgen import canvas
        if(canv == None):
            self.canv = canvas.Canvas(fileName, pagesize=gerberPageSize, pageCompression = 1 )
        else:
            self.canv = canv

        self.Initialize()

    # }}}
    # {{{ Initialize

    def Initialize( self ):
        from reportlab.lib import colors
        self.canv.setLineCap( 1 )
        self.canv.setLineJoin( 1 )
        self.unit = inch
        self.apertures = {}
        self.macroDefinitions = {}
        self.px = 0.0
        self.py = 0.0
        self.x = 0.0
        self.y = 0.0
        self.i = 0.0
        self.j = 0.0
        self.path = None
        self.polyPath = None
        self.leadingZeroSuppression = 1
        self.absolute = 1
        self.inch = 1
        self.xFormat = (2,3)
        self.yFormat = (2,3)
        self.tool = None
        self.toolWidth = None
        self.dnumber = 2
        self.nCodeLimit = 4
        self.gCodeLimit = 2
        self.dCodeLimit = 2
        self.mCodeLimit = 2
        self.linearInterpolation = 1
        self.clockWise = 1
        self.singleQuadrant = 1
        self.interpolationScale = 1.0
        self.areaFill = 0
        self.fgColor = colors.Color(0.8,0.8,0.8)
        self.bgColor = colors.Color(1,1,1)
        self.curFgColor = self.fgColor
        self.curBgColor = self.bgColor
        self.canv.setStrokeColor(self.curFgColor)
        self.canv.setFillColor(self.curFgColor)


    def setColors(self, fg, bg):
        self.fgColor = fg
        self.curFgColor = fg
        self.bgColor = bg
        self.curBgColor = bg
        self.canv.setStrokeColor(self.curFgColor)
        self.canv.setFillColor(self.curFgColor)

    # }}}
    # {{{ ExecuteAreaFill

    def ExecuteAreaFill( self ):
        c = self.canv
        if self.path:
            c.drawPath( self.path, stroke=1, fill=0 )
            self.path = None
            
        if self.dnumber == 1:
            if self.polyPath is None:
                self.polyPath = c.beginPath()
                self.polyPath.moveTo( self.px, self.py )
                # print "moveto %s %s" % (self.px, self.py)
            if self.linearInterpolation:
                if self.x != self.px or self.y != self.py:
                    UpdateLineExtents(self.px,self.py, self.x, self.y, c._lineWidth)
                    self.polyPath.lineTo( self.x, self.y )
                    # print "lineto %s %s" % (self.x, self.y )
            else:
                if self.x != self.px or self.y != self.py:
                    self.ArcPath( self.polyPath )
        elif self.dnumber == 2:
            if self.polyPath:
                self.polyPath.close()
                # print "close"
                c.drawPath( self.polyPath, stroke=0, fill=1 )
                self.polyPath = None
        else:
            raise GerberError( "Illegal D-code within area fill" )

    # }}}
    # {{{ Arc Path

    def ArcPath( self, path ):
        c=self.canv
        i,j   = self.i, self.j
        px,py = self.px, self.py
        x,y   = self.x, self.y
        radius = math.sqrt( i*i + j*j )
        if radius == 0.0:
            return
            
        if self.singleQuadrant:
            if i < 0.0 or j < 0.0:
                raise GerberError( "Negative i or j values with Single Quadrant Interpolation" )
            if py < y:
                dx =  i
            else:
                dx = -i
            if px < x:
                dy = -j
            else:
                dy =  j
                
            if not self.clockWise:
                dx, dy = -dx, -dy
                
            centerx = px + dx
            centery = py + dy
                
            startAngle = math.atan2( py-centery, px-centerx ) * 180.0 / math.pi
            endAngle   = math.atan2(  y-centery,  x-centerx ) * 180.0 / math.pi
            
            extent = endAngle - startAngle
            if self.clockWise and extent >= 0.0:
                extent -= 360.0
            elif not self.clockWise and extent <= 0.0:
                extent += 360.0
            
            x1 = centerx - radius
            x2 = centerx + radius
            y1 = centery - radius
            y2 = centery + radius
            UpdateArcExtents( x1, y1, x2, y2, startAngle, extent, c._lineWidth )
            path.arcTo( x1, y1, x2, y2, startAngle, extent )
            # print "arc %s %s %s %s %s %s" % ( x1, y1, x2, y2, startAngle, extent )
        else:
            dx,dy = i,j
            centerx = px + dx
            centery = py + dy
            
            startAngle = math.atan2( py-centery, px-centerx ) * 180.0 / math.pi
            endAngle   = math.atan2(  y-centery,  x-centerx ) * 180.0 / math.pi
            
            extent = endAngle - startAngle
            if self.clockWise and extent >= 0.0:
                extent -= 360.0
            elif not self.clockWise and extent <= 0.0:
                extent += 360.0
            
            x1 = centerx - radius
            x2 = centerx + radius
            y1 = centery - radius
            y2 = centery + radius

            UpdateArcExtents( x1, y1, x2, y2, startAngle, extent, c._lineWidth )
            path.arcTo( x1, y1, x2, y2, startAngle, extent )
            # print "arc %s %s %s %s %s %s" % ( x1, y1, x2, y2, startAngle, extent )

    # }}}
    # {{{ Flush

    def Flush( self ):
        c = self.canv
        if self.polyPath:
            self.polyPath.close()
            c.drawPath( self.polyPath, stroke=0, fill=1 )
            self.polyPath = None

        if self.path:
            c.drawPath( self.path, stroke=1, fill=0 )
            self.path = None

    # }}}
    
    def DoRectangularPath( self ):
        x1, y1 = self.x,  self.y
        x2, y2 = self.px, self.py
        
        if x1 > x2:
            x1,y1,x2,y2 = x2,y2,x1,y1
        
        dx = 0.5 * self.tool.xdimension * self.unit
        dy = 0.5 * self.tool.ydimension * self.unit
        
        path = self.canv.beginPath()
        if y1 < y2:
            path.moveTo( x1 - dx, y1 - dy )
            path.lineTo( x1 - dx, y1 + dy )
            path.lineTo( x2 - dx, y2 + dy )
            path.lineTo( x2 + dx, y2 + dy )
            path.lineTo( x2 + dx, y2 - dy )
            path.lineTo( x1 + dx, y1 - dy )
            path.lineTo( x1 - dx, y1 - dy )
        elif y1 > y2:
            path.moveTo( x1 - dx, y1 + dy )
            path.lineTo( x1 + dx, y1 + dy )
            path.lineTo( x2 + dx, y2 + dy )
            path.lineTo( x2 + dx, y2 - dy )
            path.lineTo( x2 - dx, y2 - dy )
            path.lineTo( x1 - dx, y1 - dy )
            path.lineTo( x1 - dx, y1 + dy )
        else:
            path.moveTo( x1 - dx, y1 - dy )
            path.lineTo( x1 - dx, y1 + dy )
            path.lineTo( x2 + dx, y2 + dy )
            path.lineTo( x2 + dx, y2 - dy )
            path.lineTo( x1 - dx, y1 - dy )
            
        self.canv.drawPath( path, stroke=0, fill=1 )
    
    # {{{ ExecuteBlock

    def ExecuteBlock( self ): 
        c = self.canv
        if self.dnumber == 1:
            if self.tool is None:
                raise GerberError("No aperture selected")
                
            if self.tool.rectangular:
                if self.path:
                    c.drawPath( self.path, stroke=1, fill=0 )
                    self.path = None
                if self.linearInterpolation:
                    self.DoRectangularPath()
                        
                self.px, self.py = self.x, self.y
                return
                
            newWidth = self.tool.pathWidth
            if newWidth is None:    
                raise GerberError("Illegal aperture selected for path")

            newWidth = newWidth * self.unit
            newLineCap = self.tool.lineCap
                    
            if c._lineWidth != newWidth or c._lineCap != newLineCap:
                if self.path:
                    c.drawPath( self.path, stroke=1, fill=0 )
                    self.path = None
                c.setLineWidth( newWidth )
                c.setLineCap( newLineCap )
                    
            if self.path is None:
                self.path = c.beginPath()
                self.path.moveTo( self.px, self.py )
            
            if self.linearInterpolation:
                UpdateLineExtents(self.px,self.py, self.x, self.y, c._lineWidth)
                self.path.lineTo( self.x, self.y )
            else:
                self.ArcPath( self.path )
        elif self.dnumber == 2:
            if self.path:
                c.drawPath( self.path )
                self.path = None
        elif self.dnumber == 3:
            if self.path:
                c.drawPath( self.path )
                self.path = None
                
            if self.tool is None:
                raise GerberError("No aperture selected for flash")
            self.tool.Flash(self)
            self.dnumber = 0
            
        self.px, self.py = self.x, self.y

    # }}}
    # {{{ Value
    def Value( self, str, format ):
        factor = 1.0
        left  = format[0]
        right = format[1]
        totalLength = left + right
        
        if len(str) >= 1 and str[0] == '-':
            factor = -1.0
            str = str[1:]
        elif len(str) >= 1 and str[0] == '+':
            factor = 1.0
            str = str[1:]
        
        neededZeros = right + left - len(str)    
        if self.leadingZeroSuppression:
            if neededZeros > 0:
                str = '0' * neededZeros + str
            pointPosition = len(str)-right
        else:
            if neededZeros > 0:
                str = str + '0' * neededZeros
            pointPosition = left
        str = str[:pointPosition] + '.' + str[pointPosition:]
        return factor * float( str ) * self.unit
    # }}}
    # {{{ HandleDCode
    def HandleDCode( self, dCode ):
        num = int(dCode[1:])
        self.dnumber = num
        if num >= 10:
            if not self.apertures.has_key( num ):
                raise GerberError("Unknown Aperture: %s" % dCode )
            
            self.tool = self.apertures[ num ]
        elif not 1 <= num <= 3:
            raise GerberError("Invalid D-Code: %s" % dCode)
    # }}}
    # {{{ HandleGCode
    def HandleGCode( self, gCode ):
        num = int(gCode[1:])
        if num == 54 or num == 55:
            pass #Tool preparation, not really needed
        elif num == 0:
            pass
        elif num == 1:
            self.linearInterpolation = 1
            self.interpolationScale = 1.0
        elif num == 2:
            self.linearInterpolation = 0
            self.clockWise = 1
        elif num == 3:
            self.linearInterpolation = 0
            self.clockWise = 0
        elif num == 4:
            pass
        elif num == 10:
            self.linearInterpolation = 1
            self.interpolationScale = 10.0
        elif num == 11:
            self.linearInterpolation = 1
            self.interpolationScale = 0.1
        elif num == 12:
            self.linearInterpolation = 1
            self.interpolationScale = 0.01
        elif num == 36:
            self.areaFill = 1
            self.polyPath = None
        elif num == 37:
            self.areaFill = 0
        elif num == 70:
            self.inch = 1
        elif num == 71:
            self.inch = 0
        elif num == 74:
            self.singleQuadrant = 1
        elif num == 75:
            self.singleQuadrant = 0
        elif num == 90:
            self.absolute = 1
        elif num == 91:
            self.absolute = 0
        else:
            raise GerberError("Invalid G-Code: %s" % gCode)
    # }}}
    # {{{ HandleMCode

    def HandleMCode(self, mCode):
        if mCode in ["M0","M1","M2","M00","M01","M02"]:
            self.Flush()
#            self.canv.showPage()
        else:
            raise GerberError("Invalid M-Code: %s" % mCode)

    # }}}
    # {{{ HandleBlock

    def HandleBlock( self, str ):
        m = GerberMachine.rb.match( str )
        if m is None:
            raise GerberError("Invalid Block: %s" % str)
            return
            
        nCode, gCode, xCode, yCode, iCode, jCode, dCode, mCode = m.groups()
        if gCode:
            self.HandleGCode( gCode )
            
        if xCode:
            value = self.Value( xCode[1:], self.xFormat )
            if self.absolute:
                self.x = value
            else:
                self.x += value
            
        if yCode:
            value = self.Value( yCode[1:], self.yFormat )
            if self.absolute:
                self.y = value
            else:
                self.y += value
        
        self.i = 0.0
        self.j = 0.0    
        if iCode:
            self.i = self.Value( iCode[1:], self.xFormat )
            
        if jCode:
            self.j = self.Value( jCode[1:], self.yFormat )
            
        if dCode:
            self.HandleDCode( dCode )
           
        c = self.canv
        if gCode in [ "G36", "G74", "G75" ]:
            pass
        elif self.areaFill:
            self.ExecuteAreaFill()
        elif self.polyPath:
            self.polyPath.close()
            c.drawPath( self.polyPath, stroke=0, fill=1 )
            self.polyPath = None
        elif mCode:
            self.HandleMCode( mCode )
        else:    
            self.ExecuteBlock()
            
        self.px, self.py = self.x, self.y

    # }}}
    # {{{ Handle AD
    def HandleAD( self, str ):
        if str == "AD*":
            print "Warning: AD parameter block has no parameters."
            return
        
        m = GerberMachine.rad1.match( str ) or GerberMachine.rad0.match( str )
        if m is None:
            raise GerberError("Malformed AD block: %s" % str)

        lst = list(m.groups())
        lst = lst + GerberMachine.rad2.findall( str[m.end():] )

        dcode = lst[1]
        num = int(dcode[1:])
        shape = lst[2]
        params = lst[3:]            
        if not (10 <= num <= 999):
            raise GerberError("Illegal D-code in AD block: %s" % dcode)
        if shape == 'C':
            self.apertures[num] = CircleAperture( params )
        elif shape == 'R':
            self.apertures[num] = RectAperture( params )
        elif shape == 'O':
            self.apertures[num] = OvalAperture( params )
        elif shape == 'P':
            self.apertures[num] = PolyAperture( params )
        else:
            macroDefinition = self.macroDefinitions[ shape ]
            self.apertures[num] = macroDefinition.NewMacro( params )
    # }}}
    # {{{ HandleFS
    def HandleFS( self, str ):
        m = GerberMachine.rfs.match(str)
        if m is None:
            raise GerberError("Malformed FS block: %s" % str)
        lst = m.groups()
        
        self.leadingZeroSuppression = 1
        if lst[1]:
            self.leadingZeroSuppression = lst[1] == 'L'
            
        self.absolute = 1
        if lst[2]:
            self.absolute = lst[2] == 'A'
            
        if lst[3]:
            self.nCodeLimit = int(lst[3][1])
        if lst[4]:
            self.gCodeLimit = int(lst[4][1])
        
        self.xFormat = ( int(lst[5][1]), int(lst[5][2]) )
        if self.xFormat[0] > 6 or self.xFormat[1] > 6:
            raise GerberError("Illegal X value in FS block: %s" % str)
            
        self.yFormat = ( int(lst[6][1]), int(lst[6][2]) )
        if self.yFormat[0] > 6 or self.yFormat[1] > 6:
            raise GerberError("Illegal Y value in FS block: %s" % str)
        
        if lst[7]:
            self.dCodeLimit = int(lst[7][1])
        if lst[8]:
            self.mCodeLimit = int(lst[8][1])
    # }}}
    # {{{ HandleIF
    def HandleIF( self, str ):
        fileName = str[2:]
        self.ProcessFile( fileName )
    # }}}
    # {{{ HandleMO
    def HandleMO( self, str ):
        if str[-3:] == "IN*":
            self.unit = inch
        elif str[-3:] == "MM*":
            self.unit = mm
    # }}}
    # {{{ HandleLP

    def HandleLP( self, str ):
        self.Flush()
        if str[2] == "C":
            self.curBgColor = self.fgColor
            self.curFgColor = self.bgColor
            self.canv.setFillColor( self.bgColor )
            self.canv.setStrokeColor( self.bgColor )
        elif str[2] == "D":
            self.curFgColor = self.fgColor
            self.curBgColor = self.bgColor
            self.canv.setFillColor( self.fgColor )
            self.canv.setStrokeColor(self.fgColor )

    # }}}
    # {{{ HandleMacro
    def HandleMacro( self, str ):
        if str.find("=") != -1:
            self.currentMacro.items.append( MacroEquation( str ) )
        elif str.find(",") != -1:
            self.currentMacro.items.append( PrimitiveDefinition( str ) )
        else:
            str = str.replace("*","")
            self.currentMacro = MacroDefinition()
            self.macroDefinitions[str] = self.currentMacro
    # }}}
    # {{{ HandleParameterBlock
    def HandleParameterBlock( self, str ):
        first2 = str[:2]
        if first2 == "FS":
            self.HandleFS( str )
        elif first2  == "AD":
            self.HandleAD( str )
        elif first2 == "IF":
            self.HandleIF( str )
        elif first2 == "MO":
            self.HandleMO( str )
        elif first2 == "LP":
            self.HandleLP( str )
        elif first2 == "IN":
            pass
        elif first2 == "LN":
            pass
        else:
            print "Unimplemented data block: %s" % str
    # }}}
    # {{{ ProcessFile
    def ProcessFile( self, fname ):
        f = open( fname )
        print "Processing file: %s" % fname
        scanner = GerberScanner( f, fname )
        try:
            while 1:
                token = scanner.read()
                if token[0] is None:
                    break
                
                if token[0] == 'block':
                    if token[1] == "M02" or token[1] == "M2":
                        self.HandleBlock( "M02*" )
                    else:
                        self.HandleBlock( token[1] )
                elif token[0] == 'pblock':
                    self.HandleParameterBlock( token[1] )
                elif token[0] == 'mblock':
                    self.HandleMacro( token[1] )
        except GerberError, message:
            name, line, col = scanner.position()
            print "Error in file %s, line %s, column %s" % (name,line,col)
            print message
        print "Finished: Extents are (%4.2f, %4.2f) - (%4.2f, %4.2f) (in.)" %(gerberExtents[0] / inch,
                                                                              gerberExtents[1] / inch,
                                                                              gerberExtents[2] / inch,
                                                                              gerberExtents[3] / inch)
        
        f.close()
        return gerberExtents
    # }}}
# }}}
# {{{ Translate (filelist)

def Translate( fileList ):
    global gerberOutputFile, gerberScale, gerberOffset, gerberPageSize, gerberFitPage, gerberExtents, gerberMargin


    folder = os.path.dirname( fileList[0] )
    gerberOutputPath = os.path.join( folder, gerberOutputFile )

    pagesizes = []
    if gerberFitPage:
        print "Prereading for page sizes"
        print " ----------------------- "
        # find out how big pages are
        gm = GerberMachine( gerberOutputPath )
        for f in fileList:
            gm.Initialize()
            gm.canv.translate( gerberOffset[0], gerberOffset[1] )
            gm.canv.scale( gerberScale[0], gerberScale[1] )
            gm.canv.setLineWidth( 0.0 )
            gm.ProcessFile( f )
            pagesizes.append(gerberExtents)
            ResetExtents()
            print "----"
        gm.canv.save()
        print "--------------------------"
    
    gm = GerberMachine( gerberOutputPath )
    for f in fileList:
        gm.Initialize()
        if gerberFitPage:
            print "Reoffsetting: " + f
            extents = pagesizes[0]
            pagesizes = pagesizes[1:]
            # print gerberPageSize[0], gerberMargin
            scale1 = (gerberPageSize[0]-2*gerberMargin)/((extents[2]-extents[0]))
            scale2 = (gerberPageSize[1]-2*gerberMargin)/((extents[3]-extents[1]))
            scale = min(scale1, scale2)
            gerberScale = (scale,scale)
            gerberOffset = (-extents[0]*scale + gerberMargin, -extents[1]*scale + gerberMargin)
        print "Offset (in.): (%4.2f, %4.2f)" % (gerberOffset[0]/inch,gerberOffset[1]/inch)
        print "Scale (in.):  (%4.2f, %4.2f)" % gerberScale
        gm.canv.translate( gerberOffset[0], gerberOffset[1] )
        gm.canv.scale( gerberScale[0], gerberScale[1] )
        gm.canv.setLineWidth( 0.0 )
        gm.ProcessFile( f )
        print "----"
    gm.canv.save()

# }}}
# {{{ ReadConfiguration
def ReadConfiguration( fileList ):
    global gerberScale, gerberOffset, gerberPageSize, gerberOutputFile, gerberFitPage, gerberMargin
    if not fileList:
        return
        
    folder = os.path.dirname( fileList[0] )
    # Check for configuration file in same directory as Gerber files
    # If present, execute it as python instructions
    figFile = os.path.join( folder, "gerber2pdf.cfg" )
    if os.path.isfile(figFile):
        glo = {}
        loc = { "inch" : inch }
        execfile( figFile, glo, loc )
        gerberScale = loc.get( "gerberScale", gerberScale )
        gerberOffset = loc.get( "gerberOffset", gerberOffset )
        gerberPageSize = loc.get( "gerberPageSize", gerberPageSize )
        gerberOutputFile = loc.get( "gerberOutputFile", gerberOutputFile )
        gerberFitPage = loc.get( "gerberFitPage", gerberFitPage )
        gerberMargin = loc.get( "gerberMargin", gerberMargin )
        fileList = loc.get("fileList", fileList)
        
    return fileList
    
# }}}            
# {{{ InputDefault    
def InputDefault( message, default ):
    str = raw_input( message % default )
    try:
        value = float(str)
    except:
        value = default
    return value
# }}}
# {{{ Interact
def Interact():
    global gerberScale, gerberOffset, gerberPageSize, gerberOutputFile, gerberFitPage, gerberMargin
    
    fileList = []
    str = raw_input( "Gerber files (wildcards OK): " )
    lst = str.split()
    for item in lst:
        fileList = fileList + glob.glob( item )
    if len(fileList) == 0:
        return

    ReadConfiguration( fileList )       
     
    width, height = gerberPageSize
    width = InputDefault( "Page width (inches) [%3.1f]: ", width/inch ) * inch
    height = InputDefault( "Page height (inches) [%3.1f]: ", height/inch ) * inch
    gerberPageSize = (width,height)
    
    str = raw_input( "Fit to page? (1=yes,0=no) [%s]: " % gerberFitPage )
    try:
        gerberFitPage = int(str)
    except:
        pass

    if gerberFitPage:
        gerberMargin = InputDefault( "Margin (inches) [%4.2f]: ", gerberMargin/inch ) * inch
    else: 
        xoff, yoff = gerberOffset
        xoff = InputDefault( "X Offset (inches) [%3.1f]: ", xoff/inch ) * inch
        yoff = InputDefault( "Y Offset (inches) [%3.1f]: ", yoff/inch ) * inch        
        gerberOffset = (xoff,yoff)

        xscale, yscale = gerberScale
        xscale = InputDefault( "X Scale [%3.1f]: ", xscale )
        yscale = InputDefault( "Y Scale [%3.1f]: ", yscale )
        gerberScale = (xscale,yscale)
    
    response = raw_input( "Output file [%s]: " % gerberOutputFile )
    if response:
        gerberOutputFile = response
    
    Translate( fileList )
# }}}
# {{{ __MAIN__
if __name__ == "__main__":
    import sys

    fileList = sys.argv[1:]    
    if fileList:
        fileList = ReadConfiguration( fileList )
        Translate( fileList )
    else:
        Interact()
# }}}

# }}}


