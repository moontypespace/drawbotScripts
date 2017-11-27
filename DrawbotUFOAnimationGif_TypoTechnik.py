from fontParts.nonelab import RFont
import math

# path to any ufo file
ufo2 = u"/Users/omeier/Documents/_privateStuff/Typostammtisch/70_Tools_zum_Teilen/Beispiel/New Font-Bold.ufo"
ufo1 = u"/Users/omeier/Documents/_privateStuff/Typostammtisch/70_Tools_zum_Teilen/Beispiel/New Font-Regular.ufo"

gList = ['A'] 
moveY = 0
numFramesPerLoop = 20
canvasx = 1000
canvasy = 600
margin = 10
colorChar = 1 # black
colorBG = 0 #white


def easeInOutQuad(t):
    t *= 2
    if t < 1:
        return 0.5 * (t ** 2)
    else:
        t = 2 - t
        return 1 - 0.5 * (t ** 2)

def drawGlyph(ufo, character):
    font = RFont(ufo)
    glyph = font[character]
    B = BezierPath()
    for contour in glyph:
        for i, segment in enumerate(contour):
            # curveTo
            if len(segment.points) == 3:
                x1, y1 = segment.points[0].x, segment.points[0].y
                x2, y2 = segment.points[1].x, segment.points[1].y
                x3, y3 = segment.points[2].x, segment.points[2].y
                B.curveTo((x1, y1), (x2, y2), (x3, y3))
            # lineTo or moveTo
            else:
                x, y = segment.points[0].x, segment.points[0].y
                if i == 0:
                    B.moveTo((x, y))
                else:
                    B.lineTo((x, y))
    return B

def interpolationBezierPath(path1, path2, factor, scaleFactor):
    B = BezierPath()
    for a, contour in enumerate(path1):
        for b, segment in enumerate(contour):
            if len(segment) == 3:
                x1, y1 = (segment[0][0] - ((segment[0][0] - path2[a][b][0][0]) * factor)), (segment[0][1] - ((segment[0][1] - path2[a][b][0][1]) * factor))#segment[0][1]
                x2, y2 = (segment[1][0] - ((segment[1][0] - path2[a][b][1][0]) * factor)), (segment[1][1] - ((segment[1][1] - path2[a][b][1][1]) * factor))
                x3, y3 = (segment[2][0] - ((segment[2][0] - path2[a][b][2][0]) * factor)), (segment[2][1] - ((segment[2][1] - path2[a][b][2][1]) * factor))
                B.curveTo((x1*scaleFactor, y1*scaleFactor), (x2*scaleFactor, y2*scaleFactor), (x3*scaleFactor, y3*scaleFactor))
                #print 'Bold\t\t\t: ',  path2[a][b][0][0], path2[a][b][0][1]
                #print 'Regular\t\t: ', segment[0][0], segment[0][1]
                #print  'Interpolation\t:', x1, y1
            else:
                x, y = segment[0][0] - ((segment[0][0] - path2[a][b][0][0]) * factor), segment[0][1] - ((segment[0][1] - path2[a][b][0][1]) * factor)
                if b == 0:
                    B.moveTo((x*scaleFactor, y*scaleFactor))
                else:
                    B.lineTo((x*scaleFactor, y*scaleFactor))        
    return B
    
def animation(ufo1, ufo2, g, canvasx, canvasy, scaleFactor, marginX, marginY, moveY):
    for frame in range(numFramesPerLoop):
        t = easeInOutQuad(frame / numFramesPerLoop)
        #t = frame/numFramesPerLoop #linear
        newPage(canvasx, canvasy)
        fill(colorBG)
        rect(0, 0, canvasx, canvasy)
        frameDuration(1/10)

        tempB = interpolationBezierPath(drawGlyph(ufo1, g), drawGlyph(ufo2, g), t, scaleFactor)
        fill(colorChar)

        translate(marginX , marginY + moveY)# + 20)# zum anpassen in der y position einfach +
        drawPath(tempB)


def getHeight(ufo, character):
    glyph = RFont(ufo)[character]
    collectNodes = []
    for contour in glyph:
        for segment in contour:
            for node in segment:
                collectNodes.append(node.y)

    height = max(collectNodes) - min(collectNodes)
    return height
   
def getScale(ufo1, ufo2, g, canvasx, canvasy, margin):
    
    gHeight1 = getHeight(ufo1, g)
    gHeight2 = getHeight(ufo2, g)
        
    font1 = RFont(ufo1)
    gWidth1 = font1[g].width

    font2 = RFont(ufo2)
    gWidth2 = font2[g].width
    
    maxWidth = gWidth1 if gWidth1 >= gWidth2 else gWidth2
    maxHeight = gHeight1 if gHeight1 >= gHeight2 else gHeight2
    
    scaletocanvasx = (canvasx - (margin*2)) / maxWidth
    scaletocanvasy = (canvasy - (margin*2)) / maxHeight
    scaletocanvas = scaletocanvasx if scaletocanvasx < scaletocanvasy else scaletocanvasy
    
    marginX = (canvasx - (maxWidth*scaletocanvas))/2
    marginY = (canvasy - (maxHeight*scaletocanvas))/2

    return scaletocanvas, marginX, marginY
        

def main(ufo1, ufo2, g, canvasx, canvasy, margin, moveY):

    scaleFactor, marginX, marginY = getScale(ufo1, ufo2, g, canvasx, canvasy, margin)

    animation(ufo1, ufo2, g, canvasx, canvasy, scaleFactor, marginX, marginY, moveY)
    animation(ufo2, ufo1, g, canvasx, canvasy, scaleFactor, marginX, marginY, moveY) #second for a loop back
    
    saveImage(["~/Desktop/TypoTechnikStammtisch_%s.gif" %g]) 

for g in gList:
    print 'Start: ', g
    newDrawing()
    main(ufo1, ufo2, g, canvasx, canvasy, margin, moveY)
    print 'Finished: ', g
