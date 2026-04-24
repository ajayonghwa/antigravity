import cadquery as cq

class Splitter:
    def __init__(self, model):
        self.model = model

    def apply_planar_split(self, origin, normal):
        # The most basic CadQuery split possible
        try:
            # We must use the original solid and perform a split operation
            solid = self.model.val()
            # Create a plane and split
            side_a = self.model.copyWorkplane(cq.Plane(origin=origin, normal=normal)).split(keepTop=True)
            side_b = self.model.copyWorkplane(cq.Plane(origin=origin, normal=normal)).split(keepBottom=True)
            return [side_a, side_b]
        except:
            return [self.model]

class StrategyPlanner:
    def __init__(self, model, **kwargs):
        self.model = model

    def plan_and_execute(self):
        print("!!! TEST FORCED SPLIT !!!")
        # Just split once at X=0 to see if it works
        s = Splitter(self.model)
        results = s.apply_planar_split(cq.Vector(0,0,0), cq.Vector(1,0,0))
        print(f"FORCED SPLIT produced {len(results)} bodies")
        return results
