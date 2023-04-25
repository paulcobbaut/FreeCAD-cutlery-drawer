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

doc = App.newDocument("Tide")

# drawer
c_depth = 30  # The depth of a hole that holds forks, spoons, knives...
b_height = 10 # The height that is for sure above the Fillet for the bottom vertex of the vertical edges
b_radius = 3  # Bottom Fillet Radius
s_radius = 2  # Side Fillet Radius (somehow cannot be more than 2)

# forks
# handle width/length and tines width/length in mm
# assuming a fork has two parts: a handle and a tines 
fork14 = { "handw": 14, "handl": 100, "tinew": 24, "tinel": 50 }
fork15 = { "handw": 15, "handl": 100, "tinew": 26, "tinel": 55 }
fork18 = { "handw": 18, "handl": 115, "tinew": 28, "tinel": 65 }
fork20 = { "handw": 20, "handl": 140, "tinew": 30, "tinel": 75 }

# spoons
# handle width/length and bowl width/length in mm
# assuming a spoon has two parts: a handle and a bowl
# bowll odd number == 100% CPU for minutes
spoon13 = { "handw": 14, "handl":  90, "bowlw": 30, "bowll": 46 }
spoon15 = { "handw": 16, "handl": 100, "bowlw": 35, "bowll": 56 }
spoon18 = { "handw": 18, "handl": 120, "bowlw": 42, "bowll": 66 }
spoon21 = { "handw": 20, "handl": 140, "bowlw": 50, "bowll": 76 }

# knives
# simple rectangle box for knives
knive17 = { "width": 30, "length": 170 }
knive18 = { "width": 32, "length": 180 }
knive21 = { "width": 34, "length": 215 }
knive24 = { "width": 36, "length": 245 }

# specials

# creates a sketch for one fork size
def create_fork_Sketch(label, fork):
    BodyLabel   = 'Body_'   + label
    SketchLabel = 'Sketch_' + label
    # create Body and Sketch Object
    Body_obj   = doc.addObject("PartDesign::Body", BodyLabel)
    Sketch_obj = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
    # create points
    point0 = App.Vector(0                          , 0                            , 0)
    point1 = App.Vector(fork["handw"]              , 0                            , 0)
    point2 = App.Vector(fork["handw"]              , fork["handl"]                , 0)
    point3 = App.Vector(fork["tinew"]              , fork["handl"]                , 0)
    point4 = App.Vector(fork["tinew"]              , fork["handl"] + fork["tinel"], 0)
    point5 = App.Vector(fork["handw"]-fork["tinew"], fork["handl"] + fork["tinel"], 0)
    point6 = App.Vector(fork["handw"]-fork["tinew"], fork["handl"]                , 0)
    point7 = App.Vector(0                          , fork["handl"]                , 0)
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
def create_spoon_Sketch(label, spoon):
    BodyLabel   = 'Body_'   + label
    SketchLabel = 'Sketch_' + label
    # added to handle length for overlap with ellipse followed by trim
    overlap = 40 
    # create Body and Sketch Object
    Body_obj = doc.addObject("PartDesign::Body", BodyLabel)
    Sketch_obj = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
    # create points
    point0 = App.Vector(0             , 0                       , 0)
    point1 = App.Vector(spoon["handw"], 0                       , 0)
    point2 = App.Vector(spoon["handw"], spoon["handl"] + overlap, 0)
    point3 = App.Vector(0             , spoon["handl"] + overlap, 0)
    # create lines that kinda surround a spoon handle
    Sketch_obj.addGeometry(Part.LineSegment(point0,point1),False)
    Sketch_obj.addGeometry(Part.LineSegment(point1,point2),False)
    Sketch_obj.addGeometry(Part.LineSegment(point2,point3),False)
    Sketch_obj.addGeometry(Part.LineSegment(point3,point0),False)
    # create an ellipse that kinda surrounds a spoon bowl
    # major axis(bottom point), minor_axis(right point), center
    e_major  = App.Vector(spoon["handw"]/2                   , spoon["handl"]                   , 0)
    e_minor  = App.Vector(spoon["handw"]/2 + spoon["bowlw"]/2, spoon["handl"] + spoon["bowll"]/2, 0)
    e_center = App.Vector(spoon["handw"]/2                   , spoon["handl"] + spoon["bowll"]/2, 0)
    Sketch_obj.addGeometry(Part.Ellipse(e_major, e_minor, e_center),False)
    # trim the unneeded lines
    Sketch_obj.trim(2,App.Vector(spoon["handw"]/2, spoon["handl"]+40, 0))
    Sketch_obj.trim(1,App.Vector(spoon["handw"]  , spoon["handl"]+20, 0))
    Sketch_obj.trim(2,App.Vector(0               , spoon["handl"]+20, 0))
    Sketch_obj.trim(3,App.Vector(spoon["handw"]/2, spoon["handl"]   , 0))
    return Sketch_obj

# create a sketch for one knive size
def create_knive_Sketch(label, knive):
    BodyLabel   = 'Body_'   + label
    SketchLabel = 'Sketch_' + label
    # create Body and Sketch Object
    Body_obj   = doc.addObject("PartDesign::Body", BodyLabel)
    Sketch_obj = doc.getObject(BodyLabel).newObject("Sketcher::SketchObject", SketchLabel)
    # create points
    point0 = App.Vector(0             , 0              , 0)
    point1 = App.Vector(knive["width"], 0              , 0)
    point2 = App.Vector(knive["width"], knive["length"], 0)
    point3 = App.Vector(0             , knive["length"], 0)
    # create lines that form a rectangle
    Sketch_obj.addGeometry(Part.LineSegment(point0,point1),False)
    Sketch_obj.addGeometry(Part.LineSegment(point1,point2),False)
    Sketch_obj.addGeometry(Part.LineSegment(point2,point3),False)
    Sketch_obj.addGeometry(Part.LineSegment(point3,point0),False)
    return Sketch_obj

# pads a sketch
def create_Pad(label):
    BodyLabel   = 'Body_' + label
    SketchLabel = 'Sketch_' + label
    PadLabel    = 'Pad_' + label
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
def create_Fillet(label):
    BodyLabel    = 'Body_'    + label
    FilletLabel  = 'Fillet_'  + label
    IFilletLabel = 'IFillet_' + label
    PadLabel     = 'Pad_'     + label
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

# spoons
Sketch_spoon13 = create_spoon_Sketch('spoon13', spoon13)
Pad_spoon13 = create_Pad('spoon13')
Fillet_spoon13 = create_Fillet('spoon13')

Sketch_spoon15 = create_spoon_Sketch('spoon15', spoon15)
Pad_spoon15 = create_Pad('spoon15')
Fillet_spoon15 = create_Fillet('spoon15')

Sketch_spoon18 = create_spoon_Sketch('spoon18', spoon18)
Pad_spoon18 = create_Pad('spoon18')
Fillet_spoon18 = create_Fillet('spoon18')

Sketch_spoon21 = create_spoon_Sketch('spoon21', spoon21)
Pad_spoon21 = create_Pad('spoon21')
Fillet_spoon21 = create_Fillet('spoon21')

# forks
Sketch_fork14 = create_fork_Sketch('fork14',fork14)
Pad_fork14 = create_Pad('fork14')
Fillet_fork14 = create_Fillet('fork14')

Sketch_fork15 = create_fork_Sketch('fork15',fork15)
Pad_fork15 = create_Pad('fork15')
Fillet_fork15 = create_Fillet('fork15')

Sketch_fork18 = create_fork_Sketch('fork18',fork18)
Pad_fork18 = create_Pad('fork18')
Fillet_fork18 = create_Fillet('fork18')

Sketch_fork15 = create_fork_Sketch('fork20',fork20)
Pad_fork15 = create_Pad('fork20')
Fillet_fork15 = create_Fillet('fork20')

# knives
Sketch_knive17 = create_knive_Sketch('knive17',knive17)
Pad_knive17 = create_Pad('knive17')
Fillet_knive17 = create_Fillet('knive17')

Sketch_knive18 = create_knive_Sketch('knive18',knive18)
Pad_knive18 = create_Pad('knive18')
Fillet_knive18 = create_Fillet('knive18')

Sketch_knive21 = create_knive_Sketch('knive21',knive21)
Pad_knive21 = create_Pad('knive21')
Fillet_knive21 = create_Fillet('knive21')

Sketch_knive24 = create_knive_Sketch('knive24',knive24)
Pad_knive24 = create_Pad('knive24')
Fillet_knive24 = create_Fillet('knive24')

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

position = App.Vector(0, 300, 0)
doc.getObject('Sketch_fork14').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(100, 300, 0)
doc.getObject('Sketch_fork15').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(200, 300, 0)
doc.getObject('Sketch_fork18').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(300, 300, 0)
doc.getObject('Sketch_fork20').Placement = FreeCAD.Placement(position, rotation) 

position = App.Vector(0, 600, 0)
doc.getObject('Sketch_knive17').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(100, 600, 0)
doc.getObject('Sketch_knive18').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(200, 600, 0)
doc.getObject('Sketch_knive21').Placement = FreeCAD.Placement(position, rotation) 
position = App.Vector(300, 600, 0)
doc.getObject('Sketch_knive24').Placement = FreeCAD.Placement(position, rotation) 

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
