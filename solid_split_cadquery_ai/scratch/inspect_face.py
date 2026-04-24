import cadquery as cq
box = cq.Workplane("XY").box(10, 10, 10)
face = box.faces(">Z").val()
print(dir(face))
