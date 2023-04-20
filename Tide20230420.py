"""
Tide bestek schuif
Tide cuttlery drawer
Paul Cobbaut
2023-04-20
"""

import FreeCAD as App

doc = App.newDocument("Tide20230420py")
obj = doc.addObject("PartDesign::Body", "Body")

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


def create_fork_sketch(sketch, handw, handl, tinew, tinel):
  point0 = App.Vector(0,           0,           0)
  point1 = App.Vector(handw,       0,           0)
  point2 = App.Vector(handw,       handl,       0)
  point3 = App.Vector(tinew,       handl,       0)
  point4 = App.Vector(tinew,       handl+tinel, 0)
  point5 = App.Vector(handw-tinew, handl+tinel, 0)
  point6 = App.Vector(handw-tinew, handl,       0)
  point7 = App.Vector(0,           handl,       0)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point0,point1),False)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point1,point2),False)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point2,point3),False)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point3,point4),False)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point4,point5),False)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point5,point6),False)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point6,point7),False)
  doc.getObject(sketch).addGeometry(Part.LineSegment(point7,point0),False)


def create_pad(sketch, pad):
  doc.getObject('Body').newObject('PartDesign::Pad',pad)
  doc.getObject(pad).Profile = doc.getObject(sketch)
  doc.getObject(pad).Length = 30
  doc.getObject(pad).AlongSketchNormal = 1
  doc.getObject(pad).Direction = (0, 0, 1)
  doc.getObject(sketch).Visibility = False


sketch_fork14cm = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_fork14cm")
sketch_fork15cm = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_fork15cm")
sketch_fork18cm = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_fork18cm")
sketch_fork20cm = doc.getObject('Body').newObject("Sketcher::SketchObject", "sketch_fork20cm")

create_fork_sketch('sketch_fork14cm',fork14cm_handw, fork14cm_handl, fork14cm_tinew, fork14cm_tinel)
create_fork_sketch('sketch_fork15cm',fork15cm_handw, fork15cm_handl, fork15cm_tinew, fork15cm_tinel)
create_fork_sketch('sketch_fork18cm',fork18cm_handw, fork18cm_handl, fork18cm_tinew, fork18cm_tinel)
create_fork_sketch('sketch_fork20cm',fork20cm_handw, fork20cm_handl, fork20cm_tinew, fork20cm_tinel)

rotation = App.Rotation(0, 0, 0)

position = App.Vector(0, 0, 0)
doc.getObject('sketch_fork14cm').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(100, 0, 0)
doc.getObject('sketch_fork15cm').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(200, 0, 0)
doc.getObject('sketch_fork18cm').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(300, 0, 0)
doc.getObject('sketch_fork20cm').Placement = FreeCAD.Placement(position, rotation) 

create_pad('sketch_fork14cm','pad_fork14cm')
create_pad('sketch_fork15cm','pad_fork15cm')
create_pad('sketch_fork18cm','pad_fork18cm')
create_pad('sketch_fork20cm','pad_fork20cm')


doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()



