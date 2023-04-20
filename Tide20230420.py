"""
Tide bestek schuif
Tide cuttlery drawer
Paul Cobbaut
2023-04-20
"""

import FreeCAD as App
import Part
import Sketcher

doc = App.newDocument("Tide20230420py")

# handle width/length and tines width/length in mm
fork14cm_handw = 15
fork14cm_handl = 100
fork14cm_tinew = 24
fork14cm_tinel = 50

fork15cm_handw = 15
fork15cm_handl = 100
fork15cm_tinew = 26
fork15cm_tinel = 55

fork18cm_handw = 18
fork18cm_handl = 115
fork18cm_tinew = 28
fork18cm_tinel = 65

fork20cm_handw = 20
fork20cm_handl = 140
fork20cm_tinew = 30
fork20cm_tinel = 75


def create_fork_Sketch(BodyLabel, SketchLabel, handw, handl, tinew, tinel):
    Sketch_obj = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
    point0 = App.Vector(0,           0,           0)
    point1 = App.Vector(handw,       0,           0)
    point2 = App.Vector(handw,       handl,       0)
    point3 = App.Vector(tinew,       handl,       0)
    point4 = App.Vector(tinew,       handl+tinel, 0)
    point5 = App.Vector(handw-tinew, handl+tinel, 0)
    point6 = App.Vector(handw-tinew, handl,       0)
    point7 = App.Vector(0,           handl,       0)
    Sketch_obj.addGeometry(Part.LineSegment(point0,point1),False)
    Sketch_obj.addGeometry(Part.LineSegment(point1,point2),False)
    Sketch_obj.addGeometry(Part.LineSegment(point2,point3),False)
    Sketch_obj.addGeometry(Part.LineSegment(point3,point4),False)
    Sketch_obj.addGeometry(Part.LineSegment(point4,point5),False)
    Sketch_obj.addGeometry(Part.LineSegment(point5,point6),False)
    Sketch_obj.addGeometry(Part.LineSegment(point6,point7),False)
    Sketch_obj.addGeometry(Part.LineSegment(point7,point0),False)
    return Sketch_obj

def create_fork_Pad(BodyLabel, SketchLabel, PadLabel):
    Pad_obj = doc.getObject(BodyLabel).newObject('PartDesign::Pad',PadLabel)
    Pad_obj.Profile = doc.getObject(SketchLabel)
    Pad_obj.Length = 30
    Pad_obj.ReferenceAxis = (doc.getObject(SketchLabel), ['N_Axis'])
    Pad_obj.Label = PadLabel
    Pad_obj.AlongSketchNormal = 1
    Pad_obj.Direction = (0, 0, 1)
    return Pad_obj

def create_fork_Fillet(BodyLabel, FilletLabel, PadLabel):
    Fillet_obj = doc.getObject(BodyLabel).newObjectAt('PartDesign::Fillet',FilletLabel)
    Fillet_obj.Base = (doc.getObject(PadLabel),['Face9',])
    Fillet_obj.Radius = 2
    return Fillet_obj


Body_fork14cm = doc.addObject("PartDesign::Body", "Body_fork14cm")
Sketch_fork14cm = create_fork_Sketch('Body_fork14cm','Sketch_fork14cm',fork14cm_handw, fork14cm_handl, fork14cm_tinew, fork14cm_tinel)
Pad_fork14cm = create_fork_Pad('Body_fork14cm','Sketch_fork14cm','Pad_fork14cm')
Fillet_fork14cm = create_fork_Fillet('Body_fork14cm','Fillet_fork14cm','Pad_fork14cm')

Body_fork15cm = doc.addObject("PartDesign::Body", "Body_fork15cm")
Sketch_fork15cm = create_fork_Sketch('Body_fork15cm','Sketch_fork15cm',fork15cm_handw, fork15cm_handl, fork15cm_tinew, fork15cm_tinel)
Pad_fork15cm = create_fork_Pad('Body_fork15cm','Sketch_fork15cm','Pad_fork15cm')
Fillet_fork15cm = create_fork_Fillet('Body_fork15cm','Fillet_fork15cm','Pad_fork15cm')

Body_fork18cm = doc.addObject("PartDesign::Body", "Body_fork18cm")
Sketch_fork18cm = create_fork_Sketch('Body_fork18cm','Sketch_fork18cm',fork18cm_handw, fork18cm_handl, fork18cm_tinew, fork18cm_tinel)
Pad_fork18cm = create_fork_Pad('Body_fork18cm','Sketch_fork18cm','Pad_fork18cm')
Fillet_fork18cm = create_fork_Fillet('Body_fork18cm','Fillet_fork18cm','Pad_fork18cm')

Body_fork15cm = doc.addObject("PartDesign::Body", "Body_fork20cm")
Sketch_fork15cm = create_fork_Sketch('Body_fork20cm','Sketch_fork20cm',fork20cm_handw, fork20cm_handl, fork20cm_tinew, fork20cm_tinel)
Pad_fork15cm = create_fork_Pad('Body_fork20cm','Sketch_fork20cm','Pad_fork20cm')
Fillet_fork15cm = create_fork_Fillet('Body_fork20cm','Fillet_fork20cm','Pad_fork20cm')

rotation = App.Rotation(0, 0, 0)
position = App.Vector(0, 0, 0)
doc.getObject('Sketch_fork14cm').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(100, 0, 0)
doc.getObject('Sketch_fork15cm').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(200, 0, 0)
doc.getObject('Sketch_fork18cm').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(300, 0, 0)
doc.getObject('Sketch_fork20cm').Placement = FreeCAD.Placement(position, rotation) 

doc.recompute()

FreeCADGui.ActiveDocument.ActiveView.fitAll()

