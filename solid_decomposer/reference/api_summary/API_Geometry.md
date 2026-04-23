  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Analysis.MeshNode.Point`
    - **summary:** Gets the location.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DataMatrixBarcodeProperties.Size`
    - **summary:** Gets or sets the data matrix size.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Barcode.Create(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.BarcodeType,System.String)`
    - **summary:** Creates a barcode.
    - **param:** The parent in which the barcode should be created.
      - *@name:* `parent`
    - **param:** The anchor location in the UV space of the plane of the parent.
      - *@name:* `anchorLocation`
    - **param:** The barcode type.
      - *@name:* `type`
    - **param:** The barcode data.
      - *@name:* `data`
    - **returns:** A barcode.
    - **remarks** If the  is not valid for the , 
            then  will be  for the created barcode.
      - **paramref**
        - *@name:* `data`
      - **paramref**
        - *@name:* `type`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.IBarcode.IsValid`
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Barcode.Create(SpaceClaim.Api.V22.DatumPlane,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.BarcodeType,System.String)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Barcode.Create(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.BarcodeType,System.String)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Barcode.Create(SpaceClaim.Api.V22.IDatumPlane,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.BarcodeType,System.String)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Barcode.Create(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.BarcodeType,System.String)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Barcode.GetLocation(SpaceClaim.Api.V22.LocationPoint)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Barcode.SetLocation(SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Barcode.AnchorPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.BarcodeType.DataMatrix`
    - **summary:** Data Matrix.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DataMatrixBarcodeSize`
    - **summary:** Data matrix barcode size

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.AutomaticSquare`
    - **summary:** Compute size of square symbol automatically

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.AutomaticRectangular`
    - **summary:** Compute size of rectangular symbol automatically

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square10x10`
    - **summary:** Fixed square symbol - 10 x  10

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square12x12`
    - **summary:** Fixed square symbol - 12 x  12

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square14x14`
    - **summary:** Fixed square symbol - 14 x  14

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square16x16`
    - **summary:** Fixed square symbol - 16 x  16

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square18x18`
    - **summary:** Fixed square symbol - 18 x  18

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square20x20`
    - **summary:** Fixed square symbol - 20 x  20

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square22x22`
    - **summary:** Fixed square symbol - 22 x  22

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square24x24`
    - **summary:** Fixed square symbol - 24 x  24

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square26x26`
    - **summary:** Fixed square symbol - 26 x  26

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square32x32`
    - **summary:** Fixed square symbol - 32 x  32

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square36x36`
    - **summary:** Fixed square symbol - 36 x  36

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square40x40`
    - **summary:** Fixed square symbol - 40 x  40

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square44x44`
    - **summary:** Fixed square symbol - 44 x  44

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square48x48`
    - **summary:** Fixed square symbol - 48 x  48

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square52x52`
    - **summary:** Fixed square symbol - 52 x  52

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square64x64`
    - **summary:** Fixed square symbol - 64 x  64

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square72x72`
    - **summary:** Fixed square symbol - 72 x  72

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square80x80`
    - **summary:** Fixed square symbol - 80 x  80

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square88x88`
    - **summary:** Fixed square symbol - 88 x  88

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square96x96`
    - **summary:** Fixed square symbol - 96 x  96

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square104x104`
    - **summary:** Fixed square symbol-size 104 x 104

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square120x120`
    - **summary:** Fixed square symbol-size 120 x 120

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square132x132`
    - **summary:** Fixed square symbol-size 132 x 132

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Square144x144`
    - **summary:** Fixed square symbol-size 144 x 144

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Rectangular8x18`
    - **summary:** Fixed rectangular symbol -  8 x 18

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Rectangular8x32`
    - **summary:** Fixed rectangular symbol -  8 x 32

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Rectangular12x26`
    - **summary:** Fixed rectangular symbol - 12 x 26

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Rectangular12x36`
    - **summary:** Fixed rectangular symbol - 12 x 36

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Rectangular16x36`
    - **summary:** Fixed rectangular symbol - 16 x 36

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.Rectangular16x48`
    - **summary:** Fixed rectangular symbol - 16 x 48

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension8x48`
    - **summary:** Fixed DMRE rectangular extension symbol - 8 x 48

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension8x64`
    - **summary:** Fixed DMRE rectangular extension symbol - 8 x 64

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension12x64`
    - **summary:** Fixed DMRE rectangular extension symbol - 12 x 64

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension16x64`
    - **summary:** Fixed DMRE rectangular extension symbol - 16 x 64

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension24x32`
    - **summary:** Fixed DMRE rectangular extension symbol - 24 x 32

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension24x36`
    - **summary:** Fixed DMRE rectangular extension symbol - 24 x 36

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension24x48`
    - **summary:** Fixed DMRE rectangular extension symbol - 24 x 48

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension24x64`
    - **summary:** Fixed DMRE rectangular extension symbol - 24 x 64

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension26x32`
    - **summary:** Fixed DMRE rectangular extension symbol - 26 x 32

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension26x40`
    - **summary:** Fixed DMRE rectangular extension symbol - 26 x 40

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension26x48`
    - **summary:** Fixed DMRE rectangular extension symbol - 26 x 48

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DataMatrixBarcodeSize.RectangularExtension26x64`
    - **summary:** Fixed DMRE rectangular extension symbol - 26 x 64

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.GeometricToleranceCallout.FrameA`
    - **summary:** Gets the first feature control frame.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.GeometricToleranceCallout.FrameB`
    - **summary:** Gets the second feature control frame, if present.
    - **remarks** If  is , then  will not be .
            
            If  is , then  might not be ,
            which simply means that two single-segment feature control frames are present.
            This facility is used to vertically align the compartments of the two feature control frames.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.GeometricToleranceCallout.IsComposite`
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.GeometricToleranceCallout.FrameB`
      - **b:** null
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.GeometricToleranceCallout.IsComposite`
      - **b:** false
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.GeometricToleranceCallout.FrameB`
      - **b:** null

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.FeatureControlFrame`
    - **summary:** A feature control frame for a geometric tolerance.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FeatureControlFrame.Characteristic`
    - **summary:** Gets the geometric characteristic of the frame.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FeatureControlFrame.ToleranceText`
    - **summary:** Gets the text in the tolerance compartment.
    - **remarks** can be used to parse the tolerance text.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParseTolerance(System.Boolean@,System.Double@,System.Nullable{SpaceClaim.Api.V22.MaterialCondition}@,System.Double@)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParseTolerance(System.Boolean@,System.Double@,System.Nullable{SpaceClaim.Api.V22.MaterialCondition}@,System.Double@)`
    - **summary** Converts the  into its equivalent data, if possible.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.ToleranceText`
    - **param** if the tolerance zone is diametric; otherwise .
      - *@name:* `diametric`
      - **b:** true
      - **b:** false
    - **param:** The tolerance value.
      - *@name:* `tolerance`
    - **param:** The material condition, if specified.
      - *@name:* `materialCondition`
    - **param:** The projected tolerance zone.
      - *@name:* `projectedZone`
    - **returns** if it was possible to parse the ; otherwise .
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.ToleranceText`
      - **b:** false
    - **remarks** If no material condition symbol is specified,  is set to .
            
            If no projected tolerance zone is specified,  is set to 0.
      - **paramref**
        - *@name:* `materialCondition`
      - **b:** null
      - **para**
      - **paramref**
        - *@name:* `projectedZone`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FeatureControlFrame.PrimaryDatumText`
    - **summary:** Gets the text in the primary datum compartment.
    - **remarks** can be used to parse the primary datum text.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParsePrimaryDatum(SpaceClaim.Api.V22.DatumReference@,SpaceClaim.Api.V22.DatumReference@)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParsePrimaryDatum(SpaceClaim.Api.V22.DatumReference@,SpaceClaim.Api.V22.DatumReference@)`
    - **summary** Converts the  into a , if possible.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.PrimaryDatumText`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DatumReference`
    - **param:** The datum reference.
      - *@name:* `datum`
    - **param** An additional datum reference, if the datum is established by two features, else .
      - *@name:* `combinedDatum`
      - **b:** null
    - **returns** if it was possible to parse the ; otherwise .
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.PrimaryDatumText`
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FeatureControlFrame.SecondaryDatumText`
    - **summary:** Gets the text in the secondary datum compartment.
    - **remarks** can be used to parse the secondary datum text.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParseSecondaryDatum(SpaceClaim.Api.V22.DatumReference@)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParseSecondaryDatum(SpaceClaim.Api.V22.DatumReference@)`
    - **summary** Converts the  into a , if possible.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.SecondaryDatumText`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DatumReference`
    - **param:** The datum reference.
      - *@name:* `datum`
    - **returns** if it was possible to parse the ; otherwise .
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.SecondaryDatumText`
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FeatureControlFrame.TertiaryDatumText`
    - **summary:** Gets the text in the tertiary datum compartment.
    - **remarks** can be used to parse the tertiary datum text.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParseTertiaryDatum(SpaceClaim.Api.V22.DatumReference@)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FeatureControlFrame.TryParseTertiaryDatum(SpaceClaim.Api.V22.DatumReference@)`
    - **summary** Converts the  into a , if possible.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.TertiaryDatumText`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DatumReference`
    - **param:** The datum reference.
      - *@name:* `datum`
    - **returns** if it was possible to parse the ; otherwise .
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.FeatureControlFrame.TertiaryDatumText`
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IBlockAnnotation.GetLocation(SpaceClaim.Api.V22.LocationPoint)`
    - **summary:** Gets the location of the specified location point.
    - **param:** The location point whose location is sought.
      - *@name:* `locationPoint`
    - **returns:** The location in UV space.
    - **remarks** The location is in the UV space of the plane of the .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IAnnotationParent`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IBlockAnnotation.SetLocation(SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint)`
    - **summary:** Sets the location and anchor point of the object.
    - **param:** The location for the anchor point.
      - *@name:* `anchorLocation`
    - **param:** The meaning of the anchor point.
      - *@name:* `anchorPoint`
    - **remarks** The location is in the UV space of the plane of the .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IAnnotationParent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IBlockAnnotation.AnchorPoint`
    - **summary:** Gets or sets the anchor point of the object.
    - **remarks** The anchor point of the note is the location that remains fixed when the note is edited.
            
            Changing the anchor point does not reposition the note.
            Instead,  can be used to reposition the note.
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.IBlockAnnotation.SetLocation(SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AttachToPlane.#ctor(SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Constructs an AttachToPlane object.
    - **param:** The plane to use.
      - *@name:* `plane`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AttachToFace.#ctor(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.PointUV,System.Boolean)`
    - **summary:** Constructs an AttachToFace object.
    - **param:** The face to which to attach the image.
      - *@name:* `desFace`
    - **param:** The location in the surface of the face.
      - *@name:* `location`
    - **param:** Whether the image is reversed.
      - *@name:* `reversed`
    - **remarks** The  is the center of the image in the parameter space of the surface of the face.
            
            See  for a description of the  argument.
      - **paramref**
        - *@name:* `location`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.AttachToFace.IsReversed`
      - **paramref**
        - *@name:* `reversed`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.TextInfo.BaselineCurve`
    - **summary:** Gets the text baseline curve.
    - **remarks:** The curve will be a line (linear text) or an arc (circular text).

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SurfaceFinishParameterType.DirectionOfLay`
    - **summary:** Direction of lay.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Symbol.Curves`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Symbol.CurveGroups`
    - **exclude**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SymbolInsert.Create(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Symbol,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Creates a symbol insert.
    - **param:** The parent drawing sheet.
      - *@name:* `parent`
    - **param:** The symbol master to instantiate.
      - *@name:* `template`
    - **param:** The location for the contained symbol within the plane of the drawing sheet.
      - *@name:* `location`
    - **returns:** A symbol insert.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SymbolInsert.Create(SpaceClaim.Api.V22.DatumPlane,SpaceClaim.Api.V22.Symbol,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Creates a symbol insert.
    - **param:** The parent datum plane.
      - *@name:* `parent`
    - **param:** The symbol master to instantiate.
      - *@name:* `template`
    - **param:** The location for the contained symbol within the plane of the datum plane.
      - *@name:* `location`
    - **returns:** A symbol insert.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Table.Create(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.Double,System.Double,System.String[0:,0:])`
    - **summary:** Creates a table.
    - **param:** The parent in which the table should be created.
      - *@name:* `parent`
    - **param:** The anchor location in the UV space of the plane of the parent.
      - *@name:* `anchorLocation`
    - **param:** The anchor point.
      - *@name:* `anchorPoint`
    - **param:** The height of each row.
      - *@name:* `rowHeight`
    - **param:** The width of each column.
      - *@name:* `columnWidth`
    - **param:** The font size in meters.
      - *@name:* `fontSize`
    - **param:** Text for the cells in the table.
      - *@name:* `text`
    - **returns:** A table.
    - **remarks** The number of rows and columns is determined by the dimensions of the  matrix.
            The matrix is in row major order, i.e. cells are indexed as .
      - **paramref**
        - *@name:* `text`
      - **c:** text[row, column]

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Table.Create(SpaceClaim.Api.V22.DatumPlane,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.Double,System.Double,System.String[0:,0:])`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Table.Create(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.Double,System.Double,System.String[0:,0:])`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Table.Create(SpaceClaim.Api.V22.IDatumPlane,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.Double,System.Double,System.String[0:,0:])`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Table.Create(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.Double,System.Double,System.String[0:,0:])`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Table.GetLocation(SpaceClaim.Api.V22.LocationPoint)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Table.SetLocation(SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Table.AnchorPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IBlockEdge.EdgeSplitPoints`
    - **summary:** Gets the edge split points

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IBlockEdgePoint.Parent`
    - **summary:** Gets the parent part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.SketchConstraint.Curves`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Bolt.Create(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignFace},SpaceClaim.Api.V22.BoltProperties,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignEdge},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignEdge},System.Boolean,System.String,System.String)`
    - **summary:** Creates a bolt.
    - **param:** Bolt hole faces.
      - *@name:* `designFaces`
    - **param:** Bolt properties.
      - *@name:* `boltProperties`
    - **param:** Bolt head point.
      - *@name:* `head`
    - **param:** Bolt tail point.
      - *@name:* `tail`
    - **param:** Bolt tail point.
      - *@name:* `headEdgeLoop`
    - **param:** Bolt tail point.
      - *@name:* `tailEdgeLoop`
    - **param:** Indicates whether the bolt is on a blind hole or through hole.
      - *@name:* `isBlind`
    - **param:** The bolt name.
      - *@name:* `name`
    - **param:** The bolt source part name.
      - *@name:* `boltSourceName`
    - **returns:** A bolt.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.IDesignCurveGroup`
    - **exclude**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveGroup.Parent`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveGroup.Type`
    - **summary:** Gets the type of the group.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveGroup.Curves`
    - **summary:** Gets the design curves in the group.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IDesignCurveGroup.ReplaceCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignCurve})`
    - **summary:** Replaces the curves with a new set.
    - **param**
      - *@name:* `desCurves`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignCurveGroupGeneral`
    - **exclude**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroupGeneral.GetVisibility(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroupGeneral.SetVisibility(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Boolean})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroupGeneral.IsVisible(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroupGeneral.Name`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroupGeneral.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ITransformable.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroupGeneral.Layer`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroupGeneral.DefaultVisibility`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignCurveGroup`
    - **exclude**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroup.Create(System.String,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignCurve})`
    - **summary:** Creates a design curve group.
    - **param:** The name of the curve group.
      - *@name:* `name`
    - **param:** The curves to be included in the group.
      - *@name:* `desCurves`
    - **returns:** The new design curve group.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroup.Create(System.String,SpaceClaim.Api.V22.DesignCurveGroupType,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignCurve})`
    - **summary:** Creates a design curve group.
    - **param:** The name of the curve group.
      - *@name:* `name`
    - **param:** The type of the curve group.
      - *@name:* `type`
    - **param:** The curves to be included in the group.
      - *@name:* `desCurves`
    - **returns:** The new design curve group.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroup.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignMesh.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroup.Type`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignCurveGroup.Type`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroup.Curves`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignCurveGroup.Curves`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroup.SpaceClaim#Api#V22#IDesignCurveGroup#Curves`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignCurveGroup.Curves`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroup.GetVisibility(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroup.SetVisibility(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Boolean})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroup.IsVisible(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroup.Layer`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroup.DefaultVisibility`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurveGroup.Name`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGroup.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ITransformable.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.FacePoint`
    - **summary:** A curve point master.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FacePoint.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IFacePoint.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FacePoint.Position`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.FacePoint.ExportIdentifier`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.IFacePoint`
    - **summary:** A curve point.
    - **remarks** A curve point is an implicit doc object, which means you cannot create or delete one. 
            Its parent is a  and the curve point represents an endpoint of that curve. If the parent is deleted, 
            the curve point will report that  is .
            
            The parent may be a , , or .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.IDeletable.IsDeleted`
      - **b:** true
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IDesignEdge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IDesignCurve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IBeam`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IFacePoint.Parent`
    - **summary:** Gets the parent design edge.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IFacePoint.Position`
    - **summary:** Gets the position.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IFacePoint.Type`
    - **summary:** Gets the face point type

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.FacePointType`
    - **summary:** Specifies the type of face point

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.FacePointType.ConeApex`
    - **summary:** Cone apex

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.FacePointType.SphereCenter`
    - **summary:** Sphere center

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.FacePointType.SkewConeApex`
    - **summary:** Skew Cone Apex

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Helix`
    - **summary:** A helix.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV`
    - **summary:** Represents the evaluation of a UV curve at some parameter value.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV.Param`
    - **summary:** Gets the parameter at which the evaluation was performed.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV.Point`
    - **summary:** The point on the curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV.Tangent`
    - **summary:** The tangent direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV.Derivative`
    - **summary:** The first derivative.
    - **remarks** The first derivative is in the direction of the 
            and has a magnitude equal to the velocity (rate of change of position) at that point.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV.Tangent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV.Derivative2`
    - **summary:** The second derivative.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluationUV.Curvature`
    - **summary:** The curvature.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.NurbsCurveUV`
    - **summary:** A NURBS (Non-Uniform Rational B-Spline) curve in UV space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsCurveUV.IsRational`
    - **summary:** Gets whether the spline curve is rational.
    - **remarks** If the spline curve is rational, then the  of each 
            is significant; otherwise the weights are all the same, and their value is 1.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ControlPointUV.Weight`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ControlPointUV`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsCurveUV.Data`
    - **summary:** Gets data describing the spline curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsCurveUV.ControlPoints`
    - **summary:** Gets the control points for the spline curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsCurveUV.Evaluate(System.Double)`
    - **summary:** Evaluates the curve at the given parameter.
    - **param:** The parameter at which to evaluate.
      - *@name:* `t`
    - **returns:** The evaluation of the curve.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Polygon`
    - **summary:** A regular polygon.
    - **remarks** The axis of the polygon is in the  direction of its .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Polygon.Frame`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Polygon.Points`
    - **summary:** Gets the vertices.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Polygon.InnerRadius`
    - **summary:** Gets the inner radius.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Polygon.SideCount`
    - **summary:** Gets the number of sides.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Polygon.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Polygon.Plane`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Polygon.Axis`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Polygon.AsSpline(SpaceClaim.Api.V22.Geometry.Interval)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.FitMethod`
    - **summary:** Curve-fitting method.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.FitMethod.Lines`
    - **summary:** Fit lines.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.FitMethod.Arcs`
    - **summary:** Fit arcs.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.FitMethod.Splines`
    - **summary:** Fit splines.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.FitMethod.LinesAndArcs`
    - **summary:** Fit lines and arcs.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.FitMethod.LinesAndSplines`
    - **summary:** Fit lines and splines.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.FitMethod.LinesAndArcsTangentize`
    - **summary:** Fit tangent lines and arcs.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.LineSegment`
    - **summary:** A line segment.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IArrow`
    - **summary:** A planar profile in the shape of an arrow.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IArrow.HeadLength`
    - **summary:** Gets the length of the arrowhead.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IArrow.HeadWidth`
    - **summary:** Gets the width of the arrowhead.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IArrow.ShaftLength`
    - **summary:** Gets the length of the shaft of the arrow.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IArrow.ShaftWidth`
    - **summary:** Gets the width of the shaft of the arrow.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IArrow.Overlap`
    - **summary:** Gets how far the shaft penetrates the back of the arrowhead.
    - **remarks:** A positive overlap produces an arrowhead with swept back wings.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ArrowProfile`
    - **summary:** A planar profile in the shape of an arrow.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ArrowProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Double,System.Double,System.Double,System.Double,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Constructs a planar profile in the shape of an arrow.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The length of the arrowhead.
      - *@name:* `headLength`
    - **param:** The width of the arrowhead.
      - *@name:* `headWidth`
    - **param:** The length of the shaft.
      - *@name:* `shaftLength`
    - **param:** The width of the shaft.
      - *@name:* `shaftWidth`
    - **param:** How far the shaft penetrates the back of the arrowhead.
      - *@name:* `overlap`
    - **param:** The location within the plane.
      - *@name:* `location`
    - **param:** The rotation angle.
      - *@name:* `angle`
    - **remarks** A positive  produces an arrowhead with swept back wings.
      - **paramref**
        - *@name:* `overlap`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ArrowProfile.Location`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ArrowProfile.Angle`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ArrowProfile.HeadLength`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ArrowProfile.HeadWidth`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ArrowProfile.ShaftLength`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ArrowProfile.ShaftWidth`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ArrowProfile.Overlap`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasPlanarPlacement`
    - **summary:** An object that has location and angle within the UV space of a plane.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasPlanarPlacement.Location`
    - **summary:** Gets the location within the plane.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasPlanarPlacement.Angle`
    - **summary:** Gets the rotation angle.
    - **remarks** The angle is in radians.
            
            The angle specifies the clockwise rotation about the normal of the plane
            (counterclockwise rotation as seen looking down onto the plane).
      - **para**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IPolygon`
    - **summary:** A planar profile, which is a polygon.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IPolygon.Points`
    - **summary:** Gets the points of the polygon.
    - **remarks** The first point is the start of the first segment of the .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IProfile.Boundary`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IPolygon.PointsUV`
    - **summary:** Gets the points of the polygon in the UV space of the plane.
    - **remarks** The first point is the start of the first segment of the .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IProfile.Boundary`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.PolygonProfile`
    - **summary:** A planar profile, which is a polygon.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolygonProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point})`
    - **summary:** Constructs a polygon profile passing through the specified points.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The points of the polygon.
      - *@name:* `points`
    - **exception:** Must have at least 3 points.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** Points are not coplanar.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The points are coplanar but do not lie on the specified plane.
      - *@cref:* `T:System.ArgumentException`
    - **remarks:** The points are absolute 3D points and are not affected by the orientation of the plane. The points must lie in the plane.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolygonProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.PointUV})`
    - **summary:** Constructs a polygon profile passing through the specified points.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The points of the polygon.
      - *@name:* `pointsUV`
    - **remarks:** The points are in the UV space of the plane.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolygonProfile.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolygonProfile.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolygonProfile.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolygonProfile.BoxUV`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolygonProfile.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolygonProfile.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolygonProfile.Points`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolygonProfile.PointsUV`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasRotationalSymmetry`
    - **summary:** An object with rotational symmetry.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasRotationalSymmetry.Order`
    - **summary:** Gets the order of the rotational symmetry.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IRegularPolygon`
    - **summary:** A planar profile in the shape of a regular polygon.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IRegularPolygon.InnerRadius`
    - **summary:** Get the inner radius of the polygon.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IRegularPolygon.OuterRadius`
    - **summary:** Gets the outer radius of the polygon.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IRegularPolygon.Side`
    - **summary:** Gets the side length.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile`
    - **summary:** A planar profile in the shape of a regular polygon.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Int32,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Constructs a planar profile in the shape of a regular polygon.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The order of the polygon.
      - *@name:* `order`
    - **param:** The outer radius of the polygon.
      - *@name:* `outerRadius`
    - **param:** The location within the plane.
      - *@name:* `location`
    - **param:** The rotation angle.
      - *@name:* `angle`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile.Location`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile.Angle`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile.OuterRadius`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile.InnerRadius`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile.Side`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RegularPolygonProfile.Order`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IStar`
    - **summary:** A planar profile in the shape of a star.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IStar.InnerRadius`
    - **summary:** Gets the inner radius of the star.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IStar.OuterRadius`
    - **summary:** Gets the outer radius of the star.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.StarProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Int32,System.Double,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Constructs a planar profile in the shape of a star.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The order of the star.
      - *@name:* `order`
    - **param:** The inner radius of the star.
      - *@name:* `innerRadius`
    - **param:** The outer radius of the star.
      - *@name:* `outerRadius`
    - **param:** The location within the plane.
      - *@name:* `location`
    - **param:** The rotation angle.
      - *@name:* `angle`
    - **remarks** The star is centered at the  supplied.
      - **paramref**
        - *@name:* `location`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.StarProfile.Location`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.StarProfile.Angle`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.StarProfile.InnerRadius`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.StarProfile.OuterRadius`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.StarProfile.Order`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.PolylineOptions`
    - **summary** Specifies options used with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Curve.GetPolyline(SpaceClaim.Api.V22.Geometry.Interval,SpaceClaim.Api.V22.Geometry.PolylineOptions)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Curve.GetPolyline(SpaceClaim.Api.V22.Geometry.Interval,SpaceClaim.Api.V22.Geometry.PolylineOptions)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.PolylineOptions.Default`
    - **summary:** A default set of polyline options.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.PolylineOptions.#ctor`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolylineOptions.CurveDeviation`
    - **summary:** Gets the maximum deviation from the true curve position.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolylineOptions.AngleDeviation`
    - **summary:** Gets the maximum deviation from the true curve tangent.
    - **remarks:** The value is in radians.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PolylineOptions.MaximumChordLength`
    - **summary:** Gets the maximum chord length, or zero if not specified.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolylineOptions.#ctor`
    - **summary** Constructs a  with a default set of options.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PolylineOptions`
    - **remarks** The default options are:
      - **list**
        - *@type:* `bullet`
        - **item** = 0.00075 (0.75 mm)
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Geometry.PolylineOptions.CurveDeviation`
        - **item** = 10° (in radians)
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Geometry.PolylineOptions.AngleDeviation`
        - **item** = 0 (unspecified)
          - **see**
            - *@cref:* `P:SpaceClaim.Api.V22.Geometry.PolylineOptions.MaximumChordLength`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolylineOptions.#ctor(System.Double,System.Double)`
    - **summary** Constructs a  object.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PolylineOptions`
    - **param:** The maximum deviation from the true curve position.
      - *@name:* `curveDeviation`
    - **param:** The maximum deviation from the true curve tangent.
      - *@name:* `angleDeviation`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PolylineOptions.#ctor(System.Double,System.Double,System.Double)`
    - **summary** Constructs a  object.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PolylineOptions`
    - **param:** The maximum deviation from the true curve position.
      - *@name:* `curveDeviation`
    - **param:** The maximum deviation from the true curve tangent.
      - *@name:* `angleDeviation`
    - **param:** The maximum chord length, or zero if not specified.
      - *@name:* `maxChordLength`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IProfile`
    - **summary:** A planar profile.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IProfile.Boundary`
    - **summary:** Gets the boundary of the profile.
    - **remarks** For profiles with implicit boundaries, such as  or ,
            the segments are in clockwise order about the plane normal (counter-clockwise as seen looking down onto
            the plane), and the first segment starts on or crosses over the X-axis of the plane.
            
            If the profile has an explicit boundary, created using the 
            constructor, no such ordering is required.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IRegularPolygon`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IStar`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Profile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Profile`
    - **summary:** A planar profile.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Profile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **summary:** Constructs a planar profile with a specified boundary.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The boundary segments.
      - *@name:* `boundary`
    - **remarks:** The boundary segments should lie in the plane.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Profile.Boundary`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Profile.Plane`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Profile.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Profile.BoxUV`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Profile.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Profile.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Profile.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Profile.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Profile.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Profile.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Profile.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ICircle`
    - **summary:** A planar profile in the shape of a circle.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ICircle.Radius`
    - **summary:** Gets the radius of the circle.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.CircleProfile`
    - **summary:** A planar profile in the shape of a circle.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CircleProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Constructs a planar profile in the shape of a circle.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The radius of the circle.
      - *@name:* `radius`
    - **param:** The location within the plane.
      - *@name:* `location`
    - **param:** The rotation angle.
      - *@name:* `angle`
    - **remarks** The circle is centered at the  supplied.
      - **paramref**
        - *@name:* `location`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CircleProfile.Location`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CircleProfile.Angle`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CircleProfile.Radius`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CircleProfile.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CircleProfile.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CircleProfile.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CircleProfile.BoxUV`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CircleProfile.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IOblong`
    - **summary:** A planar profile in the shape of an oblong.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IOblong.Width`
    - **summary:** Gets the width of the oblong.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IOblong.Height`
    - **summary:** Gets the height of the oblong.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.OblongProfile`
    - **summary:** Specifies details for an oblong form.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.OblongProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Double,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Constructs a planar profile in the shape of an oblong.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The width of the oblong.
      - *@name:* `width`
    - **param:** The height of the oblong.
      - *@name:* `height`
    - **param:** The location within the plane.
      - *@name:* `location`
    - **param:** The rotation angle.
      - *@name:* `angle`
    - **remarks** The oblong is centered at the  supplied.
            The width is measured along the X-axis of the plane,
            and the height is measured along the Y-axis of the plane.
      - **paramref**
        - *@name:* `location`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.OblongProfile.Location`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.OblongProfile.Angle`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.OblongProfile.Width`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.OblongProfile.Height`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.OblongProfile.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.OblongProfile.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.OblongProfile.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.OblongProfile.BoxUV`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IRectangle`
    - **summary:** A planar profile in the shape of a rectangle.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IRectangle.Width`
    - **summary:** Gets the width of the rectangle.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IRectangle.Height`
    - **summary:** Gets the height of the rectangle.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.RectangleProfile`
    - **summary:** A planar profile in the shape of a rectangle.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.RectangleProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Double,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Constructs a planar profile in the shape of a rectangle.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The width of the rectangle.
      - *@name:* `width`
    - **param:** The height of the rectangle.
      - *@name:* `height`
    - **param:** The location within the plane.
      - *@name:* `location`
    - **param:** The rotation angle.
      - *@name:* `angle`
    - **remarks** The rectangle is centered at the  supplied.
            The width is measured along the X-axis of the plane,
            and the height is measured along the Y-axis of the plane.
      - **paramref**
        - *@name:* `location`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RectangleProfile.Location`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RectangleProfile.Angle`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RectangleProfile.Width`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RectangleProfile.Height`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.RectangleProfile.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RectangleProfile.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.RectangleProfile.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ISquare`
    - **summary:** A planar profile in the shape of a square.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.SquareProfile`
    - **summary:** A planar profile in the shape of a square.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.SquareProfile.#ctor(SpaceClaim.Api.V22.Geometry.Plane,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Constructs a planar profile in the shape of a square.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** The side length.
      - *@name:* `side`
    - **param:** The location within the plane.
      - *@name:* `location`
    - **param:** The rotation angle.
      - *@name:* `angle`
    - **remarks** The square is centered at the  supplied.
            and oriented with the X and Y axes of the plane.
      - **paramref**
        - *@name:* `location`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SquareProfile.Location`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SquareProfile.Angle`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SquareProfile.Side`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.SquareProfile.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SquareProfile.Area`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SquareProfile.Perimeter`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.PlacementUV`
    - **summary:** A location and orientation within the UV space of a plane.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.PlacementUV.#ctor(SpaceClaim.Api.V22.Geometry.PointUV,System.Double)`
    - **summary:** Creates a placement.
    - **param:** The location in UV space.
      - *@name:* `location`
    - **param:** The angle from the U direction.
      - *@name:* `angle`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PlacementUV.Location`
    - **summary:** Gets the location in UV space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.PlacementUV.Angle`
    - **summary:** Gets the angle from the U direction.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ParamForm`
    - **summary:** The parameterization form.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.ParamForm.Open`
    - **summary:** The parameterization is open.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.ParamForm.Closed`
    - **summary:** The parameterization is closed.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.ParamForm.Periodic`
    - **summary:** The parameterization is periodic.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Transformations`
    - **summary:** A bit field specifying transformations.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.None`
    - **summary:** No transformations.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.TranslateX`
    - **summary:** Translate along X.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.TranslateY`
    - **summary:** Translate along Y.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.TranslateZ`
    - **summary:** Translate along Z.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.RotateX`
    - **summary:** Rotate about X.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.RotateY`
    - **summary:** Rotate about Y.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.RotateZ`
    - **summary:** Rotate about Z.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Transformations.All`
    - **summary:** All transformations.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasCurveShape`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IHasCurveShape`
    - **typeparam:** The type of curve.
      - *@name:* `TCurve`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasCurveShape`
    - **summary:** The object implementing this interface has curve shape.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ICurveShape`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ICurveShape`
    - **typeparam:** The type of curve.
      - *@name:* `TCurve`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ICurveShape`1.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ICurveShape`
    - **summary:** The object implementing this interface has a curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ICurveShape.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasSurfaceShape`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IHasSurfaceShape`
    - **typeparam:** The type of surface.
      - *@name:* `TSurface`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasSurfaceShape`
    - **summary:** The object implementing this interface has surface shape.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ISurfaceShape`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ISurfaceShape`
    - **typeparam:** The type of surface.
      - *@name:* `TSurface`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ISurfaceShape`1.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ISurfaceShape`
    - **summary:** The object implementing this interface has a surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ISurfaceShape.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.DirectionUV`
    - **summary:** A 2D direction in UV space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.DirectionUV.IsZero`
    - **summary:** Gets whether the direction is indeterminate.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.DirectionUV.UnitVector`
    - **summary:** Gets a unit vector for the direction.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Parameterization`
    - **summary:** The parameterization of a curve, or of the U or V direction of a surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Parameterization.Form`
    - **summary:** Gets parameterization form.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Parameterization.Bounds`
    - **summary:** Gets the parameterization bounds.
    - **remarks** If the start or end is , then the parameterization is infinite in that direction.
      - **b:** null

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.PointCurve`
    - **summary:** A curve existing only at a point.
    - **remarks** A  is a degenerate curve, existing only at a point.
            Conceptually it can be thought of as a  with a zero .
            
            A  has no direction so its  is .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PointCurve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Circle`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Circle.Radius`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PointCurve`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Tangent`
      - **see**
        - *@cref:* `F:SpaceClaim.Api.V22.Geometry.Direction.Zero`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ISpaceShape`
    - **summary:** The object implementing this interface has space geometry.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ISpaceShape.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Space`
    - **summary:** A 3D space.
    - **remarks** A space represents unbounded 3D space.
             returns the same point,
            and  returns .
            
            Any two spaces are considered equal, e.g.  returns .
            
            This class only exists to complete the classification of geometry types, and is of no particular use.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.ISpatial.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.ISpatial.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
      - **b:** true
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Geometry.IsCoincident(SpaceClaim.Api.V22.Geometry.Geometry)`
      - **b:** true
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Space.Create`
    - **summary:** Creates a space.
    - **returns:** A space.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Space.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Space)`
    - **summary:** Transforms a space.
    - **param:** The transformation to apply.
      - *@name:* `trans`
    - **param:** The space to be transformed.
      - *@name:* `space`
    - **returns:** A transformed copy of the space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedGeometry.Shape`
    - **summary:** Gets the shape of the object.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedGeometry.GetClosestSeparation(SpaceClaim.Api.V22.Geometry.ITrimmedGeometry)`
    - **summary:** Get the closest separation between two objects.
    - **param:** The other object.
      - *@name:* `other`
    - **returns:** The closest separation between the two objects.
    - **remarks** In the returned ,  is a point on this object,
            and  is a point on the  object.
            
            If this method is used with two  objects (e.g. two  objects),
            and one object is entirely inside the other, the separation returned is zero, since the separation is
            between the trimmed spaces, and not their surface boundaries.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Separation`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Separation.PointA`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Separation.PointB`
      - **paramref**
        - *@name:* `other`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedSpace`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Body`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Separation`
    - **summary:** The separation between two objects.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Separation.PointA`
    - **summary:** The point on the first object.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Separation.PointB`
    - **summary:** The point on the second object.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Separation.Distance`
    - **summary:** The separation distance.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.VectorUV`
    - **summary:** A 2D displacement vector in UV space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.VectorUV.Direction`
    - **summary:** Gets the direction of the vector.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.VectorUV.Magnitude`
    - **summary:** Gets the magnitude of the vector.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Accuracy`
    - **summary:** The Accuracy class provides a safe way to compare length, angles, areas, and volumes. Due to the
            slight inaccuracies in representing calculated values digitally, comparisons are made using well-defined
            tolerances that account for this slight inaccuracy.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`
    - **summary:** Gets the linear resolution.
    - **remarks** Two lengths are considered equal if their difference is less than the .
            To compare two lengths, use the  method.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualLengths(System.Double,System.Double)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.AngularResolution`
    - **summary:** Gets the angular resolution.
    - **remarks** Two angles are considered equal if their difference is less than the .
            To compare two angles, use the  method.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.AngularResolution`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualAngles(System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualLengths(System.Double,System.Double)`
    - **summary:** Compares two length values to see if they are equal.
    - **param:** The first length value.
      - *@name:* `lengthA`
    - **param:** The second length value.
      - *@name:* `lengthB`
    - **returns** Returns  if the values are within
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualAreas(System.Double,System.Double)`
    - **summary** Compares two area values to see if they are equal within a predefined tolerance based 
            on .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`
    - **param:** The first area value.
      - *@name:* `areaA`
    - **param:** The second area value.
      - *@name:* `areaB`
    - **returns** Returns  if the values are within the tolerance.
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualVolumes(System.Double,System.Double)`
    - **summary** Compares two volume values to see if they are equal within a predefined tolerance
            based on .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`
    - **param:** The first volume value.
      - *@name:* `volumeA`
    - **param:** The second volume value.
      - *@name:* `volumeB`
    - **returns** Returns  if the values are within the tolerance.
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualAngles(System.Double,System.Double)`
    - **summary:** Compares two angular values to see if they are equal.
    - **param:** The first angular value.
      - *@name:* `angleA`
    - **param:** The second angular value.
      - *@name:* `angleB`
    - **returns** Returns  if the values are within
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.AngularResolution`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.LengthIsNegative(System.Double)`
    - **summary:** Determines if the length value is negative.
    - **param:** Length value to check
      - *@name:* `length`
    - **returns** Returns  if the length value is less than -.
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.LengthIsPositive(System.Double)`
    - **summary:** Determines if the length value is positive.
    - **param:** Length value to check
      - *@name:* `length`
    - **returns** Returns  if the length value is greater than .
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.LengthIsZero(System.Double)`
    - **summary** Determines if the length value is zero (between plus and minus  inclusive).
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.LinearResolution`
    - **param:** Length value to check
      - *@name:* `length`
    - **returns** Returns  if the length value is effectively zero.
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.AngleIsNegative(System.Double)`
    - **summary:** Determines if the angle value is negative.
    - **param:** Length value to check
      - *@name:* `angle`
    - **returns** Returns  if the angle value is less than -.
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.AngularResolution`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.AngleIsPositive(System.Double)`
    - **summary:** Determines if the angle value is positive.
    - **param:** Length value to check
      - *@name:* `angle`
    - **returns** Returns  if the angle value is greater than .
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.AngularResolution`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.AngleIsZero(System.Double)`
    - **summary** Determines if the angle value is zero (between plus and minus  inclusive).
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Accuracy.AngularResolution`
    - **param:** Length value to check
      - *@name:* `angle`
    - **returns** Returns  if the angle value is effectively zero.
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.CompareLengths(System.Double,System.Double)`
    - **summary:** Compares two length values.
    - **param:** The first length value to compare.
      - *@name:* `lengthA`
    - **param:** The second length value to compare.
      - *@name:* `lengthB`
    - **returns** if  is less than .
              if  is equal to  (see Remarks).
             if  is greater than .
      - **b:** -1
      - **i:** lengthA
      - **i:** lengthB
      - **br**
      - **b:** 0
      - **i:** lengthA
      - **i:** lengthB
      - **br**
      - **b:** 1
      - **i:** lengthA
      - **i:** lengthB
      - **br**
    - **remarks** CompareLengths first checks if the two lengths are equal (see ). 
            If they are not equal, they are compared directly to each other to determine which is 
            the smaller or larger of the two.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualLengths(System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.CompareAngles(System.Double,System.Double)`
    - **summary:** Compares two angle values.
    - **param:** The first angle value to compare.
      - *@name:* `angleA`
    - **param:** The second angle value to compare.
      - *@name:* `angleB`
    - **returns** if  is less than .
              if  is equal to  (see Remarks).
             if  is greater than .
      - **b:** -1
      - **i:** angleA
      - **i:** angleB
      - **br**
      - **b:** 0
      - **i:** angleA
      - **i:** angleB
      - **br**
      - **b:** 1
      - **i:** angleA
      - **i:** angleB
      - **br**
    - **remarks** CompareAngles first checks if the two angles are equal (see ). 
            If they are not equal, they are compared directly to each other to determine which is 
            the smaller or larger of the two.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualAngles(System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.CompareAreas(System.Double,System.Double)`
    - **summary:** Compares two area values.
    - **param:** The first area value to compare.
      - *@name:* `areaA`
    - **param:** The second area value to compare.
      - *@name:* `areaB`
    - **returns** if  is less than .
              if  is equal to  (see Remarks).
             if  is greater than .
      - **b:** -1
      - **i:** areaA
      - **i:** areaB
      - **br**
      - **b:** 0
      - **i:** areaA
      - **i:** areaB
      - **br**
      - **b:** 1
      - **i:** areaA
      - **i:** areaB
      - **br**
    - **remarks** CompareAreas first checks if the two lengths are equal (see ). 
            If they are not equal, they are compared directly to each other to determine which is 
            the smaller or larger of the two.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualAreas(System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.CompareVolumes(System.Double,System.Double)`
    - **summary:** Compares two volume values.
    - **param:** The first volume value to compare.
      - *@name:* `volumeA`
    - **param:** The second volume value to compare.
      - *@name:* `volumeB`
    - **returns** if  is less than .
              if  is equal to  (see Remarks).
             if  is greater than .
      - **b:** -1
      - **i:** volumeA
      - **i:** volumeB
      - **br**
      - **b:** 0
      - **i:** volumeA
      - **i:** volumeB
      - **br**
      - **b:** 1
      - **i:** volumeA
      - **i:** volumeB
      - **br**
    - **remarks** CompareVolumes first checks if the two volumes are equal (see ). 
            If they are not equal, they are compared directly to each other to determine which is 
            the smaller or larger of the two.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Accuracy.EqualVolumes(System.Double,System.Double)`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IBounded`
    - **summary:** The object implementing this interface is bounded in nature.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.IBounded.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **summary:** Gets the bounding box of the object under the given transformation.
    - **param:** The transformation to be applied to the object.
      - *@name:* `trans`
    - **returns:** The bounding box.
    - **remarks** The bounding box is guaranteed to enclose the object.
            It may not fit tightly around the object, although it often does.
            The overload  can be used to obtain a tight box.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.IBounded.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.IBounded.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **summary:** Gets the bounding box of the object under the given transformation.
    - **param:** The transformation to be applied to the object.
      - *@name:* `trans`
    - **param:** Whether the bounding box is required to fit tightly around the object.
      - *@name:* `tight`
    - **returns:** The bounding box.
    - **remarks** If  is , the bounding box will fit tightly around the object.
            This calculation is typically more expensive, so it should only be used if necessary.
            
            If  is , the bounding box is guaranteed to enclose the object.
            It may not fit tightly around the object, although it often does.
      - **paramref**
        - *@name:* `tight`
      - **b:** true
      - **para**
      - **paramref**
        - *@name:* `tight`
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.IBounded.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Gets the extreme point of the object.
    - **param:** The first direction.
      - *@name:* `dirA`
    - **param:** The second direction.
      - *@name:* `dirB`
    - **param:** The third direction.
      - *@name:* `dirC`
    - **returns:** The extreme point.
    - **remarks** The three directions must be mutually perpendicular, but they do not need to be right-handed.
            
            The extreme point in direction  is returned.
            If the extreme in that direction is not a single point, then  is used.
            If the extreme is still not a single point, then  is used.
      - **para**
      - **paramref**
        - *@name:* `dirA`
      - **paramref**
        - *@name:* `dirB`
      - **paramref**
        - *@name:* `dirC`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Box.Empty`
    - **summary:** An empty box.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.Create(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a box of zero size located at a specified point.
    - **param:** The location of the box.
      - *@name:* `point`
    - **returns:** The created box.
    - **remarks** A box of zero size has a  of ,
            but it is not empty ( returns false).
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Box.Size`
      - **see**
        - *@cref:* `F:SpaceClaim.Api.V22.Geometry.Vector.Zero`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Box.IsEmpty`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.Create(SpaceClaim.Api.V22.Geometry.Point[])`
    - **summary:** Creates a box that contains a list of points.
    - **param:** Zero or more points to be contained by the box.
      - *@name:* `points`
    - **returns:** The created box.
    - **remarks:** If no points are supplied, an empty box is created.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.Create(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.Point})`
    - **summary:** Creates a box that contains a collection of points.
    - **param:** Points to be contained by the box.
      - *@name:* `points`
    - **returns:** The created box.
    - **remarks:** If the collection of points is empty, an empty box is created.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Box.IsEmpty`
    - **summary:** Gets whether the box is empty.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Box.Center`
    - **summary:** Gets the center of the box.
    - **exception:** The box is empty.
      - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Box.Size`
    - **summary:** Gets the size of the box.
    - **remarks** The size is the vector from the  to the .
            If the box is empty, a  size is returned.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Box.MinCorner`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Box.MaxCorner`
      - **see**
        - *@cref:* `F:SpaceClaim.Api.V22.Geometry.Vector.Zero`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Box.MinCorner`
    - **summary:** Gets the minimum corner of the box.
    - **exception:** The box is empty.
      - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Box.MaxCorner`
    - **summary:** Gets the maximum corner of the box.
    - **exception:** The box is empty.
      - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Box.Corners`
    - **summary:** Gets all corners of the box.
    - **exception:** The box is empty.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks:** The corners returned are distinct, i.e. duplicates are removed.
            The number of points returned could be zero, one, two, four, or eight.
            An empty box returns zero corners.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Gets whether the box contains a point.
    - **param:** The point to test.
      - *@name:* `point`
    - **returns** if the box contains the point; otherwise .
      - **b:** true
      - **b:** false
    - **remarks:** A point on the boundary of the box is considered contained by it.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.IntersectsPlane(SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Gets whether the box intersects a plane.
    - **param:** The plane to test.
      - *@name:* `plane`
    - **returns** if the box and the plane intersect; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.Inflate(System.Double)`
    - **summary:** Inflates the box all around by a specified amount.
    - **param:** The amount to inflate.
      - *@name:* `extent`
    - **returns:** An inflated box.
    - **exception:** The box is empty.
      - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.op_BitwiseOr(SpaceClaim.Api.V22.Geometry.Box,SpaceClaim.Api.V22.Geometry.Box)`
    - **summary:** Unites two boxes.
    - **param:** The first box to unite.
      - *@name:* `first`
    - **param:** The second box to unite.
      - *@name:* `second`
    - **returns:** The union of the two boxes.
    - **remarks:** If one of the boxes is empty, the other box is returned.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Box.op_BitwiseAnd(SpaceClaim.Api.V22.Geometry.Box,SpaceClaim.Api.V22.Geometry.Box)`
    - **summary:** Intersects two boxes.
    - **param:** The first box to intersect.
      - *@name:* `first`
    - **param:** The second box to intersect.
      - *@name:* `second`
    - **returns:** The intersection of the two boxes.
    - **remarks:** If either box is empty, or the boxes do not intersect, an empty box is returned.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.BoxUV`
    - **summary:** A box in UV-space.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.BoxUV.Empty`
    - **summary:** An empty box.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.BoxUV.IsEmpty`
    - **summary:** Gets whether the box is empty.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.BoxUV.op_BitwiseOr(SpaceClaim.Api.V22.Geometry.BoxUV,SpaceClaim.Api.V22.Geometry.BoxUV)`
    - **summary:** Unites two boxes.
    - **param:** The first box to unite.
      - *@name:* `first`
    - **param:** The second box to unite.
      - *@name:* `second`
    - **returns:** The union of the two boxes.
    - **remarks:** If one of the boxes is empty, the other box is returned.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.BoxUV.op_BitwiseAnd(SpaceClaim.Api.V22.Geometry.BoxUV,SpaceClaim.Api.V22.Geometry.BoxUV)`
    - **summary:** Intersects two boxes.
    - **param:** The first box to intersect.
      - *@name:* `first`
    - **param:** The second box to intersect.
      - *@name:* `second`
    - **returns:** The intersection of the two boxes.
    - **remarks:** If either box is empty, or the boxes do not intersect, an empty box is returned.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Circle`
    - **summary:** A circle.
    - **remarks** The axis of the circle is in the  direction of its .
            
            The parameter specifies the clockwise angle around the axis (right hand corkscrew law),
            with a zero parameter at , and a period of 2*pi.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Circle.Frame`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Curve.Parameterization`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.Create(SpaceClaim.Api.V22.Geometry.Frame,System.Double)`
    - **summary:** Creates a circle.
    - **param:** The position and orientation of the circle.
      - *@name:* `frame`
    - **param:** The radius of the circle.
      - *@name:* `radius`
    - **returns:** A circle.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.CreateThroughPoints(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a circle passing through three points.
    - **param:** The plane of the circle.
      - *@name:* `plane`
    - **param:** Point to pass through.
      - *@name:* `thruPoint1`
    - **param:** Point to pass through.
      - *@name:* `thruPoint2`
    - **param:** Point to pass through.
      - *@name:* `thruPoint3`
    - **returns** A circle if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.CreateTangentToThree(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.CurveParam)`
    - **summary:** Creates a circle tangent to three curves.
    - **param:** The plane of the circle.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent1`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent2`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent3`
    - **returns** A circle if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.CreateTangentToTwo(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a circle tangent to two curves, passing through a point.
    - **param:** The plane of the circle.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent1`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent2`
    - **param:** Point to pass through.
      - *@name:* `thruPoint`
    - **returns** A circle if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.CreateTangentToTwo(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.CurveParam,System.Double)`
    - **summary:** Creates a circle tangent to two curves, with a given radius.
    - **param:** The plane of the circle.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent1`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent2`
    - **param:** The radius of the circle.
      - *@name:* `radius`
    - **returns** A circle if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.CreateTangentToOne(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a circle tangent to a curve, passing through two points.
    - **param:** The plane of the circle.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent`
    - **param:** Point to pass through.
      - *@name:* `thruPoint1`
    - **param:** Point to pass through.
      - *@name:* `thruPoint2`
    - **returns** A circle if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.CreateTangentToOne(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.Point,System.Double)`
    - **summary:** Creates a circle tangent to a curve, passing through a point, with a given radius.
    - **param:** The plane of the circle.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent`
    - **param:** Point to pass through.
      - *@name:* `thruPoint`
    - **param:** The radius of the circle.
      - *@name:* `radius`
    - **returns** A circle if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.CreateTangentToOne(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a circle tangent to a curve, centered on a curve, passing through a point.
    - **param:** The plane of the circle.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent`
    - **param:** Help point on curve on which the center should lie.
      - *@name:* `center`
    - **param:** Point to pass through.
      - *@name:* `thruPoint`
    - **returns** A circle if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Circle.Radius`
    - **summary:** Gets the radius of the circle.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Circle.TryOffsetParam(System.Double,System.Double,System.Double@)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Circle.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Circle.Plane`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Circle.Axis`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Cone`
    - **summary:** A cone.
    - **remarks** The axis of the cone is in the  direction of its .
            
            The U parameter specifies the clockwise angle around the axis (right hand corkscrew law),
            with a zero parameter at , and a period of 2*pi.
            
            The V parameter specifies the distance along the axis,
            with a zero parameter at the XY plane of the  of the cone.
            
            A cone has the given  in the XY plane of its ,
            and increases in radius in the direction of .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Cone.Frame`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Cone.Frame`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Cone.Radius`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Cone.Frame`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Cone.Radius`
    - **summary:** The radius of the cone in the XY plane of its frame.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Cone.HalfAngle`
    - **summary:** The half angle of the cone.
    - **remarks** The cone increases in radius in the direction of .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Cone.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Cone.Axis`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Curve`
    - **summary:** A 3D curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.Evaluate(System.Double)`
    - **summary:** Evaluates the curve at the given parameter.
    - **param:** The parameter at which to evaluate.
      - *@name:* `t`
    - **returns:** The evaluation of the curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Projects a point to the curve, returning the evaluation at the closest point.
    - **param:** The point to project.
      - *@name:* `point`
    - **returns:** The evaluation at the closest point.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Curve)`
    - **summary:** Transforms a curve.
    - **param:** The transformation to apply.
      - *@name:* `trans`
    - **param:** The curve to be transformed.
      - *@name:* `curve`
    - **returns:** A transformed copy of the curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.GetLength(SpaceClaim.Api.V22.Geometry.Interval)`
    - **summary:** Gets the length of an interval of the curve.
    - **param:** The parametric interval of the curve.
      - *@name:* `interval`
    - **returns:** The length of the interval of the curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.GetPolyline(SpaceClaim.Api.V22.Geometry.Interval,SpaceClaim.Api.V22.Geometry.PolylineOptions)`
    - **summary:** Gets a polyline approximation of an interval of the curve.
    - **param:** The parametric interval of the curve.
      - *@name:* `interval`
    - **param:** Polyline options.
      - *@name:* `options`
    - **returns:** A list of points describing the polyline.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.TryOffsetParam(System.Double,System.Double,System.Double@)`
    - **summary:** Offsets a parameter along the curve.
    - **param:** The parameter to offset.
      - *@name:* `start`
    - **param:** The distance to offset, which can be negative.
      - *@name:* `distance`
    - **param:** The resulting parameter.
      - *@name:* `result`
    - **returns** if successful; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** For a bounded non-periodic curve, this method will fail (i.e. return )
            if the offset would result in a parameter outside the parametric
             of the curve.
      - **b:** false
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Parameterization.Bounds`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.ContainsParam(System.Double)`
    - **summary:** Tests whether a parameter is within the parametric range of the curve.
    - **param:** The parameter to test.
      - *@name:* `param`
    - **returns** if within the parametric range of the curve; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.IntersectCurve(SpaceClaim.Api.V22.Geometry.Curve)`
    - **summary:** Gets the intersections between this curve and another curve.
    - **param:** The other curve to intersect.
      - *@name:* `curve`
    - **returns:** Zero or more intersection points.
    - **remarks** For each intersection point,  is on this curve,
            and  is on the other curve.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IntPoint`2.EvaluationA`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IntPoint`2.EvaluationB`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Curve.AsSpline(SpaceClaim.Api.V22.Geometry.Interval)`
    - **summary:** Gets a NURBS approximation for the curve.
    - **param:** The region of interest.
      - *@name:* `region`
    - **returns** The spline approximation; else  if not possible.
      - **b:** null
    - **remarks** A spline curve is returned that covers at least the specified region.
            The parameterization of the spline curve is not the same as the original curve.
            
            When dealing with the curve of an ,
            the  of the edge can be supplied as the region.
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Edge`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.Bounds`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IntPoint`2`
    - **summary:** An intersection point.
    - **typeparam:** The first evaluation type.
      - *@name:* `TEvaluationA`
    - **typeparam:** The second evaluation type.
      - *@name:* `TEvaluationB`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.IntPoint`2.#ctor(`0,`1,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Constructs an intersection point.
    - **param:** The first evaluation.
      - *@name:* `evalA`
    - **param:** The second evaluation
      - *@name:* `evalB`
    - **param:** The intersection point.
      - *@name:* `point`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IntPoint`2.Point`
    - **summary:** Gets the intersection point.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IntPoint`2.EvaluationA`
    - **summary:** Gets the first evaluation.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IntPoint`2.EvaluationB`
    - **summary:** Gets the second evaluation.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.CurveEvaluation`
    - **summary:** Represents the evaluation of a curve at some parameter value.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Param`
    - **summary:** Gets the parameter at which the evaluation was performed.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Point`
    - **summary:** The point on the curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Tangent`
    - **summary:** The tangent direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Derivative`
    - **summary:** The first derivative.
    - **remarks** The first derivative is in the direction of the 
            and has a magnitude equal to the velocity (rate of change of position) at that point.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Tangent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Derivative2`
    - **summary:** The second derivative.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveEvaluation.Curvature`
    - **summary:** The curvature.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.CurveParam`
    - **summary:** A parameter on a curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveParam.#ctor(SpaceClaim.Api.V22.Geometry.Curve,System.Double)`
    - **summary:** Creates a curve point.
    - **param:** A curve.
      - *@name:* `curve`
    - **param** A parameter on the .
      - *@name:* `param`
      - **paramref**
        - *@name:* `curve`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveParam.Curve`
    - **summary:** Gets the curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveParam.Param`
    - **summary:** Gets the parameter on the curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.Create(SpaceClaim.Api.V22.Geometry.Curve,SpaceClaim.Api.V22.Geometry.Interval)`
    - **overloads**
      - **summary:** Creates a curve segment.
    - **summary** Creates a  from an unbounded  and parameter .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.CurveSegment`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Curve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Interval`
    - **param:** The underlying unbounded curve.
      - *@name:* `curve`
    - **param:** The parameter bounds.
      - *@name:* `bounds`
    - **returns:** A segment of the curve.
    - **exception** is a null reference.
      - *@cref:* `T:System.ArgumentNullException`
      - **paramref**
        - *@name:* `curve`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.Create(SpaceClaim.Api.V22.Geometry.Curve,SpaceClaim.Api.V22.Geometry.Interval,System.Boolean)`
    - **summary** Creates a  from an unbounded  and parameter .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.CurveSegment`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Curve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Interval`
    - **param:** The underlying unbounded curve.
      - *@name:* `curve`
    - **param:** The parameter bounds.
      - *@name:* `bounds`
    - **param:** Whether the curve segment has reversed sense.
      - *@name:* `reversed`
    - **returns:** A segment of the curve.
    - **exception** is a null reference.
      - *@cref:* `T:System.ArgumentNullException`
      - **paramref**
        - *@name:* `curve`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.Create(SpaceClaim.Api.V22.Geometry.Curve)`
    - **summary** Creates a  for the entirety of a curve.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.CurveSegment`
    - **param:** The underlying unbounded curve.
      - *@name:* `curve`
    - **returns:** A segment of the curve.
    - **remarks** This method is useful for creating a  for a complete circle or ellipse,
            since there is no need to supply a parametric interval.
            
            The  must have a finite parametric range.
            An exception is thrown if the parametric range of the curve is infinite.
            For example, this will happen if a  is supplied as the .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.CurveSegment`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.CurveSegment`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Line`
      - **paramref**
        - *@name:* `curve`
    - **exception:** The curve has infinite parameterization.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.Create(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a line segment between the specified points.
    - **param:** The start point.
      - *@name:* `start`
    - **param:** The end point.
      - *@name:* `end`
    - **returns** The line segment, or  if the  and  points are coincident.
      - **b:** null
      - **paramref**
        - *@name:* `start`
      - **paramref**
        - *@name:* `end`
    - **remarks** Creates a  whose  is a .
            The  point has a parameter value of 0, and
            the  point has a parameter value equal to the length of the line segment.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.CurveSegment`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.Geometry`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Line`
      - **paramref**
        - *@name:* `start`
      - **paramref**
        - *@name:* `end`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.Create(SpaceClaim.Api.V22.Geometry.LineSegment)`
    - **summary:** Create a line segment.
    - **param:** The line segment.
      - *@name:* `segment`
    - **returns** The line segment, or  if the length of  is zero.
      - **b:** null
      - **paramref**
        - *@name:* `segment`
    - **remarks** Creates a  whose  is a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.CurveSegment`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.Geometry`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Line`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.CreateArc(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates an arc.
    - **param:** The center point.
      - *@name:* `center`
    - **param:** The start point.
      - *@name:* `start`
    - **param:** The end point.
      - *@name:* `end`
    - **param:** The axis of the arc.
      - *@name:* `axis`
    - **returns:** An arc.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.CreateHelix(SpaceClaim.Api.V22.Geometry.Line,SpaceClaim.Api.V22.Geometry.Point,System.Double,System.Double,System.Double,SpaceClaim.Api.V22.CircularSense)`
    - **summary:** Creates a helix.
    - **param:** The axis.
      - *@name:* `axis`
    - **param:** The starting point.
      - *@name:* `startPoint`
    - **param:** The height.
      - *@name:* `height`
    - **param:** The distances between rotations.
      - *@name:* `pitch`
    - **param:** The taper angle. A negative angle tapers inwards.
      - *@name:* `taperAngle`
    - **param:** The sense, looking along the axis from the origin.
      - *@name:* `sense`
    - **returns:** A helical curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.Bounds`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.Length`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.StartPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.EndPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.IntersectCurve(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.Offset(SpaceClaim.Api.V22.Geometry.Plane,System.Double)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.Offset(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.OffsetChain(SpaceClaim.Api.V22.Geometry.Plane,System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.OffsetCornerType)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.OffsetChain(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.OffsetCornerType)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.ApproximateChain(System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.FitMethod)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.SelectFragment(System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.GetPolyline(SpaceClaim.Api.V22.Geometry.PolylineOptions)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.IsCoincident(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.ProjectToPlane(SpaceClaim.Api.V22.Geometry.Plane)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.GetClosestSeparation(SpaceClaim.Api.V22.Geometry.ITrimmedGeometry)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.GetGeometry``1`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.CurveSegment.IsReversed`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.CurveSegment.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Cylinder`
    - **summary:** A cylinder.
    - **remarks** The axis of the cylinder is in the  direction of its .
            
            The U parameter specifies the clockwise angle around the axis (right hand corkscrew law),
            with a zero parameter at , and a period of 2*pi.
            
            The V parameter specifies the distance along the axis,
            with a zero parameter at the XY plane of the  of the cylinder.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Cylinder.Frame`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Cylinder.Frame`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Surface.Parameterization`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Cylinder.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Cylinder.Axis`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Direction`
    - **summary:** A 3D direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Direction.IsZero`
    - **summary:** Gets whether the direction is indeterminate.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Direction.UnitVector`
    - **summary:** Gets a unit vector in this direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Direction.ArbitraryPerpendicular`
    - **summary:** Gets an arbitrary perpendicular direction.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Direction.Cross(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Calculates the cross product of two directions.
    - **remarks** If the two directions are parallel, no exception is thrown, but a zero direction is returned ( is true).
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Direction.IsZero`
    - **param:** The first direction.
      - *@name:* `dirA`
    - **param:** The second direction.
      - *@name:* `dirB`
    - **returns:** The resulting direction.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Ellipse`
    - **summary:** An ellipse.
    - **remarks** The axis of the ellipse is in the  direction of its .
            
            The parameter specifies the clockwise angle around the axis (right hand corkscrew law),
            with a zero parameter at , and a period of 2*pi.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Ellipse.Frame`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Curve.Parameterization`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Ellipse.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Ellipse.Plane`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Ellipse.Axis`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Frame`
    - **summary:** A local coordinate system.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Frame.Create(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates a frame from its X and Y directions.
    - **param:** The origin of the frame.
      - *@name:* `origin`
    - **param:** The X direction of the frame.
      - *@name:* `dirX`
    - **param:** The Y direction of the frame.
      - *@name:* `dirY`
    - **returns:** A frame.
    - **remarks** A frame uses a right-handed system of mutually perpendicular XYZ axes.
            It is not necessary to supply the Z direction, since this is defined by
            .
      - **c** = Direction.(, )
        - **i:** dirZ
        - **see**
          - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Direction.Cross(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
        - **paramref**
          - *@name:* `dirX`
        - **paramref**
          - *@name:* `dirY`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Frame.Create(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Frame.Create(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates a frame using arbitrary X and Y directions.
    - **param:** The origin of the frame.
      - *@name:* `origin`
    - **param:** The Z direction of the frame.
      - *@name:* `dirZ`
    - **returns:** A frame.
    - **remarks** A frame uses a right-handed system of mutually perpendicular XYZ axes.
            This overload creates arbitrary X and Y directions such that 
            .
      - **c** = Direction.(, )
        - **paramref**
          - *@name:* `dirZ`
        - **see**
          - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Direction.Cross(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
        - **i:** dirX
        - **i:** dirY
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Frame.Create(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasFrame`
    - **summary:** The object implementing this interface has a frame.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasFrame.Frame`
    - **summary:** Gets the frame of the object.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Geometry.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Geometry)`
    - **summary:** Transforms a geometry object.
    - **param:** The transformation to apply.
      - *@name:* `trans`
    - **param:** The geometry object to be transformed.
      - *@name:* `geometry`
    - **returns:** The transformed geometry object.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Geometry.IsCoincident(SpaceClaim.Api.V22.Geometry.Geometry)`
    - **summary:** Compares two geometry objects to see if they are coincident.
    - **param:** Geometry to compare to.
      - *@name:* `other`
    - **returns** if the geometries are coincident; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Geometry.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Geometry.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IShape`
    - **summary:** The object implementing this interface has geometry.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IShape.Geometry`
    - **summary:** Gets the geometry of the object.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.IShape.GetGeometry``1`
    - **summary** Filters the geometry based on the  specified.
            Returns null if the geometry is not of that type.
      - **typeparamref**
        - *@name:* `TFilter`
    - **typeparam:** The type of geometry sought.
      - *@name:* `TFilter`
    - **returns:** The geometry of that type, or null if the geometry is not of that type.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`
    - **summary:** Gets whether the sense of the object is opposite to the sense of its geometry.
    - **remarks** For example,  implements .
            A hole and a boss are both examples of a  with a  as its geometry.
            With a cylinder, the surface normal always points away from the axis of the cylinder.
            For a hole, the face normal points towards the axis, so  is true,
            whereas for a boss, the face normal points away from the axis, so  is false.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Face`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ISurfaceShape`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Face`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Cylinder`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Interval`
    - **summary:** A parametric interval.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Interval.Start`
    - **summary:** Gets the start parameter of the interval.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Interval.End`
    - **summary:** Gets the end parameter of the interval.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Interval.Span`
    - **summary:** Gets the span of the interval.
    - **remarks** The span is the difference between the  and  parameters.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.Start`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.End`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Interval.Contains(System.Double)`
    - **summary:** Gets whether the interval contains the specified parameter.
    - **param:** The parameter to test.
      - *@name:* `param`
    - **returns** if the parameter is contained in the interval; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** The parameters,  and , are contained within the interval.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.Start`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.End`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Interval.GetProportion(System.Double)`
    - **summary:** Gets the proportion of the interval that the specified parameter represents.
    - **param:** The parameter for which the proportion is sought.
      - *@name:* `param`
    - **returns:** The proportion along the interval at the specified parameter.
    - **remarks** The  parameter has a proportion of 0,
            and the  parameter has a proportion of 1.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.Start`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.End`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Interval.GetParameter(System.Double)`
    - **summary:** Gets the parameter at the specified proportion along the interval.
    - **param:** The proportion along the interval.
      - *@name:* `proportion`
    - **returns:** The parameter at the specified proportion.
    - **remarks** The  indexer is equivalent to this method.
            
             is equivalent to , and
             is equivalent to .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.Item(System.Double)`
      - **para**
      - **c:** GetParameter(0)
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.Start`
      - **c:** GetParameter(1)
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.End`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Interval.Item(System.Double)`
    - **summary:** Gets the parameter at the specified proportion along the interval.
    - **param:** The proportion along the interval.
      - *@name:* `proportion`
    - **returns:** The parameter at the specified proportion.
    - **remarks** This indexer is equivalent to .
            
             is equivalent to , and
             is equivalent to .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Interval.GetParameter(System.Double)`
      - **para**
      - **c:** interval[0]
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.Start`
      - **c:** interval[1]
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Interval.End`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Line`
    - **summary:** A line.
    - **remarks** The parameter specifies the distance from the  in the direction of .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Line.Origin`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Line.Direction`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Curve.Parameterization`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Line.Create(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates a line.
    - **param:** A point through which the line passes.
      - *@name:* `origin`
    - **param:** The direction of the line.
      - *@name:* `dir`
    - **returns:** A line.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Line.CreateThroughPoints(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a line passing through two points.
    - **param:** Point to pass through.
      - *@name:* `thruPoint1`
    - **param:** Point to pass through.
      - *@name:* `thruPoint2`
    - **returns** A line if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Line.CreateTangentToTwo(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.CurveParam)`
    - **summary:** Creates a line tangent to two curves.
    - **param:** The plane in which the line should lie.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent1`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent2`
    - **returns** A line if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Line.CreateTangentToOne(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a line tangent to a curve, and passing through a point.
    - **param:** The plane in which the line should lie.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent`
    - **param:** Point to pass through.
      - *@name:* `thruPoint`
    - **returns** A line if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Line.CreateTangentToOne(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates a line tangent to a curve, with a given direction.
    - **param:** The plane in which the line should lie.
      - *@name:* `plane`
    - **param:** Help point on tangent curve.
      - *@name:* `tangent`
    - **param:** The direction of the line.
      - *@name:* `dir`
    - **returns** A line if successful; otherwise .
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Line.Origin`
    - **summary:** Gets the origin of the line.
    - **remarks:** The origin is the point on the line with a parameter value of zero.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Line.Direction`
    - **summary:** Gets the direction of the line.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Line.TryOffsetParam(System.Double,System.Double,System.Double@)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasAxis`
    - **summary:** The object implementing this interface has an axis.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasAxis.Axis`
    - **summary:** Gets the axis of the object.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.NurbsData`
    - **summary:** Data for a NURBS (Non-Uniform Rational B-Spline) curve or surface.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsData.#ctor(System.Int32,System.Boolean,System.Boolean,SpaceClaim.Api.V22.Geometry.Knot[])`
    - **summary:** Creates data for a NURBS curve or surface.
    - **param:** The order of the NURBS curve or surface.
      - *@name:* `order`
    - **param:** Whether the NURBS curve or surface is closed.
      - *@name:* `closed`
    - **param:** Whether the NURBS curve or surface is periodic.
      - *@name:* `periodic`
    - **param:** The knot vector for the NURBS curve or surface.
      - *@name:* `knots`
    - **exception:** The geometry can only be period if it is also closed.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.Order`
    - **summary:** Gets the order of the NURBS curve or surface.
    - **remarks** The  is one less than the .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.Degree`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.Order`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.Degree`
    - **summary:** Gets the degree of the NURBS curve or surface.
    - **remarks** The  is one less than the .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.Degree`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.Order`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.IsClosed`
    - **summary:** Gets whether the NURBS curve or surface is closed.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.IsPeriodic`
    - **summary:** Gets whether the NURBS curve or surface is periodic.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsData.Knots`
    - **summary:** Gets the knot vector for the NURBS curve or surface.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Knot`
    - **summary:** A knot within the knot vector of a NURBS curve or surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Knot.Parameter`
    - **summary:** Gets the parametric location of the knot.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Knot.Multiplicity`
    - **summary:** Gets the number of times the knot parameter is used.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ControlPoint`
    - **summary:** A control point for a NURBS curve or surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ControlPoint.Position`
    - **summary:** Gets the position of the control point.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ControlPoint.Weight`
    - **summary:** Gets the weight applied to the control point.
    - **remarks** If the spline is rational, then the  of each 
            is significant; otherwise the weights are all the same, and their value is 1.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ControlPoint.Weight`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ControlPoint`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ControlPointUV`
    - **summary:** A control point for a NURBS curve in UV space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ControlPointUV.Position`
    - **summary:** Gets the position of the control point.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ControlPointUV.Weight`
    - **summary:** Gets the weight applied to the control point.
    - **remarks** If the spline is rational, then the  of each 
            is significant; otherwise the weights are all the same, and their value is 1.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ControlPoint.Weight`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ControlPoint`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.PointUV`
    - **summary:** A 2D point in UV space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Plane.PlaneXY`
    - **summary:** The X-Y plane.
    - **remarks** This is equivalent to calling:
      - **code:** Plane.Create(Frame.Create(Point.Origin, Direction.DirX, Direction.DirY))

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Plane.PlaneYZ`
    - **summary:** The Y-Z plane.
    - **remarks** This is equivalent to calling:
      - **code:** Plane.Create(Frame.Create(Point.Origin, Direction.DirY, Direction.DirZ))

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Plane.PlaneZX`
    - **summary:** The Z-X plane.
    - **remarks** This is equivalent to calling:
      - **code:** Plane.Create(Frame.Create(Point.Origin, Direction.DirZ, Direction.DirX))

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Plane.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ProceduralCurve`
    - **summary:** A procedural curve.
    - **remarks:** A procedural curve is a curve that is defined in terms of other objects.
            Examples include: intersection curves, offset curves, etc.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ProceduralSurface`
    - **summary:** A procedural surface.
    - **remarks:** A procedural surface is a surface that is defined in terms of other objects.
            Examples include: fillet surfaces, offset surfaces, swept surfaces, ruled surfaces, etc.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ProceduralSurface.AsSpline(SpaceClaim.Api.V22.Geometry.BoxUV)`
    - **summary:** Gets a NURBS approximation for the procedural surface.
    - **param:** The region of interest.
      - *@name:* `region`
    - **returns** The spline approximation; else  if not possible.
      - **b:** null
    - **remarks** A spline surface is returned that covers at least the specified region.
            The parameterization of the spline surface is not the same as the procedural surface.
            
            When dealing with the surface of a ,
            the  of the face can be supplied as the region.
            Passing a smaller region may or may not produce in a smaller spline surface.
            Passing a larger region may fail to produce a spline surface, in which case  is returned.
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Face`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Face.BoxUV`
      - **b:** null

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ISpatial`
    - **summary:** The object implementing this interface is spatial in nature.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ISpatial.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Projects a point to the object, returning the closest point on the object,
            or the original point if that is already contained by the object.
    - **param:** The point to project.
      - *@name:* `point`
    - **returns:** The projected point.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ISpatial.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Gets whether the point is contained by the object, either within it, or on its boundary.
    - **param:** The point to test.
      - *@name:* `point`
    - **returns:** Whether the point is contained by the object.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Sphere`
    - **summary:** A sphere.
    - **remarks** Imagine a sphere with  of its  pointing North:
            
            The U parameter specifies the longitude angle, increasing clockwise (East) about  (right hand corkscrew law).
            It has a zero parameter at , and a period of 2*pi.
            
            The V parameter specifies the latitude, increasing North, with a zero parameter at the equator,
            and a range of [-pi/2, pi/2].
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Sphere.Frame`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
      - **para**
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Surface.Parameterization`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Sphere.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.NurbsCurve`
    - **summary:** A NURBS (Non-Uniform Rational B-Spline) curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsCurve.CreateFromControlPoints(SpaceClaim.Api.V22.Geometry.NurbsData,SpaceClaim.Api.V22.Geometry.ControlPoint[])`
    - **summary:** Creates a NURBS curve from control points.
    - **param:** The NURBS data.
      - *@name:* `data`
    - **param:** The control points for the curve.
      - *@name:* `controlPoints`
    - **returns:** The created NURBS curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsCurve.CreateFromKnotPoints(System.Boolean,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Nullable{SpaceClaim.Api.V22.Geometry.Vector},System.Nullable{SpaceClaim.Api.V22.Geometry.Vector})`
    - **summary:** Creates a NURBS curve from a list of knot points.
    - **param:** Whether the NURBS curve is periodic.
      - *@name:* `periodic`
    - **param:** A list of knot points to pass through.
      - *@name:* `points`
    - **param** Start derivative; else  for natural.
      - *@name:* `startDerivative`
      - **b:** null
    - **param** End derivative; else  for natural.
      - *@name:* `endDerivative`
      - **b:** null
    - **returns:** The created NURBS curve.
    - **remarks:** The NURBS curve created has order 4.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsCurve.CreateFromKnotPoints(System.Boolean,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point})`
    - **summary:** Creates a NURBS curve from a list of knot points.
    - **param:** Whether the NURBS curve is periodic.
      - *@name:* `periodic`
    - **param:** A list of knot points to pass through.
      - *@name:* `points`
    - **returns:** The created NURBS curve.
    - **remarks:** The NURBS curve created has order 4.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsCurve.CreateThroughPoints(System.Boolean,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Double,System.Nullable{SpaceClaim.Api.V22.Geometry.Vector},System.Nullable{SpaceClaim.Api.V22.Geometry.Vector})`
    - **summary:** Creates a NURBS curve that fits through a list of points.
    - **param:** Whether the NURBS curve is periodic.
      - *@name:* `periodic`
    - **param:** A list of points to pass through.
      - *@name:* `points`
    - **param:** The fit tolerance.
      - *@name:* `fitTolerance`
    - **param** Start derivative; else  for natural.
      - *@name:* `startDerivative`
      - **b:** null
    - **param** End derivative; else  for natural.
      - *@name:* `endDerivative`
      - **b:** null
    - **returns:** The created NURBS curve.
    - **remarks:** The NURBS curve created has order 4.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsCurve.CreateThroughPoints(System.Boolean,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Double)`
    - **summary:** Creates a NURBS curve that fits through a list of points.
    - **param:** Whether the NURBS curve is periodic.
      - *@name:* `periodic`
    - **param:** A list of points to pass through.
      - *@name:* `points`
    - **param:** The fit tolerance.
      - *@name:* `fitTolerance`
    - **returns:** The created NURBS curve.
    - **remarks:** The NURBS curve created has order 4.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsCurve.IsRational`
    - **summary:** Gets whether the spline curve is rational.
    - **remarks** If the spline curve is rational, then the  of each 
            is significant; otherwise the weights are all the same, and their value is 1.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ControlPoint.Weight`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ControlPoint`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsCurve.Data`
    - **summary:** Gets data describing the spline curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsCurve.ControlPoints`
    - **summary:** Gets the control points for the spline curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsCurve.Extend(SpaceClaim.Api.V22.Geometry.Interval)`
    - **summary:** Creates a new extended curve based on the supplied interval.
    - **param:** The parametric extent of the new curve to create.
      - *@name:* `interval`
    - **returns** A new NURBS curve if successful; otherwise .
      - **b:** null
    - **remarks:** The curve is extended naturally so that the extension is C2 continuous.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.NurbsSurface`
    - **summary:** A NURBS (Non-Uniform Rational B-Spline) surface.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsSurface.Create(SpaceClaim.Api.V22.Geometry.NurbsData,SpaceClaim.Api.V22.Geometry.NurbsData,SpaceClaim.Api.V22.Geometry.ControlPoint[0:,0:])`
    - **summary:** Creates a NURBS surface.
    - **param:** The NURBS data in the U direction.
      - *@name:* `dataU`
    - **param:** The NURBS data in the V direction.
      - *@name:* `dataV`
    - **param:** The control points for the surface.
      - *@name:* `controlPoints`
    - **returns:** The created NURBS surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsSurface.IsRational`
    - **summary:** Gets whether the spline surface is rational.
    - **remarks** If the spline surface is rational, then the  of each 
            is significant; otherwise the weights are all the same, and their value is 1.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ControlPoint.Weight`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ControlPoint`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsSurface.DataU`
    - **summary:** Gets data describing the spline surface in the U direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsSurface.DataV`
    - **summary:** Gets data describing the spline surface in the V direction.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.NurbsSurface.ControlPoints`
    - **summary:** Gets the control points for the spline surface.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.NurbsSurface.Trim(SpaceClaim.Api.V22.Geometry.BoxUV)`
    - **summary** Creates a new trimmed  based on the supplied .
      - **b:** NurbsSurface
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.BoxUV`
    - **param:** Specifies how to trim the surface.
      - *@name:* `boxUV`
    - **returns** A  NurbsSurface trimmed to the desired range.
      - **i:** new
    - **exception** has an invalid range. End must be greater than Start.
      - *@cref:* `T:System.ArgumentOutOfRangeException`
      - **i:** boxUV

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Surface`
    - **summary:** A 3D surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Surface.IsRuled`
    - **summary:** Gets whether the surface is straight in the U and V parameter directions.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Surface.IsSingular`
    - **summary:** Gets whether there is a parametric singularity at the Start or End of the U or V range.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Surface.Evaluate(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Evaluates the surface at the given parameter.
    - **param:** The parameter at which to evaluate.
      - *@name:* `param`
    - **returns:** The evaluation of the surface.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Surface.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Projects a point to the surface, returning the evaluation at the closest point.
    - **param:** The point to project.
      - *@name:* `point`
    - **returns:** The evaluation at the closest point on the surface.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Surface.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Surface)`
    - **summary:** Transforms a surface.
    - **param:** The transformation to apply.
      - *@name:* `trans`
    - **param:** The surface to be transformed.
      - *@name:* `surface`
    - **returns:** A transformed copy of the surface.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Surface.GetLength(SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Gets the length in the surface between two parameters in UV space.
    - **param:** The first parameter.
      - *@name:* `paramA`
    - **param:** The second parameter.
      - *@name:* `paramB`
    - **returns:** The length in the surface.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Surface.TryOffsetParam(SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.Geometry.DirectionUV,System.Double,SpaceClaim.Api.V22.Geometry.PointUV@)`
    - **summary:** Offsets a point in UV space within the surface.
    - **param:** The UV point to offset.
      - *@name:* `start`
    - **param:** The direction in which to offset.
      - *@name:* `dir`
    - **param:** The distance to offset within the surface.
      - *@name:* `distance`
    - **param:** The resulting UV point.
      - *@name:* `result`
    - **returns** if successful; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** The method will fail (i.e. return ) if the offset would result in a UV point outside
            the parametric  of the surface.
      - **b:** false
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Parameterization.Bounds`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Surface.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Tests whether a parameter is within the parametric range of the surface.
    - **param:** The parameter to test.
      - *@name:* `param`
    - **returns** if within the parametric range of the surface; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Surface.IntersectCurve(SpaceClaim.Api.V22.Geometry.Curve)`
    - **summary:** Gets the intersections between the surface and a curve.
    - **param:** The curve to intersect.
      - *@name:* `curve`
    - **returns:** Zero or more intersection points.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.UV`1`
    - **summary:** U and V values.
    - **typeparam**
      - *@name:* `T`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.UV`1.#ctor(`0,`0)`
    - **summary:** Constructs a UV object.
    - **param** The  value.
      - *@name:* `u`
      - **i:** u
    - **param** The  value.
      - *@name:* `v`
      - **i:** v

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.UV`1.U`
    - **summary** Gets or sets the  value;
      - **i:** u

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.UV`1.V`
    - **summary** Gets or sets the  value;
      - **i:** v

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.Param`
    - **summary:** Gets the parameter at which the evaluation was performed.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.Point`
    - **summary:** Gets the point on the surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.Normal`
    - **summary:** Gets the normal to the surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.DerivativeU`
    - **summary:** The first derivative with respect to U.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.DerivativeV`
    - **summary:** The first derivative with respect to V.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.DerivativeUU`
    - **summary:** The second derivative with respect to U.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.DerivativeUV`
    - **summary:** The second derivative with respect to U and V.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.DerivativeVV`
    - **summary:** The second derivative with respect to V.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.MaxCurvature`
    - **summary:** The maximum curvature.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.MinCurvature`
    - **summary:** The minimum curvature.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.MaxCurvatureDirection`
    - **summary:** The direction of maximum curvature.
    - **remarks** The  and  are perpendicular
            and both directions lie in the surface.
            
            If the curvature is the same in all directions in the surface at this position,
            the two directions are arbitrary, but still perpendicular.
            This also applies if the curvature is zero, e.g. the surface is a .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.MaxCurvatureDirection`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.MinCurvatureDirection`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Plane`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.MinCurvatureDirection`
    - **summary:** The direction of maximum curvature.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.MaxCurvatureDirection`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.GetTangent(SpaceClaim.Api.V22.Geometry.DirectionUV)`
    - **summary:** Gets the 3D tangent direction in the specified UV direction.
    - **param:** The UV direction in which the tangent is sought.
      - *@name:* `dir`
    - **returns:** The 3D tangent direction.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.ProjectDirection(SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Projects a 3D direction onto the surface to give a UV direction in the surface.
    - **param:** The 3D direction to project.
      - *@name:* `dir`
    - **returns:** The UV direction in the surface.
    - **remarks** If the 3D  is zero or parallel to the , a zero UV direction is returned.
      - **paramref**
        - *@name:* `dir`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SurfaceEvaluation.Normal`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Torus`
    - **summary:** A torus.
    - **remarks** Imagine a torus with its axis ( of its ) pointing North.
            
            The U parameter specifies the longitude, increasing clockwise (East) about the axis (right hand corkscrew law).
            It has a zero parameter at , and a period of 2*pi.
            
            The V parameter specifies the latitude, increasing North, with a zero parameter at the equator.
            For a donut, where the  is greater than the ,
            the range is [-pi, pi] and the parameterization is periodic.
            For a degenerate torus, the range is restricted accordingly and the parameterization is non-periodic.
            
            The  property can be used to obtain the parameterization in the U and V directions.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirZ`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Torus.Frame`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Torus.MajorRadius`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Torus.MinorRadius`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Surface.Parameterization`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Surface.Parameterization`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Torus.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Torus.Plane`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Torus.Axis`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve`
    - **typeparam:** The type of curve.
      - *@name:* `TCurve`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve`1.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve`
    - **summary:** The object implementing this interface has a shape represented by a trimmed curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedCurve`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedCurve`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedCurve`
    - **summary:** A trimmed curve, i.e. a curve with parametric bounds.
    - **remarks** Curves are unbounded in nature, e.g. a  is infinite, and a  is complete.
            A trimmed curve places parameter bounds on a the curve, e.g. a line segment or an arc, respectively.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Line`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Circle`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Projects a point to the trimmed curve, returning the evaluation at the closest point.
    - **param:** The point to project.
      - *@name:* `point`
    - **returns:** The evaluation at the closest point.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.Bounds`
    - **summary:** Gets the parametric bounds of the trimmed curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.Length`
    - **summary:** Gets the length of the trimmed curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.StartPoint`
    - **summary:** Gets the start point of the trimmed curve.
    - **remarks** The start point is equivalent to 
            and is not affected by the value of .
            
            For example,  implements .
             also has properties,  and ,
            which are in terms of the direction of the edge.
            If  is true, then the direction of the edge is opposite to the
            direction of the curve, so the  will be at the ,
            and the  will be at the .
      - **c:** Geometry.Evaluate(Bounds.Start).Point
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Edge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedCurve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Edge`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.EndPoint`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.StartPoint`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.EndPoint`
    - **summary:** Gets the end point of the trimmed curve.
    - **remarks** The end point is equivalent to 
            and is not affected by the value of .
            
            For example,  implements .
             also has properties,  and ,
            which are in terms of the direction of the edge.
            If  is true, then the direction of the edge is opposite to the
            direction of the curve, so the  will be at the ,
            and the  will be at the .
      - **c:** Geometry.Evaluate(Bounds.End).Point
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Edge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedCurve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Edge`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.EndPoint`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndVertex`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.StartPoint`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.IntersectCurve(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **summary:** Gets the intersections between this trimmed curve and another trimmed curve.
    - **param:** The other trimmed curve to intersect.
      - *@name:* `segment`
    - **returns:** Zero or more intersection points.
    - **remarks** For each intersection point,  is on this trimmed curve,
            and  is on the other trimmed curve.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IntPoint`2.EvaluationA`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IntPoint`2.EvaluationB`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.Offset(SpaceClaim.Api.V22.Geometry.Plane,System.Double)`
    - **summary:** Offsets the trimmed curve by a distance.
    - **param:** Plane in which to offset.
      - *@name:* `plane`
    - **param:** Distance to offset.
      - *@name:* `distance`
    - **returns:** Zero or more trimmed curves.
    - **remarks** The trimmed curve is offset so that no portion of the result is closer to the original than the offset distance.
            This may involve splitting and trimming such that more than one trimmed curve results.
            
            The offset direction is "to the right" of this trimmed curve, as seen looking down onto the plane.
            That is, the offset direction is:
            
            .
            
            The direction of the curve is used, so the offset direction is not affected by the value of .
      - **para**
      - **para**
      - **c** Direction.(, plane.DirZ)
        - **see**
          - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Direction.Cross(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
        - **i:** curve tangent direction
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.Offset(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam)`
    - **summary:** Offsets the trimmed curve so as to be tangent to a curve.
    - **param:** Plane in which to offset.
      - *@name:* `plane`
    - **param:** A point on a curve near the tangency position.
      - *@name:* `helpPoint`
    - **returns:** Zero or more trimmed curves.
    - **remarks** The offset direction and distance is determined by the condition that the trimmed curve should be tangent to
            the  curve near the help point specified.
            
            The trimmed curve is offset so that no portion of the result is closer to the original than the offset distance.
            This may involve splitting and trimming such that more than one trimmed curve results.
      - **paramref**
        - *@name:* `helpPoint`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.OffsetChain(SpaceClaim.Api.V22.Geometry.Plane,System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.OffsetCornerType)`
    - **summary:** Offsets a chain of trimmed curves by a distance.
    - **param:** Plane in which to offset.
      - *@name:* `plane`
    - **param:** Distance to offset.
      - *@name:* `distance`
    - **param:** Other trimmed curves in the chain.
      - *@name:* `others`
    - **param:** Type of external corners to produce.
      - *@name:* `cornerType`
    - **returns:** Zero or more trimmed curves.
    - **remarks** The chain of trimmed curves is offset so that no portion of the result is closer to the original than the offset distance.
            This may involve splitting and trimming of individual offset curves.
            
            The offset direction is "to the right" of this trimmed curve, as seen looking down onto the plane.
            That is, the offset direction is:
            
            .
            
            The direction of the curve is used, so the offset direction is not affected by the value of .
            
            If the trimmed curves do not form a single chain, an attempt is made to offset chains in a consistent direction.
            
            For external corners, the offset trimmed curves will not meet,
            and then  specifies how they should be connected.
      - **para**
      - **para**
      - **c** Direction.(, plane.DirZ)
        - **see**
          - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Direction.Cross(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
        - **i:** curve tangent direction
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.IShape.IsReversed`
      - **para**
      - **para**
      - **paramref**
        - *@name:* `cornerType`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.OffsetChain(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.OffsetCornerType)`
    - **summary:** Offsets a chain of trimmed curves.
    - **param:** Plane in which to offset.
      - *@name:* `plane`
    - **param:** A point on a curve near the tangency position.
      - *@name:* `helpPoint`
    - **param:** Other trimmed curves in the chain.
      - *@name:* `others`
    - **param:** Type of external corners to produce.
      - *@name:* `cornerType`
    - **returns:** Zero or more trimmed curves.
    - **remarks** The offset direction and distance is determined by the condition that the trimmed curve should be tangent to
            the  curve near the help point specified.
            
            The chain of trimmed curves is offset so that no portion of the result is closer to the original than the offset distance.
            This may involve splitting and trimming of individual offset curves.
            
            If the trimmed curves do not form a single chain, an attempt is made to offset chains in a consistent direction.
            
            For external corners, the offset trimmed curves will not meet,
            and then  specifies how they should be connected.
      - **paramref**
        - *@name:* `helpPoint`
      - **para**
      - **para**
      - **para**
      - **paramref**
        - *@name:* `cornerType`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.SelectFragment(System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **summary:** Selects a fragment of the trimmed curve.
    - **param:** Parameter identifying the fragment to select.
      - *@name:* `param`
    - **param:** Other trimmed curves which may intersect with this trimmed curve so as to fragment it.
      - *@name:* `cuts`
    - **returns** A results object describing the selected fragment; or  if no fragment results.
      - **b:** null
    - **exception:** Parameter is outside the bounds of the trimmed curve.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** The  are intersected with the trimmed curve to define fragments along it.
            The fragment containing the specified  is returned as ,
            and one or two remaining fragments are returned in .
            
            If there are no intersection points, then  is returned.
            Also, if one intersection point is produced, but the trimmed curve is periodic, then  is returned.
            
            If the selected fragment was cut at the , then  indicates
            the cut that produced this intersection.
            Similarly for  and .
      - **paramref**
        - *@name:* `cuts`
      - **paramref**
        - *@name:* `param`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.SelectedFragment`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.OtherFragments`
      - **para**
      - **b:** null
      - **b:** null
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.StartPoint`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.StartCut`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.EndPoint`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.EndCut`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.GetPolyline(SpaceClaim.Api.V22.Geometry.PolylineOptions)`
    - **summary:** Get a polyline approximation of the trimmed curve.
    - **param:** Polyline options.
      - *@name:* `options`
    - **returns:** A list of points describing the polyline.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.IsCoincident(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **summary:** Compares two trimmed curves to see if they are coincident.
    - **param:** Trimmed curve to compare to.
      - *@name:* `other`
    - **returns** if the trimmed curves are coincident; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.ProjectToPlane(SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Projects the trimmed curve to a plane.
    - **param:** Target plane
      - *@name:* `plane`
    - **returns:** The projected trimmed curve.
    - **remarks** If a line segment is projected to a plane, and the line is perpendicular to the plane,
            a trimmed  is returned.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PointCurve`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.SelectFragmentResult`
    - **summary** Describes the result of calling .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.SelectFragment(System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.SelectedFragment`
    - **summary:** The selected fragment.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.OtherFragments`
    - **summary:** One or two other fragments.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.StartCut`
    - **summary:** The start cut, if the start was trimmed.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.SelectFragmentResult.EndCut`
    - **summary:** The end cut, if the end was trimmed.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.OffsetCornerType`
    - **summary:** Specifies how to connect offset trimmed curves for external corners.
    - **remarks** See  for more information.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedCurve.OffsetChain(SpaceClaim.Api.V22.Geometry.Plane,System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.OffsetCornerType)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.OffsetCornerType.Round`
    - **summary:** The offset trimmed curves are connected by an arc centered at the original corner.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.OffsetCornerType.LinearExtension`
    - **summary:** The offset trimmed curves are connected by extending them with tangent straight lines.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.OffsetCornerType.NaturalExtension`
    - **summary** The offset trimmed curves are connected by extending the curves, if possible;
            otherwise  is used.
      - **see**
        - *@cref:* `F:SpaceClaim.Api.V22.Geometry.OffsetCornerType.Round`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedSpace`
    - **summary:** The object implementing this interface has a shape represented by a trimmed space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedSpace.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedSpace`
    - **summary:** A finite region of 3D space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedSpace.Volume`
    - **summary:** Gets the volume of the trimmed space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedSpace.SurfaceArea`
    - **summary:** Gets the surface area of the trimmed space.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedSpace.GetCollision(SpaceClaim.Api.V22.Geometry.ITrimmedSpace)`
    - **summary:** Gets the collision between this object and another.
    - **param:** The other object to test with.
      - *@name:* `other`
    - **returns:** The nature of the collision between the two objects.
    - **remarks** If the two objects intersect,  methods, such as
            , , or  could
            be used to discover details of the intersection.
            The 
            method can be used to that the original objects are not modified.
            
            If the two objects touch,  could
            be used to discover where the touching condition occurs.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Body`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Intersect(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body})`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Fuse(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body},System.Boolean,SpaceClaim.Api.V22.Modeler.Tracker)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Imprint(SpaceClaim.Api.V22.Modeler.Body)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Copy(System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Modeler.Face,SpaceClaim.Api.V22.Modeler.Face}@,System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Modeler.Edge,SpaceClaim.Api.V22.Modeler.Edge}@)`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedGeometry.GetClosestSeparation(SpaceClaim.Api.V22.Geometry.ITrimmedGeometry)`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Collision`
    - **summary:** Describes the nature of a collision between two objects.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Collision.None`
    - **summary:** The objects do not collide.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Collision.Touch`
    - **summary:** The objects touch.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Geometry.Collision.Intersect`
    - **summary:** The objects intersect.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedSurface`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedSurface`
    - **typeparam:** The type of surface.
      - *@name:* `TSurface`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedSurface`1.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedSurface`
    - **summary:** The object implementing this interface has a shape represented by a trimmed surface.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasTrimmedSurface.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedSurface`1`
    - **inheritdoc**
      - *@cref:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedSurface`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasArea.Area`
    - **summary:** Gets the surface area.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasArea.Perimeter`
    - **summary:** Gets the length of the perimeter.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.ITrimmedSurface`
    - **summary:** A trimmed surface, i.e. a surface with a boundary.
    - **remarks** Surfaces are unbounded in nature, e.g. a  is infinite.
            A trimmed surface is a surface with a boundary.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Plane`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedSurface.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Projects a point to the trimmed surface, returning the evaluation at the closest point.
    - **param:** The point to project.
      - *@name:* `point`
    - **returns:** The evaluation at the closest point.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.ITrimmedSurface.BoxUV`
    - **summary:** Gets the UV bounding box of the trimmed surface.
    - **remarks:** The UV box is not guaranteed to fit tightly around the object, although it often does.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedSurface.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Gets whether the given UV parameter is within or on the boundary of the trimmed surface.
    - **param**
      - *@name:* `param`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.ITrimmedSurface.IntersectCurve(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **summary:** Gets the intersections between the trimmed surface and a curve segment.
    - **param:** The curve segment to intersect.
      - *@name:* `segment`
    - **returns:** Zero or more intersection points.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Vector`
    - **summary:** A 3D displacement vector.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Vector.Direction`
    - **summary:** Gets the direction of the vector.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Vector.Magnitude`
    - **summary:** Gets the magnitude of the vector.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Vector.Project(SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Projects the vector to give the component in the specified direction.
    - **param:** The direction in which to project.
      - *@name:* `dir`
    - **returns:** The projected vector.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Matrix`
    - **summary:** A transformation matrix.
            Matrices are pre-multiplication, as in:  x' = M*x.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.CreateTranslation(SpaceClaim.Api.V22.Geometry.Vector)`
    - **summary** Creates a translation matrix from the specified .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Vector`
    - **param:** The translation.
      - *@name:* `translation`
    - **returns:** The translation matrix.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.CreateScale(System.Double,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a scaling matrix from the specified origin and scale factor.
    - **param:** The scale factor, which must be positive.
      - *@name:* `scale`
    - **param:** The origin about which to scale.
      - *@name:* `point`
    - **returns:** The scaling matrix.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.CreateScale(System.Double)`
    - **summary:** Creates a scaling matrix about the origin.
    - **param:** The scale factor, which must be positive.
      - *@name:* `scale`
    - **returns:** The scaling matrix.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.CreateRotation(SpaceClaim.Api.V22.Geometry.Line,System.Double)`
    - **summary:** Creates a rotation matrix through an angle about an axis.
    - **param:** The axis of rotation.
      - *@name:* `axis`
    - **param:** The angle of rotation, measured clockwise about the direction of the axis.
      - *@name:* `angle`
    - **returns:** The rotation matrix.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.CreateMapping(SpaceClaim.Api.V22.Geometry.Frame)`
    - **summary:** Creates a matrix representing a transformation to the specified coordinate system.
    - **remarks** A  represents a coordinate system (origin and axes).
            This method creates a transformation to that coordinate system.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Frame`
    - **param:** The frame of the coordinate system.
      - *@name:* `frame`
    - **returns:** The transformation matrix.
    - **exception:** The directions are not perpendicular.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.IsIdentity`
    - **summary:** Gets whether the matrix is the identity matrix.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.HasTranslation`
    - **summary:** Gets whether the matrix has a translation component.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.HasScale`
    - **summary:** Gets whether the matrix has a scale component.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.HasRotation`
    - **summary:** Gets whether the matrix has a rotation component.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Translation`
    - **summary:** Gets the translation component of the matrix.
    - **remarks** A matrix can be decomposed into its , , and  components,
            such that:
            
            The translation component depends on the order of composition, whereas the scale and rotation components do not.
            For decompositions with different orders, see the 6 overloads of .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Translation`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Scale`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Rotation`
      - **code:** this == Translation * Scale * Rotation
        - *@lang:* `C#`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Geometry.Matrix.Decompose(SpaceClaim.Api.V22.Geometry.Vector@,System.Double@,SpaceClaim.Api.V22.Geometry.Matrix@)`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Scale`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Rotation`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Scale`
    - **summary:** Gets the scale component of the matrix.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Translation`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Translation`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Rotation`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Rotation`
    - **summary:** Gets the rotation component of the matrix.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Translation`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Translation`
    - **seealso**
      - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Scale`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.IsMirror`
    - **summary:** Gets whether the matrix is mirrored.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.Decompose(SpaceClaim.Api.V22.Geometry.Vector@,System.Double@,SpaceClaim.Api.V22.Geometry.Matrix@)`
    - **overloads**
      - **summary:** Decomposes the matrix into its translation, scale, and rotation components.
    - **summary:** Decomposes the matrix into its translation, scale, and rotation components.
    - **param:** The translation component.
      - *@name:* `translation`
    - **param:** The scale component.
      - *@name:* `scale`
    - **param:** The rotation component.
      - *@name:* `rotation`
    - **remarks** The matrix (M) is decomposed into its translation (T), scale (S), and rotation (R) components,
            such that , or more precisely:
      - **c:** M = T * S * R
      - **code:** this == CreateTranslation(translation) * CreateScale(scale) * rotation
        - *@lang:* `C#`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.Decompose(System.Double@,SpaceClaim.Api.V22.Geometry.Vector@,SpaceClaim.Api.V22.Geometry.Matrix@)`
    - **summary:** Decomposes the matrix into its translation, scale, and rotation components.
    - **param:** The scale component.
      - *@name:* `scale`
    - **param:** The translation component.
      - *@name:* `translation`
    - **param:** The rotation component.
      - *@name:* `rotation`
    - **remarks** The matrix (M) is decomposed into its translation (T), scale (S), and rotation (R) components,
            such that , or more precisely:
      - **c:** M = S * T * R
      - **code:** this == CreateScale(scale) * CreateTranslation(translation) * rotation
        - *@lang:* `C#`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.Decompose(SpaceClaim.Api.V22.Geometry.Matrix@,SpaceClaim.Api.V22.Geometry.Vector@,System.Double@)`
    - **summary:** Decomposes the matrix into its translation, scale, and rotation components.
    - **param:** The rotation component.
      - *@name:* `rotation`
    - **param:** The translation component.
      - *@name:* `translation`
    - **param:** The scale component.
      - *@name:* `scale`
    - **remarks** The matrix (M) is decomposed into its translation (T), scale (S), and rotation (R) components,
            such that , or more precisely:
      - **c:** M = R * T * S
      - **code:** this == rotation * CreateTranslation(translation) * CreateScale(scale)
        - *@lang:* `C#`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.Decompose(System.Double@,SpaceClaim.Api.V22.Geometry.Matrix@,SpaceClaim.Api.V22.Geometry.Vector@)`
    - **summary:** Decomposes the matrix into its translation, scale, and rotation components.
    - **param:** The scale component.
      - *@name:* `scale`
    - **param:** The rotation component.
      - *@name:* `rotation`
    - **param:** The translation component.
      - *@name:* `translation`
    - **remarks** The matrix (M) is decomposed into its translation (T), scale (S), and rotation (R) components,
            such that , or more precisely:
      - **c:** M = S * R * T
      - **code:** this == CreateScale(scale) * rotation * CreateTranslation(translation)
        - *@lang:* `C#`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.Decompose(SpaceClaim.Api.V22.Geometry.Vector@,SpaceClaim.Api.V22.Geometry.Matrix@,System.Double@)`
    - **summary:** Decomposes the matrix into its translation, scale, and rotation components.
    - **param:** The translation component.
      - *@name:* `translation`
    - **param:** The rotation component.
      - *@name:* `rotation`
    - **param:** The scale component.
      - *@name:* `scale`
    - **remarks** The matrix (M) is decomposed into its translation (T), scale (S), and rotation (R) components,
            such that , or more precisely:
      - **c:** M = T * R * S
      - **code:** this == CreateTranslation(translation) * rotation * CreateScale(scale))
        - *@lang:* `C#`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.Decompose(SpaceClaim.Api.V22.Geometry.Matrix@,System.Double@,SpaceClaim.Api.V22.Geometry.Vector@)`
    - **summary:** Decomposes the matrix into its translation, scale, and rotation components.
    - **param:** The rotation component.
      - *@name:* `rotation`
    - **param:** The scale component.
      - *@name:* `scale`
    - **param:** The translation component.
      - *@name:* `translation`
    - **remarks** The matrix (M) is decomposed into its translation (T), scale (S), and rotation (R) components,
            such that , or more precisely:
      - **c:** M = R * S * T
      - **code:** this == rotation * CreateScale(scale) * CreateTranslation(translation))
        - *@lang:* `C#`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Item(System.Int32,System.Int32)`
    - **summary:** Gets the elements of the matrix as a 4x4 array.
    - **exception:** Index must be in the range [0:3].
      - *@cref:* `T:System.IndexOutOfRangeException`
    - **remarks** The matrix is a pre-multiplication transform.
            
            The rotation is in m[0:2,0:2] and contains no scaling in its leading diagonal.
            
            The translation is (m[0,3]/m[3,3], m[1,3]/m[3,3], m[2,3]/m[3,3]).
            
            The uniform scale is 1/m[3,3].
      - **para**
      - **para**
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Matrix.Inverse`
    - **summary:** Gets the inverse transformation.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.TryGetRotation(SpaceClaim.Api.V22.Geometry.Line@,System.Double@)`
    - **summary:** Convert a matrix into the equivalent rotation about an axis.
    - **param:** Axis of rotation.
      - *@name:* `axis`
    - **param** Angle of rotation in the range .
      - *@name:* `angle`
      - **i:** 0 <= angle <= 2*pi
    - **returns:** Success flag.
    - **remarks:** Returns false if the matrix does not have a rotation component.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Matrix)`
    - **summary:** Multiplies two matrices.
    - **param:** The first matrix.
      - *@name:* `matrixA`
    - **param:** The second matrix.
      - *@name:* `matrixB`
    - **returns:** The resulting matrix.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Frame)`
    - **summary** Transforms a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Frame`
    - **param:** The transformation to apply.
      - *@name:* `matrix`
    - **param:** The frame to be transformed.
      - *@name:* `frame`
    - **returns:** The transformed frame.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Box)`
    - **summary** Transforms a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Box`
    - **param:** The transformation to apply.
      - *@name:* `matrix`
    - **param:** The box to be transformed.
      - *@name:* `box`
    - **returns:** The transformed box.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary** Transforms a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Point`
    - **param:** The transformation to apply.
      - *@name:* `matrix`
    - **param:** The point to be transformed.
      - *@name:* `point`
    - **returns:** The transformed point.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Vector)`
    - **summary** Transforms a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Vector`
    - **param:** The transformation to apply.
      - *@name:* `matrix`
    - **param:** The vector to be transformed.
      - *@name:* `vec`
    - **returns:** The transformed vector.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary** Transforms a .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Direction`
    - **param:** The transformation to apply.
      - *@name:* `matrix`
    - **param:** The direction to be transformed.
      - *@name:* `dir`
    - **returns:** The transformed direction.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Geometry.Matrix.op_Multiply(SpaceClaim.Api.V22.Geometry.Matrix,System.Double)`
    - **summary:** Transforms a length by applying the scale factor of the matrix.
    - **param:** The transformation to apply.
      - *@name:* `matrix`
    - **param:** The length to be transformed.
      - *@name:* `length`
    - **returns:** The transformed length.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.IHasPlane.Plane`
    - **summary:** Gets the plane of the object.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Geometry.Point`
    - **summary:** A 3D position.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Geometry.Point.Vector`
    - **summary:** Gets the vector from the origin to this point.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.CurveMethods.FindCurveParamsAtLengths(SpaceClaim.Api.V22.Geometry.Curve,System.Double,System.Collections.Generic.ICollection{System.Double})`
    - **summary**
    - **param**
      - *@name:* `iCurve`
    - **param**
      - *@name:* `iStartParam`
    - **param**
      - *@name:* `iLength`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.BodyMethods.ProjectPlanarLines(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Direction,System.Double,SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Projects a set of coplanar curves onto a body.
    - **param:** Faces on the body to project onto.
      - *@name:* `targetFaces`
    - **param:** Curves to project.
      - *@name:* `trimmedCurves`
    - **param:** Direction vector of the projection
      - *@name:* `dir`
    - **param:** Distance parameter
      - *@name:* `distance`
    - **param:** Optional hint plane that contains the curves to project.
      - *@name:* `plane`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.BodyMethods.ProjectPlanarLines(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Projects a set of coplanar curves onto a body.
    - **param:** Faces on the body to project onto.
      - *@name:* `targetFaces`
    - **param:** Curves to project.
      - *@name:* `trimmedCurves`
    - **param:** Direction vector of the projection
      - *@name:* `dir`
    - **param:** Optional hint plane that contains the curves to project.
      - *@name:* `plane`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.BoundaryCondition.Create(SpaceClaim.Api.V22.Unsupported.Live.Solution,SpaceClaim.Api.V22.IDocObject,SpaceClaim.Api.V22.Unsupported.Live.BoundaryConditionType,SpaceClaim.Api.V22.Geometry.Vector)`
    - **summary:** Creates a vector boundary condition at a single location.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.BoundaryCondition.Create(SpaceClaim.Api.V22.Unsupported.Live.Solution,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject},SpaceClaim.Api.V22.Unsupported.Live.BoundaryConditionType,SpaceClaim.Api.V22.Geometry.Vector)`
    - **summary:** Creates a vector boundary condition at a collection of locations.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Calculator.CreatePointCalculator(SpaceClaim.Api.V22.Unsupported.Live.Solution,System.String,SpaceClaim.Api.V22.Unsupported.Live.ResultType,SpaceClaim.Api.V22.Unsupported.Live.IntegrantType,SpaceClaim.Api.V22.Unsupported.Live.ComponentType,System.Numerics.Vector3,SpaceClaim.Api.V22.Unsupported.Live.DiscreteOperatorType,SpaceClaim.Api.V22.Unsupported.Live.StatisticalOperatorType,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDisplayType,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.IDocObject)`
    - **summary:** Creates a custom point calculator at a single location.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Calculator.CreatePointCalculator(SpaceClaim.Api.V22.Unsupported.Live.Solution,System.String,SpaceClaim.Api.V22.Unsupported.Live.ResultType,SpaceClaim.Api.V22.Unsupported.Live.IntegrantType,SpaceClaim.Api.V22.Unsupported.Live.ComponentType,System.Numerics.Vector3,SpaceClaim.Api.V22.Unsupported.Live.DiscreteOperatorType,SpaceClaim.Api.V22.Unsupported.Live.StatisticalOperatorType,SpaceClaim.Api.V22.Unsupported.Live.CalculatorDisplayType,SpaceClaim.Api.V22.Geometry.Point,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary:** Creates a custom point calculator at a collection of locations.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Unsupported.Live.Calculator.PointLocation`
    - **summary:** Gets the calculator's point location.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Streamlines.SetLocation(SpaceClaim.Api.V22.Geometry.Frame)`
    - **summary:** Sets the location of the elliptical seeding region for the active streamlines.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Live.Streamlines.SetSize(SpaceClaim.Api.V22.Geometry.BoxUV)`
    - **summary:** Sets the size of the elliptical seeding region for the active streamlines.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.RuledCutting.FaceMethods.GetTightUVBox(SpaceClaim.Api.V22.Modeler.Face,System.Collections.Generic.IEnumerable{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Boolean)`
    - **summary:** samples the outer edges of a face to calculate a tight UV box.
            face.Shape.BoxUV was giving loose, slightly oversized boxes in some cases,
            this is the workaround
    - **param**
      - *@name:* `face`
    - **param**
      - *@name:* `edges`
    - **param**
      - *@name:* `align`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.RuledCutting.FaceMethods.Align(SpaceClaim.Api.V22.Geometry.BoxUV,SpaceClaim.Api.V22.Modeler.Face,System.Boolean)`
    - **summary:** aligns a uv range box to an existing face,
            such that they have the same direction, and unruled dimensions
    - **param:** the bounds
      - *@name:* `box`
    - **param:** the face to align the bounds to
      - *@name:* `face`
    - **param:** option to force the unruled dimension to a full period
      - *@name:* `forcePeriodic`
    - **returns**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Unsupported.RuledCutting.OrderingEngine.Contour.StartPoint`
    - **summary:** The starting point (leading point) of a cut or scribe

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Unsupported.RuledCutting.OrderingEngine.Contour.EndPoint`
    - **summary:** The ending point (leadout point) of a cut or a scribe.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.RuledCutting.OrderingEngine.Contour.OverrideStartPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Moves the starting point (leadin point) of a cut. Only works for a closed contour.
    - **param**
      - *@name:* `point`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Unsupported.PenStroke.Points`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.PenStroke.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.PenStroke.Scale(SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.UIDimensionGeometry.CoincidentWith(SpaceClaim.Api.V22.Unsupported.UIDimensionGeometry)`
    - **summary:** True if the solution sets of the two geometries match, but are not necessarily identical.
    - **param**
      - *@name:* `other`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.UIDimensionGeometry.GetStartPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** The point relative to which this geometry is measuring.
    - **param**
      - *@name:* `targetPoint`
    - **returns**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DatumPoint`
    - **summary:** A datum point master.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPoint.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a datum point.
    - **param:** Parent part.
      - *@name:* `parent`
    - **param:** Name for the datum point.
      - *@name:* `name`
    - **param:** Location of the datum point.
      - *@name:* `point`
    - **returns:** The new datum point.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPoint.Create(SpaceClaim.Api.V22.IPart,System.String,SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DatumPoint.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Geometry.Point)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDatumPoint.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.Position`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.Pinned`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.Determinants`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPoint.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.Layer`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.DefaultVisibility`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPoint.GetVisibility(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPoint.SetVisibility(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Boolean})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPoint.IsVisible(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.Name`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.CanSuppress`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPoint.IsSuppressed`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.IDatumPoint`
    - **summary:** A datum point.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDatumPoint.Parent`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDatumPoint.Position`
    - **summary:** Gets the position.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDatumPoint.Pinned`
    - **summary:** Gets whether the datum point is pinned.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDatumPoint.Determinants`
    - **summary:** Gets the objects that determine the point.
    - **remarks:** If the point does not have determinants, then an empty collection is returned.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Hole.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.HoleCreationInfo)`
    - **summary:** Creates a hole on the specified face at the specified location using the defined creation properties.
    - **param:** The face on which the hole is to be created.
      - *@name:* `referenceFace`
    - **param:** The position of the hole on the face.
      - *@name:* `point`
    - **param:** A HoleCreationInfo structure that contains additional properties for creating the hole.
      - *@name:* `creationInfo`
    - **returns:** The newly created hole.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Hole.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.HoleCreationInfo)`
    - **summary:** Creates a hole on the specified face at the specified location using the defined creation properties.
    - **param:** The face on which the hole is to be created.
      - *@name:* `referenceFace`
    - **param:** The UV position of the hole on the face.
      - *@name:* `point`
    - **param:** A HoleCreationInfo structure that contains additional properties for creating the hole.
      - *@name:* `creationInfo`
    - **returns**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.AlternateReferenceFrame`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.AlternateReferenceFrame`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.Direction`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.Direction`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.DrillPointAngle`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.DrillPointAngle`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Hole.Point`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IHole.Point`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IHole.AlternateReferenceFrame`
    - **summary** Gets or sets the alternate (off-face) reference frame for the hole. Can be .
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IHole.Direction`
    - **summary:** Gets the direction of the hole axis.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IHole.DrillPointAngle`
    - **summary:** Gets the angle of the drill point.
    - **remarks** Can be .
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IHole.Point`
    - **summary:** Gets the center point of the hole on the face.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.CurvePoint`
    - **summary:** A curve point master.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CurvePoint.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.ICurvePoint.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CurvePoint.Position`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CurvePoint.ExportIdentifier`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.ICurvePoint`
    - **summary:** A curve point.
    - **remarks** A curve point is an implicit doc object, which means you cannot create or delete one. 
            Its parent is a  and the curve point represents an endpoint of that curve. If the parent is deleted, 
            the curve point will report that  is .
            
            The parent may be a , , or .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.IHasTrimmedCurve`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.IDeletable.IsDeleted`
      - **b:** true
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IDesignEdge`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IDesignCurve`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IBeam`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ICurvePoint.Parent`
    - **summary:** Gets the parent design edge.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ICurvePoint.Position`
    - **summary:** Gets the position.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.HoleCreationInfo.DrillPointAngle`
    - **summary** Specifies the drill point at the bottom of a blind hole. It will only apply if not  and  is specified.
      - **b:** null
      - **see**
        - *@cref:* `F:SpaceClaim.Api.V22.HoleCreationInfo.HoleDepth`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Display.PointPrimitive`
    - **summary:** A point primitive.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Display.PointPrimitive.Create(SpaceClaim.Api.V22.Geometry.Point,System.Single)`
    - **summary:** Creates a point primitive.
    - **param:** The location.
      - *@name:* `point`
    - **param:** The circle radius, in pixels.
      - *@name:* `radius`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Display.Polygon.#ctor(SpaceClaim.Api.V22.Geometry.Direction,System.Collections.Generic.IList{System.Int32})`
    - **summary:** Constructs a mesh polygon.
    - **param:** The normal of the planar polygon.
      - *@name:* `normal`
    - **param:** Vertices of the polygon.
      - *@name:* `vertices`
    - **remarks** The polygon is described by its , which are 
            indices in the vertex list of the mesh, as supplied to
            .
            The vertices should be clockwise about the  of the plane
            (counter-clockwise as seen looking down onto the plane).
      - **paramref**
        - *@name:* `vertices`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Display.MeshPrimitive.CreatePolygons(System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Display.Polygon})`
      - **paramref**
        - *@name:* `normal`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Display.Polygon.#ctor(SpaceClaim.Api.V22.Geometry.Direction,System.Int32[])`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Display.Polygon.#ctor(SpaceClaim.Api.V22.Geometry.Direction,System.Collections.Generic.IList{System.Int32})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Display.PolypointPrimitive.Create(System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Single)`
    - **summary:** Creates a polypoint primitive
    - **param:** The locations of the points.
      - *@name:* `points`
    - **param:** The circle radius, in pixels.
      - *@name:* `radius`
    - **returns**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Display.CurvePrimitive`
    - **summary:** A trimmed curve primitive.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Display.Graphic.Create(SpaceClaim.Api.V22.Display.GraphicStyle,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Display.Primitive},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Display.Graphic},SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Display.MeshEdgeDisplay)`
    - **summary:** Creates a graphic with some primitives, nested graphics, and a transform.
    - **param** Graphic style, or .
      - *@name:* `style`
      - **b:** null
    - **param** Primitives to display, or .
      - *@name:* `primitives`
      - **b:** null
    - **param** Nested graphics, or .
      - *@name:* `graphics`
      - **b:** null
    - **param:** The transform to be applied.
      - *@name:* `transform`
    - **param:** Options for mesh edge display.
      - *@name:* `edgeDisplay`
    - **returns:** A graphic.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.MeshColorMap.#ctor(System.Drawing.Bitmap,System.Drawing.Color,System.Collections.Generic.IDictionary{System.Int32,SpaceClaim.Api.V22.Geometry.PointUV})`
    - **summary:** Constructs a color map for a mesh.
    - **param:** A bitmap describing the color map.
      - *@name:* `colorMap`
    - **param:** The default color.
      - *@name:* `defaultColor`
    - **param:** Parameters for mesh vertices.
      - *@name:* `vertexParams`
    - **remarks** Each entry in  is a vertex id and a UV parameter to be assigned to that vertex.
            U and V should be in the range [0, 1].
            Values outside this range are clamped to the range.
            
            The U value is the proportion of the width of the color map, so U=0 is the first column, and U=1 is the last column.
            
            Similarly the V value is the proportion of the height of the color map, so V=0 is the first row, and V=1 is the last row.
            
            Mesh facets involving vertices that not listed in  will be shown in the .
      - **paramref**
        - *@name:* `vertexParams`
      - **para**
      - **para**
      - **para**
      - **paramref**
        - *@name:* `vertexParams`
      - **paramref**
        - *@name:* `defaultColor`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper.TryGetTransformFrame(SpaceClaim.Api.V22.Geometry.Frame@,SpaceClaim.Api.V22.Geometry.Transformations@)`
    - **summary:** Gets the transform frame for the lightweight custom object.
    - **param:** The transform frame.
      - *@name:* `frame`
    - **param:** Allowable transformations.
      - *@name:* `transformations`
    - **returns** if the custom object has a transform frame; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** Override this method to allow the custom object to be used with the Move tool.
            The position and orientation of the transform frame is used for the Move tool handles.
            
             is a bit field that specifies which transformations are suitable for this object.
            This is a hint to the Move tool for which handles to display.
            If multiple objects are selected, each object may offer different transformations,
            and in this case, the union of Move tool handles is presented.
            This means  can be called with a transformation that may be unsuitable for this object.
            You can skip such a transform, or adjust it to make it suitable.
      - **para**
      - **paramref**
        - *@name:* `transformations`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper.Transform(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper.Transform(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **summary:** Transforms the lightweight custom object.
    - **param:** The transformation to apply.
      - *@name:* `trans`
    - **param:** A flag indicating whether this is the final transform.
      - *@name:* `final`
    - **remarks** Override this method if the custom object supports being transformed. The default implementation does nothing.
            
            This method is used by the Move tool.
            
            The changes are not subject to undo/redo.
      - **para**
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper.TryGetTransformPath(SpaceClaim.Api.V22.Geometry.ITrimmedCurve@)`
    - **summary:** Returns a reference path for transformation of other objects
    - **param**
      - *@name:* `trimmedCurve`
    - **returns**
    - **remarks:** This is used for the Move Tool 'Move Direction', 'Move Along Trajectory', and 'Orient to Object' operations

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper.TryGetTransformTargetPoint(SpaceClaim.Api.V22.Geometry.Point@)`
    - **summary:** Returns a target point for transformation of other objects
    - **param**
      - *@name:* `point`
    - **returns**
    - **remarks:** This is used for the Move Tool 'Up To' operation

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper.TryGetMeasurementReference(SpaceClaim.Api.V22.Geometry.ITrimmedCurve@)`
    - **summary:** Returns a reference for measurements.
    - **param**
      - *@name:* `trimmedCurve`
    - **returns**
    - **remarks:** Returning true will override the default behavior of extracting the geometry from the rendering.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WorkbenchImportOptions.WorkPoints`
    - **summary** Gets or sets Workbench preference to import Workpoints (default = ).
      - **b:** false
    - **exclude**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.WrapCurves`
    - **summary:** Gets whether curves are wrapped around the body.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.ExtendCurves`
    - **summary:** Gets whether curves are extended to the edges of faces.
    - **remarks** This option has no effect if  is set to .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.WrapCurves`
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Mesh.GetCollision(SpaceClaim.Api.V22.Geometry.ITrimmedSpace)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Mesh.GetClosestSeparation(SpaceClaim.Api.V22.Geometry.ITrimmedGeometry)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Mesh.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Mesh.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Mesh.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Mesh.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Mesh.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.MeshEdge.Direction`
    - **summary:** Gets the direction of the edge.
    - **remarks:** The direction is from the start vertex to the end vertex.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.EdgeRendering.#ctor(System.Boolean,SpaceClaim.Api.V22.Geometry.Interval)`
    - **summary:** Constructs an edge rendering.
    - **param:** Whether the edge segment is hidden.
      - *@name:* `hidden`
    - **param:** The interval of the edge segment.
      - *@name:* `interval`
    - **remarks** The  is in terms of the curve of the original edge.
      - **paramref**
        - *@name:* `interval`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.FaceRendering.#ctor(System.Boolean,SpaceClaim.Api.V22.Geometry.ITrimmedCurve,SpaceClaim.Api.V22.Geometry.Point[])`
    - **summary:** Constructs a face rendering.
    - **param:** Whether the silhouette segment is hidden.
      - *@name:* `hidden`
    - **param:** The silhouette segment.
      - *@name:* `segment`
    - **param:** The silhouette polyline.
      - *@name:* `polyline`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.TransformedBody.#ctor(SpaceClaim.Api.V22.Modeler.Body,SpaceClaim.Api.V22.Geometry.Matrix)`
    - **summary:** Constructs a transformed body.
    - **param:** A body.
      - *@name:* `body`
    - **param:** A transform.
      - *@name:* `transform`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.ImprintCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face})`
    - **summary:** Imprints curves onto the body to create edges.
    - **param:** Trimmed curves to imprint.
      - *@name:* `segments`
    - **param** Faces to imprint on; else  to use all faces in the body.
      - *@name:* `faces`
      - **b:** null
    - **returns:** Edges created, and the segment that was imprinted to create them.
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.GetImprintedCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetImprintedCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face})`
    - **summary:** Gets imprinted curves, without modifying the body.
    - **param:** Trimmed curves to imprint.
      - *@name:* `segments`
    - **param** Faces to imprint on; else  to use all faces in the body.
      - *@name:* `faces`
      - **b:** null
    - **returns:** Imprinted curves.
    - **remarks** This method is similar to , only it does not modify the body.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.ImprintCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CreatePlanarBody(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **summary:** Creates a planar body from a profile.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** A collection of trimmed curves describing the boundary of the profile.
      - *@name:* `profile`
    - **returns:** The created body.
    - **remarks** The  must be a closed loop of trimmed curves.
            There can be inner loops, which will give rise to holes.
            The trimmed curves can be listed in any order.
            
            An exception will be thrown if the resulting body is non-manifold.
      - **paramref**
        - *@name:* `profile`
      - **br**
    - **exception:** Invalid profile.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CreatePlanarBody(SpaceClaim.Api.V22.Geometry.Plane,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Boolean,System.Boolean,System.Boolean,System.Collections.Generic.IDictionary{SpaceClaim.Api.V22.Geometry.ITrimmedCurve,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Edge}}@)`
    - **summary:** Creates a planar body from a profile.
    - **param:** The plane of the profile.
      - *@name:* `plane`
    - **param:** A collection of trimmed curves describing the boundary of the profile.
      - *@name:* `profile`
    - **param** to allow creation of a non-manifold body; otherwise .
      - *@name:* `allowNonManifold`
      - **b:** true
      - **b:** false
    - **param** to remove internal edges; otherwise .
      - *@name:* `mergeTopology`
      - **b:** true
      - **b:** false
    - **param** to remove inner regions; otherwise .
      - *@name:* `removeInnerRegions`
      - **b:** true
      - **b:** false
    - **param:** A dictionary of curves to edges in the new body.
      - *@name:* `curvesToEdges`
    - **returns:** The created body.
    - **remarks** The  must be a closed loop of trimmed curves.
            There can be inner loops, which will give rise to holes.
            The trimmed curves can be listed in any order.
      - **paramref**
        - *@name:* `profile`
    - **exception:** Invalid profile.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CreateSurfaceBody(SpaceClaim.Api.V22.Geometry.Surface,SpaceClaim.Api.V22.Geometry.BoxUV)`
    - **summary:** Creates a body from a region of a surface.
    - **param:** The surface.
      - *@name:* `surface`
    - **param:** The region of the surface.
      - *@name:* `region`
    - **returns:** A body of one face.
    - **remarks** If the surface  is bounded
            (e.g. a , a , or a )
            an  region can be supplied to use the entire surface;
            otherwise (e.g. a , a , or a ),
            an explicit region must be supplied.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Surface.Parameterization`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Sphere`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Torus`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.NurbsSurface`
      - **see**
        - *@cref:* `F:SpaceClaim.Api.V22.Geometry.BoxUV.Empty`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Plane`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Cylinder`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Cone`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.CreateWireBody(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **summary:** Creates a wire body of one edge.
    - **param:** The shape of the edge.
      - *@name:* `segment`
    - **returns:** A wire body of one edge.
    - **remarks** This method creates a wire body containing a single edge.
            Wire bodies with more than one edge can be created using .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.Fuse(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Body},System.Boolean,SpaceClaim.Api.V22.Modeler.Tracker)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.TaperFaces(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.Face},SpaceClaim.Api.V22.Geometry.Plane,System.Double)`
    - **summary:** Tapers a collection of faces.
    - **param:** The faces to taper.
      - *@name:* `faces`
    - **param:** The neutral plane.
      - *@name:* `neutralPlane`
    - **param:** The taper angle in radians.
      - *@name:* `taperAngle`
    - **exception:** Taper angle must be in the range [-pi/2, pi/2].
      - *@cref:* `T:System.ArgumentException`
    - **remarks:** A positive taper angle tapers inwards in the direction of the plane normal.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.ExtrudeProfile(SpaceClaim.Api.V22.Geometry.Profile,System.Double)`
    - **summary:** Creates a body by extruding a planar profile.
    - **param:** The profile to extrude.
      - *@name:* `profile`
    - **param:** The distance to extrude.
      - *@name:* `distance`
    - **returns:** The created body.
    - **remarks** The resulting body is capped with a planar face at the start and end.
            
            The  must be a closed loop of trimmed curves.
            There can be inner loops, which will give rise to holes.
            The trimmed curves can be listed in any order.
      - **para**
      - **paramref**
        - *@name:* `profile`
    - **exception:** Invalid profile.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.SweepProfile(SpaceClaim.Api.V22.Geometry.Profile,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **summary:** Creates a body by sweeping a planar profile along a path.
    - **param:** The profile to sweep.
      - *@name:* `profile`
    - **param:** A sweep path.
      - *@name:* `path`
    - **returns:** The created body.
    - **remarks** If the path is open, the resulting body is capped with a planar face at the start and end.
            
            The  must be a closed loop of trimmed curves.
            There can be inner loops, which will give rise to holes.
            The trimmed curves can be listed in any order.
            
            The  must be listed in order as a chain.
      - **para**
      - **paramref**
        - *@name:* `profile`
      - **para**
      - **paramref**
        - *@name:* `path`
    - **exception:** Invalid profile.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The path is invalid, or it is unsuitable for the profile.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.SweepChain(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **summary:** Creates a body by sweeping a chain of curves along a path.
    - **param:** A chain of trimmed curves.
      - *@name:* `chain`
    - **param:** A sweep path.
      - *@name:* `path`
    - **returns:** The created body.
    - **remarks** Both  and  must be listed in order as a chain.
            
            The  to be swept can be open or closed, and need not be planar.
      - **paramref**
        - *@name:* `chain`
      - **paramref**
        - *@name:* `path`
      - **para**
      - **paramref**
        - *@name:* `chain`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.LoftProfiles(System.Collections.Generic.IList{System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve}},System.Boolean,System.Boolean)`
    - **summary:** Creates a body by lofting between profiles.
    - **param:** A list of profiles to loft through.
      - *@name:* `profiles`
    - **param:** Whether the loft should be periodic.
      - *@name:* `periodic`
    - **param:** Whether ruled surfaces should be produced.
      - *@name:* `ruled`
    - **returns:** The created body.
    - **remarks** Surfaces produced have a U parameter in the direction of the profile curves,
            and a V parameter in the direction of lofting.
            
            Profiles can have different numbers of segments.
            A minimum twist solution is produced.
            
            Profiles should be all closed or all open.
            Closed profiles cannot contain inner loops.
            If closed profiles are supplied, a closed (solid) body is produced, if possible;
            otherwise an open (sheet) body is produced.
            
            The  argument applies when the profiles are closed.
            It is ignored if the profiles are open.
            
            
            If  is , separate ruled surfaces are produced between each pair of profiles.
            If  is , the loft continues from the last profile back to the first profile,
            but the surfaces are not periodic.
      - **para**
      - **para**
      - **para**
      - **paramref**
        - *@name:* `periodic`
      - **list**
        - *@type:* `bullet`
        - **item** If  is , at least three profiles must be supplied.
            		The loft continues from the last profile back to the first profile to produce surfaces that are periodic in V.
          - **paramref**
            - *@name:* `periodic`
          - **b:** true
        - **item** If  is , at least two profiles must be supplied.
            		If the first and last profiles are planar, end capping faces are created;
            		otherwise an open (sheet) body is produced.
          - **paramref**
            - *@name:* `periodic`
          - **b:** false
      - **para**
      - **paramref**
        - *@name:* `ruled`
      - **b:** true
      - **paramref**
        - *@name:* `periodic`
      - **b:** true
    - **exception:** Insufficient number of profiles supplied.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The profiles are unsuitable for lofting.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.LoftProfiles(System.Collections.Generic.IList{System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve}},System.Double,System.Double)`
    - **summary:** Creates a body by lofting between profiles. This interface is designed for controlling the magnitude of the
            tangent vectors if the profiles are edges on a sheet or solid body and will use the surface to enforce tangency.
    - **param:** A list of profiles to loft through.
      - *@name:* `profiles`
    - **param:** Value between 0 and 2. A value of 1.0 should produce the surface with least amount of curvature.
      - *@name:* `startMagnitude`
    - **param:** Value between 0 and 2. A value of 1.0 should produce the surface with least amount of curvature.
      - *@name:* `endMagnitude`
    - **returns:** The created body.
    - **remarks** Surfaces produced have a U parameter in the direction of the profile curves,
            and a V parameter in the direction of lofting.
            
            Profiles can have different numbers of segments.
            A minimum twist solution is produced.
            
            Profiles should be all closed or all open.
            Closed profiles cannot contain inner loops.
            If closed profiles are supplied, a closed (solid) body is produced, if possible;
            otherwise an open (sheet) body is produced.
      - **para**
      - **para**
      - **para**
    - **exception:** Insufficient number of profiles supplied.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The profiles are unsuitable for lofting.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.LoftProfiles(SpaceClaim.Api.V22.Modeler.Loop,System.Collections.Generic.IList{System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve}},SpaceClaim.Api.V22.Modeler.Loop,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **summary:** Creates a body by lofting between profiles using guide curves.
    - **param:** The start profile, or null if not specified.
      - *@name:* `startLoop`
    - **param:** A list of profiles to loft through, or null if not specified.
      - *@name:* `profiles`
    - **param:** The end profile, or null if not specified.
      - *@name:* `endLoop`
    - **param:** A list of guide curves.
      - *@name:* `guides`
    - **returns:** The created body.
    - **remarks** If startLoop or endLoop are supplied, the resulting faces will be tangent to the profiles. 
            
            Guide curves can be provided in tangent continuous pieces. 
            
            Surfaces produced have a U parameter in the direction of the profile curves,
            and a V parameter in the direction of lofting.
            
            Profiles can have different numbers of segments.
            A minimum twist solution is produced.
      - **para**
      - **para**
      - **para**
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.ProjectCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Modeler.ProjectionOptions)`
    - **summary:** Projects trimmed curves to the body.
    - **param:** Trimmed curves to project.
      - *@name:* `segments`
    - **param:** Direction of projection.
      - *@name:* `dir`
    - **param:** Projection options.
      - *@name:* `options`
    - **returns:** Projected trimmed curves and the faces in which they lie.
    - **remarks** The returned dictionary contains the projected trimmed curves, and for each one, the face in which it lies.
            
            The trimmed curves are projected in both the positive and negative sense of the specified 
            in order to find the projected result.
            
            Only projections onto faces are returned.
            If a trimmed curve projects onto an edge, this is not returned.
            
            When  is specified as ,
            only portions of each trimmed curve that are on or outside the body are projected.
            Portions that are inside the body are ignored.
            
            If projected trimmed curves intersect, they are split.
            For example, if two crossing trimmed curves project to the same face, four trimmed curves are returned.
      - **para**
      - **paramref**
        - *@name:* `dir`
      - **para**
      - **para**
      - **see:** ProjectionOptions.Extent
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.ProjectionOptions.Extent`
      - **see:** ProjectionExtent.ClosestFaces
        - *@cref:* `F:SpaceClaim.Api.V22.Modeler.ProjectionExtent.ClosestFaces`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.WrapPlanarCurves(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Modeler.ProjectionOptions,SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Wraps a set of coplanar curves onto a body.
    - **param:** Trimmed curves to wrap.
      - *@name:* `segments`
    - **param:** A reference point in the source curve plane.
      - *@name:* `sourcePoint`
    - **param:** A reference point on the body.
      - *@name:* `targetPoint`
    - **param:** Projection options.
      - *@name:* `options`
    - **param:** Optional hint plane that contains segments.
      - *@name:* `plane`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.WrapPlanarCurvesParallel(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point,System.Int32,SpaceClaim.Api.V22.Geometry.Plane)`
    - **exclude**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.WrapPlanarCurvesParallel(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Modeler.ProjectionOptions,System.Int32,System.Boolean,SpaceClaim.Api.V22.Geometry.Plane)`
    - **exclude**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetHiddenLineImage(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.TransformedBody},SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates a hidden line image.
    - **param:** Bodies to be rendered.
      - *@name:* `transformedBodies`
    - **param:** The view direction, towards the viewer.
      - *@name:* `viewDir`
    - **returns:** A table of body renderings for the supplied bodies.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Split(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Modeler.Tracker)`
    - **summary:** Splits the body into pieces.
    - **param:** A dividing plane at which to split the body.
      - *@name:* `plane`
    - **param** A tracker to receive information about splits and merges; or  if not required.
      - *@name:* `tracker`
      - **b:** null
    - **remarks** The body is split in-situ, so that additional pieces are created.
             can be used to get the number of pieces in the result,
            and  can be used to create separate bodies, if required.
            
            If the  does not pass through the body, no changes are made.
            
            The body must not belong to a design body.
             can be used to see if the body belongs to a design body.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Modeler.Body.PieceCount`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Modeler.Body.SeparatePieces`
      - **para**
      - **paramref**
        - *@name:* `plane`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DesignBody.GetDesignBody(SpaceClaim.Api.V22.Modeler.Body)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetCollision(SpaceClaim.Api.V22.Geometry.ITrimmedSpace)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetClosestSeparation(SpaceClaim.Api.V22.Geometry.ITrimmedGeometry)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Body.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.VariableRadiusRound.#ctor(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Modeler.RadiusPoint})`
    - **summary:** Create a variable radius round specification.
    - **param:** Two or more radius values along the edge.
      - *@name:* `radiusPoints`
    - **exception:** At least two radius points must be supplied.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.VariableRadiusRound.RadiusPoints`
    - **summary:** Gets the radius points along the edge.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Modeler.RadiusPoint`
    - **summary:** Specifies the radius of a variable radius round.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.RadiusPoint.#ctor(System.Double,System.Double)`
    - **summary:** Creates a radius point.
    - **param:** The location along the edge as a parameter on its curve.
      - *@name:* `param`
    - **param:** The round radius at that location.
      - *@name:* `radius`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.RadiusPoint.Param`
    - **summary:** The location along the edge as a parameter on its curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.RadiusPoint.Radius`
    - **summary:** The round radius.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.StartPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.EndPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.IntersectCurve(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.Offset(SpaceClaim.Api.V22.Geometry.Plane,System.Double)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.Offset(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.OffsetChain(SpaceClaim.Api.V22.Geometry.Plane,System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.OffsetCornerType)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.OffsetChain(SpaceClaim.Api.V22.Geometry.Plane,SpaceClaim.Api.V22.Geometry.CurveParam,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.OffsetCornerType)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.ApproximateChain(System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},SpaceClaim.Api.V22.Geometry.FitMethod)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.SelectFragment(System.Double,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.GetPolyline(SpaceClaim.Api.V22.Geometry.PolylineOptions)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.IsCoincident(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.ProjectToPlane(SpaceClaim.Api.V22.Geometry.Plane)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Edge.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.GetClosestSeparation(SpaceClaim.Api.V22.Geometry.ITrimmedGeometry)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.GetGeometry``1`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Edge.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.ProjectPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.ContainsParam(SpaceClaim.Api.V22.Geometry.PointUV)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.IntersectCurve(SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Modeler.Face.Geometry`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.GetClosestSeparation(SpaceClaim.Api.V22.Geometry.ITrimmedGeometry)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.GetGeometry``1`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Face.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.FaceTessellation.CreateTransformedCopy(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **summary:** Gets the transformed faceted tessellation of a face.
    - **param:** The transformation to be applied to the object.
      - *@name:* `trans`
    - **returns:** Transformed face tessellation.
    - **remarks:** Returns transformed faceted tessellation by applying given transformation

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Vertex.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Vertex.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Vertex.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Modeler.Vertex.ContainsPoint(SpaceClaim.Api.V22.Geometry.Point)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignWindowOptions.CreateSketchCurves`
    - **summary** Gets or sets whether to create sketch curves (rather than layout curves) when using sketch tools (default = ).
      - **b:** true

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DrawingWindowOptions.CreateSketchCurves`
    - **summary** Gets or sets whether to create sketch curves (rather than layout curves) when using sketch tools (default = ).
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightFacePattern.CreatePattern(SpaceClaim.Api.V22.DesignFace,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignFace},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.PlacementUV})`
    - **summary:** Creates a pattern of cutouts, using this cutout as a template.
    - **param:** The substrate face of the pattern.
      - *@name:* `substrateDesFace`
    - **param:** The faces of the cutout.
      - *@name:* `desFaces`
    - **param:** Placements for other members of the pattern.
      - *@name:* `otherMembers`
    - **returns:** A lightweight pattern.
    - **remarks** A  is created, using this form as  for the pattern.
            
            A  pattern displays the pattern without creating geometry for the other members,
            whereas a  pattern creates identical cutout geometry for all members.
            
            If a  is required,  can be called.
            
            Each  in  specifies a location and orientation
            within the UV space of the plane of the  face.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.LightweightFacePattern`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.CutoutFacePattern.TemplateFaces`
      - **para**
      - **i:** lightweight
      - **i:** heavyweight
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.HeavyweightFacePattern`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.LightweightFacePattern.ConvertToHeavyweight`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PlacementUV`
      - **paramref**
        - *@name:* `otherMembers`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.ISheetMetalForm.Substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BendOptions.#ctor(System.Nullable{System.Double},System.Nullable{System.Double},System.Nullable{System.Double},System.Nullable{System.Double},SpaceClaim.Api.V22.BendOptions.BendDirection)`
    - **summary:** Constructs a bend options object.
    - **param:** Bend radius in milliseconds.
      - *@name:* `radius`
    - **param:** Bend angle in
      - *@name:* `angle`
    - **param:** Vee die width in meters.
      - *@name:* `veeDieWidth`
    - **param:** Bend allowance in meters.
      - *@name:* `bendAllowance`
    - **param:** Direction of bend.
      - *@name:* `direction`
    - **remarks** See  for more information.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.SheetMetalBendHandler.UpdateBendOptions(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.IDocObject)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Session.Start(SpaceClaim.Api.V22.StartupOptions)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BridgeForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.RectangleProfile,System.Double,System.Double,System.Double,System.Double)`
    - **summary:** Creates a bridge form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Height of the form.
      - *@name:* `height`
    - **param:** Side wall taper angle.
      - *@name:* `taperAngle`
    - **param:** Round radius at the top of the form.
      - *@name:* `topRadius`
    - **param:** Round radius at the bottom of the form.
      - *@name:* `bottomRadius`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BridgeForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.RectangleProfile,System.Double,System.Double,System.Double,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.BridgeForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.RectangleProfile,System.Double,System.Double,System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BridgeForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IBridgeForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CardGuideForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.RectangleProfile,System.Double,System.Double,System.Double,System.Double)`
    - **summary:** Creates a card guide form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Height of the form.
      - *@name:* `height`
    - **param:** Spacing.
      - *@name:* `spacing`
    - **param:** Round radius at the top of the form.
      - *@name:* `topRadius`
    - **param:** Round radius at the bottom of the form.
      - *@name:* `bottomRadius`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CardGuideForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.RectangleProfile,System.Double,System.Double,System.Double,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.CardGuideForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.RectangleProfile,System.Double,System.Double,System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CardGuideForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ICardGuideForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BossForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double,System.Double)`
    - **summary:** Creates a boss form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Height of the boss.
      - *@name:* `height`
    - **param:** Inner radius of the boss.
      - *@name:* `innerRadius`
    - **returns:** A new boss form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BossForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.BossForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BossForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IBossForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DimpleForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`
    - **summary:** Creates a Dimple form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Height of the form.
      - *@name:* `height`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DimpleForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DimpleForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DimpleForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IDimpleForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.RoundedLouverForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double,System.Double,System.Double)`
    - **summary:** Creates a RoundedLouver form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** Location of the form.
      - *@name:* `frame`
    - **param:** Height of the form.
      - *@name:* `height`
    - **param:** Length of the form.
      - *@name:* `length`
    - **param:** Width of the form.
      - *@name:* `width`
    - **param:** Round radius at the top of the form.
      - *@name:* `topRadius`
    - **param:** Round radius at the bottom of the form.
      - *@name:* `bottomRadius`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.RoundedLouverForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double,System.Double,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.RoundedLouverForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double,System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.RoundedLouverForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IRoundedLouverForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LouverForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double)`
    - **summary:** Creates a louver form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** Location of the form.
      - *@name:* `frame`
    - **param:** Height of the form.
      - *@name:* `height`
    - **param:** Length of the form.
      - *@name:* `length`
    - **param:** Width of the form.
      - *@name:* `width`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LouverForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.LouverForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LouverForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ILouverForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ThreadPunchForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.String)`
    - **summary:** Creates a thread punch form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** Location of the form.
      - *@name:* `frame`
    - **param:** Thread size.
      - *@name:* `threadSize`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ThreadPunchForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.String)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ThreadPunchForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame,System.String)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ThreadPunchForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IThreadPunchForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.RaisedCountersinkForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`
    - **summary:** Creates a raised countersink form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Height of the form.
      - *@name:* `height`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.RaisedCountersinkForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.RaisedCountersinkForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.RaisedCountersinkForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IRaisedCountersinkForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CountersinkForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`
    - **summary:** Creates a countersink form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Inner radius of the form.
      - *@name:* `innerRadius`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CountersinkForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.CountersinkForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.CircleProfile,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CountersinkForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ICountersinkForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Collections.Generic.ICollection{System.Int32},System.Double,SpaceClaim.Api.V22.CustomFormOptions)`
    - **summary:** Creates an embossed sheet metal form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Segments of the profile boundary that should produce vents.
      - *@name:* `vents`
    - **param:** The height of the embossed form.
      - *@name:* `height`
    - **param:** Further options.
      - *@name:* `options`
    - **returns:** A new sheet metal form.
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** The  must be a planar face.
            
            The profile must be a single loop with no self-intersections, which lies in the plane of the  face.
            
             specifies the segments in the profile that should create vents.
            There must be at least one segment which is not vented, so that the form is attached to the face.
      - **paramref**
        - *@name:* `substrate`
      - **para**
      - **paramref**
        - *@name:* `substrate`
      - **para**
      - **paramref**
        - *@name:* `vents`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Collections.Generic.ICollection{System.Int32},System.Double,SpaceClaim.Api.V22.CustomFormOptions)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.CustomForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Collections.Generic.ICollection{System.Int32},System.Double,SpaceClaim.Api.V22.CustomFormOptions)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ICustomForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ExtrusionForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Double)`
    - **summary:** Creates an extrusion form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Overall height of the extrusion.
      - *@name:* `height`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
            
            The outline must be a single loop with no self-intersections, which lies in the plane of the  face.
      - **paramref**
        - *@name:* `substrate`
      - **para**
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ExtrusionForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ExtrusionForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ExtrusionForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IExtrusionForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CupForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Double,System.Double,System.Double,System.Double)`
    - **summary:** Creates a cup form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **param:** Height of the form.
      - *@name:* `height`
    - **param:** Side-wall angle.
      - *@name:* `taperAngle`
    - **param:** Round radius at the top of the form.
      - *@name:* `topRadius`
    - **param:** Round radius at the bottom of the form.
      - *@name:* `bottomRadius`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
            
            The outline must be a single loop with no self-intersections, which lies in the plane of the  face.
      - **paramref**
        - *@name:* `substrate`
      - **para**
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CupForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Double,System.Double,System.Double,System.Double)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.CupForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile,System.Double,System.Double,System.Double,System.Double)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CupForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ICupForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.KnockoutForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile)`
    - **summary:** Creates a knockout form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
            
            The outline must be a single loop with no self-intersections, which lies in the plane of the  face.
      - **paramref**
        - *@name:* `substrate`
      - **para**
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.KnockoutForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Profile)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.KnockoutForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.KnockoutForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IKnockoutForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CutoutForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile)`
    - **summary:** Creates a cutout form.
    - **param:** The planar face in which to create the form.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **returns:** A new sheet metal form.
    - **remarks** The  must be a planar face.
            
            The outline must be a single loop with no self-intersections, which lies in the plane of the  face.
      - **paramref**
        - *@name:* `substrate`
      - **para**
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CutoutForm.Create(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Profile)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.CutoutForm.Create(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CutoutForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ICutoutForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CutoutForm.CreatePattern(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.PlacementUV})`
    - **summary:** Creates a pattern of cutout forms, using this form as a template.
    - **param:** Placements for other members of the pattern.
      - *@name:* `otherMembers`
    - **returns:** A lightweight pattern.
    - **remarks** A  is created, using this form as the  for the pattern.
            
            A pattern is based on a  form.
            A  pattern displays the pattern without creating forms for the other members,
            whereas a  pattern creates identical linked copies of the template form for all members.
            
            If a  is required,  can be called.
            
            Each  in  specifies a location and orientation
            within the UV space of the plane of the  face.
            
            The  property gives the placement for this form.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.LightweightFormPattern`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.CutoutFormPattern.Template`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.CutoutFormPattern.Template`
      - **i:** lightweight
      - **i:** heavyweight
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.HeavyweightFormPattern`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.LightweightFormPattern.ConvertToHeavyweight`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PlacementUV`
      - **paramref**
        - *@name:* `otherMembers`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.ISheetMetalForm.Substrate`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.CutoutForm.Placement`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.LightweightNote.AnchorPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ILightweightNote.AnchorPoint`
    - **summary:** Gets the anchor point of the note.
    - **remarks:** The anchor point of the note is the location that remains fixed when the note is edited.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalFormHandler.CreateForm(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Profile)`
    - **summary:** Creates a sheet metal form.
    - **param:** The planar substrate face.
      - *@name:* `substrate`
    - **param:** The profile of the form.
      - *@name:* `profile`
    - **returns** The sheet metal form, or  if unsuccessful.
      - **b:** null
    - **remarks** The  is a planar face in the sheet metal part.
            
            The  is has the same outline as the 
            returned from , and is in the desired position and orientation in the
            plane of the  face.
      - **paramref**
        - *@name:* `substrate`
      - **para**
      - **paramref**
        - *@name:* `profile`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SheetMetalFormPreview.Profile`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.SheetMetalFormHandler.CreatePreview`
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalFormPreview.#ctor(System.String,SpaceClaim.Api.V22.Geometry.Profile)`
    - **summary:** Creates a sheet metal form preview.
    - **param:** The name of the sheet metal form.
      - *@name:* `name`
    - **param:** The profile of the sheet metal form.
      - *@name:* `profile`
    - **remarks** This object is returned from the  method of the  class.
            
            The  is used as the name in the undo droplist.
            The  provides the outline of the form, and can be supplied in any plane.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.SheetMetalFormHandler.CreatePreview`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.SheetMetalFormHandler`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SheetMetalFormPreview.Name`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SheetMetalFormPreview.Profile`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumLine.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Creates a datum line.
    - **param:** Parent part.
      - *@name:* `parent`
    - **param:** Name for the datum line.
      - *@name:* `name`
    - **param:** Line of the datum line.
      - *@name:* `line`
    - **returns:** The new datum line.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumLine.Create(SpaceClaim.Api.V22.IPart,System.String,SpaceClaim.Api.V22.Geometry.Line)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DatumLine.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Geometry.Line)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumLine.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Collections.Generic.IList{SpaceClaim.Api.V22.Modeler.Facet})`
    - **summary:** Creates a design mesh from a list of vertices and facets.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name of the design mesh.
      - *@name:* `name`
    - **param:** A list of vertices.
      - *@name:* `vertices`
    - **param:** A list of facets.
      - *@name:* `facets`
    - **returns:** A design mesh.
    - **remarks** Each  is described by three indices, which are positions in the  list.
            
            The  of the design mesh is a  object.
            Each vertex in the  list becomes a  in the ,
            and each facet in the  list becomes a  in the .
            
            The  of the  is its position in the  list,
            and the  of the  is its position in the  list.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Modeler.Facet`
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
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.PointF},System.Collections.Generic.IList{SpaceClaim.Api.V22.Modeler.Facet})`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DesignMesh.Create(SpaceClaim.Api.V22.Part,System.String,System.Collections.Generic.IList{SpaceClaim.Api.V22.Geometry.Point},System.Collections.Generic.IList{SpaceClaim.Api.V22.Modeler.Facet})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignMesh.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.MassProperties.GetInertiaTensor(SpaceClaim.Api.V22.Geometry.Frame)`
    - **summary:** Gets the inertia tensor for a specified frame.
    - **param:** The frame for the inertia tensor.
      - *@name:* `frame`
    - **returns:** The inertia tensor.
    - **remarks:** The tensor is returned as a symmetric 3x3 matrix.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.MassProperties.GetMoment(SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Gets the moment of inertia about a specified axis.
    - **param:** The axis.
      - *@name:* `axis`
    - **returns:** The moment of inertia about the specified axis.
    - **remarks** This method can be used to obtain the principle moments by supplying the axes of the  frame.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.MassProperties.PrincipleAxes`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PartExportFormat.PdfGeometry`
    - **summary** A 3D PDF (".pdf") file, written in  format (containing a B-Rep).
      - **b:** PRC

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Camera.LookDirection`
    - **summary:** Gets the direction in which the camera points.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Camera.UpDirection`
    - **summary:** Gets the orientation of the top of the camera.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.SketchCurves`
    - **summary:** Select sketch curves.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Points`
    - **summary:** Select points.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Readout.TargetPoint`
    - **summary:** Gets or sets the target point for the readout measurement.
    - **remarks** The  is the "to point" for the measurement.
            
            When the readout is created, the target point is , which means the readout is not displayed.
            The target point can be set to  at any time to hide the readout.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Readout.TargetPoint`
      - **para**
      - **b:** null
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CoordinateSystem.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Geometry.Frame)`
    - **summary:** Creates a coordinate system.
    - **param:** The part in which the coordinate system should be created.
      - *@name:* `parent`
    - **param:** The name of the coordinate system.
      - *@name:* `name`
    - **param:** The frame of the coordinate system.
      - *@name:* `frame`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CoordinateSystem.Create(SpaceClaim.Api.V22.IPart,System.String,SpaceClaim.Api.V22.Geometry.Frame)`
    - **summary:** Creates a coordinate system.
    - **param:** The part in which the coordinate system should be created.
      - *@name:* `parent`
    - **param:** The name of the coordinate system.
      - *@name:* `name`
    - **param:** The frame of the coordinate system.
      - *@name:* `frame`
    - **returns**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CoordinateSystem.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CoordinateSystem.Frame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetBendFace(SpaceClaim.Api.V22.DesignCurve)`
    - **summary:** Gets the bend face which is annotated by a design curve.
    - **param:** The design curve.
      - *@name:* `desCurve`
    - **returns** The bend face; else  if  does not annotate a bend face.
      - **b:** null
      - **paramref**
        - *@name:* `desCurve`
    - **remarks** The bend face is a design face within this flat pattern part.
             can be used to get the corresponding face in the folded sheet metal part.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.FlatPatternAspect.GetFoldedFace(SpaceClaim.Api.V22.DesignFace)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FlatPatternAspect.TryGetUnfoldTransform(SpaceClaim.Api.V22.DesignBody,SpaceClaim.Api.V22.Geometry.Matrix@)`
    - **summary:** Gets the transform from the folded sheet metal part to an unfolded body.
    - **param:** The unfolded design body.
      - *@name:* `desBody`
    - **param:** The transform from the folded part.
      - *@name:* `transform`
    - **returns** if a transform is defined; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** The flat pattern part contains a collection of design bodies.
            
            Each flat region of the sheet metal part, which is not a sheet metal feature,
            appears as a separate design body transformed into its position in the flat pattern part.
            For such flat pattern bodies, this method returns .
            
            For other design bodies in the flat pattern, where material was unbent or unformed to produce that body,
            no transformation is defined, and this method returns .
      - **para**
      - **b:** true
      - **para**
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreateBends(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Point,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.BendSpecification},System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DesignCurve})`
    - **summary:** Creates sheet metal bends.
    - **param:** The face in which to create bends.
      - *@name:* `face`
    - **param** An anchor point to indicate which region of the  stays fixed.
      - *@name:* `anchorPoint`
      - **paramref**
        - *@name:* `face`
    - **param:** A collection of bend specifications.
      - *@name:* `bendSpecs`
    - **param:** Design curves to be moved with the faces in which they lie.
      - *@name:* `desCurvesToMove`
    - **returns:** A collection of new bends.
    - **exception:** Operation failed.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** This methods creates sheet metal bends within a face.
            
            The  indicates which region of the  stays fixed as bends are applied.
            
            If the bend angle is positive, the bend is upwards, i.e. towards the face normal.
            
            As bends are applied, faces will move.
             specifies design curves that should be moved with the faces in which they lie.
            If  is , any suitable design curves in the  will be moved,
            otherwise only those design curves specified in  will be considered.
      - **para**
      - **paramref**
        - *@name:* `anchorPoint`
      - **paramref**
        - *@name:* `face`
      - **para**
      - **para**
      - **paramref**
        - *@name:* `desCurvesToMove`
      - **paramref**
        - *@name:* `desCurvesToMove`
      - **b:** null
      - **paramref**
        - *@name:* `face`
      - **paramref**
        - *@name:* `desCurvesToMove`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreateInternalBead(SpaceClaim.Api.V22.DesignFace,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve},System.Double,System.Double)`
    - **summary:** Creates a sheet metal bead, which is internal to a face.
    - **param:** The face in which to create the bead.
      - *@name:* `substrate`
    - **param:** The path for the bead to follow.
      - *@name:* `path`
    - **param:** The radius of the bead.
      - *@name:* `beadRadius`
    - **param:** The radius to be applied to the edges of the bead.
      - *@name:* `edgeRadius`
    - **returns:** A sheet metal bead.
    - **remarks** The trimmed curves in the  should form a smooth (tangent continuous) path with no self-intersections.
            
            The bead must lie within the boundary of the  face.
      - **paramref**
        - *@name:* `path`
      - **para**
      - **paramref**
        - *@name:* `substrate`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreatePartitionBead(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction,System.Double,System.Double)`
    - **summary:** Creates a straight sheet metal bead across a face.
    - **param:** The face in which to create the bead.
      - *@name:* `substrate`
    - **param:** A point in the substrate face to locate the bead.
      - *@name:* `pointInFace`
    - **param:** The direction of the bead within the face.
      - *@name:* `dir`
    - **param:** The radius of the bead.
      - *@name:* `beadRadius`
    - **param:** The radius to be applied to the edges of the bead.
      - *@name:* `edgeRadius`
    - **returns:** A sheet metal bead.
    - **remarks** A bead is created, which passes through  in the orientation of  within the face,
            and extends in both directions until it meets the boundary of the face.
      - **paramref**
        - *@name:* `pointInFace`
      - **paramref**
        - *@name:* `dir`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreateMarker(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Creates a sheet metal marker in a planar face.
    - **param:** The planar design face in which the marker should live.
      - *@name:* `face`
    - **param:** The location of the marker within the plane of the design face.
      - *@name:* `location`
    - **returns:** A sheet metal marker.
    - **exception:** The face must be planar and not a side face.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** The  must be planar and not a side face.
      - **paramref**
        - *@name:* `face`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalAspect.CreateHem(SpaceClaim.Api.V22.DesignEdge,SpaceClaim.Api.V22.HemStyle,SpaceClaim.Api.V22.Geometry.Interval)`
    - **summary:** Creates a hem bend along a straight edge, limited to parametric bounds.
    - **param:** The straight edge for the hem.
      - *@name:* `edge`
    - **param:** The style of the hem.
      - *@name:* `style`
    - **param:** The bounds of the hem.
      - *@name:* `bounds`
    - **returns:** A hem bend.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.BendSpecification.Create(SpaceClaim.Api.V22.Geometry.ITrimmedCurve,System.Double,System.Double,System.Nullable{System.Double})`
    - **summary:** Constructs a sheet metal bend specification.
    - **param:** The bend line, which should cut across the face.
      - *@name:* `bendLine`
    - **param:** The bend angle, where positive is upwards, i.e. towards the face normal.
      - *@name:* `angle`
    - **param:** The inner radius.
      - *@name:* `innerRadius`
    - **param:** The optional bend allowance override.
      - *@name:* `bendAllowanceOverride`
    - **returns:** A bend specification.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SheetMetalForm.Copy(SpaceClaim.Api.V22.DesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ISheetMetalForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ISheetMetalForm.Copy(SpaceClaim.Api.V22.IDesignFace,SpaceClaim.Api.V22.Geometry.Frame)`
    - **summary:** Creates a copy of the form at a new location.
    - **param:** A planar substrate face.
      - *@name:* `substrate`
    - **param:** The position and orientation of the form within the substrate face.
      - *@name:* `frame`
    - **returns:** A copy of the form.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.SpotWeld.WeldPoints`
    - **summary:** Gets the weld points for this spot weld.
    - **remarks** There are two or more weld points.
            
            Each entry contains the face in which the weld point lies, and the location of the weld point in the surface of that face.
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomWrapper.TryGetTransformFrame(SpaceClaim.Api.V22.Geometry.Frame@,SpaceClaim.Api.V22.Geometry.Transformations@)`
    - **summary:** Gets the transform frame for the custom object.
    - **param:** The transform frame.
      - *@name:* `frame`
    - **param:** Allowable transformations.
      - *@name:* `transformations`
    - **returns** if the custom object has a transform frame; otherwise .
      - **b:** true
      - **b:** false
    - **remarks** Override this method to allow the custom object to be used with the Move tool.
            The position and orientation of the transform frame is used for the Move tool handles.
            
             is a bit field that specifies which transformations are suitable for this object.
            This is a hint to the Move tool for which handles to display.
            If multiple objects are selected, each object may offer different transformations,
            and in this case, the union of Move tool handles is presented.
            This means  can be called with a transformation that may be unsuitable for this object.
            You can skip such a transform, or adjust it to make it suitable.
      - **para**
      - **paramref**
        - *@name:* `transformations`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.CustomWrapper.Transform(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomWrapper.TryGetPositionOrigin(SpaceClaim.Api.V22.Geometry.Point@)`
    - **summary:** Gets the position origin for the custom object.
    - **param:** The position origin.
      - *@name:* `origin`
    - **returns** if the custom object has a position origin; otherwise .
      - **b:** true
      - **b:** false
    - **remarks:** Override this method to specify a position origin to be used with the Move tool.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomWrapper.Transform(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **summary:** Transforms the custom object.
    - **param:** The transformation to apply.
      - *@name:* `trans`
    - **param:** A flag indicating whether this is the final transform.
      - *@name:* `final`
    - **remarks** Override this method if the custom object supports being transformed.
            The default implementation does nothing.
            
            This method is used by the Move tool.
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.CustomWrapper.TryGetTransformPath(SpaceClaim.Api.V22.Geometry.ITrimmedCurve@)`
    - **summary:** Returns a reference path for transformation of other objects
    - **param**
      - *@name:* `trimmedCurve`
    - **returns**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.LocationPoint`
    - **summary:** Specifies a location within a rectangular block of annotation.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.InteractionContext.DesignCurveParent`
    - **summary:** Gets the parent for new design curves, in context-space.
    - **remarks** Even though it is mapped to context-space, the design curve parent may be an occurrence,
            e.g. if the context is an assembly and the user is sketching on a datum plane in a component.
            
            The value is never .
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.InteractionContext.GetSelectionPoint(SpaceClaim.Api.V22.IDocObject)`
    - **summary:** Gets the hit point for the selected object, in context-space.
    - **param:** The object for which the selection hit point is sought.
      - *@name:* `selectedObject`
    - **returns** The selection hit point, or  if not available.
      - **b:** null
    - **remarks** If an object is selected by clicking in the graphics window, then a hit point will be available for it.
            If the object was box-selected, or selected in the Structure View, then a hit point will not be available
            and  is returned.
            
             is also returned if the object is not currently selected.
      - **b:** null
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.InteractionContext.PreselectionPoint`
    - **summary:** Gets the hit point of the preselected object, in context-space.
    - **remarks** If the current preselection was made in the Structure View, then a hit point will not be available
            and  is returned.
            
             is also returned if there is no currently preselected object ( is ).
      - **b:** null
      - **para**
      - **b:** null
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.Preselection`
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.InteractionContext.GetVisibleCurves(SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Gets visible design curves, in context-space.
    - **param** A plane in context-space, or .
      - *@name:* `plane`
      - **b:** null
    - **returns:** Visible curves in context-space.
    - **remarks** If  is not , only design curves that lie in that plane are returned.
      - **paramref**
        - *@name:* `plane`
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.InteractionContext.GetPixelSize(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Gets the screen pixel size for the active view, in context-space.
    - **param:** The context-space point at which the pixel size is required.
      - *@name:* `point`
    - **returns:** The screen pixel size in context-space.
    - **remarks** This method returns the distance in context-space which corresponds to one pixel in screen-space.
            
            The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.InteractionContext.ProjectToScreen(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Projects a context-space point into screen-space.
    - **param:** A point in context-space.
      - *@name:* `point`
    - **returns:** The projection of the point in screen-space.
    - **remarks** The result is in the pixel-space of the active view.
            
            The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.InteractionContext.GetCursorRay(System.Drawing.Point)`
    - **summary:** Gets the context-space cursor ray at a position in screen-space.
    - **param:** A screen-space point.
      - *@name:* `screenPoint`
    - **returns:** The corresponding cursor ray in context-space.
    - **remarks** The  is in the pixel-space of the active view.
            
            The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.
      - **paramref**
        - *@name:* `screenPoint`
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ImportOptions.ImportCurves`
    - **summary** Gets or sets whether to import curves (default = ).
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ImportOptions.ImportPoints`
    - **summary** Gets or sets whether to import points (default = ).
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Beam.Create(SpaceClaim.Api.V22.Part,SpaceClaim.Api.V22.DesignCurve)`
    - **summary:** Creates a beam.
    - **param:** A beam profile part.
      - *@name:* `profilePart`
    - **param:** A design curve.
      - *@name:* `desCurve`
    - **returns:** A beam.
    - **remarks** The  must be of type
      - **i:** profilePart
      - **see**
        - *@cref:* `F:SpaceClaim.Api.V22.PartType.BeamProfile`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Beam.SectionFrame`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IBeam.SectionFrame`
    - **summary:** Gets the section frame at the start of the beam.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SectionProperties.#ctor(System.Double,System.Double,System.Double,System.Double,System.Double,System.Double,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Constructs a section properties object.
    - **param:** The area of the section.
      - *@name:* `area`
    - **param:** The moment of inertia about the X-axis.
      - *@name:* `ixx`
    - **param:** The moment of inertia about the Y-axis.
      - *@name:* `iyy`
    - **param:** The product of inertia.
      - *@name:* `ixy`
    - **param:** The warping constant (Cw).
      - *@name:* `warpingConstant`
    - **param:** The torsion constant (J).
      - *@name:* `torsionConstant`
    - **param:** The centroid of the section.
      - *@name:* `centroid`
    - **param:** The shear center.
      - *@name:* `shearCenter`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ConnectionTable.WireCurves`
    - **summary:** The wire curves for this table.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ConnectionTable.GetTangentChain(SpaceClaim.Api.V22.IWireCurve)`
    - **summary:** Gets the wire curves that form a tangent chain with the specified wire curve.
    - **param:** The seed wire curve.
      - *@name:* `seed`
    - **returns** Wire curves forming a tangent chain, including the  wire curve.
      - **paramref**
        - *@name:* `seed`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ConnectionTable.GetConnections(SpaceClaim.Api.V22.IWireCurve)`
    - **summary:** Gets the connections that a wire curve has to other wire curves.
    - **param:** The wire curve.
      - *@name:* `wireCurve`
    - **returns:** Connections that the wire curve has to other wire curves.
    - **remarks** Each  returned has two  objects,
            describing the connection to a wire curve.
            The  is for the supplied 
            and the  is for the other wire curve.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.WireCurveConnection`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.WireCurvePoint`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.WireCurveConnection.FirstPoint`
      - **paramref**
        - *@name:* `wireCurve`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.WireCurveConnection.SecondPoint`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.WireCurveConnection`
    - **summary:** A connection between two wire curves.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WireCurveConnection.#ctor(SpaceClaim.Api.V22.WireCurvePoint,SpaceClaim.Api.V22.WireCurvePoint,System.Boolean)`
    - **summary:** Constructs a wire curve connection.
    - **param:** Details of the point on the first wire curve.
      - *@name:* `firstPoint`
    - **param:** Details of the point on the second wire curve.
      - *@name:* `secondPoint`
    - **param:** Whether the two wire curves are tangent where they meet.
      - *@name:* `tangent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WireCurveConnection.FirstPoint`
    - **summary:** Gets details of the point on the first wire curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WireCurveConnection.SecondPoint`
    - **summary:** Gets details of the point on the second wire curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WireCurveConnection.IsTangent`
    - **summary:** Gets whether the two wire curves are tangent where they meet.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.WireCurvePoint`
    - **summary:** Details of a connection to a wire curve.
    - **remarks** See  for more information.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.WireCurveConnection`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WireCurvePoint.#ctor(SpaceClaim.Api.V22.IWireCurve,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.PointType)`
    - **summary:** Constructs a wire curve point.
    - **param:** The wire curve.
      - *@name:* `wireCurve`
    - **param:** The wire curve point.
      - *@name:* `point`
    - **param:** The type of point.
      - *@name:* `pointType`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WireCurvePoint.WireCurve`
    - **summary:** Gets the wire curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WireCurvePoint.Point`
    - **summary:** Gets the point.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WireCurvePoint.PointType`
    - **summary:** Gets the type of point.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.PointType`
    - **summary:** A type of point.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PointType.StartPoint`
    - **summary:** The start point.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PointType.EndPoint`
    - **summary:** The end point.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PointType.MidPoint`
    - **summary:** The mid-point.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PointType.Center`
    - **summary:** The center point.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.PointType.None`
    - **summary:** A point which does not fit one of the other categories.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Section.Curves`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.ISection.Curves`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Section.GetCurves(SpaceClaim.Api.V22.DesignFace)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.ISection.GetCurves(SpaceClaim.Api.V22.IDesignFace)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Section.GetCurves(SpaceClaim.Api.V22.IDesignFace)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Section.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Section.GetBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Section.GetExtremePoint(SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction,SpaceClaim.Api.V22.Geometry.Direction)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ISection.Curves`
    - **summary:** Gets all section curves in this section.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ISection.GetCurves(SpaceClaim.Api.V22.IDesignFace)`
    - **summary:** Gets the section curves for a given face.
    - **param:** The design face whose section curves are required.
      - *@name:* `desFace`
    - **returns:** A collection of section curves; empty if the face is not sectioned.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.SectionCurve`
    - **summary:** A section curve master.
    - **remarks**
      - **inheritdoc**
        - *@cref:* `T:SpaceClaim.Api.V22.ISectionCurve`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.SectionCurve.Face`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.ISectionCurve.Face`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.SectionCurve.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.ISectionCurve.Parent`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.ISectionCurve`
    - **summary:** A section curve.
    - **remarks** See  for more information.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.ISection`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ISectionCurve.Parent`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ISectionCurve.Face`
    - **summary:** Gets the face being sectioned.
    - **remarks:** If the section plane passes through an edge, the most perpendicular face is returned.
            If both faces are equally perpendicular, the face behind the section plane is returned.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WireCurve.CreateConnectionTable(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IWireCurve})`
    - **summary:** Creates a connection table for a collection of design curves.
    - **param:** Collection of design curves.
      - *@name:* `wireCurves`
    - **returns:** A connection table for the design curves.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WireCurve.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DerivedPoint.Point`
    - **summary:** Gets the point.
    - **remarks** If the point cannot be determined,  is returned.
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DerivedPoint.Document`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DrawingViewBoundary.Create(SpaceClaim.Api.V22.DerivedPoint,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`
    - **summary:** Creates a clipping boundary for a drawing view.
    - **param:** The anchor point in model-space.
      - *@name:* `anchorPoint`
    - **param:** The clipping profile in paper-space.
      - *@name:* `profile`
    - **returns:** A drawing view clipping boundary.
    - **remarks** The  property specifies the boundary of a drawing view.
            
            The  specifies the clipping profile in paper-space.
            The profile must be a single connected close loop, which is not self-intersecting.
            The segments of the profile can be in any order and direction.
            
            The  is a point in model-space to which the boundary is anchored.
            The anchor point is a , which allows it to be linked to geometry in the model.
            If the view projection changes, or the anchor point moves, the clipping profile maintains its connection to the anchor point.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.Boundary`
      - **para**
      - **paramref**
        - *@name:* `profile`
      - **para**
      - **paramref**
        - *@name:* `anchorPoint`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DerivedPoint`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DrawingViewBoundary.AnchorPoint`
    - **summary:** Gets the anchor point in model-space.
    - **remarks** See the  method for more information.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DrawingViewBoundary.Create(SpaceClaim.Api.V22.DerivedPoint,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.Geometry.ITrimmedCurve})`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DrawingViewStyle.WireFrame`
    - **summary:** The view is shown in wire-frame.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnDragEvent(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called to determine whether mouse dragging should be handled by the tool.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **returns** to handle drag events in the tool; else  for default handling.
      - **b:** true
      - **b:** false
    - **remarks** If the return value is , the tool handles drag behavior and  will be called. This is the default if this method is not overridden.
            
            If the return value is , default handling will be used, and dragging will perform a pick box selection.
      - **b:** true
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnDragStart(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
      - **para**
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnDragStart(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called when the mouse drag begins.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **returns** to continue with the drag operation; else  to cancel.
      - **b:** true
      - **b:** false
    - **remarks** If the return value is ,  will be called for each mouse move during the drag. 
            
            If the return value is , the drag will be canceled. This is the default if this method is not overridden.
      - **b:** true
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnDragMove(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
      - **para**
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnDragMove(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called for each mouse move during a drag.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnDragEnd(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called at the end of the drag.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnClickEvent(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called to determine whether mouse clicks should be handled by the tool.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **returns** to handle mouse clicks in the tool; else  for default handling.
      - **b:** true
      - **b:** false
    - **remarks** If the return value is , the tool handles mouse clicks and  will be called. This is the default if this method is not overridden.
            
            If the return value is , default selection handling will occur.
      - **b:** true
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnClickStart(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
      - **para**
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnClickStart(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called on a mouse click.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **returns** to continue with the click sequence; else  to end.
      - **b:** true
      - **b:** false
    - **remarks** If the return value is , then  will be called for the next mouse click. This may be useful 
            when multiple clicks are required for an operation. 
            
            If the return value is , the click sequence will end. This is the default if this method is not overridden.
      - **b:** true
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnClickEnd(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
      - **para**
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnClickMove(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called when the mouse is moved while in a click sequence.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **remarks** This method will be called as long as a previous call to  or  returned true, 
            and  has not been called.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnClickStart(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnClickEnd(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnClickCancel`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnClickEnd(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
    - **summary:** Called for subsequent mouse clicks.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **returns** to continue with the click sequence; else  to end.
      - **b:** true
      - **b:** false
    - **remarks** If the return value is , then  will be called for the next mouse click.  
            
            If the return value is , then the click sequence will end, and subsequent clicks will restart with . 
            This is the default value if the method is not overridden.
      - **b:** true
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnClickEnd(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`
      - **para**
      - **b:** false
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.OnClickStart(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnMouseDown(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line,System.Windows.Forms.MouseButtons)`
    - **summary:** Called when a mouse button is pressed.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **param:** The button which has been pressed.
      - *@name:* `button`
    - **returns** if the mouse event was handled by the tool and no further processing should be performed; else  for default handling.
      - **b:** true
      - **b:** false
    - **remarks:** The default return value is false;

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnMouseMove(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line,System.Windows.Forms.MouseButtons)`
    - **summary:** Called when a mouse button is pressed.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **param:** The button which has been pressed.
      - *@name:* `button`
    - **returns** if the mouse event was handled by the tool and no further processing should be performed; else  for default handling.
      - **b:** true
      - **b:** false
    - **remarks** Default handling includes preselection, so a return value of  will prevent any preselection from occurring. 
            
            The default return value is false;
      - **b:** true
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnMouseUp(System.Drawing.Point,SpaceClaim.Api.V22.Geometry.Line,System.Windows.Forms.MouseButtons)`
    - **summary:** Called when a mouse button is released.
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** The cursor ray.
      - *@name:* `cursorRay`
    - **param:** The button which has been pressed.
      - *@name:* `button`
    - **returns** if the mouse event was handled by the tool and no further processing should be performed; else  for default handling.
      - **b:** true
      - **b:** false
    - **remarks:** The default return value is false;

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.OnMouseWheel(System.Drawing.Point,System.Int32)`
    - **summary:** Called when the mouse wheel is rotated
    - **param:** The cursor position.
      - *@name:* `cursorPos`
    - **param:** A signed count of the number of detents the mouse wheel has rotated.
      - *@name:* `delta`
    - **returns** if the mouse event was handled by the tool and no further processing should be performed; else  for default handling.
      - **b:** true
      - **b:** false
    - **remarks** will be a positive number when the wheel is rotated forward (away from the user), and negative when rotated backward.
      - **paramref**
        - *@name:* `delta`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateOffsetReadout(SpaceClaim.Api.V22.Geometry.Curve,System.Boolean)`
    - **summary:** Creates readout, which measures an offset from a curve.
    - **param:** The curve from which the offset is measured.
      - *@name:* `curve`
    - **param:** Whether the offset is symmetric about the curve.
      - *@name:* `symmetric`
    - **returns:** A readout.
    - **remarks** By providing a  as the , the distance from a point can be measured.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.PointCurve`
      - **paramref**
        - *@name:* `curve`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateRadiusReadout(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates a readout, which measures a radius.
    - **param:** v.
      - *@name:* `origin`
    - **returns:** A readout.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateDiameterReadout(SpaceClaim.Api.V22.Geometry.Point,System.Boolean)`
    - **summary:** Creates a readout, which measures a diameter.
    - **param:** The origin about which the diameter is measured.
      - *@name:* `origin`
    - **param:** Whether the readout should use a leader.
      - *@name:* `useLeader`
    - **returns:** A readout.
    - **remarks** If  is , the  property of the 
            is set to , so that the presentation is like a radius readout, only the value is doubled;
            otherwise the presentation is like a linear dimension across the diameter.
      - **paramref**
        - *@name:* `useLeader`
      - **b:** true
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Readout.UseLeader`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Readout`
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateLengthReadout(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction,System.Boolean,System.Boolean)`
    - **summary:** Creates a readout, which measures a length in a particular direction.
    - **param:** The origin from which the length is measured.
      - *@name:* `origin`
    - **param:** The direction of measurement.
      - *@name:* `dir`
    - **param:** Whether the measurement is symmetric about the origin.
      - *@name:* `symmetric`
    - **param:** Whether the dimension line should follow the target point.
      - *@name:* `followTarget`
    - **returns:** A readout.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateAngleReadout(SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction,System.Boolean,System.Boolean)`
    - **summary:** Creates a readout, which measures an angle from a base direction.
    - **param:** The origin about which the angle is measured
      - *@name:* `origin`
    - **param:** The direction of the zero angle.
      - *@name:* `baseDir`
    - **param:** Whether the measurement is symmetric about the base direction.
      - *@name:* `symmetric`
    - **param:** Whether the dimension line should follow the target point.
      - *@name:* `followTarget`
    - **returns:** A readout.
    - **remarks:** The angle is between 0 and 180 degrees.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateAngleReadout(SpaceClaim.Api.V22.Geometry.Frame,System.Boolean,System.Boolean)`
    - **summary:** Creates a readout, which measures an angle about an axis.
    - **param:** The frame for the measurement.
      - *@name:* `frame`
    - **param:** Whether the angle must be positive.
      - *@name:* `positive`
    - **param:** Whether the dimension line should follow the target point.
      - *@name:* `followTarget`
    - **returns:** A readout.
    - **remarks** The  specifies how the measurement is made.
            The  direction of the  is the direction of the zero angle,
            and the  direction of the  is the axis direction.
            
            The angle is measured in a clockwise direction about the axis.
            If  is , the angle is between 0 and 360 degrees;
            otherwise the angle is between -180 and 180 degrees.
      - **paramref**
        - *@name:* `frame`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
      - **paramref**
        - *@name:* `frame`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirY`
      - **paramref**
        - *@name:* `frame`
      - **para**
      - **paramref**
        - *@name:* `positive`
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateCurveLengthReadout(SpaceClaim.Api.V22.Geometry.Curve,System.Double)`
    - **summary:** Creates a readout, which measures a length along a curve.
    - **param:** The curve along which the length is measured.
      - *@name:* `curve`
    - **param:** The start parameter from which to measure.
      - *@name:* `startParam`
    - **returns:** A readout.
    - **remarks:** The distance is a zero or positive value.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateIndicator(SpaceClaim.Api.V22.Geometry.Point)`
    - **summary:** Creates an indicator at a point.
    - **param:** The position of the indicator.
      - *@name:* `position`
    - **returns:** An indicator.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateIndicator(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDesignCurve})`
    - **summary:** Creates an indicator for a collection of curves.
    - **param:** The curves.
      - *@name:* `desCurves`
    - **returns:** An indicator.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateDirectionHandle(System.Drawing.Color,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates a direction handle.
    - **param** The color to use, or  for the default handle color.
      - *@name:* `color`
      - **see**
        - *@cref:* `F:System.Drawing.Color.Empty`
    - **param:** The position of the handle.
      - *@name:* `position`
    - **param:** The direction to show.
      - *@name:* `dir`
    - **returns:** A handle.
    - **remarks** The handle is created, but it is not selected.
            You can set  to select the handle.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Tool.SelectedHandle`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.CreateAxisHandle(System.Drawing.Color,SpaceClaim.Api.V22.Geometry.Point,SpaceClaim.Api.V22.Geometry.Direction)`
    - **summary:** Creates an axis handle.
    - **param** The color to use, or  for the default handle color.
      - *@name:* `color`
      - **see**
        - *@cref:* `F:System.Drawing.Color.Empty`
    - **param:** The position of the handle.
      - *@name:* `position`
    - **param:** The axis direction to show.
      - *@name:* `dir`
    - **returns:** A handle.
    - **remarks** The handle is created, but it is not selected.
            You can set  to select the handle.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Tool.SelectedHandle`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGeneral.GetVisibility(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGeneral.SetVisibility(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Boolean})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGeneral.IsVisible(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurveGeneral.Scale(SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignCurve`
    - **summary:** A design curve master.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParentMaster,SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **summary:** Creates a design curve.
    - **param:** The parent of the design curve.
      - *@name:* `parent`
    - **param:** The shape of the design curve.
      - *@name:* `shape`
    - **returns:** The new design curve.
    - **remarks** If the  is a planar object, e.g. a  or ,
            then the  should lie in that plane.
      - **paramref**
        - *@name:* `parent`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DrawingSheet`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.DatumPlane`
      - **paramref**
        - *@name:* `shape`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParentMaster,SpaceClaim.Api.V22.Geometry.ITrimmedCurve,System.Nullable{System.Boolean})`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParentMaster,SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParent,SpaceClaim.Api.V22.Geometry.ITrimmedCurve,System.Nullable{System.Boolean})`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParentMaster,SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParent,SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParentMaster,SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurve.IsConstruction`
    - **summary:** Gets or sets whether the design curve is a construction object.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.GetLineWeight(SpaceClaim.Api.V22.IAppearanceContext)`
    - **summary:** Gets the line weight of the design curve in the specified context.
    - **param** The appearance context, or  for the appearance in design windows.
      - *@name:* `context`
      - **b:** null
    - **returns:** The line weight of the object.
    - **remarks** See  for more information.
            
            If the value is , the line weight of the layer is used.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IAppearanceContext`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.SetLineWeight(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{SpaceClaim.Api.V22.LineWeight})`
    - **summary:** Sets the line weight of the design curve in the specified context.
    - **param** The appearance context, or  for the appearance in design windows.
      - *@name:* `context`
      - **b:** null
    - **param:** The line weight to use.
      - *@name:* `weight`
    - **remarks** See  for more information.
            
            If the value is , the line weight of the layer is used.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IAppearanceContext`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.GetLineStyle(SpaceClaim.Api.V22.IAppearanceContext)`
    - **summary:** Gets the line style of the design curve in the specified context.
    - **param** The appearance context, or  for the appearance in design windows.
      - *@name:* `context`
      - **b:** null
    - **returns:** The line style of the object.
    - **remarks** See  for more information.
            
            If the value is , the line style of the layer is used.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IAppearanceContext`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.SetLineStyle(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{SpaceClaim.Api.V22.LineStyle})`
    - **summary:** Sets the line style of the design curve in the specified context.
    - **param** The appearance context, or  for the appearance in design windows.
      - *@name:* `context`
      - **b:** null
    - **param:** The line style to use.
      - *@name:* `style`
    - **remarks** See  for more information.
            
            If the value is , the line style of the layer is used.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.IAppearanceContext`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurve.Parent`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IDesignCurve.Parent`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurve.Shape`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Copy`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IDesignCurve.Copy`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Replace(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DocObject})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.GetColor(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.SetColor(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Drawing.Color})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurve.Layer`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurve.DefaultVisibility`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.GetVisibility(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.SetVisibility(SpaceClaim.Api.V22.IAppearanceContext,System.Nullable{System.Boolean})`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.IsVisible(SpaceClaim.Api.V22.IAppearanceContext)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurve.CanSuppress`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DesignCurve.IsSuppressed`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignCurve.Scale(SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.IDesignCurve`
    - **summary:** A design curve.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurve.Parent`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurve.Shape`
    - **summary:** Gets or sets the shape of the design curve.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IDesignCurve.Copy`
    - **summary:** Creates a copy of the design curve.
    - **returns:** A copy of the design curve.
    - **remarks:** The copy has the same parent, geometry, name, layer, line style, line width, and color as the original.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveParent.Master`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveParent.Curves`
    - **summary:** Gets the child design curves.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveParent.CurveGroups`
    - **exclude**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveParentMaster.Curves`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IDesignCurveParentMaster.CurveGroups`
    - **exclude**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.RollDirection`
    - **summary** The roll direction. Used with .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.SessionRolledEventArgs`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.RollDirection.Undo`
    - **summary:** An undo.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.RollDirection.Redo`
    - **summary:** A redo.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.SessionRolledEventArgs.Direction`
    - **summary:** Gets whether the operation is an undo or redo.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Component.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**
    - **exception:** The matrix has a scale component.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPlane.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Creates a datum plane.
    - **param:** The parent part.
      - *@name:* `parent`
    - **param:** The name for the datum plane.
      - *@name:* `name`
    - **param:** The plane of the datum plane.
      - *@name:* `plane`
    - **returns:** A datum plane.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPlane.Create(SpaceClaim.Api.V22.IPart,System.String,SpaceClaim.Api.V22.Geometry.Plane)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.DatumPlane.Create(SpaceClaim.Api.V22.Part,System.String,SpaceClaim.Api.V22.Geometry.Plane)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPlane.Curves`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DatumPlane.CurveGroups`
    - **exclude**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DatumPlane.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.GetTessellationBoundingBox(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **summary:** Gets the bounding box, using the faceted representation of the design body for higher performance.
    - **param:** The transformation to be applied to the object.
      - *@name:* `trans`
    - **param:** Whether the bounding box is required to fit tightly around the object.
      - *@name:* `tight`
    - **returns:** The bounding box.
    - **remarks** If  is , the bounding box will fit tightly around the object.
            This calculation is typically more expensive, so it should only be used if necessary.
            
            If  is , the bounding box is guaranteed to enclose the object.
            It may not fit tightly around the object, although it often does.
      - **paramref**
        - *@name:* `tight`
      - **b:** true
      - **para**
      - **paramref**
        - *@name:* `tight`
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DesignBody.Scale(SpaceClaim.Api.V22.Geometry.Frame,System.Double,System.Double,System.Double)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DrawingSheet.TranslateViews(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.DrawingView},SpaceClaim.Api.V22.Geometry.VectorUV)`
    - **summary:** Translates views within the drawing sheet.
    - **param:** The views to translate.
      - *@name:* `views`
    - **param:** A translation vector in paper-space.
      - *@name:* `translation`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DrawingSheet.Curves`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DrawingSheet.CurveGroups`
    - **exclude**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DrawingSheet.SpaceClaim#Api#V22#IDesignCurveParent#Master`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DrawingView.CreateGeneralView(SpaceClaim.Api.V22.DrawingSheet,SpaceClaim.Api.V22.Part,SpaceClaim.Api.V22.Geometry.Matrix,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Creates a general view.
    - **param:** The sheet in which to create the view.
      - *@name:* `parent`
    - **param:** The part to show.
      - *@name:* `part`
    - **param:** The projection to be used.
      - *@name:* `projection`
    - **param:** The location on the sheet for the new view.
      - *@name:* `location`
    - **returns:** A general view.
    - **exception:** The drawing sheet and part do not belong to the same document.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The projection has a translation or scale component.
      - *@cref:* `T:System.ArgumentException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DrawingView.CreateProjectedView(SpaceClaim.Api.V22.DrawingView,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Creates a projected view.
    - **param:** The view to project.
      - *@name:* `sourceView`
    - **param:** The location on the sheet for the new view.
      - *@name:* `location`
    - **returns** A projected view; or  if the projection could not be determined from the .
      - **b:** null
      - **paramref**
        - *@name:* `location`
    - **remarks** The  should be left, right, above, or below the .
            The source view location can be determined as the  of the  of the view.
            
            If the  is not suitably placed, the projection cannot be determined and  is returned.
            
            The sheet uses 1st angle or 3rd angle projection, and this is used to determine the projection from the  supplied.
            The  property of the sheet indicates which projection convention is used.
            
            The projected view has the same  and  as the .
      - **paramref**
        - *@name:* `location`
      - **paramref**
        - *@name:* `sourceView`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.BoxUV.Center`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.Extent`
      - **para**
      - **paramref**
        - *@name:* `location`
      - **b:** null
      - **para**
      - **paramref**
        - *@name:* `location`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingSheet.IsThirdAngle`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.ViewScale`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.Style`
      - **paramref**
        - *@name:* `sourceView`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.DrawingView.CreateDetailView(SpaceClaim.Api.V22.DrawingView,SpaceClaim.Api.V22.Geometry.PointUV)`
    - **summary:** Creates a detail view.
    - **param:** The view to be detailed
      - *@name:* `sourceView`
    - **param:** The location on the sheet for the new view.
      - *@name:* `location`
    - **returns:** A detail view.
    - **remarks** A detail view is a view with a projection that is linked to a .
            The detail view is created with the default style of the sheet,
            and the same scale as the source view.
            
            The scale can be overridden by setting the  property,
            or by setting the  property of the  aspect.
            
            The style can be overridden by setting the  property.
            
            The detail view is created with no clipping boundary.
            The  property can be used to set the clipping boundary.
      - **paramref**
        - *@name:* `sourceView`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.ViewScale`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DetailViewAspect.Enlargement`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.DetailView`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.Style`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DrawingView.Boundary`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Note.Create(SpaceClaim.Api.V22.IAnnotationParentMaster,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.String)`
    - **summary:** Creates a text note.
    - **param:** The annotation parent in which the note should be created.
      - *@name:* `parent`
    - **param:** The anchor location in the UV space of the plane of the annotation parent.
      - *@name:* `anchorLocation`
    - **param:** The anchor point.
      - *@name:* `anchorPoint`
    - **param:** The font size in meters.
      - *@name:* `fontSize`
    - **param:** The text to display.
      - *@name:* `text`
    - **returns:** The new text note.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Note.Create(SpaceClaim.Api.V22.IAnnotationParent,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.String)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.Note.Create(SpaceClaim.Api.V22.IAnnotationParentMaster,SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint,System.Double,System.String)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Note.GetLocation(SpaceClaim.Api.V22.LocationPoint)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Note.SetLocation(SpaceClaim.Api.V22.Geometry.PointUV,SpaceClaim.Api.V22.LocationPoint)`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Note.AnchorPoint`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.CreateBeamProfile(SpaceClaim.Api.V22.Document,System.String,SpaceClaim.Api.V22.Geometry.Profile)`
    - **summary:** Creates a new beam profile part.
    - **param:** The document in which the part should live.
      - *@name:* `doc`
    - **param:** The name for the part.
      - *@name:* `name`
    - **param:** A closed profile.
      - *@name:* `profile`
    - **returns:** A beam profile part.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.DatumPoints`
    - **inheritdoc**
      - *@cref:* `P:SpaceClaim.Api.V22.IPart.DatumPoints`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.GetDesignCurvesInPlane(SpaceClaim.Api.V22.Geometry.Plane)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IPart.GetDesignCurvesInPlane(SpaceClaim.Api.V22.Geometry.Plane)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.IsSketchCurve(SpaceClaim.Api.V22.DesignCurve)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IPart.IsSketchCurve(SpaceClaim.Api.V22.IDesignCurve)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Part.SetSketchCurve(SpaceClaim.Api.V22.DesignCurve,System.Boolean)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.IPart.SetSketchCurve(SpaceClaim.Api.V22.IDesignCurve,System.Boolean)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.Curves`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Part.CurveGroups`
    - **exclude**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.IPart.DatumPoints`
    - **summary:** Gets the datum points contained by the part.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IPart.GetDesignCurvesInPlane(SpaceClaim.Api.V22.Geometry.Plane)`
    - **summary:** Gets the design curves that lie in the specified plane.
    - **param:** The plane in which design curves are sought.
      - *@name:* `plane`
    - **returns:** Design curves that lie in the specified plane.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IPart.IsSketchCurve(SpaceClaim.Api.V22.IDesignCurve)`
    - **summary:** Gets whether the design curve is a sketch curve.
    - **param:** The design curve to test.
      - *@name:* `desCurve`
    - **returns** if the design curves is a sketch curve; otherwise .
      - **b:** true
      - **b:** false
    - **exception:** The design curve does not belong to this part.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** When the user finishes sketching a profile, design curves in the sketch plane
            get automatically converted into a planar design body ready for 3D tools.
            
            Design curves created using the  method
            do not get automatically converted in this way unless  is used to set
            the design curve to be a .
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.DesignCurve.Create(SpaceClaim.Api.V22.IDesignCurveParent,SpaceClaim.Api.V22.Geometry.ITrimmedCurve)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.IPart.SetSketchCurve(SpaceClaim.Api.V22.IDesignCurve,System.Boolean)`
      - **i:** sketch curve

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.IPart.SetSketchCurve(SpaceClaim.Api.V22.IDesignCurve,System.Boolean)`
    - **summary:** Sets a design curve to be a sketch curve.
    - **param:** The design curve.
      - *@name:* `desCurve`
    - **param** to set the design curve to be a sketch curve; otherwise .
      - *@name:* `isSketchCurve`
      - **b:** true
      - **b:** false
    - **exception:** The design curve does not belong to this part.
      - *@cref:* `T:System.ArgumentException`
    - **remarks**
      - **inheritdoc**
        - *@cref:* `M:SpaceClaim.Api.V22.IPart.IsSketchCurve(SpaceClaim.Api.V22.IDesignCurve)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.ITransformable.Transform(SpaceClaim.Api.V22.Geometry.Matrix)`
    - **summary** Transforms the object by applying a transformation .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Geometry.Matrix`
    - **param:** The transformation matrix to apply.
      - *@name:* `trans`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.SetProjection(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean,System.Boolean)`
    - **summary:** Sets the view projection for the active view.
    - **param:** The new projection to use.
      - *@name:* `projection`
    - **param:** Whether to fit the scene to the window.
      - *@name:* `zoomExtents`
    - **param:** Whether to animate the change to the projection.
      - *@name:* `animate`
    - **remarks:** The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.SetProjection(SpaceClaim.Api.V22.Geometry.Frame,System.Double)`
    - **summary:** Sets the view projection for the active view.
    - **param:** The view plane.
      - *@name:* `viewPlane`
    - **param:** The size of the view in model-space.
      - *@name:* `viewSize`
    - **remarks** This method can be used to set the view projection for a specific scene in the view.
            
            The projection is set so as to look flat onto the XY plane of the .
            The  of the  is centered in the view,
            and the orientation is with  to the right, and  up.
            
            The size of the scene is controlled by ,
            which is the model-space size that should fill the view.
            The  will occupy the smaller of the width or height of view.
            
            The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.
      - **para**
      - **paramref**
        - *@name:* `viewPlane`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.Origin`
      - **paramref**
        - *@name:* `viewPlane`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirX`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.DirY`
      - **para**
      - **paramref**
        - *@name:* `viewSize`
      - **paramref**
        - *@name:* `viewSize`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.TransformCamera(SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **summary:** Transforms the camera for the scene.
            The scene must be in FlyThrough mode

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.GetCameraFrame`
    - **summary:** Gets the camera's frame for the scene.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.CreateBitmap(System.Drawing.Size,System.Boolean,System.Boolean,SpaceClaim.Api.V22.Geometry.Matrix,System.Boolean)`
    - **summary:** Creates a bitmap image of the current scene shown in the window.
    - **param:** The size of the bitmap.
      - *@name:* `size`
    - **param:** Hides the grid.
      - *@name:* `hideGrid`
    - **param:** Hides the drawing sheet matte.
      - *@name:* `hideDrawingMatte`
    - **param:** The scene projection to use.
      - *@name:* `projection`
    - **param:** Whether to use a transparent background.
      - *@name:* `transparentBackground`
    - **returns:** A bitmap.
    - **remarks** This method is designed to create a thumbnail image,
            so  is expected to be smaller than the  of the window.
            
            If the aspect ratio of  does not match the aspect ratio of the  of the window,
            the resulting image will be cropped.
      - **paramref**
        - *@name:* `size`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.Size`
      - **para**
      - **paramref**
        - *@name:* `size`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.Size`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.SetClipVolume(SpaceClaim.Api.V22.Window.ClipViewShape,SpaceClaim.Api.V22.Geometry.Frame,System.Double)`
    - **summary:** Sets the clipping volume for the window.
    - **param:** The shape of the clipping volume.
      - *@name:* `shape`
    - **param:** A frame that defines the origin and orientation of the clipping volume.
      - *@name:* `frame`
    - **param:** The radius of the clipping volume.
      - *@name:* `radius`
    - **remarks** For a  clipping shape,  defines the center and orientation of the clipping region. 
            
            For a  clipping shape, the  property of  is used to define the center of the clipping region.
      - **b:** Box
      - **paramref**
        - *@name:* `frame`
      - **para**
      - **b:** Sphere
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Geometry.Frame.Origin`
      - **paramref**
        - *@name:* `frame`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Window.ClearClipVolume`

---
