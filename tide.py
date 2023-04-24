"""
Tide bestek schuif
Tide cuttlery drawer
Paul Cobbaut
2023-04-20

The goal is to 3D print a cutlery drawer(*).
The tableware consists of:
4 sizes forks:  14-15-18-20cm
4 sizes knives: 16-18-21-24cm
4 sizes spoons: 13-15-18-21cm
11 special items 

Idea is to create an object that fills the drawer and then cut out the holes that
contain all the items. So the objects created in this script will be subtracted
from the drawer space.

(*) Primary goal is to just have fun.
"""

import FreeCAD as App
import Part
import Sketcher
import PartDesign
import re

doc = App.newDocument("Tide20230420py")

# drawer
c_depth = 30  # The depth of a hole that holds forks, spoons, knives...
b_height = 10 # The height that is for sure above the Fillet for the bottom vertex of the vertical edges
b_radius = 3  # Bottom Fillet Radius
s_radius = 2  # Side Fillet Radius (somehow cannot be more than 2)

# forks
# handle width/length and tines width/length in mm
# assuming a fork has two parts: a handle and a tines 
fork14_handw = 15
fork14_handl = 100
fork14_tinew = 24
fork14_tinel = 50

fork15_handw = 15
fork15_handl = 100
fork15_tinew = 26
fork15_tinel = 55

fork18_handw = 18
fork18_handl = 115
fork18_tinew = 28
fork18_tinel = 65

fork20_handw = 20
fork20_handl = 140
fork20_tinew = 30
fork20_tinel = 75

# spoons
# handle width/length and bowl width/length in mm
# assuming a spoon has two parts: a handle and a bowl
spoon13_handw = 14
spoon13_handl = 90
spoon13_bowlw = 30
spoon13_bowll = 46/2

spoon15_handw = 16
spoon15_handl = 100
spoon15_bowlw = 35
spoon15_bowll = 56/2

spoon18_handw = 18
spoon18_handl = 120
spoon18_bowlw = 42
spoon18_bowll = 66/2

spoon21_handw = 20
spoon21_handl = 140
spoon21_bowlw = 50
spoon21_bowll = 76/2


# creates a sketch for one fork size
def create_fork_Sketch(BodyLabel, SketchLabel, handw, handl, tinew, tinel):
    # create Sketch Object
    Sketch_obj = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
    # create points
    point0 = App.Vector(0,           0,           0)
    point1 = App.Vector(handw,       0,           0)
    point2 = App.Vector(handw,       handl,       0)
    point3 = App.Vector(tinew,       handl,       0)
    point4 = App.Vector(tinew,       handl+tinel, 0)
    point5 = App.Vector(handw-tinew, handl+tinel, 0)
    point6 = App.Vector(handw-tinew, handl,       0)
    point7 = App.Vector(0,           handl,       0)
    # create lines that kinda surround a fork
    Sketch_obj.addGeometry(Part.LineSegment(point0,point1),False)
    Sketch_obj.addGeometry(Part.LineSegment(point1,point2),False)
    Sketch_obj.addGeometry(Part.LineSegment(point2,point3),False)
    Sketch_obj.addGeometry(Part.LineSegment(point3,point4),False)
    Sketch_obj.addGeometry(Part.LineSegment(point4,point5),False)
    Sketch_obj.addGeometry(Part.LineSegment(point5,point6),False)
    Sketch_obj.addGeometry(Part.LineSegment(point6,point7),False)
    Sketch_obj.addGeometry(Part.LineSegment(point7,point0),False)
    return Sketch_obj

# create a sketch for one spoon size
def create_spoon_Sketch(BodyLabel, SketchLabel, handw, handl, bowlw, bowll):
    # create Sketch Object
    Sketch_obj = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
    # create points
    point0 = App.Vector(0,           0,           0)
    point1 = App.Vector(handw,       0,           0)
    point2 = App.Vector(handw,       handl + 40,       0)
    point3 = App.Vector(0,           handl + 40,       0)
    # create lines that kinda surround a spoon handle
    Sketch_obj.addGeometry(Part.LineSegment(point0,point1),False)
    Sketch_obj.addGeometry(Part.LineSegment(point1,point2),False)
    Sketch_obj.addGeometry(Part.LineSegment(point2,point3),False)
    Sketch_obj.addGeometry(Part.LineSegment(point3,point0),False)
    # create an ellipse that kinda surrounds a spoon bowl
    # major axis(bottom point), minor_axis(right point), center
    e_major  = App.Vector(handw/2           ,handl         ,0)
    e_minor  = App.Vector(handw/2 + bowlw/2 ,handl + bowll ,0)
    e_center = App.Vector(handw/2           ,handl + bowll ,0)
    Sketch_obj.addGeometry(Part.Ellipse(e_major, e_minor, e_center),False)
    # trim the unneeded lines
    Sketch_obj.trim(2,App.Vector(handw/2,handl+40,0))
    Sketch_obj.trim(1,App.Vector(handw,handl+20,0))
    Sketch_obj.trim(2,App.Vector(0,handl+20,0))
    Sketch_obj.trim(3,App.Vector(handw/2,handl,0))


# pads a sketch
def create_Pad(BodyLabel, SketchLabel, PadLabel):
    # create Pad Object
    Pad_obj = doc.getObject(BodyLabel).newObject('PartDesign::Pad',PadLabel)
    Pad_obj.Profile = doc.getObject(SketchLabel)
    Pad_obj.Length = c_depth
    Pad_obj.ReferenceAxis = (doc.getObject(SketchLabel), ['N_Axis'])
    Pad_obj.Label = PadLabel
    Pad_obj.AlongSketchNormal = 1
    Pad_obj.Direction = (0, 0, 1)
    doc.getObject(SketchLabel).Visibility = False
    doc.recompute()
    return Pad_obj

# rounds some corners 
def create_Fillet(BodyLabel, FilletLabel, IFilletLabel, PadLabel):
    # first Fillet the bottom
    # find bottom edges
    bottom_edges = []
    for idx_edge, edge in enumerate(doc.getObject(BodyLabel).getObject(PadLabel).Shape.Edges):
        z1 = edge.Vertexes[1].Point.z
        if z1 == 0:
            bottom_edges.append('Edge' + str(idx_edge + 1))
    # create Fillet on found edges at the bottom
    Fillet_bottom = doc.getObject(BodyLabel).newObjectAt('PartDesign::Fillet',IFilletLabel)
    Fillet_bottom.Base = (doc.getObject(PadLabel),bottom_edges)
    Fillet_bottom.Radius = b_radius
    doc.recompute()
    # second Fillet the vertical edges
    # find vertical edges
    vertical_edges = []
    for idx_edge, edge in enumerate(doc.getObject(BodyLabel).getObject(IFilletLabel).Shape.Edges):
        z0 = edge.Vertexes[0].Point.z
        z1 = edge.Vertexes[1].Point.z
        if (z0 < b_height) and (z1 == c_depth):
            vertical_edges.append('Edge' + str(idx_edge + 1))
    # create Fillet on found vertical edges
    Fillet_vertical = doc.getObject(BodyLabel).newObjectAt('PartDesign::Fillet',FilletLabel)
    Fillet_vertical.Base = (doc.getObject(IFilletLabel),vertical_edges)
    Fillet_vertical.Radius = s_radius
    doc.recompute()
    return Fillet_vertical


# 14 spoon
Body_spoon13 = doc.addObject("PartDesign::Body", "Body_spoon13")
Sketch_spoon13 = create_spoon_Sketch('Body_spoon13','Sketch_spoon13', spoon13_handw, spoon13_handl, spoon13_bowlw, spoon13_bowll)
Pad_spoon13 = create_Pad('Body_spoon13','Sketch_spoon13','Pad_spoon13')
Fillet_spoon13 = create_Fillet('Body_spoon13','Fillet_spoon13','IFillet_spoon13','Pad_spoon13')

Body_spoon15 = doc.addObject("PartDesign::Body", "Body_spoon15")
Sketch_spoon15 = create_spoon_Sketch('Body_spoon15','Sketch_spoon15', spoon15_handw, spoon15_handl, spoon15_bowlw, spoon15_bowll)
Pad_spoon15 = create_Pad('Body_spoon15','Sketch_spoon15','Pad_spoon15')
Fillet_spoon15 = create_Fillet('Body_spoon15','Fillet_spoon15','IFillet_spoon15','Pad_spoon15')

Body_spoon18 = doc.addObject("PartDesign::Body", "Body_spoon18")
Sketch_spoon18 = create_spoon_Sketch('Body_spoon18','Sketch_spoon18', spoon18_handw, spoon18_handl, spoon18_bowlw, spoon18_bowll)
Pad_spoon18 = create_Pad('Body_spoon18','Sketch_spoon18','Pad_spoon18')
Fillet_spoon18 = create_Fillet('Body_spoon18','Fillet_spoon18','IFillet_spoon18','Pad_spoon18')

Body_spoon21 = doc.addObject("PartDesign::Body", "Body_spoon21")
Sketch_spoon21 = create_spoon_Sketch('Body_spoon21','Sketch_spoon21', spoon21_handw, spoon21_handl, spoon21_bowlw, spoon21_bowll)
Pad_spoon21 = create_Pad('Body_spoon21','Sketch_spoon21','Pad_spoon21')
Fillet_spoon21 = create_Fillet('Body_spoon21','Fillet_spoon21','IFillet_spoon21','Pad_spoon21')

# separating the objects
rotation = App.Rotation(0, 0, 0)
position = App.Vector(0, 0, 0)
doc.getObject('Sketch_spoon13').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(100, 0, 0)
doc.getObject('Sketch_spoon15').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(200, 0, 0)
doc.getObject('Sketch_spoon18').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(300, 0, 0)
doc.getObject('Sketch_spoon21').Placement = FreeCAD.Placement(position, rotation) 

# create fillet-ed pads for the four fork sizes
# 14 fork
Body_fork14 = doc.addObject("PartDesign::Body", "Body_fork14")
Sketch_fork14 = create_fork_Sketch('Body_fork14','Sketch_fork14',fork14_handw, fork14_handl, fork14_tinew, fork14_tinel)
Pad_fork14 = create_Pad('Body_fork14','Sketch_fork14','Pad_fork14')
Fillet_fork14 = create_Fillet('Body_fork14','Fillet_fork14','IFillet_fork14','Pad_fork14')

# 15 fork
Body_fork15 = doc.addObject("PartDesign::Body", "Body_fork15")
Sketch_fork15 = create_fork_Sketch('Body_fork15','Sketch_fork15',fork15_handw, fork15_handl, fork15_tinew, fork15_tinel)
Pad_fork15 = create_Pad('Body_fork15','Sketch_fork15','Pad_fork15')
Fillet_fork15 = create_Fillet('Body_fork15','Fillet_fork15','IFillet_fork15','Pad_fork15')

# 18 fork
Body_fork18 = doc.addObject("PartDesign::Body", "Body_fork18")
Sketch_fork18 = create_fork_Sketch('Body_fork18','Sketch_fork18',fork18_handw, fork18_handl, fork18_tinew, fork18_tinel)
Pad_fork18 = create_Pad('Body_fork18','Sketch_fork18','Pad_fork18')
Fillet_fork18 = create_Fillet('Body_fork18','Fillet_fork18','IFillet_fork18','Pad_fork18')

# 20 fork
Body_fork15 = doc.addObject("PartDesign::Body", "Body_fork20")
Sketch_fork15 = create_fork_Sketch('Body_fork20','Sketch_fork20',fork20_handw, fork20_handl, fork20_tinew, fork20_tinel)
Pad_fork15 = create_Pad('Body_fork20','Sketch_fork20','Pad_fork20')
Fillet_fork15 = create_Fillet('Body_fork20','Fillet_fork20','IFillet_fork20','Pad_fork20')


# separating the objects
rotation = App.Rotation(0, 0, 0)
position = App.Vector(0, 300, 0)
doc.getObject('Sketch_fork14').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(100, 300, 0)
doc.getObject('Sketch_fork15').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(200, 300, 0)
doc.getObject('Sketch_fork18').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(300, 300, 0)
doc.getObject('Sketch_fork20').Placement = FreeCAD.Placement(position, rotation) 

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
