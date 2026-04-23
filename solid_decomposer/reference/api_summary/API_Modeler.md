  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnalysisAspect.SharedFaceGroups`
    - **summary:** Gets groups of shared faces.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnalysisAspect.SharedEdgeGroups`
    - **summary:** Gets groups of shared edges.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnalysisAspect.SharedEdgeBeamGroups`
    - **summary:** Gets shared information related to edges and beams.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AnalysisAspect.IsBafflePair(SpaceClaim.Api.V22.IDesignBody,SpaceClaim.Api.V22.IDesignBody,System.Double)`
    - **summary:** Gets whether bodies form a baffle system.
    - **param:** The first body.
      - *@name:* `desBodyA`
    - **param:** The second body.
      - *@name:* `desBodyB`
    - **param:** The tolerance value.
      - *@name:* `tolerance`
    - **remarks** The tolerance is in meters.
            
            Only baffle systems with solid-surface connections are recognized.
      - **para**
    - **returns** if the bodies form a baffle system; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AnalysisAspect.GetBafflesAndExternalShells(System.Collections.Generic.IList{SpaceClaim.Api.V22.IDesignBody},System.Collections.Generic.IList{SpaceClaim.Api.V22.IDesignBody},System.Double,System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.IDesignBody,System.Collections.Generic.IList{SpaceClaim.Api.V22.IDesignBody}}@,System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.IDesignBody,System.Collections.Generic.IList{SpaceClaim.Api.V22.IDesignBody}}@)`
    - **summary:** Returns baffle systems and external shells.
    - **param:** Solid bodies in the part.
      - *@name:* `solidBodies`
    - **param:** surface bodies in the part.
      - *@name:* `surfaceBodies`
    - **param:** The tolerance value.
      - *@name:* `tolerance`
    - **param**
      - *@name:* `solidBodyToBaffles`
    - **param**
      - *@name:* `solidBodyToExternalShells`
    - **remarks** The tolerance is in meters.
            
            Baffle systems and external shells with solid-surface connections are recognized.
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AnalysisAspect.IsInternalBafflePair(SpaceClaim.Api.V22.IDesignBody,SpaceClaim.Api.V22.IDesignBody,System.Double)`
    - **summary:** Gets whether bodies form a internal baffle system.
    - **param:** The first body.
      - *@name:* `desBodyA`
    - **param:** The second body.
      - *@name:* `desBodyB`
    - **param:** The tolerance value.
      - *@name:* `tolerance`
    - **remarks** The tolerance is in meters.
            
            Only baffle systems with solid-surface connections are recognized.
      - **para**
    - **returns** if the bodies form a internal baffle system; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.EdgeSizeControl.SpaceClaim#Api#V22#Analysis#IEdgeSizeControl#Edges`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.Analysis.IEdgeSizeControl.Edges`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.IEdgeSizeControl.Parent`
    - **summary:** Gets the parent part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.IFaceSizeControl.Parent`
    - **summary:** Gets the parent part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.HexaBlocking.SuperEdgeCount`
    - **summary:** Gets the number of super edges.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.HexaBlocking.SuperFaceCount`
    - **summary:** Gets the number of super faces.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Analysis.MeshBodySettings.Create(SpaceClaim.Api.V22.DesignBody)`
    - **summary:** Creates Mesh Settings Object on a given body
    - **returns:** The newly created Mesh Settings object

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Analysis.MeshBodySettings.Create(SpaceClaim.Api.V22.IDesignBody)`
    - **summary:** Creates Mesh Settings Object on a given body
    - **returns:** The newly created Mesh Settings object

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.BodyMesh.FaceElements`
    - **summary:** Gets face elements.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.BodyMesh.EdgeElements`
    - **summary:** Gets edge elements.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Analysis.FaceElement`
    - **summary:** A face mesh element.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.FaceElement.Id`
    - **summary:** Gets the id.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.FaceElement.Type`
    - **summary:** Gets the element type.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Analysis.EdgeElement`
    - **summary:** An edge mesh element.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.EdgeElement.Id`
    - **summary:** Gets the id.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.EdgeElement.Type`
    - **summary:** Gets the element type.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Analysis.PartMesh`
    - **summary:** A part mesh.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.PartMesh.Id`
    - **summary:** Gets the id.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.PartMesh.NodeCount`
    - **summary:** Gets the total number of nodes.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.PartMesh.ElementCount`
    - **summary:** Gets the total number of elements.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.PartMesh.BodyMeshes`
    - **summary:** Gets the body meshes.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.AssemblyMesh.PartMeshes`
    - **summary:** Gets the part meshes.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDatumFeature.Faces`
    - **summary:** Gets the faces used to define the datum feature.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.AttachToFace`
    - **summary:** Specifies the attachment of an image to a design face.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `T:SpaceClaim.Api.V22.ImageAttachment`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AttachToFace.Face`
    - **summary:** Gets the design face to which the image is attached.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AttachToFace.Location`
    - **summary:** Gets or sets the location of the center of the image in the parameter space of the surface of the face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AttachToFace.Angle`
    - **summary:** Gets or sets the orientation angle of the image.
    - **remarks:** The angle is in radians.
            The angle specifies the clockwise rotation about the normal of the surface of the face,
            (i.e. a counterclockwise rotation as seen looking down onto the surface), measured from the local 
            U direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AttachToFace.IsReversed`
    - **summary:** Gets or sets whether the image is reversed.
    - **remarks** If the image is not reversed, then the front of the image is in the direction of the surface normal.
            If it is reversed, then the back of the image is in the direction of the surface normal.
            
            To create an image on a design face, so that the front of the image is visible when looking at the face,
            you can set this property to be equal to the  property of
            the  of the design face.
            
            
            
            The sense of the  is not affected by whether the image is reversed,
            i.e. the image is reversed left-to-right  rotating by the .
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Face.IsReversed`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DesignFace.Shape`
      - **para**
      - **code:** IDesignFace desFace = ...
            Face shape = desFace.Shape;
            
            AttachToFace attachment = new AttachToFace();
            attachment.Face = desFace;
            attachment.IsReversed = shape.IsReversed;
            attachment.Location = shape.BoxUV.Center;
            
            image.Attachment = attachment;
        - *@lang:* `C#`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.AttachToFace.Angle`
      - **i:** after
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.AttachToFace.Angle`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IBlockEdge.Parent`
    - **summary:** Gets the parent part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IBlockFace.Parent`
    - **summary:** Gets the parent part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Blocking.BlockEdges`
    - **summary:** Gets the block edges of the blocking

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Blocking.BlockFaces`
    - **summary:** Gets the block faces of the blocking

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.CustomPartProperty`
    - **summary:** A custom property of a part.
    - **remarks** returns the collection of custom properties for a part.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Part.CustomProperties`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomPartProperty.Create(SpaceClaim.Api.V22.Part,System.String,System.String)`
    - **summary** Creates a custom property with a  value.
      - **see**
        - *@cref:* `T:System.String`
    - **param:** The part in which the custom property should be created.
      - *@name:* `part`
    - **param:** The name of the custom property.
      - *@name:* `name`
    - **param:** The value for the custom property.
      - *@name:* `value`
    - **returns:** The new custom property.
    - **exception:** A custom property already exists with the specified name.
      - *@cref:* `T:System.ArgumentException`
    - **remarks:** To make custom property names unique, add-in developers should prefix private custom properties
            as follows: "<company name>.<add-in name>.<custom property name>", e.g. "BeachSoft.PebbleDesigner.RockType".

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomPartProperty.Create(SpaceClaim.Api.V22.Part,System.String,System.Boolean)`
    - **summary** Creates a custom property with a  value.
      - **see**
        - *@cref:* `T:System.Boolean`
    - **param:** The part in which the custom property should be created.
      - *@name:* `part`
    - **param:** The name of the custom property.
      - *@name:* `name`
    - **param:** The value for the custom property.
      - *@name:* `value`
    - **returns:** The new custom property.
    - **exception:** A custom property already exists with the specified name.
      - *@cref:* `T:System.ArgumentException`
    - **remarks:** To make custom property names unique, add-in developers should prefix private custom properties
            as follows: "<company name>.<add-in name>.<custom property name>", e.g. "BeachSoft.PebbleDesigner.RockType".

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomPartProperty.Create(SpaceClaim.Api.V22.Part,System.String,System.Double)`
    - **summary** Creates a custom property with a  value.
      - **see**
        - *@cref:* `T:System.Double`
    - **param:** The part in which the custom property should be created.
      - *@name:* `part`
    - **param:** The name of the custom property.
      - *@name:* `name`
    - **param:** The value for the custom property.
      - *@name:* `value`
    - **returns:** The new custom property.
    - **exception:** A custom property already exists with the specified name.
      - *@cref:* `T:System.ArgumentException`
    - **remarks:** To make custom property names unique, add-in developers should prefix private custom properties
            as follows: "<company name>.<add-in name>.<custom property name>", e.g. "BeachSoft.PebbleDesigner.RockType".

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomPartProperty.Create(SpaceClaim.Api.V22.Part,System.String,System.DateTime)`
    - **summary** Creates a custom property with a  value.
      - **see**
        - *@cref:* `T:System.DateTime`
    - **param:** The part in which the custom property should be created.
      - *@name:* `part`
    - **param:** The name of the custom property.
      - *@name:* `name`
    - **param:** The value for the custom property.
      - *@name:* `value`
    - **returns:** The new custom property.
    - **exception:** A custom property already exists with the specified name.
      - *@cref:* `T:System.ArgumentException`
    - **remarks:** To make custom property names unique, add-in developers should prefix private custom properties
            as follows: "<company name>.<add-in name>.<custom property name>", e.g. "BeachSoft.PebbleDesigner.RockType".

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CustomPartProperty.Name`
    - **summary:** Gets the name of the custom property.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CustomPartProperty.Value`
    - **summary:** Gets or sets the value of the custom property.
    - **exception:** Attempt to change the value type.
      - *@cref:* `T:System.InvalidCastException`
    - **remarks** The value type of the custom property is cannot be changed.
            For example, if you create a custom property with a  value, you cannot later assign a  value to it.
      - **b:** bool
      - **b:** string

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomPartProperty.Delete`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CustomPartProperty.IsDeleted`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.CustomPartPropertyDictionary`
    - **summary** A dictionary mapping names to  objects.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.CustomPartProperty`
    - **remarks** You can access a custom property of a specific name by looking it up using the indexer or the  method.
            Names are case sensitive.
            
            The collection of custom properties can be accessed using the  property.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.CustomPartPropertyDictionary.TryGetValue(System.String,SpaceClaim.Api.V22.CustomPartProperty@)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.CustomPartPropertyDictionary.Values`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.BoltHeadShape`
    - **summary:** The bolt head shape types.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BoltProperties.#ctor(SpaceClaim.Api.V22.BoltHeadShape,System.Double,System.Double,System.Double,System.String,System.String)`
    - **summary:** Constructs a bolt properties object.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Calculator.Create(SpaceClaim.Api.V22.Unsupported.Live.Solution,System.String,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDomainType,SpaceClaim.Api.V22.Unsupported.Live.ResultType,SpaceClaim.Api.V22.Unsupported.Live.IntegrantType,SpaceClaim.Api.V22.Unsupported.Live.ComponentType,System.Numerics.Vector3,SpaceClaim.Api.V22.Unsupported.Live.DiscreteOperatorType,SpaceClaim.Api.V22.Unsupported.Live.StatisticalOperatorType,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDisplayType,SpaceClaim.Api.V22.IDocObject)`
    - **summary:** Creates a custom surface or volume calculator at a single location.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Calculator.Create(SpaceClaim.Api.V22.Unsupported.Live.Solution,System.String,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDomainType,SpaceClaim.Api.V22.Unsupported.Live.ResultType,SpaceClaim.Api.V22.Unsupported.Live.IntegrantType,SpaceClaim.Api.V22.Unsupported.Live.ComponentType,System.Numerics.Vector3,SpaceClaim.Api.V22.Unsupported.Live.DiscreteOperatorType,SpaceClaim.Api.V22.Unsupported.Live.StatisticalOperatorType,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDisplayType,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary:** Creates a custom surface or volume calculator at a collection of locations.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Calculator.CreatePlaneCalculator(SpaceClaim.Api.V22.Unsupported.Live.Solution,System.String,SpaceClaim.Api.V22.Unsupported.Live.ResultType,SpaceClaim.Api.V22.Unsupported.Live.IntegrantType,SpaceClaim.Api.V22.Unsupported.Live.ComponentType,System.Numerics.Vector3,SpaceClaim.Api.V22.Unsupported.Live.DiscreteOperatorType,SpaceClaim.Api.V22.Unsupported.Live.StatisticalOperatorType,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDisplayType,SpaceClaim.Api.V22.IDocObject)`
    - **summary:** Creates a custom plane calculator at a single location.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Calculator.CreatePlaneCalculator(SpaceClaim.Api.V22.Unsupported.Live.Solution,System.String,SpaceClaim.Api.V22.Unsupported.Live.ResultType,SpaceClaim.Api.V22.Unsupported.Live.IntegrantType,SpaceClaim.Api.V22.Unsupported.Live.ComponentType,System.Numerics.Vector3,SpaceClaim.Api.V22.Unsupported.Live.DiscreteOperatorType,SpaceClaim.Api.V22.Unsupported.Live.StatisticalOperatorType,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDisplayType,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary:** Creates a custom plane calculator at a collection of locations.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Unsupported.Live.Result.ShowParticles`
    - **summary:** Gets or sets whether result particles are shown.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Result.SetComponent(SpaceClaim.Api.V22.Unsupported.Live.ComponentType)`
    - **summary:** Sets the result component to be used for display.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Solution.Create(SpaceClaim.Api.V22.Unsupported.Live.SolutionType,SpaceClaim.Api.V22.Unsupported.Live.TimeIntegrationType,System.String,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignBody})`
    - **summary:** Creates a solution for a collection of bodies.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.ComponentMethods.SetComponentSticky(SpaceClaim.Api.V22.IComponent,System.Boolean)`
    - **summary:** Set component as temporarily locked, preventing it from being deleted or reparented
    - **param**
      - *@name:* `comp`
    - **param**
      - *@name:* `isLocked`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.RuledCutting.FaceMethods.GetInflatedBoxUV(SpaceClaim.Api.V22.Modeler.Face,System.Double,System.Boolean,System.Boolean)`
    - **summary:** finds a uvbox that represents the initial size of the face 
            grown by a size in world units in the u and or v directions
    - **param:** face used as a base for finding the inflated uvbox
      - *@name:* `face`
    - **param:** amount in real world units to grow the uvbox of the face
      - *@name:* `size`
    - **param:** flag to grow in u direction
      - *@name:* `u`
    - **param:** flag to grow in v direction
      - *@name:* `v`
    - **returns**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.SpaceClaim#Api#V22#IHole#Faces`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.Faces`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.SpaceClaim#Api#V22#IHole#ReferenceFace`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.ReferenceFace`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.Faces`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.Faces`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.ReferenceFace`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.ReferenceFace`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IHole.Faces`
    - **summary:** Gets the faces of the hole.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IHole.ReferenceFace`
    - **summary:** Gets the reference face for the hole.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.PartType`
    - **summary:** The state of a sheet metal form in the flat pattern.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartType.Normal`
    - **summary:** A normal part.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartType.SheetMetal`
    - **summary:** A sheet metal part.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartType.FlatPattern`
    - **summary:** An sheet metal flat pattern part.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartType.BeamProfile`
    - **summary:** A beam profile part.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartType.Bolt`
    - **summary:** A bolt part.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartType.Markup`
    - **summary:** A 3D Markup part.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Display.MeshEdgeDisplay`
    - **summary:** Options for mesh edge display.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Display.MeshEdgeDisplay.None`
    - **summary:** No mesh edges are displayed.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Display.MeshEdgeDisplay.MeshJunctions`
    - **summary** Displays the junctions between meshes in this .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Display.Graphic`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Display.MeshEdgeDisplay.MeshJunctionsUnlessSmooth`
    - **summary** Displays the junctions between meshes in this ,
            except where mesh edges meet smoothly (matching normals).
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Display.Graphic`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Display.MeshEdgeDisplay.ExteriorBoundary`
    - **summary** Displays the exterior boundary after meshes in this  have been connected.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Display.Graphic`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Display.MeshEdgeDisplay.Polygons`
    - **summary:** Displays the outlines of all polygons.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignMeshLoop.Edges`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignMeshLoop.Edges`
    - **summary:** Gets the mesh edges in a loop.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnalysisOptions.SingleConnectedEdgeColor`
    - **summary** Gets or sets single connected edge color (default = ).
      - **see**
        - *@cref:* `P:System.Drawing.Color.DarkRed`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnalysisOptions.DoubleConnectedEdgeColor`
    - **summary** Gets or sets double connected edge color (default = ).
      - **see**
        - *@cref:* `P:System.Drawing.Color.Black`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnalysisOptions.TripleConnectedEdgeColor`
    - **summary** Gets or sets triple connected edge color (default = ).
      - **see**
        - *@cref:* `P:System.Drawing.Color.DeepPink`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnalysisOptions.MultipleConnectedEdgeColor`
    - **summary** Gets or sets multiple connected edge color (default = ).
      - **see**
        - *@cref:* `P:System.Drawing.Color.Yellow`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.StlImportType.ConnectedFaceted`
    - **summary:** Create a lightweight mesh with full connectivity information between facets.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.StlImportType.SimpleFaceted`
    - **summary:** Create a lightweight mesh with no connectivity information between facets.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.StlImportType.SolidOrSurfaceMergeFaces`
    - **summary:** Convert STL triangles into full geometry and seamlessly merge one or more faces.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.ProjectionExtent`
    - **summary:** Specifies the extent of a projection.
    - **remarks** This type is used with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.ProjectCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Modeler.ProjectionOptions)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.ProjectionExtent.ClosestFaces`
    - **summary:** Project to the closest faces.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.ProjectionExtent.AllFaces`
    - **summary:** Project to all faces.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.ProjectionOptions`
    - **summary** Specifies options used with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.ProjectCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Modeler.ProjectionOptions)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.ProjectCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Modeler.ProjectionOptions)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.ProjectionOptions.Default`
    - **summary:** A default set of projection options.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.ProjectionOptions.#ctor`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.Extent`
    - **summary:** Gets the extent of the projection.
    - **remarks** This option has no effect if  is set to .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.WrapCurves`
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.ProjectionOptions.#ctor`
    - **summary** Constructs a  with a default set of options.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.ProjectionOptions`
    - **remarks** The default options are:
      - **list**
        - *@type:* `bullet`
        - **item** = ProjectionExtent.ClosestFaces
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.Extent`
        - **item** = false
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.WrapCurves`
        - **item** = false
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.ExtendCurves`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.ProjectionOptions.#ctor(SpaceClaim.Api.V22.Modeler.ProjectionExtent,System.Boolean)`
    - **summary** Constructs a  object.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.ProjectionOptions`
    - **param:** The extent of the projection.
      - *@name:* `extent`
    - **param:** Whether curves are extended to the edges of faces.
      - *@name:* `extendCurves`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.ProjectionOptions.#ctor(System.Boolean)`
    - **summary** Constructs a  object.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.ProjectionOptions`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.ProjectionOptions.#ctor(SpaceClaim.Api.V22.Modeler.ProjectionExtent,System.Boolean,System.Boolean)`
    - **summary** Constructs a  object.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.ProjectionOptions`
    - **param:** The extent of the projection.
      - *@name:* `extent`
    - **param:** Whether curves are extended to the edges of faces.
      - *@name:* `extendCurves`
    - **param:** Whether curves are wrapped around the body.
      - *@name:* `wrapCurves`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.TessellationOptions`
    - **summary** Specifies options used with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions,System.Boolean,System.Boolean)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.TessellationOptions.Default`
    - **summary:** A default set of tessellation options.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.TessellationOptions.#ctor`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.SurfaceDeviation`
    - **summary:** Gets the maximum deviation from the true surface position.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.AngleDeviation`
    - **summary:** Gets the maximum deviation from the true surface normal.
    - **remarks:** The value is in radians.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.MaximumAspectRatio`
    - **summary:** Gets the maximum aspect ratio of facets, or zero if not specified.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.MaximumEdgeLength`
    - **summary:** Gets the maximum facet edge length, or zero if not specified.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.TessellationOptions.#ctor`
    - **summary** Constructs a  with a default set of options.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.TessellationOptions`
    - **remarks** The default options are:
      - **list**
        - *@type:* `bullet`
        - **item** = 0.00075 (0.75 mm)
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.SurfaceDeviation`
        - **item** = 20° (in radians)
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.AngleDeviation`
        - **item** = 0 (unspecified)
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.MaximumAspectRatio`
        - **item** = 0 (unspecified)
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.TessellationOptions.MaximumEdgeLength`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.TessellationOptions.#ctor(System.Double,System.Double)`
    - **summary** Constructs a  object.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.TessellationOptions`
    - **param:** The maximum deviation from the true surface position.
      - *@name:* `surfaceDeviation`
    - **param:** The maximum deviation from the true surface normal.
      - *@name:* `angleDeviation`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.TessellationOptions.#ctor(System.Double,System.Double,System.Double,System.Double)`
    - **summary** Constructs a  object.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.TessellationOptions`
    - **param:** The maximum deviation from the true surface position.
      - *@name:* `surfaceDeviation`
    - **param:** The maximum deviation from the true surface normal.
      - *@name:* `angleDeviation`
    - **param:** The maximum aspect ratio of facets, or zero if not specified.
      - *@name:* `maxAspectRatio`
    - **param:** The maximum facet edge length, or zero if not specified.
      - *@name:* `maxEdgeLength`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.BodyIntersection`
    - **summary:** A result from intersecting two bodies.
    - **remarks** This type is used by .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetIntersections(SpaceClaim.Api.V22.Modeler.Body)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.BodyIntersection.Segment`
    - **summary:** Gets the intersection between the two contributing topologies.
    - **remarks** If the intersection is a point, the curve of the segment will be a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PointCurve`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.BodyIntersection.ContributorA`
    - **summary:** Gets the contributor (face, edge, or vertex) from the subject body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.BodyIntersection.ContributorB`
    - **summary:** Gets the contributor (face, edge, or vertex) from the other body.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Mesh`
    - **summary:** A mesh.
    - **remarks** A  contains topology in terms of connected ,
            , and  objects.
            
            The mesh can be open or non-manifold.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Mesh`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.MeshFace`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.MeshEdge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.MeshVertex`
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Mesh.Faces`
    - **summary:** Gets the faces in the mesh.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Mesh.Edges`
    - **summary:** Gets the edges in the mesh.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Mesh.Vertices`
    - **summary:** Gets the vertices in the mesh.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Mesh.IsClosed`
    - **summary:** Gets whether the mesh is closed.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Mesh.IsManifold`
    - **summary:** Gets whether the mesh is manifold.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Mesh.Volume`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Mesh.SurfaceArea`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.MeshEdge`
    - **summary:** A mesh edge.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshEdge.Vertices`
    - **summary:** Gets the start and end vertices of the edge.
    - **remarks:** The returned list has two vertices: { start, end }.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshEdge.Faces`
    - **summary:** Gets the faces adjacent to this edge.
    - **remarks:** The mesh can be open or non-manifold, so each edge has one or more faces adjacent to it.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.MeshFace`
    - **summary:** A mesh face.
    - **remarks** Mesh faces are triangular, so they have three  and three .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Vertices`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Edges`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Normal`
    - **summary:** Gets the normal of the plane of the face.
    - **remarks** The  and  are ordered clockwise about the .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Vertices`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Edges`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Normal`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Vertices`
    - **summary:** Gets the three vertices of the face.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Normal`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Edges`
    - **summary:** Gets the three edges of the face.
    - **remarks** Edges[0] is opposite Vertices[0],
            Edges[1] is opposite Vertices[1], and
            Edges[2] is opposite Vertices[2].
            
            The  of each edge is arbitrary.
      - **inheritdoc**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.Normal`
      - **para**
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshEdge.Direction`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshFace.AdjacentFaces`
    - **summary:** Gets the adjacent faces.
    - **remarks:** Adjacent faces are faces that share an edge with this face.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.MeshTopology`
    - **summary:** A mesh face, mesh edge, or mesh vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshTopology.Mesh`
    - **summary:** Gets the mesh in which this topology lives.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshTopology.Index`
    - **summary:** Gets the index of this topology.
    - **remarks:** Each mesh face, mesh edge, or mesh vertex has a zero-based index, which is unique for that type within the mesh.
            That is, two mesh faces in the same mesh will have different indices,
            but a mesh edge or mesh vertex might both have the same index as a mesh face.
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.DesignMesh.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Collections.Generic.IList{SpaceClaim.Api.V22.Modeler.Facet})`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.MeshVertex`
    - **summary:** A mesh vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshVertex.Position`
    - **summary:** Gets the position of the vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshVertex.Edges`
    - **summary:** Gets the edges connected to this vertex.
    - **remarks:** The result is at least two edges.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshVertex.Faces`
    - **summary:** Gets the faces connected to this vertex.
    - **remarks:** The result is at least one face.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.BodyRendering`
    - **summary:** A hidden line rendering of a body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.BodyRendering.EdgeRenderings`
    - **summary:** Gets the edge renderings.
    - **remarks:** The values in the table describe edge segments.
            A segment is either visible, or hidden by a face.
            Segments that are hidden behind silhouettes or other edges are typically not returned at all,
            since there is no need for these to be displayed.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.BodyRendering.FaceRenderings`
    - **summary:** Gets the face renderings.
    - **remarks:** The values in the table describe silhouette segments.
            A segment is either visible, or hidden by a face.
            Segments that are hidden behind edges or other silhouettes are typically not returned at all,
            since there is no need for these to be displayed.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.EdgeRendering`
    - **summary:** A hidden line rendering of a segment of an edge.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.EdgeRendering.IsHidden`
    - **summary:** Gets whether the edge segment is hidden by a face.
    - **remarks** See  for more information.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.BodyRendering.EdgeRenderings`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Modeler.BodyRendering.EdgeRenderings`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.EdgeRendering.Interval`
    - **summary:** Gets the interval of the edge segment.
    - **remarks:** The interval is in terms of the curve of the original edge.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.FaceRendering`
    - **summary:** A hidden line rendering of a segment of a silhouette.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.FaceRendering.IsHidden`
    - **summary:** Gets whether the silhouette is hidden by a face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.FaceRendering.Segment`
    - **summary:** Gets the silhouette segment.
    - **remarks** The segment is in the transformed space of the .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.TransformedBody`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.FaceRendering.Polyline`
    - **summary:** Gets the silhouette polyline.
    - **remarks** The polyline is in the transformed space of the .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.TransformedBody`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.TransformedBody`
    - **summary:** A body and a transform.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.TransformedBody.Body`
    - **summary:** Gets the body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.TransformedBody.Transform`
    - **summary:** Gets the transform.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Body`
    - **summary:** A modeler body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.RoundEdges(System.Collections.Generic.ICollection{System.Collections.Generic.KeyValuePair{SpaceClaim.Api.V22.Modeler.Edge,SpaceClaim.Api.V22.Modeler.EdgeRound}})`
    - **summary:** Rounds a collection of edges.
    - **param:** Round specifications for each edge.
      - *@name:* `edgeRounds`
    - **returns:** Created round faces and their original edge.
    - **remarks** The return value is a dictionary mapping each newly created round face to the edge that was rounded to create it.
            More than one round face might be created from the same edge.
            The edge may be , e.g. for a vertex face.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Save(SpaceClaim.Api.V22.Modeler.BodySaveFormat,System.String)`
    - **summary:** Saves the body to a file in the format of the modeler.
    - **param:** Whether to use text or binary format.
      - *@name:* `format`
    - **param:** The full path of the file to create.
      - *@name:* `path`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.IsClosed`
    - **summary:** Gets whether the body is a closed body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.PieceCount`
    - **summary:** Gets the number of disjoint pieces of the body.
    - **remarks** A body can have one or more disjoint pieces.
            For example, using  can leave the body in two pieces.
            
             can be used to separate the pieces into separate bodies.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Subtract(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparatePieces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparatePieces`
    - **summary:** Separates disjoint pieces into separate bodies of one piece each.
    - **returns:** Separate bodies.
    - **remarks:** This method returns one or more separate bodies, including the original body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparateNonManifold`
    - **summary:** Separates a body into its non-manifold portions.
    - **returns:** Separate bodies.
    - **remarks** If the body is already manifold ( = true), then it is returned as-is with no changes. 
            
            If the body is non-manifold, then all disjoint pieces are returned as separate bodies. The original body is deleted.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Body.IsManifold`
      - **br**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CombinePieces(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`
    - **summary:** Combines bodies into a single disjoint body.
    - **param:** Other bodies to combine.
      - *@name:* `otherPieces`
    - **remarks** This method does the opposite of .
            
            No boolean or fusing operation is performed.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparatePieces`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Unite(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`
    - **summary:** Unites tools bodies with this target body.
    - **param:** The tool bodies to be united with this target body.
      - *@name:* `toolBodies`
    - **exception:** Some modeler bodies belong to design bodies and some do not.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** If any of the bodies involved belongs to a , then all the bodies must belong to design bodies,
            and the design bodies must all belong to the same .
             can be used to see if a body belongs to a design body.
            
            All tool bodies are consumed in the boolean operation, so  will be true for each tool body afterwards.
            The target body is deleted only if the result is empty.
            
            Bodies involved may be disjoint.
            If a body belongs to a design body, it can only be disjoint if it is a planar body.
            Planar bodies are flat bodies entirely in one plane, such as those created using .
            Therefore if the target body belongs to a design body and the result is disjoint, but not a planar body,
            the target body is separated and additional design bodies are created in the same part.
            
            The operation works on open or closed bodies.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignBody`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignBody(SpaceClaim.Api.V22.Modeler.Body)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Topology.IsDeleted`
      - **para**
      - **see:** CreatePlanarBody
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.CreatePlanarBody(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Unite(SpaceClaim.Api.V22.Modeler.Body[])`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Unite(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Subtract(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`
    - **summary:** Subtracts tools bodies from this target body.
    - **param:** The tool bodies to be subtracted from this target body.
      - *@name:* `toolBodies`
    - **exception:** Some modeler bodies belong to design bodies and some do not.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** If any of the bodies involved belongs to a , then all the bodies must belong to design bodies,
            and the design bodies must all belong to the same .
             can be used to see if a body belongs to a design body.
            
            All tool bodies are consumed in the boolean operation, so  will be true for each tool body afterwards.
            The target body is deleted only if the result is empty.
            
            Bodies involved may be disjoint.
            If a body belongs to a design body, it can only be disjoint if it is a planar body.
            Planar bodies are flat bodies entirely in one plane, such as those created using .
            Therefore if the target body belongs to a design body and the result is disjoint, but not a planar body,
            the target body is separated and additional design bodies are created in the same part.
            
            The operation works on open or closed bodies.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignBody`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignBody(SpaceClaim.Api.V22.Modeler.Body)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Topology.IsDeleted`
      - **para**
      - **see:** CreatePlanarBody
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.CreatePlanarBody(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Subtract(SpaceClaim.Api.V22.Modeler.Body[])`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Subtract(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Intersect(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`
    - **summary:** Intersects tools bodies with this target body.
    - **param:** The tool bodies to be intersected with this target body.
      - *@name:* `toolBodies`
    - **exception:** Some modeler bodies belong to design bodies and some do not.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** Design bodies do not belong to the same part.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** If any of the bodies involved belongs to a , then all the bodies must belong to design bodies,
            and the design bodies must all belong to the same .
             can be used to see if a body belongs to a design body.
            
            All tool bodies are consumed in the boolean operation, so  will be true for each tool body afterwards.
            The target body is deleted only if the result is empty.
            
            Bodies involved may be disjoint.
            If a body belongs to a design body, it can only be disjoint if it is a planar body.
            Planar bodies are flat bodies entirely in one plane, such as those created using .
            Therefore if the target body belongs to a design body and the result is disjoint, but not a planar body,
            the target body is separated and additional design bodies are created in the same part.
            
            The operation works on open or closed bodies.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignBody`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignBody(SpaceClaim.Api.V22.Modeler.Body)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Topology.IsDeleted`
      - **para**
      - **see:** CreatePlanarBody
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.CreatePlanarBody(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Intersect(SpaceClaim.Api.V22.Modeler.Body[])`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Intersect(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Fuse(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body},System.Boolean,SpaceClaim.Api.V22.Modeler.Tracker)`
    - **summary:** Fuses two or more bodies together into a single body.
    - **param:** Tool bodies to fuse onto this target body.
      - *@name:* `toolBodies`
    - **param:** Whether to skip bodies that fail to fuse.
      - *@name:* `skipProblemBodies`
    - **param** A tracker to receive information about splits and merges; or  if not required.
      - *@name:* `tracker`
      - **b:** null
    - **exception:** A modeler body belongs to a design body.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** Fuses tool bodies onto this target body.
            
            Faces and edges in the tool bodies are transferred to this target body, and the tool bodies are deleted.
            Bodies are imprinted and coincident topology is joined.
            Unlike a boolean operation, no trimming is performed.
            
            None of the bodies involved can belong to a design body.
             can be used to see if a body belongs to a design body.
            
            The resulting body may be non-manifold.
             can be used to see if a body is manifold or non-manifold.
            Non-manifold bodies can not be used to create design bodies.
            
            The  flag controls what happens if it was not possible to fuse one or more of the tool bodies.
            If  is  and the operation was unsuccessful, an  is thrown.
            If  is , any bodies that could not be fused are simply skipped.
            Any skipped bodies are unchanged and their  state will be .
            
            A  can be provided, which will receive information about splits and merges that took place.
      - **para**
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignBody(SpaceClaim.Api.V22.Modeler.Body)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Body.IsManifold`
      - **para**
      - **paramref**
        - *@name:* `skipProblemBodies`
      - **paramref**
        - *@name:* `skipProblemBodies`
      - **b:** false
      - **see**
        - *@cref:* `T:System.InvalidOperationException`
      - **paramref**
        - *@name:* `skipProblemBodies`
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Topology.IsDeleted`
      - **b:** false
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Tracker`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.IsManifold`
    - **summary:** Gets whether the body is manifold.
    - **remarks** Non-manifold bodies can be created when  is used.
            
            Non-manifold bodies can not be used to create design bodies.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Fuse(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body},System.Boolean,SpaceClaim.Api.V22.Modeler.Tracker)`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Imprint(SpaceClaim.Api.V22.Modeler.Body)`
    - **summary:** Imprints two bodies on each other.
    - **param:** The other body to imprint.
      - *@name:* `other`
    - **exception:** Some modeler bodies belong to design bodies and some do not.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** Design bodies do not belong to the same part.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** Finds the intersection between the two bodies and imprints the result onto both bodies.
            New edges are imprinted, and if closed loops of edges are produced, new faces are created.
            
            If either of the bodies involved belongs to a , then both bodies must belong to design bodies,
            and the design bodies must both belong to the same .
             can be used to see if a body belongs to a design body.
            
            The operation works on open or closed bodies.
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignBody`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignBody(SpaceClaim.Api.V22.Modeler.Body)`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetIntersections(SpaceClaim.Api.V22.Modeler.Body)`
    - **summary:** Gets the intersection between this body and another body.
    - **param:** The other body.
      - *@name:* `other`
    - **returns:** The intersections.
    - **remarks** Neither body is modified.
            
            A collection of  objects is returned.
            Each one provides the geometry of the intersection,
            the contributing topology from the subject (this body),
            and the contributing topology from the other body.
            Contributing topology can be a face, an edge, or a vertex.
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.BodyIntersection`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Copy`
    - **summary:** Creates a copy of the body.
    - **returns:** A new body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Copy(System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Modeler.Face,SpaceClaim.Api.V22.Modeler.Face}@,System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Modeler.Edge,SpaceClaim.Api.V22.Modeler.Edge}@)`
    - **summary:** Creates a copy of the body.
    - **param:** A dictionary of old-to-new face mappings.
      - *@name:* `oldFaceToNewFace`
    - **param:** A dictionary of old-to-new edge mappings.
      - *@name:* `oldEdgeToNewEdge`
    - **returns:** A new body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CopyFaces(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face})`
    - **summary:** Creates a copy of one or more faces of the body.
    - **param:** The faces to copy.
      - *@name:* `faces`
    - **returns:** A new body.
    - **exception:** Faces must belong to this body.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** If the faces are not connected, then the resulting body will be disjoint ( will be greater than 1).
            The disjoint pieces can be separated using .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Body.PieceCount`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparatePieces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CopyFaces(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Modeler.Face,SpaceClaim.Api.V22.Modeler.Face}@,System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Modeler.Edge,SpaceClaim.Api.V22.Modeler.Edge}@)`
    - **summary:** Creates a copy of one or more faces of the body.
    - **param:** The faces to copy.
      - *@name:* `faces`
    - **param:** A dictionary of old-to-new face mappings.
      - *@name:* `oldFaceToNewFace`
    - **param:** A dictionary of old-to-new edge mappings.
      - *@name:* `oldEdgeToNewEdge`
    - **returns:** A new body.
    - **exception:** Faces must belong to this body.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** If the faces are not connected, then the resulting body will be disjoint ( will be greater than 1).
            The disjoint pieces can be separated using .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Body.PieceCount`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparatePieces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions)`
    - **summary:** Gets a faceted representation of the faces of the body.
    - **param** The faces in this body whose tessellation is sought; else  for all faces.
      - *@name:* `faces`
      - **b:** null
    - **param:** Tessellation options.
      - *@name:* `options`
    - **returns:** Face tessellations for each face.
    - **exception:** Faces must belong to this body.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** Facets for adjacent faces are guaranteed to meet up with no gaps if faceted in the same call to .
            If adjacent faces are faceted in separate calls to , gaps may sometimes occur.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions,System.Boolean,System.Boolean)`
    - **summary:** Gets a faceted representation of the faces of the body.
    - **param** The faces in this body whose tessellation is sought; else  for all faces.
      - *@name:* `faces`
      - **b:** null
    - **param:** Tessellation options.
      - *@name:* `options`
    - **param:** Whether to perform the faceting in parallel, using multiple threads.
      - *@name:* `parallel`
    - **param:** Whether to show a popup progress window.
      - *@name:* `showProgress`
    - **returns:** Face tessellations for each face.
    - **exception:** Faces must belong to this body.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** Facets for adjacent faces are guaranteed to meet up with no gaps if faceted in the same call to .
            If adjacent faces are faceted in separate calls to , gaps may sometimes occur.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions,System.Boolean,System.Boolean)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions,System.Boolean,System.Boolean)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Reverse`
    - **summary:** Reverses the normals of all faces of the body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.Shells`
    - **summary:** Gets all the shells (connected face sets) of the body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.Faces`
    - **summary:** Gets all the faces of the body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.Edges`
    - **summary:** Gets all the edges of the body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.Vertices`
    - **summary:** Gets all the vertices of the body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CreateNurbsBody(SpaceClaim.Api.V22.Modeler.Body)`
    - **summary:** Creates a new body made up of NURBS surfaces, using face geometry and topology from an existing body.
    - **param:** The original body.
      - *@name:* `body`
    - **returns:** The created NURBS body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CreateNurbsBody(SpaceClaim.Api.V22.Modeler.Face)`
    - **summary:** Creates a new body made up of a NURBS surface, using face geometry and topology from an existing face.
    - **param:** The original face.
      - *@name:* `face`
    - **returns:** The created NURBS body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Import(SpaceClaim.Api.V22.Modeler.ForeignBody,System.Collections.Generic.IDictionary{System.String,SpaceClaim.Api.V22.Modeler.Face}@,System.Collections.Generic.IDictionary{System.String,SpaceClaim.Api.V22.Modeler.Edge}@)`
    - **summary:** Imports a custom foreign body.
    - **param:** The foreign body to import.
      - *@name:* `foreignBody`
    - **param:** A mapping from foreign face id to face.
      - *@name:* `idToFace`
    - **param:** A mapping from foreign edge id to edge.
      - *@name:* `idToEdge`
    - **returns:** The imported body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.OffsetFaces(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},System.Double)`
    - **summary:** Offsets faces.
    - **param** The faces to be offset; else  to offset all faces in the body.
      - *@name:* `faces`
      - **b:** null
    - **param:** The offset distance.
      - *@name:* `offset`
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks:** The offset is positive in the direction of the face normal,
            i.e. a positive value offsets outwards, and a negative value offsets inwards.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.OffsetFaces(System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Modeler.Face,System.Double})`
    - **summary:** Offsets faces.
    - **param:** The offset to be used for each face.
      - *@name:* `faceToOffset`
    - **remarks:** The offset is positive in the direction of the face normal,
            i.e. a positive value offsets outwards, and a negative value offsets inwards.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.Volume`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Body.SurfaceArea`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Dispose`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.EdgeRound`
    - **summary:** Specifies an edge round.
    - **remarks** This class is abstract.
            Derived classes  and  can be created.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.FixedRadiusRound`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.VariableRadiusRound`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.FixedRadiusRound`
    - **summary:** Specified a fixed radius edge round.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.FixedRadiusRound.#ctor(System.Double)`
    - **summary:** Creates a fixed radius round specification.
    - **param:** The round radius.
      - *@name:* `radius`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.FixedRadiusRound.Radius`
    - **summary:** Gets the round radius.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.VariableRadiusRound`
    - **summary:** Specifies a variable radius edge round.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Tracker`
    - **summary:** A tracker, which can be used to receive information about splits and merges during a modeling operation.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Tracker.Create`
    - **summary:** Creates a tracker.
    - **returns**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.BodySaveFormat`
    - **summary:** Specifies the format to use when saving a body to a file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.BodySaveFormat.Text`
    - **summary:** Text format.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.BodySaveFormat.Binary`
    - **summary:** Binary format.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Edge`
    - **summary:** A modeler edge.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.IsSmooth`
    - **summary:** Gets whether the edge is smooth.
    - **remarks:** The edge is smooth if the faces that meet at the edge are tangent continuous across the edge.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.IsConcave`
    - **summary:** Gets whether the edge is concave.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.Faces`
    - **summary:** Gets the faces that share this edge.
    - **remarks:** An edge will have one or two faces.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.Fins`
    - **summary:** Gets the fins that use this edge.
    - **remarks** Note that an edge could have the same face on both sides of it (e.g. an edge drawn part-way across a face),
            in which case  would return one face, whereas  would return two fins.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.Faces`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.Fins`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
    - **summary:** Gets the start vertex of the edge.
    - **remarks** An edge may be classified as being one of three types:
      - **ol**
        - **li** -  and  are distinct.
          - **i:** Open
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
        - **li** -  and  are the same.
          - **i:** Closed
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
        - **li** -  and  are both .
          - **i:** Ring
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
          - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
    - **summary:** Gets the end vertex of the edge.
    - **remarks** An edge may be classified as being one of three types:
      - **ol**
        - **li** -  and  are distinct.
          - **i:** Open
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
        - **li** -  and  are the same.
          - **i:** Closed
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
        - **li** -  and  are both .
          - **i:** Ring
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
          - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.Shell`
    - **summary:** Gets the shell to which this edge belongs.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.Precision`
    - **summary:** Gets the modeling precision of the edge.
    - **remarks:** If the edge is not a tolerant edge, zero is returned.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.Bounds`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.Length`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.IsReversed`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Face`
    - **summary:** A modeler face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.Edges`
    - **summary:** Gets the edges that form the boundary of the face.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.SurfaceAsTrimmedSpline`
    - **exclude**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.SurfaceAsTrimmedSpline2(System.Boolean@)`
    - **exclude**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.Loops`
    - **summary:** Gets the edge loops of the face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.AdjacentFaces`
    - **summary:** Gets the faces that border this face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.Shell`
    - **summary:** Gets the shell to which the faces belongs.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.GetAdjacentFace(SpaceClaim.Api.V22.Modeler.Edge)`
    - **summary:** Gets the face on the other side of the specified edge.
    - **param:** An edge within the boundary of this face.
      - *@name:* `edge`
    - **returns** The other face; otherwise  if there is no other face meeting the specified edge.
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.BoxUV`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.IsReversed`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Fin`
    - **summary:** A modeler fin.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Fin.IsReversed`
    - **summary:** Gets whether the fin direction is the opposite of the edge direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Fin.Edge`
    - **summary:** Gets the edge that this fin uses.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Fin.Loop`
    - **summary:** Gets the loop to which this fin belongs.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Fin.AsSplineUV`
    - **summary:** Gets a NURBS approximation for the curve in UV space.
    - **returns** The spline approximation; else  if not possible.
      - **b:** null
    - **remarks** The curve is returned in the UV space of the associated face, obtained using .
      - **see:** Fin.Loop.Face
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Loop.Face`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Loop`
    - **summary:** A connected part of the boundary of a face.
    - **remarks:** The apex of a cone has a degenerate loop consisting of zero fins, but one vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Loop.IsOuter`
    - **summary:** Gets whether the loop is an outer loop, rather than an inner loop.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Loop.Face`
    - **summary:** Gets the face to which this loop belongs.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Loop.Edges`
    - **summary:** Gets the edges that form the boundary of the loop.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Loop.Fins`
    - **summary:** Gets the fins that describe the boundary of the loop.
    - **remarks:** The fins are returned in order around the loop.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Loop.Vertices`
    - **summary:** Gets the vertices in the boundary of the loop.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Shell`
    - **summary:** A collection of connected faces and edges.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Shell.Faces`
    - **summary:** Gets all the faces of the shell.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Shell.Edges`
    - **summary:** Gets all the edges of the shell.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Shell.Vertices`
    - **summary:** Gets all the vertices of the shell.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Shell.Type`
    - **summary:** Gets the type of shell.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.ShellType.Outer`
    - **summary:** The shell is the outer boundary of a body.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.ShellType.Inner`
    - **summary:** The shell is the inner boundary of a body.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Modeler.ShellType.General`
    - **summary:** The shell is open or non-manifold.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.FaceTessellation`
    - **summary:** The faceted tessellation of a face.
    - **remarks** Facets are described as three indices in the  list.
            Facet vertices are ordered clockwise around the face normal (counterclockwise as you look down onto the face).
            
            Each entry in the  list specifies the position, normal, and texture parameter of the vertex.
            The texture parameter is the UV value of the underlying surface at that position.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.FaceTessellation.Vertices`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.FaceTessellation.Vertices`
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.FaceTessellation.Vertices`
    - **summary:** Gets the vertex list.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.FaceTessellation`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.FaceTessellation.Facets`
    - **summary:** Gets the facets.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.FaceTessellation`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Facet`
    - **summary:** A triangular facet.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Topology`
    - **summary:** The base class for modeler topology types.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Topology.IsDeleted`
    - **summary:** Gets whether the topology has been deleted.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Topology.Body`
    - **summary:** Gets the body to which this topology belongs.
    - **remarks** is also derived from , and if you ask a body for its , it returns itself.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Body`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Topology`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Topology.Body`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.Vertex`
    - **summary:** A modeler vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Vertex.Position`
    - **summary:** Gets the position of the vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Vertex.Faces`
    - **summary:** Gets all the faces around the vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Vertex.Edges`
    - **summary:** Gets all the edges that meet at the vertex.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Vertex.Shell`
    - **summary:** Gets the shell to which this vertex belongs.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Vertex.Precision`
    - **summary:** Gets the modeling precision of the vertex.
    - **remarks:** If the vertex is not a tolerant vertex, zero is returned.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.CutoutFacePattern`
    - **summary:** A sheet metal cutout pattern.
    - **remarks** This is an abstract base class for  and .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.LightweightFacePattern`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.HeavyweightFacePattern`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CutoutFacePattern.TemplateFaces`
    - **summary:** Gets the faces on which the pattern is based.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CutoutFacePattern.GetPattern(SpaceClaim.Api.V22.DesignFace)`
    - **summary:** Gets the pattern to which the face belongs, if any.
    - **remarks** If the face is not part of a pattern,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CutoutFacePattern.Delete`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CutoutFacePattern.IsDeleted`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.HeavyweightFacePattern`
    - **summary:** A heavyweight pattern.
    - **remarks** A pattern is based on a set of faces which form a cutout. 
            A  pattern displays the pattern without creating geometry for the other members,
            whereas a  pattern creates geometry for all members.
      - **i:** lightweight
      - **i:** heavyweight

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.HeavyweightFacePattern.Members`
    - **summary:** Gets the members of the pattern.
    - **remarks** The faces of  is first in the returned list.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.CutoutFacePattern.TemplateFaces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.HeavyweightFacePattern.ConvertToLightweight`
    - **summary:** Converts the heavyweight pattern into a lightweight pattern.
    - **returns:** An equivalent lightweight pattern.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `T:SpaceClaim.Api.V22.HeavyweightFacePattern`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.HeavyweightFacePattern.Delete`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.HeavyweightFacePattern.IsDeleted`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.LightweightFacePattern`
    - **summary:** A lightweight sheet metal cutout pattern.
    - **remarks** A pattern is based on a set of faces which form a cutout. 
            A  pattern displays the pattern without creating geometry for the other members,
            whereas a  pattern creates geometry for all members.
      - **i:** lightweight
      - **i:** heavyweight

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightFacePattern.GetPlacements(SpaceClaim.Api.V22.DesignFace)`
    - **summary:** Gets the placements for the pattern members.
    - **remarks** The placement for the  cutout is first in the returned list.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.CutoutFacePattern.TemplateFaces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightFacePattern.ConvertToHeavyweight`
    - **summary:** Converts the lightweight pattern into a heavyweight pattern.
    - **returns:** An equivalent heavyweight pattern.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `T:SpaceClaim.Api.V22.LightweightFacePattern`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightFacePattern.Delete`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.LightweightFacePattern.IsDeleted`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalBendHandler.UpdateBendOptions(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.IDocObject)`
    - **summary:** Overrides sheet metal bend tool options panel values.
    - **param:** The planar sheet metal face of the bend.
      - *@name:* `desFace`
    - **param:** Reference of the bend.
      - *@name:* `reference`
    - **returns** An instance of  with desired values to override bend tool option.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.BendOptions`
    - **remarks** The  is a planar sheet metal face that the reference  or 
             is on.
            The  is a  or  which the 
            sheet metal bend references.
            
            Return an instance of  with the desired values in the override method. When a 
             or  is clicked to create a sheet metal bend in the bend tool, 
            values from returned  will be used to populate the options panel.
            If bend table is set in the sheet metal part, bend radius value be overridden only if it is available in the 
            value list.
      - **paramref**
        - *@name:* `desFace`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignEdge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignCurve`
      - **paramref**
        - *@name:* `reference`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignEdge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignCurve`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.BendOptions`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignEdge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignCurve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.BendOptions`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.LaserEdgeRelief`
    - **summary:** A laser stamp aligned to the edge of the flange.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.LaserEdgeRelief.Default`
    - **summary:** The default relief, where the size will be determined automatically.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.LightweightNote.AnchorFace`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ILightweightNote.AnchorFace`
    - **summary:** Gets the anchor face of the note.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumLine.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary:** Creates a datum line from determinants.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name for the datum line.
      - *@name:* `name`
    - **param:** The objects used to determine the line.
      - *@name:* `determinants`
    - **returns:** A datum line.
    - **exception:** Cannot derive a line from the determinants.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** If the  are unsuitable, an exception is thrown.
             can be used to test the suitability of determinants before creating the datum line.
      - **paramref**
        - *@name:* `determinants`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DatumLine.GetLine(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.Create(SpaceClaim.Api.V22.Part,System.String,System.Single[],System.Int32[])`
    - **summary:** Creates a design mesh from an array of vertex (X,Y,Z) values and facet indices.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name of the design mesh.
      - *@name:* `name`
    - **param:** A list of vertices.
      - *@name:* `vertices`
    - **param:** A list of facets.
      - *@name:* `facets`
    - **returns:** A design mesh.
    - **exception:** Array length should be divisible by 3.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** Each vertex is described by three floats in the  array,
            and each facet is described by three vertex indices,
            therefore the length of each array should be divisible by 3.
            Each vertex index is a zero-based count of the vertex number,
            i.e. the vertex starts at index  in the  array.
            
            The  of the design mesh is a  object.
            Each vertex in the  array becomes a  in the ,
            and each facet in the  array becomes a  in the .
            
            The  of the  is its vertex index in the  array,
            and the  of the  is its facet index in the  array.
      - **paramref**
        - *@name:* `vertices`
      - **c:** (3 * vertex index)
      - **paramref**
        - *@name:* `vertices`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DesignMesh.Shape`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Mesh`
      - **paramref**
        - *@name:* `vertices`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.MeshVertex`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Mesh`
      - **paramref**
        - *@name:* `facets`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.MeshFace`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Mesh`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshTopology.Index`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.MeshVertex`
      - **paramref**
        - *@name:* `vertices`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.MeshTopology.Index`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.MeshFace`
      - **paramref**
        - *@name:* `facets`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.GetFaceColor(SpaceClaim.Api.V22.Modeler.MeshFace)`
    - **summary:** Gets the color of a mesh face.
    - **param:** A mesh face.
      - *@name:* `meshFace`
    - **returns** The color of the mesh face, or  if the design mesh color is used.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.SetFaceColor(SpaceClaim.Api.V22.Modeler.MeshFace,System.Nullable{System.Drawing.Color})`
    - **summary:** Sets the color of a mesh face.
    - **param:** A mesh face.
      - *@name:* `meshFace`
    - **param** The color to use, or  to use the color of the design mesh.
      - *@name:* `color`
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.SetFaceColor(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.MeshFace},System.Nullable{System.Drawing.Color})`
    - **summary:** Sets the color of a collection of mesh faces.
    - **param:** The mesh faces to color.
      - *@name:* `meshFaces`
    - **param** The color to use, or  to use the color of the design mesh.
      - *@name:* `color`
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignMesh.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.GetDesignMeshTopology(SpaceClaim.Api.V22.Modeler.MeshTopology)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IDesignMesh.GetDesignMeshTopology(SpaceClaim.Api.V22.Modeler.MeshTopology)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.GetDesignMeshRegion(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.MeshFace})`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IDesignMesh.GetDesignMeshRegion(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.MeshFace})`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignMesh.Shape`
    - **summary:** Gets the shape of the design mesh.
    - **remarks:** Returns null for a simple (non-connected) mesh.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IDesignMesh.GetDesignMeshTopology(SpaceClaim.Api.V22.Modeler.MeshTopology)`
    - **summary:** Gets the design mesh item for a mesh face, mesh edge, or mesh vertex.
    - **param:** A mesh face, mesh edge, or mesh vertex.
      - *@name:* `meshTopology`
    - **returns:** A design mesh item.
    - **remarks** The returned value is a doc object that can be set as the ,
            or as part of the .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.SingleSelection`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.Selection`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IDesignMesh.GetDesignMeshRegion(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.MeshFace})`
    - **summary:** Gets the design mesh item for a region of mesh faces.
    - **param:** The mesh faces of the region.
      - *@name:* `meshRegion`
    - **returns:** A design mesh item.
    - **remarks** The returned value is a doc object that can be set as the ,
            or as part of the .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.SingleSelection`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.Selection`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignMeshRegion.Faces`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignMeshRegion.Faces`
    - **summary:** Gets the mesh faces in the region.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AxialBend.SetAngle(System.Double,SpaceClaim.Api.V22.IDesignFace)`
    - **inheritdoc**
    - **exception** The value given for  is not valid.
      - *@cref:* `T:System.ArgumentException`
      - **paramref**
        - *@name:* `angle`
    - **exception** The specified  is not valid.
      - *@cref:* `T:System.ArgumentException`
      - **paramref**
        - *@name:* `referenceFace`
    - **exception** The bend  cannot be modified.
      - *@cref:* `T:System.InvalidOperationException`
      - **paramref**
        - *@name:* `angle`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.PartExportFormat`
    - **summary** Specifies an export format for use with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Part.Export(SpaceClaim.Api.V22.PartExportFormat,System.String,System.Boolean,SpaceClaim.Api.V22.ExportOptions)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.CatiaV5Part`
    - **summary:** A Catia V5 (".CATPart") part file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.CatiaV5Assembly`
    - **summary:** A Catia V5 (".CATProduct") assembly file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.CatiaV5Graphics`
    - **summary:** A Catia V5 (".cgr") graphics file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.Iges`
    - **summary:** An IGES (".igs") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.Step`
    - **summary:** A STEP (".stp") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.Vda`
    - **summary:** A VDA (".vda") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.JtOpen`
    - **summary:** A JT Open (".jt") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.ParasolidText`
    - **summary:** A Parasolid text (".x_t") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.ParasolidBinary`
    - **summary:** A Parasolid binary (".x_b") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.AcisText`
    - **summary:** An ACIS text (".sat") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.AcisBinary`
    - **summary:** An ACIS binary (".sab") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.Rhino`
    - **summary:** A Rhino (".3dm") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.PdfFacets`
    - **summary** A 3D PDF (".pdf") file, written in  format (containing facets).
      - **b:** Universal 3D

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.SketchUp`
    - **summary:** A SketchUp (".skp") file.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.SheetMetalFeature.Faces`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.ISheetMetalFeature.Faces`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ISheetMetalFeature.Faces`
    - **summary:** Gets the faces of the sheet metal feature.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Faces`
    - **summary:** Select faces.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Edges`
    - **summary:** Select edges.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.FacetedBodies`
    - **summary:** Select faceted bodies (meshes).

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.LightweightComponents`
    - **summary:** Select lightweight custom objects.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.AnchorCondition.Component`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IAnchorCondition.Component`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CustomFormOptions.RemoveTopFace`
    - **summary:** Gets or sets whether to remove the top face of the form.
    - **remarks** The default is  if no value is specified.
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FlatPatternAspect.FoldedPart`
    - **summary:** Gets the sheet metal part for which this part is a flat pattern.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FlatPatternAspect.AnchorFace`
    - **summary:** Gets the anchor face of the unfolding operation.
    - **remarks** The anchor face is a design face within this flat pattern part.
             can be used to get the corresponding face in the folded sheet metal part.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetFoldedFace(SpaceClaim.Api.V22.DesignFace)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetFoldedFace(SpaceClaim.Api.V22.DesignFace)`
    - **summary:** Gets the folded counterpart of a flat pattern face.
    - **param:** The face within the flat pattern part.
      - *@name:* `unfoldedFace`
    - **returns:** The corresponding face in the folded sheet metal part.
    - **remarks** If the face does not have a folded counterpart,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetUnfoldedFaces(SpaceClaim.Api.V22.DesignFace)`
    - **summary:** Gets the unfolded counterparts of a sheet metal face.
    - **param:** The face within the folded sheet metal part.
      - *@name:* `foldedFace`
    - **returns:** The corresponding faces in the flat pattern part.
    - **remarks** Faces of a sheet metal form may not have counterparts in the flat pattern part.
            This is determined by the  table and the  value.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FlatPatternAspect.FormStates`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FlatPatternAspect.DefaultFormState`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetFoldedEdge(SpaceClaim.Api.V22.DesignEdge)`
    - **summary:** Gets the folded counterpart of a flat pattern edge.
    - **param:** The edge within the flat pattern part.
      - *@name:* `unfoldedEdge`
    - **returns:** The corresponding edge in the folded sheet metal part.
    - **remarks** If the edge does not have a folded counterpart,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetUnfoldedEdges(SpaceClaim.Api.V22.DesignEdge)`
    - **summary:** Gets the unfolded counterparts of a sheet metal edge.
    - **param:** The edge within the folded sheet metal part.
      - *@name:* `foldedEdge`
    - **returns:** The corresponding edges in the flat pattern part.
    - **remarks** Edges of a sheet metal form may not have counterparts in the flat pattern part.
            This is determined by the  table and the  value.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FlatPatternAspect.FormStates`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FlatPatternAspect.DefaultFormState`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetBendFace(SpaceClaim.Api.V22.Note)`
    - **summary:** Gets the bend face which is annotated by a note.
    - **param:** The note.
      - *@name:* `note`
    - **returns** The bend face; else  if  does not annotate a bend face.
      - **b:** null
      - **paramref**
        - *@name:* `note`
    - **remarks** The bend face is a design face within this flat pattern part.
             can be used to get the corresponding face in the folded sheet metal part.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetFoldedFace(SpaceClaim.Api.V22.DesignFace)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FlatPatternAspect.BendFaces`
    - **summary:** Gets the bend faces of this flat pattern part.
    - **remarks** The bend faces are design faces within this flat pattern part.
             can be used to get the corresponding faces in the folded sheet metal part.
            
            Only bend faces on the "front" of the flat pattern are returned.
            Bend faces on the "back" are omitted.
            The "front" is the side identified by the .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetFoldedFace(SpaceClaim.Api.V22.DesignFace)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FlatPatternAspect.AnchorFace`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetBendLine(SpaceClaim.Api.V22.DesignFace)`
    - **summary:** Gets the bend line of a bend face.
    - **param:** The bend face in this flat pattern part.
      - *@name:* `bendFace`
    - **returns** The bend line, or  if the face is not a bend face.
      - **b:** null
    - **remarks:** The bend line is a straight line lying in the plane of the bend face.
            Its start and end points lie on the boundary of the face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FlatPatternAspect.PartialBends`
    - **summary:** Gets or sets a table of bends that are to be shown in a partially bent state.
    - **remarks** By default, the flat pattern unfolds all bends to a completely flat state.
            A table can be supplied in order to show bends in a partially bent or completely bent state.
            
            The table is a dictionary supplying the bend state for each bend.
            The bend state is the proportion of completely bent, where 0 means completely flat, and 1 means completely bent.
            Bends not included in the table are assumed to be completely flat (state = 0).
      - **para**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.PartAspect`
    - **summary:** An aspect of a part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.RigidCondition.ComponentA`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IRigidCondition.ComponentA`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.RigidCondition.ComponentB`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IRigidCondition.ComponentB`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ISheetMetalAspect.GetFeature(SpaceClaim.Api.V22.IDesignFace)`
    - **summary:** Gets the sheet metal feature to which a face belongs.
    - **param:** The face.
      - *@name:* `desFace`
    - **returns:** The sheet metal feature.
    - **remarks** If the  is one of the  of a ,
            this method returns that ; otherwise  is returned.
      - **paramref**
        - *@name:* `desFace`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.ISheetMetalFeature.Faces`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.ISheetMetalFeature`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.ISheetMetalFeature`
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ISheetMetalAspect.GetOppositeFace(SpaceClaim.Api.V22.IDesignFace)`
    - **summary:** Gets the opposite face of a face.
    - **param:** A face.
      - *@name:* `desFace`
    - **returns** The opposite face; else  if there is no opposite face.
      - **b:** null
    - **remarks:** The opposite face is the face separated by the sheet metal thickness.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ISheetMetalAspect.TryApplyNote(SpaceClaim.Api.V22.INote,SpaceClaim.Api.V22.Lettering,SpaceClaim.Api.V22.IDesignFace@)`
    - **summary:** Applies a note as sheet metal lettering, if possible.
    - **param:** A note.
      - *@name:* `note`
    - **param:** The type of lettering to create.
      - *@name:* `type`
    - **param:** The face on which the lettering was applied.
      - *@name:* `substrate`
    - **returns** if successful; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** If the note lies in a planar sheet metal face, the lettering is applied,
            and the  face is returned.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.GetFeature(SpaceClaim.Api.V22.DesignFace)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ISheetMetalAspect.GetFeature(SpaceClaim.Api.V22.IDesignFace)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.GetOppositeFace(SpaceClaim.Api.V22.DesignFace)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ISheetMetalAspect.GetOppositeFace(SpaceClaim.Api.V22.IDesignFace)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.TryApplyNote(SpaceClaim.Api.V22.Note,SpaceClaim.Api.V22.Lettering,SpaceClaim.Api.V22.DesignFace@)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ISheetMetalAspect.TryApplyNote(SpaceClaim.Api.V22.INote,SpaceClaim.Api.V22.Lettering,SpaceClaim.Api.V22.IDesignFace@)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.Unfold(SpaceClaim.Api.V22.DesignFace)`
    - **summary:** Unfolds the sheet metal part.
    - **param:** The anchor face to unfold about.
      - *@name:* `anchorFace`
    - **returns:** The corresponding anchor face in the flat pattern part.
    - **remarks:** A unfolded flat pattern part is created for this sheet metal part,
            or if an unfolded part already exists, it is updated.
    - **exception:** It was not possible to unfold the part.
      - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreateMissingBends(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignEdge},System.Double)`
    - **summary:** Creates bends in place of crease edges.
    - **param:** Edges in a sheet metal body where bends need to be applied.
      - *@name:* `creaseEdges`
    - **param:** The inner radius of the bend.
      - *@name:* `innerRadius`
    - **returns:** Any bends created.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreateRips(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignEdge})`
    - **summary:** Creates rips in place of crease edges.
    - **param:** Edges in a sheet metal body to be ripped.
      - *@name:* `creaseEdges`
    - **returns:** Created rip faces.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.RepairBends(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignFace})`
    - **summary:** Creates bends in a sheet metal body after repairing the model.
    - **param:** Bend faces to be repaired in a sheet metal body.
      - *@name:* `bendFaces`
    - **returns:** Any bends created.
    - **remarks** The method looks for situations where the shape of a bend is incomplete,
            but the model can be repaired to create a bend.
            An example is where there is a cylindrical face on the outside, but a crease edge on the inside.
            
             may contain all faces of the body. Any faces which cannot be repaired will be ignored.
      - **para**
      - **paramref**
        - *@name:* `bendFaces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.GetCreaseEdges(SpaceClaim.Api.V22.DesignBody)`
    - **summary:** Gets the edges in a sheet metal body where bends need to be applied.
    - **param:** The sheet metal body.
      - *@name:* `desBody`
    - **returns:** The sharp edges in the sheet metal body.
    - **remarks:** A crease edge cannot be unfolded, because there is no bend present.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreateHem(SpaceClaim.Api.V22.DesignEdge,SpaceClaim.Api.V22.HemStyle)`
    - **summary:** Creates a hem bend along a straight edge.
    - **param:** The straight edge for the hem.
      - *@name:* `edge`
    - **param:** The style of the hem.
      - *@name:* `style`
    - **returns:** A hem bend.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IHasBendAngle.SetAngle(System.Double,SpaceClaim.Api.V22.IDesignFace)`
    - **summary:** Sets the angle of the bend.
    - **param:** The bend angle.
      - *@name:* `angle`
    - **param:** An optional stationary reference face.
      - *@name:* `referenceFace`
    - **exception** The value given for  is not valid.
      - *@cref:* `T:System.ArgumentException`
      - **paramref**
        - *@name:* `angle`
    - **exception** The specified  is not valid.
      - *@cref:* `T:System.ArgumentException`
      - **paramref**
        - *@name:* `referenceFace`
    - **exception** The bend  cannot be modified.
      - *@cref:* `T:System.InvalidOperationException`
      - **paramref**
        - *@name:* `angle`
    - **remarks** If  is null, then the stationary face will be determined automatically.
      - **em:** referenceFace
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.IHasBendAngle.Angle`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.SpotWeldJoint.DesignFaces`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ISpotWeldJoint.DesignFaces`
    - **summary:** Gets the design faces involved in this joint.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.InteractionContext.ActivePart`
    - **summary:** Gets or sets the active part, in context-space.
    - **remarks** If there is no active part,  is returned.
            This can occur in a drawing sheet that has no drawing views.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.InteractionContext.GetSection(SpaceClaim.Api.V22.IDesignBody)`
    - **summary:** Gets the section for a design body.
    - **param:** The design body.
      - *@name:* `desBody`
    - **returns** The design body section; else  if bodies are not sectioned in this context.
      - **b:** null
    - **exception:** The object does not belong to this interaction context.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.StlFileGranularity.FilePerPart`
    - **summary:** A separate STL file is created for each part (or part occurrence) that contains any bodies.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Beam.ShapeSource`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Beam.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IBeam.ShapeSource`
    - **summary** Gets the objects that determine the  of the beam.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve.Shape`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignBodyAspect`
    - **summary:** An aspect of a design body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.MidSurfaceAspect.TryGetFaceThickness(SpaceClaim.Api.V22.DesignFace,System.Double@)`
    - **summary:** Gets the thickness assigned to a design face, if available.
    - **param:** The design face whose thickness is wanted.
      - *@name:* `desFace`
    - **param:** The thickness assigned to the face.
      - *@name:* `thickness`
    - **returns** if a thickness is assigned to the face; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.MidSurfaceAspect.Create(SpaceClaim.Api.V22.DesignBody,System.Double)`
    - **summary:** Creates a MidSurfaceAspect of the specified thickness on a DesignBody.
    - **param** The  on which to create a MidSurfaceAspect.
      - *@name:* `desBody`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignBody`
    - **param:** The desired thickness
      - *@name:* `thickness`
    - **returns:** The MidSurfaceAspect.
    - **exception:** The desBody argument is null.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The thickness is not greater than zero.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The DesignBody is not open.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The DesignBody already has a MidSurfaceAspect.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AppearanceState.Create(SpaceClaim.Api.V22.Part,System.String)`
    - **summary:** Creates an appearance object.
    - **param:** The parent part, to which this appearance state applies.
      - *@name:* `parent`
    - **param:** The name of the appearance state.
      - *@name:* `name`
    - **returns:** A new appearance state.
    - **remarks** The name must be unique across all existing appearance states in the  part,
            and across all standard view projections.
            
            The appearance state is created, but  must then be called
            if object visibility is to be stored, and  must be set if the view
            projection is to be stored.
      - **paramref**
        - *@name:* `parent`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.AppearanceState.CaptureVisibility`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.AppearanceState.Projection`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Marker.Face`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IMarker.Face`
    - **summary:** Gets the face in which the marker lives.
    - **remarks:** The face is a planar sheet metal face, and not a side face.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DrawingViewStyle.HiddenEdgesDashed`
    - **summary:** The view is shown with hidden edges dashed or faint.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DrawingViewStyle.HiddenEdgesRemoved`
    - **summary:** The view is shown with hidden edges removed.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateIndicator(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignFace})`
    - **summary:** Creates an indicator for a collection of faces.
    - **param:** The faces.
      - *@name:* `desFaces`
    - **returns:** An indicator.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateIndicator(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignEdge})`
    - **summary:** Creates an indicator for a collection of edges.
    - **param:** The edges.
      - *@name:* `desEdges`
    - **returns:** An indicator.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Component`
    - **summary:** A component master.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Component.Create(SpaceClaim.Api.V22.Part,SpaceClaim.Api.V22.Part)`
    - **summary:** Creates an assembly component.
    - **param:** The parent part master.
      - *@name:* `parent`
    - **param:** The part master to instantiate.
      - *@name:* `template`
    - **returns:** The created component master.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Component.CreateFromFile(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.ImportOptions)`
    - **summary:** Creates an assembly component from an external file.
    - **param:** The parent part master.
      - *@name:* `parent`
    - **param:** The path of the component part file.
      - *@name:* `path`
    - **param** Import options to use, or  to use the current user options.
      - *@name:* `options`
      - **b:** null
    - **returns**
    - **exception:** This copy of SpaceClaim is not licensed for the specified operation.
      - *@cref:* `T:System.InvalidOperationException`
    - **exception:** Unrecognized file format.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** The component will be placed in its default orientation, unless there is a selected object. In that case, the component will be oriented to that. 
            
            This method can also be used to import a component of another CAD format.
      - **para**
      - **para** The SpaceClaim option to save the imported component to a file is ignored.
        - **br**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Component.ReplaceFromFile(System.String)`
    - **summary** Replaces the  of the component with the part loaded from the specified path.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Component.Template`
    - **param:** The path of the new part to use.
      - *@name:* `path`
    - **remarks:** If the new part is already loaded, the in-memory document will be used.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Component.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IComponent.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Component.Content`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IComponent.Content`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Component.Components`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Component.Template`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.Instance.Template`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Component.Placement`
    - **summary:** Gets or sets the placement matrix for the component.
    - **remarks** The  object is transformed by the placement matrix, 
            giving rise to occurrences of the template and its children, recursively.
            
            The matrix can contain rotation and translation, but not scale.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Component.Template`
      - **para**
    - **exception:** The matrix has a scale component.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Component.Name`
    - **summary:** Gets or sets the name of this component.
    - **remarks**
      - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.IComponent`
    - **summary:** Represents an assembly component.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IComponent.Parent`
    - **summary:** Gets the part that contains the component.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IComponent.Content`
    - **summary:** Gets the part occurrence contained by the component.
    - **remarks**
      - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IComponent.Components`
    - **summary:** Gets components contained by this component.
    - **remarks**
      - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IComponent.Name`
    - **summary:** Gets the name of this component.
    - **remarks** The name is optional and may be presented in the user interface as a suffix to the part name. 
            To set the part name, use
      - **see:** Component.Template.Name
        - *@cref:* `P:SpaceClaim.Api.V22.Part.Name`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPlane.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary:** Creates a datum plane from determinants.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name for the datum plane.
      - *@name:* `name`
    - **param:** The objects used to determine the plane.
      - *@name:* `determinants`
    - **returns:** A datum plane.
    - **exception:** Cannot derive a plane from the determinants.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** If the  are unsuitable, an exception is thrown.
             can be used to test the suitability of determinants before creating the datum plane.
      - **paramref**
        - *@name:* `determinants`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DatumPlane.GetPlane(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignBody`
    - **summary:** A design body master.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Modeler.Body)`
    - **summary:** Creates a design body master with the specified modeler body as its shape.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name of the design body.
      - *@name:* `name`
    - **param:** The shape of the design body.
      - *@name:* `modelerBody`
    - **returns:** The newly created design body.
    - **exception:** The modeler body is already used by a design body.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The modeler body is disjoint.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The modeler body is non-manifold.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The modeler body is not an open or closed solid.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** Only planar bodies are allowed to be disjoint.
            Planar bodies are flat bodies entirely in one plane, such as those created using .
            In all other cases, if the modeler body is disjoint (it has separate pieces),
            it must be separated first using .
      - **see:** CreatePlanarBody
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.CreatePlanarBody(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparatePieces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face})`
    - **summary:** Gets a faceted representation of the faces of the design body.
    - **param** The faces in this design body whose tessellation is sought; else  for all faces.
      - *@name:* `faces`
      - **b:** null
    - **returns:** Face tessellations for each face.
    - **remarks** Unlike the  method on ,
            which calculates a tessellation to a desired accuracy,
            this method returns the tessellation already being used to display the design body, if it exists.
            If the design body has only just been created using the API, it will not have been displayed yet,
            so this method will return .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Modeler.TessellationOptions)`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Body`
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetEdgeTessellation(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Edge})`
    - **summary:** Gets the tessellated version of the edges of the design body.
    - **param** The edges in this design body whose tessellation is sought; else  for all edges.
      - *@name:* `edges`
      - **b:** null
    - **returns:** Edge tessellations for each edge.
    - **remarks** This method returns the tessellation already being used to display the design body, if it exists. If the design body has only just been created
            using the API, it will not have been displayed yet, so this method will return .
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.IsLocked`
    - **summary:** Gets or sets whether the design body is locked.
    - **remarks** If the design body is locked, any attempt to modify it will throw a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.LockedException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.Save(SpaceClaim.Api.V22.Modeler.BodySaveFormat,System.String)`
    - **summary:** Saves the body to a file in the format of the modeler.
    - **param:** Whether to use text or binary format.
      - *@name:* `format`
    - **param:** The full path of the file to create.
      - *@name:* `path`
    - **remarks** This method is similar to the  method on the  type,
            except that  attributes are attached to faces and edges in the file to indicate
            which  or  they came from.
            
            See  for more information.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Save(SpaceClaim.Api.V22.Modeler.BodySaveFormat,System.String)`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Body`
      - **i:** name
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignFace`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignEdge`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.IHasExportIdentifier.ExportIdentifier`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.Save(SpaceClaim.Api.V22.Modeler.BodySaveFormat,System.String,System.Int32,System.Int32,System.Int32)`
    - **summary:** Saves the body to a file in the format of the modeler.
    - **param:** Whether to use text or binary format.
      - *@name:* `format`
    - **param:** The full path of the file to create.
      - *@name:* `path`
    - **param:** Modeler major version
      - *@name:* `majorVersion`
    - **param:** Modeler minor version
      - *@name:* `minorVersion`
    - **param:** Modeler point version
      - *@name:* `pointVersion`
    - **remarks** This method is similar to the  method on the  type,
            except that  attributes are attached to faces and edges in the file to indicate
            which  or  they came from.
            
            See  for more information.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Save(SpaceClaim.Api.V22.Modeler.BodySaveFormat,System.String)`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Body`
      - **i:** name
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignFace`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignEdge`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.IHasExportIdentifier.ExportIdentifier`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.MidSurface`
    - **summary:** Gets the mid-surface aspect of the design body.
    - **remarks** If this design body is not a mid-surface body,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.VolumeExtraction`
    - **summary:** Gets the volume extraction aspect of the design body.
    - **remarks** If this design body is not a volume extraction body,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Enclosure`
    - **summary:** Gets the enclosure aspect of the design body.
    - **remarks** If this design body is not enclosure body,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.IdentifyHoles(SpaceClaim.Api.V22.IdentifyHoleOptions)`
    - **summary:** Identifies holes on the DesignBody using the specified options.
    - **param** Options for limiting the types of holes to be found. See .
      - *@name:* `options`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IdentifyHoleOptions`
    - **returns**
    - **exception:** All the holes were not able to be identified.
      - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignBody.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Faces`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignBody.Faces`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Edges`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignBody.Edges`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignFace(SpaceClaim.Api.V22.Modeler.Face)`
    - **summary** Gets the  that has the given  as its .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignFace`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Face`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DesignFace.Shape`
    - **param:** The face whose design face master is sought.
      - *@name:* `modelerFace`
    - **returns:** The design face master whose shape is the given face.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignEdge(SpaceClaim.Api.V22.Modeler.Edge)`
    - **summary** Gets the  that has the given  as its .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignEdge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Edge`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DesignEdge.Shape`
    - **param:** The edge whose design edge master is sought.
      - *@name:* `modelerEdge`
    - **returns:** The design edge master whose shape is the given edge.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignBody(SpaceClaim.Api.V22.Modeler.Body)`
    - **summary** Gets the  that has the given  as its .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DesignBody`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Body`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DesignBody.Shape`
    - **param:** The body whose design body master is sought.
      - *@name:* `modelerBody`
    - **returns** The design body master whose shape is the given body; else  if the body is not used by a design body.
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Style`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Material`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Name`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Shape`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedSpace.Shape`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.Layer`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.DefaultVisibility`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetColor(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.SetColor(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Drawing.Color})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.SurfaceMaterial`
    - **summary:** Gets the surface material of the body.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetVisibility(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.SetVisibility(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Boolean})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.IsVisible(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.MassProperties`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHasMassProperties.MassProperties`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.CanSuppress`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignBody.IsSuppressed`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignBody.Parent`
    - **summary:** Gets the parent part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignBody.Faces`
    - **summary:** Gets the design faces in the design body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignBody.Edges`
    - **summary:** Gets the design edges in the design body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignBody.Style`
    - **summary:** Gets the display style of the design body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignBody.Name`
    - **summary:** Gets the name of the design body.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignEdge`
    - **summary:** A design edge master.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignEdge.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignEdge.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignEdge.Faces`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignEdge.Faces`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignEdge.Shape`
    - **summary:** Gets the shape of the object.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignEdge.ExportIdentifier`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignFace`
    - **summary:** A design face master.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignFace.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.Edges`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignFace.Edges`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.AdjacentFaces`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignFace.AdjacentFaces`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignFace.GetColor(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignFace.SetColor(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Drawing.Color})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.Shape`
    - **summary:** Gets the shape of the object.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.ExportIdentifier`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignFace.SurfaceMaterial`
    - **summary:** Gets the surface material of the face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignFace.Parent`
    - **summary:** Gets the parent design body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignFace.Edges`
    - **summary:** Gets the design edges in the boundary of this design face.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignFace.AdjacentFaces`
    - **summary:** Gets the design faces adjacent to this design edge.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Document.Parts`
    - **summary:** Gets the parts in this document.
    - **remarks** A document has a , which is the root of its assembly structure.
            If it has internal components (components whose parts live in the same document), then it will have other parts too.
            The  property returns all the parts in the document, including the .
            
            A "3D Markup" document has no parts of its own, so an empty collection will be returned.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.MainPart`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.Parts`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.MainPart`
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Document.MainPart`
    - **summary:** Gets the main part for this document.
    - **remarks** See comments in .
            
            A "3D Markup" document has no main part, so  will be returned.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.Parts`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Document.MainPartDisplaysFileName`
    - **summary:** Gets or sets whether the main part should use the file name as its display name.
    - **remarks** This setting controls how the  of the  is determined.
            The display name is used in the Structure panel and on window tabs.
            
            If the value is , then the  of the part is used as the display name.
            
            If the value is  and the document has been saved (its  is not )
            then the file name is used as the display name; otherwise the  of the part is used.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Part.DisplayName`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.MainPart`
      - **para**
      - **b:** false
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Part.Name`
      - **para**
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.Path`
      - **see**
        - *@cref:* `F:System.String.Empty`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Part.Name`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Document.InternalizeParts(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Part},System.Boolean)`
    - **summary:** Makes internal copies of instantiated external parts.
    - **param:** Parts to internalize.
      - *@name:* `parts`
    - **param:** Whether to internalize the entire assembly structure.
      - *@name:* `deep`
    - **returns:** The mapping from external part to internal part.
    - **remarks** External parts (parts in other documents) are copied into this document
            and  templates in this document are modified to use the internal part instead.
            Modified instances include  and  objects.
            
            A dictionary is returned mapping each original external part to the corresponding internal part.
            Any  that are not directly referenced as templates of instances in this document
            are ignored and are not included as keys in the dictionary returned.
            
            If  is , the entire assembly structure of the external part is internalized,
            which may involve parts from many documents.
            If  is , the external part itself, along with any internal parts in that document, are internalized.
            In both cases, any parts implicitly internalized are also listed in the dictionary returned.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Instance`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Component`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DrawingView`
      - **para**
      - **paramref**
        - *@name:* `parts`
      - **para**
      - **paramref**
        - *@name:* `deep`
      - **b:** true
      - **paramref**
        - *@name:* `deep`
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Document.ExternalizeParts(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Part},System.String)`
    - **summary:** Externalize parts to separate files.
    - **param:** Parts to externalize.
      - *@name:* `parts`
    - **param:** Output directory.
      - *@name:* `directory`
    - **returns:** The mapping from internal part to external part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DrawingSheet.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.IHasShape`
    - **summary:** The object implementing this interface has geometric shape.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Group.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary:** Creates a group.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name of the group.
      - *@name:* `name`
    - **param:** One or more members of the group.
      - *@name:* `members`
    - **returns:** A new group.
    - **exception:** One or more of the members do not belong to this interaction context.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** The new group does not have a dimension ( is ).
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Group.HasDimension`
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Group.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary:** Creates a group.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name of the group.
      - *@name:* `name`
    - **param:** One or more members of the group.
      - *@name:* `members`
    - **param:** One or more secondary members of the group.
      - *@name:* `secondaryMembers`
    - **returns:** A new group.
    - **exception:** One or more of the members do not belong to this interaction context.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** The new group does not have a dimension ( is ).
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Group.HasDimension`
      - **b:** false

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Part`
    - **summary:** A part master.
    - **remarks** A  is a root object, i.e. its  is 
            and its  is itself.
            In contrast, a  may not be a root object, because it might be an occurrence,
            in which case its  will be a  or .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Part.Parent`
      - **b:** null
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.IDocObject.Root`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IPart`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.IDocObject.Parent`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IComponent`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IDrawingView`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.Create(SpaceClaim.Api.V22.Document,System.String)`
    - **summary:** Creates a new part.
    - **param:** The document in which the part should live.
      - *@name:* `doc`
    - **param:** The name for the part.
      - *@name:* `name`
    - **returns:** A part.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.Export(SpaceClaim.Api.V22.PartExportFormat,System.String,System.Boolean,SpaceClaim.Api.V22.ExportOptions)`
    - **summary:** Exports the part in a particular CAD file format.
    - **param:** The file format to use.
      - *@name:* `format`
    - **param:** The path of the file to write to.
      - *@name:* `path`
    - **param** to export components too; otherwise .
      - *@name:* `deepExport`
      - **b:** true
      - **b:** false
    - **param** Export options to use, or  to use the current user options.
      - *@name:* `options`
      - **b:** null
    - **exception:** This copy of SpaceClaim is not licensed for the specified operation.
      - *@cref:* `T:System.InvalidOperationException`
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** A standard file extension will be applied according to the file type specified.
            
            If the part does not contain any design bodies, i.e. there would be nothing to export,
            an  is thrown.
            
            When exporting to an ACIS or Parasolid file, if any design bodies, design faces, or design edges have
            text attributes with the name, "@id", and non-null values, these are written as  attributes applied to 
            resulting ACIS or Parasolid entities.
            
            An ACIS  attribute is a "named attribute" (ATTRIB_GEN_NAME) with the attribute name, "ATTRIB_XACIS_ID".
            
            A Parasolid  attribute has the name, "ATTRIB_XPARASOLID_ID", and has an attribute definition as follows:
            
            
            See  for additional export possibilities.
            
            To import a file, use the  method.
      - **para**
      - **see**
        - *@cref:* `T:System.InvalidOperationException`
      - **para**
      - **i:** id
      - **para**
      - **i:** id
      - **para**
      - **i:** id
      - **code**
        ``` 
        
            static PK_ATTDEF_t Create_ATTRIB_XPARASOLID_ID() {
            	PK_ATTDEF_sf_t descriptor;
                descriptor.name = "ATTRIB_XPARASOLID_ID";
            	descriptor.attdef_class = PK_ATTDEF_class_06_c;
            
            	descriptor.n_owner_types = 6;
            	PK_CLASS_t owner_types[6] = {
            		PK_CLASS_assembly,
            		PK_CLASS_instance,
            		PK_CLASS_body,
            		PK_CLASS_face,
            		PK_CLASS_edge,
            		PK_CLASS_vertex
            	};
            	descriptor.owner_types = owner_types;
            
            	descriptor.n_fields = 1;
            	PK_ATTRIB_field_t field_types[1] = {
            		PK_ATTRIB_field_string_c
            	};
            	descriptor.field_types = field_types;
            
            	PK_ATTDEF_t attDef = PK_ENTITY_null;
            	PK_ERROR_code_t errorCode = PK_ATTDEF_create(&descriptor, &attDef);
            	if (errorCode != PK_ERROR_no_errors)
            		return PK_ENTITY_null;
            
            	return attDef;
            }
            
        ```
        - *@lang:* `C++`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.Export(SpaceClaim.Api.V22.WindowExportFormat,System.String)`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Document.Open(System.String,SpaceClaim.Api.V22.ImportOptions)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Window.Export(SpaceClaim.Api.V22.WindowExportFormat,System.String)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Document.Open(System.String,SpaceClaim.Api.V22.ImportOptions)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.ConvertToSheetMetal`
    - **summary:** Converts the part into a sheet metal part.
    - **exception:** The part cannot be converted to a sheet metal part.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** If the part is already a sheet metal part, or it is a flat pattern, an  is thrown.
      - **see**
        - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.ConvertToSheetMetal(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignFace})`
    - **summary:** Converts the part into a sheet metal part.
    - **param:** The seed faces, one per body.
      - *@name:* `desFaces`
    - **exception:** The part cannot be converted to a sheet metal part.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** If the part is already a sheet metal part, the bodies have different thicknesses, or it is a flat pattern, an  is thrown.
            
            The seed faces indicate the sides of the bodies which are fixed when changing the thickness.
      - **see**
        - *@cref:* `T:System.InvalidOperationException`
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Type`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.SpaceClaim#Api#V22#IPart#SheetMetal`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.SheetMetal`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.SheetMetal`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.IsSheetMetalSuspended`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.FlatPattern`
    - **summary:** Gets the flat pattern aspect of the part.
    - **remarks** If this part is not a flat pattern part,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.TryGetCollision(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignFace},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignFace},SpaceClaim.Api.V22.IDesignFace@,SpaceClaim.Api.V22.IDesignFace@)`
    - **summary:** Tests whether there is a collision between two sets of design faces.
    - **param:** First set of design faces.
      - *@name:* `desFacesA`
    - **param:** Second set of design faces.
      - *@name:* `desFacesB`
    - **param:** First colliding design face.
      - *@name:* `desFaceA`
    - **param:** Second colliding design face.
      - *@name:* `desFaceB`
    - **returns** if a collision was found; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** If a collision is found between a face in  and a face in ,
            then the method returns , and the output arguments  and 
            are set to the pair of colliding faces.
            If there are many collisions, only the first pair discovered is returned.
            
            The nature of the collision is not determined.
            The faces might intersect, they might be coincident, or they might touch along an edge or at a single point.
      - **paramref**
        - *@name:* `desFacesA`
      - **paramref**
        - *@name:* `desFacesB`
      - **b:** true
      - **paramref**
        - *@name:* `desFaceA`
      - **paramref**
        - *@name:* `desFaceB`
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.DisplayName`
    - **summary:** Gets the display name for the part.
    - **remarks** The display name is used in the Structure panel and on window tabs.
            
            For the , the  setting controls how the display name is determined.
            For other parts in the document, the  of the part is used as the display name.
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.MainPart`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.MainPartDisplaysFileName`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Part.Name`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Parent`
    - **summary:** Gets the parent of the part.
    - **remarks** Since a  is a root object, its parent is .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Components`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.Components`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Bodies`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.Bodies`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Meshes`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.Meshes`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.DatumPlanes`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.DatumPlanes`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.DatumLines`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.DatumLines`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.DatumFeatures`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.DatumFeatures`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.CoordinateSystems`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.CoordinateSystems`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.SpotWeldJoints`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.SpotWeldJoints`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Beams`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.Beams`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Bolts`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.Bolts`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.MatingConditions`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.MatingConditions`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.AppearanceStates`
    - **summary:** Gets the appearance states contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.ShareTopology`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.ShareTopology`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.IsEmpty`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.IsEmpty`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.CustomProperties`
    - **summary:** Gets the collection of custom properties for the part.
    - **remarks:** This property provides access to 'Component Properties' in the Properties panel.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Material`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Name`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.Delete`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Images`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.CustomObjects`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.IPart`
    - **summary:** A piece part or assembly.
    - **remarks** There is no compile-time distinction between a piece part and an assembly.
            If a part contains one or more  objects, it might be considered an assembly.
            If it contains one or more  objects, it might be considered a piece part.
            It can contain both  objects and  objects.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IComponent`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IDesignBody`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IComponent`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IDesignBody`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.Type`
    - **summary:** Gets the part type.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.SheetMetal`
    - **summary:** Gets the sheet metal aspect of the part.
    - **remarks** If this part is not a sheet metal part,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.IsSheetMetalSuspended`
    - **summary:** Gets or sets whether sheet metal behavior is suspended.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.Components`
    - **summary:** Gets the components contains by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.Bodies`
    - **summary:** Gets the design bodies contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.Meshes`
    - **summary:** Gets the design meshes contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.DatumPlanes`
    - **summary:** Gets the datum planes contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.DatumLines`
    - **summary:** Gets the datum lines contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.DatumFeatures`
    - **summary:** Gets the datum features contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.CoordinateSystems`
    - **summary:** Gets the coordinate systems contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.SpotWeldJoints`
    - **summary:** Gets the spot weld joints contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.Beams`
    - **summary:** Gets the beams contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.Bolts`
    - **summary:** Gets the bolts contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.MatingConditions`
    - **summary:** Gets the mating conditions contained by the part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.ShareTopology`
    - **summary:** Gets or sets how topology should be shared when transferring this part to analysis.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.IsEmpty`
    - **summary:** Gets whether the part is empty.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.Create(SpaceClaim.Api.V22.Part,System.Boolean)`
    - **summary:** Creates a window showing a part.
    - **param:** A part to be used as the window scene.
      - *@name:* `scene`
    - **param:** Whether the new window should be visible.
      - *@name:* `visible`
    - **returns:** A new window.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.CreateEmbedded(SpaceClaim.Api.V22.Part,SpaceClaim.Api.V22.EmbeddedWindowHandler)`
    - **summary:** Creates a window showing a part, which can be embedded in a custom user interface.
    - **param:** A part to be used as the window scene.
      - *@name:* `scene`
    - **param:** A handler for controlling the embedded window.
      - *@name:* `handler`
    - **returns:** A new window.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.GetWindows(SpaceClaim.Api.V22.Part)`
    - **summary:** Gets all windows having the specified part as their scene.
    - **param:** The window scene.
      - *@name:* `scene`
    - **returns:** Zero or more windows having the specified part as their scene.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.ExportPart(SpaceClaim.Api.V22.PartWindowExportFormat,System.String)`
    - **summary:** Exports the part in a particular file format.
    - **param:** The file format to use.
      - *@name:* `format`
    - **param:** The path of the file to write to.
      - *@name:* `path`
    - **exception:** This copy of SpaceClaim is not licensed for the specified operation.
      - *@cref:* `T:System.InvalidOperationException`
    - **exception:** The window does not show a part.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks**
      - **inheritdoc**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.Export(SpaceClaim.Api.V22.WindowExportFormat,System.String)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Part.Export(SpaceClaim.Api.V22.PartExportFormat,System.String,System.Boolean,SpaceClaim.Api.V22.ExportOptions)`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Window.ClipViewShape`
    - **summary** Specifies a clipping volume shape for use with .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.SetClipVolume(SpaceClaim.Api.V22.Window.ClipViewShape,SpaceClaim.Api.V22.Geometry.Frame,System.Double)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Window.ClipViewShape.Box`
    - **summary:** Use a box for the clipping volume.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Window.ClipViewShape.Sphere`
    - **summary:** Use a sphere for the clipping volume.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.PartWindowExportFormat`
    - **summary** Specifies an export format for use with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.ExportPart(SpaceClaim.Api.V22.PartWindowExportFormat,System.String)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartWindowExportFormat.Vrml`
    - **summary:** A VRML (".wrl") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartWindowExportFormat.Xaml`
    - **summary:** A XAML (".xaml") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartWindowExportFormat.Stl`
    - **summary:** An STL (".stl") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartWindowExportFormat.Obj`
    - **summary:** A Wavefront image (".obj") file.
            A companion material file (".mtl") is also exported.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartWindowExportFormat.Bip`
    - **summary:** A Luxion KeyShot scene (".bip") file.

---
