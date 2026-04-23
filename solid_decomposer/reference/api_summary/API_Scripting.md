  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Extensibility.AddIn.ExecuteWindowsFormsCode(System.Threading.ThreadStart)`
    - **summary:** Executes code that uses Windows Forms, so that it runs in a single-threaded apartment.
    - **param:** The code to execute.
      - *@name:* `task`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.BarcodeCodePage.Windows1252`
    - **summary:** Windows-1252 (1252)

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.VideoCapture.Window`
    - **summary:** The active window should be captured.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.VideoCapture.Application`
    - **summary:** The application window should be captured.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Application`
    - **summary:** Provides application level methods and properties for SpaceClaim.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.VideoCodecs`
    - **summary:** Gets the video codecs found on this computer.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.StartVideo(System.String,SpaceClaim.Api.V22.VideoCapture,System.Int32,SpaceClaim.Api.V22.PixelDepth,System.Boolean)`
    - **summary:** Starts a video capture using the specified codec.
    - **param:** The full path of the AVI file to create.
      - *@name:* `path`
    - **param:** What to capture.
      - *@name:* `capture`
    - **param:** The codec to use.
      - *@name:* `codec`
    - **param:** The pixel depth.
      - *@name:* `pixelDepth`
    - **param:** Whether the video should be compressed.
      - *@name:* `compressed`
    - **remarks** The  is the FourCC id of the codec.
            
            The  property can be used to list installed video codecs.
      - **paramref**
        - *@name:* `codec`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Application.VideoCodecs`
    - **exception:** A video recording is already in progress.
      - *@cref:* `T:System.InvalidOperationException`
    - **exception:** The specified video codec was not found.
      - *@cref:* `T:System.InvalidOperationException`
    - **exception:** Failed to start video recording.
      - *@cref:* `T:System.InvalidOperationException`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.StopVideo`
    - **summary:** Stops the current video capture.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Application.ExitProposed`
    - **summary:** Occurs when it is proposed that the application should exit.
    - **remarks** An event handler can cancel the operation by calling .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.CancelStatus.Cancel`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Application.ExitAgreed`
    - **summary:** Occurs when the application is about to exit.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Application.ContextMenuOpening`
    - **summary:** Occurs when the context menu is about to be shown.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Application.RadialMenuOpening`
    - **summary:** Occurs when the radial menu is about to be shown.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Application.SessionRolled`
    - **summary:** Occurs when undo or redo has taken place.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Application.SessionRolledIncremental`
    - **summary:** Occurs when undo or redo has taken place. This event is fired for each undo step in a multi-step undo.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Application.SessionChanged`
    - **summary:** Occurs when a command has been executed which modified one or more documents.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.AllowRemoteAccess`
    - **summary:** Gets or sets whether this session allows remote access.
    - **remarks** If remote access is allowed, then clients on other machines on the network can attach to this session.
            
            Setting this property to  may cause Windows Firewall messages to be displayed.
      - **para**
      - **b:** true

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.UndoSteps`
    - **summary:** Gets the list of undo steps.
    - **remarks:** Each entry in the list contains the command text that appears on the undo drop-list.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.RedoSteps`
    - **summary:** Gets the list of redo steps.
    - **remarks:** Each entry in the list contains the command text that appears on the redo drop-list.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.Undo(System.Int32)`
    - **summary:** Performs an undo of the specified number of steps.
    - **param:** The number of undo steps to perform.
      - *@name:* `nSteps`
    - **exception:** The argument is out of range.
      - *@cref:* `T:System.ArgumentOutOfRangeException`
    - **remarks** If  is negative, a  is performed.
            
             and  can be used to check the number of steps available.
            
            This method cannot be called from inside the execution of a command.
      - **paramref**
        - *@name:* `nSteps`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Application.Redo(System.Int32)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Application.UndoSteps`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Application.RedoSteps`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.Redo(System.Int32)`
    - **summary:** Performs a redo of the specified number of steps.
    - **param:** The number of redo steps to perform.
      - *@name:* `nSteps`
    - **exception:** The argument is out of range.
      - *@cref:* `T:System.ArgumentOutOfRangeException`
    - **remarks** If  is negative, an  is performed.
            
             and  can be used to check the number of steps available.
            
            This method cannot be called from inside the execution of a command.
      - **paramref**
        - *@name:* `nSteps`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Application.Undo(System.Int32)`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Application.UndoSteps`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Application.RedoSteps`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.PurgeUndo(System.Int32)`
    - **summary:** Purges the undo history.
    - **param:** The number of undo steps to keep.
      - *@name:* `nStepsToKeep`
    - **remarks** The  argument specifies the number of undo steps to keep.
            It is harmless to supply a value greater than the current number of undo steps.
            To purge all undo history and free internal memory caches you can supply a value of zero. 
            
            This method cannot be called from inside the execution of a command.
      - **paramref**
        - *@name:* `nStepsToKeep`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.Exit`
    - **summary:** Exits the SpaceClaim session to which the API is attached.
    - **remarks** The API is attached to a SpaceClaim  using .
            
            To stop a different instance of SpaceClaim,  can be used.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Session`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Api.AttachToSession(SpaceClaim.Api.V22.Session)`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Session.Stop`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.MainWindow`
    - **summary:** Gets a window that can be supplied as the owner window when displaying modal dialogs.
    - **remarks** For example, the returned window can be supplied as the  argument to 
            or .
      - **i:** owner
      - **see**
        - *@cref:* `M:System.Windows.Forms.CommonDialog.ShowDialog(System.Windows.Forms.IWin32Window)`
      - **see**
        - *@cref:* `M:System.Windows.Forms.MessageBox.Show(System.Windows.Forms.IWin32Window,System.String,System.String)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.BringToFront`
    - **summary:** Moves the application in front of all other windows.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.IsVisible`
    - **summary:** Gets or sets whether the application is visible.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.IsRibbonMinimized`
    - **summary:** Gets or sets whether the application ribbon is minimized.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.ReportStatus(System.String,SpaceClaim.Api.V22.StatusMessageType,SpaceClaim.Api.V22.Task)`
    - **summary:** Displays a message in the SpaceClaim status log.
    - **param:** Message to display.
      - *@name:* `message`
    - **param:** Type of message.
      - *@name:* `messageType`
    - **param** Code to execute if the user clicks on the message; or .
      - *@name:* `messageHandler`
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.CheckLicense(System.String)`
    - **summary:** Checks for the existence of a SpaceClaim license.
    - **param:** The name of the license to check.
      - *@name:* `name`
    - **returns** Returns  if the license exists; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.Version`
    - **summary:** Gets the version of SpaceClaim that is running.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.UserOptions`
    - **summary:** Gets or sets the current user options.
    - **remarks** The returned  object contains a snapshot of the current user options.
            Changes to option properties will not affect the user options until the 
            property is set to the new options value.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Options`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Application.UserOptions`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.TitleBarPrefix`
    - **summary:** Gets or sets the title bar prefix.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Application.TitleBarSuffix`
    - **summary:** Gets or sets the title bar suffix.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddPropertyDisplay(SpaceClaim.Api.V22.PropertyDisplay)`
    - **summary:** Adds a property display to the properties panel in the user interface.
    - **param:** The property display to be added.
      - *@name:* `display`
    - **remarks** See remarks in .
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.PropertyDisplay`
    - **seealso**
      - *@cref:* `T:SpaceClaim.Api.V22.PropertyDisplay`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddPanelContent(SpaceClaim.Api.V22.Command,System.Windows.Forms.Control,SpaceClaim.Api.V22.Panel)`
    - **summary:** Adds custom content that can be displayed in a built-in panel, replacing the standard content.
    - **param:** A command to control the visibility of the custom content.
      - *@name:* `command`
    - **param:** The custom content to display.
      - *@name:* `content`
    - **param:** The panel whose content is to be replaced.
      - *@name:* `panel`
    - **remarks** The  property of the  controls whether the
            built-in panel has its content replaced.  If  is , the
            replacement  is shown, otherwise the standard content is shown.
            
            This facility can be used to customize built-in panels when a custom window tab is activated.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.IsVisible`
      - **paramref**
        - *@name:* `command`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.IsVisible`
      - **b:** true
      - **paramref**
        - *@name:* `content`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.ShowPanel(SpaceClaim.Api.V22.Panel,System.Boolean)`
    - **summary:** Shows or hides a built-in panel.
    - **param:** The panel to show or hide.
      - *@name:* `panel`
    - **param** to show and activate the panel; otherwise .
      - *@name:* `show`
      - **b:** true
      - **b:** false
    - **remarks** If  is , the panel is hidden.
            
            If  is , the panel is shown and brought to the front of its tab group.
      - **paramref**
        - *@name:* `show`
      - **b:** false
      - **para**
      - **paramref**
        - *@name:* `show`
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.ShowPanel(SpaceClaim.Api.V22.Panel,System.Boolean,System.Boolean)`
    - **summary:** Shows or hides a built-in panel, allowing control over whether the panel is made active.
    - **param:** The panel to show or hide.
      - *@name:* `panel`
    - **param** to show the panel; otherwise .
      - *@name:* `show`
      - **b:** true
      - **b:** false
    - **param** to activate the panel; otherwise .
      - *@name:* `activate`
      - **b:** true
      - **b:** false
    - **remarks** If  is , the panel is hidden.
            
            If  and  are , the panel is brought to the front of its tab group.
      - **paramref**
        - *@name:* `show`
      - **b:** false
      - **para**
      - **paramref**
        - *@name:* `show`
      - **paramref**
        - *@name:* `activate`
      - **b:** true

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.SetAllowPanelActivation(SpaceClaim.Api.V22.Panel,System.Boolean)`
    - **summary:** Sets whether a panel can be automatically made visible and activated.
    - **param:** The panel.
      - *@name:* `panel`
    - **param** to allow automatic activation; otherwise .
      - *@name:* `allowActivation`
      - **b:** true
      - **b:** false
    - **remarks** An example of a panel which can be automatically activated is the Properties panel (by selecting a note). 
            If  is set to false, then the panel will not be activated.
            
            The default value is true.
      - **i:** allowActivation
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.GetAllowPanelActivation(SpaceClaim.Api.V22.Panel)`
    - **summary:** Gets whether a panel can be automatically made visible and activated.
    - **param:** The panel.
      - *@name:* `panel`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddOptionsPage(SpaceClaim.Api.V22.OptionsPage)`
    - **summary:** Adds a page to the options dialog.
    - **param:** The options page to be added.
      - *@name:* `page`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddFileHandler(SpaceClaim.Api.V22.FileOpenHandler)`
    - **summary:** Adds a handler for a file filter to the File Open dialog.
    - **param:** The handler to be added.
      - *@name:* `handler`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddFileHandler(SpaceClaim.Api.V22.FileSaveHandler)`
    - **summary:** Adds a handler for a file filter to the File Save dialog.
    - **param:** The handler to be added.
      - *@name:* `handler`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddSheetMetalFormHandler(SpaceClaim.Api.V22.Command,SpaceClaim.Api.V22.SheetMetalFormHandler)`
    - **summary:** Adds a handler for a custom sheet metal form.
    - **param:** A command to use for the button in the Forms Gallery.
      - *@name:* `command`
    - **param:** A handler for the custom form.
      - *@name:* `handler`
    - **remarks** The  is used for the appearance of the button in the Forms Gallery.
            The Forms Gallery will take care of the operation of the button when it is pressed, and the  will be called.
            You should not attempt to handle the  event of the command yourself,
            since this may interfere with the correct operation of the Forms Gallery.
      - **paramref**
        - *@name:* `command`
      - **paramref**
        - *@name:* `handler`
      - **see**
        - *@cref:* `E:SpaceClaim.Api.V22.Command.Executing`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddSheetMetalBendHandler(SpaceClaim.Api.V22.SheetMetalBendHandler)`
    - **summary:** Adds a handler for a custom sheet metal form.
    - **param:** A handler for the custom bend.
      - *@name:* `handler`
    - **remarks**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddSelectionHandler``1(SpaceClaim.Api.V22.SelectionHandler{``0})`
    - **summary:** Adds a handler for custom selection behavior.
    - **typeparam:** The type of object to which this handler is bound.
      - *@name:* `TDocObject`
    - **param:** The handler to be added.
      - *@name:* `handler`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddCommandFilter(SpaceClaim.Api.V22.NativeCommand,SpaceClaim.Api.V22.CommandFilter)`
    - **summary:** Adds a command filter for a native (built-in) command.
    - **param:** The native command to which the filter applies.
      - *@name:* `command`
    - **param:** A command filter to use for the native command.
      - *@name:* `filter`
    - **remarks** When the native command is executed, the  method
            is called, giving the filter first chance to handle the command.
            Any remaining or additional objects returned from the  method are then processed by the native command.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.CommandFilter.Apply(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.CommandFilter.Apply(System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.AddRecentFile(System.String)`
    - **summary:** Adds a file to the recently used files list.
    - **param:** The full path of the file.
      - *@name:* `path`
    - **remarks** This methods adds a file to the Recent Documents list on the File menu.
            
            When the user opens or saves files using the user interface, these files are automatically
            added to the Recent Documents list on the File menu.
            In contrast, when the API is used to open or save files, e.g. using 
            or  methods, no files are added to the Recent Documents list,
            because the API might be loading files from a library location unknown to the user.
            To add a file to the Recent Documents list, you can call .
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Document.Open(System.String,SpaceClaim.Api.V22.ImportOptions)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Document.Save`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Application.AddRecentFile(System.String)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.ExecuteOnMainThread(SpaceClaim.Api.V22.Task)`
    - **summary:** Executes code asynchronously on the main application thread.
    - **param:** The code to execute
      - *@name:* `task`
    - **remarks** This method can be used instead of the following method of running code on the main thread:
            
            The above code, which calls  directly, had limitations in that it would not work if the  attribute 
            in the add-in manifest was set to . This method has no such limitation.
      - **code**
        ``` 
        
            System.Windows.Forms.Application.OpenForms[0].BeginInvoke(new Task(() => {
            	// Code to be executed
            }));
            
        ```
      - **i:** BeginInvoke
      - **b:** host
      - **i:** NewAppDomain

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.OpenInKeyShot(System.String)`
    - **summary:** Opens the specified .bip file in KeyShot.
    - **param:** The KeyShot .bip file to open.
      - *@name:* `bipFilename`
    - **returns** Returns  if KeyShot was started with the requested file; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.RunScript(System.String)`
    - **summary:** Runs a script file (*.scscript or *.py).
    - **param** The path to the script file. The script file can have either be an  or a  extension.
      - *@name:* `filename`
      - **i:** .scscript
      - **i:** .py
    - **returns** Returns  if the script file was found and was able to be run; otherwise .
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.RunScript(System.String,System.Collections.Generic.Dictionary{System.String,System.Object})`
    - **summary:** Runs a script file (*.scscript or *.py).
    - **param** The path to the script file. The script file can have either be an  or a  extension.
      - *@name:* `filename`
      - **i:** .scscript
      - **i:** .py
    - **param:** The argument dictionary of named value pairs.
      - *@name:* `argDictionary`
    - **returns** Returns  if the script file was found and was able to be run; otherwise .
      - **b:** true
      - **b:** false
    - **example** Example usage:
             
             
             
             Then to access the argument named "Name" in the Python script:
      - **code:** var scriptParams = new Dictionary<string, object>();
             scriptParams.Add("Name", "Testing");
             Application.RunScript(@"c:\Test.py", scriptParams);
      - **code:** value = argsDict["Name"]

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.RunScript(System.String,System.Collections.Generic.Dictionary{System.String,System.Object},System.Object@)`
    - **summary:** Runs a script file (*.scscript or *.py).
    - **param** The path to the script file. The script file can have either be an  or a  extension.
      - *@name:* `filename`
      - **i:** .scscript
      - **i:** .py
    - **param:** The argument dictionary of named value pairs.
      - *@name:* `argDictionary`
    - **param:** The result out parameter.
      - *@name:* `result`
    - **returns** Returns  if the script file was found and was able to be run; otherwise .
      - **b:** true
      - **b:** false
    - **example** Example usage:
             
             
             
             Then to access the argument named "Name" in the Python script:
      - **code:** var scriptParams = new Dictionary<string, object>();
             scriptParams.Add("Name", "Testing");
             Application.RunScript(@"c:\Test.py", scriptParams);
      - **code:** value = argsDict["Name"]

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.RunScriptAsync(System.String,System.Collections.Generic.Dictionary{System.String,System.Object},System.Action{System.Boolean,System.Object})`
    - **summary:** Runs a script file on a background thread (*.scscript or *.py).
    - **param** The path to the script file. The script file can have either be an  or a  extension.
      - *@name:* `filename`
      - **i:** .scscript
      - **i:** .py
    - **param:** The argument dictionary of named value pairs.
      - *@name:* `argDictionary`
    - **param:** The action to perform after script completes. The first argument specifies if the script passes, the second argument is a result that can be set in the script.
      - *@name:* `onScriptComplete`
    - **returns** Returns  if the script file was found and was able to be run; otherwise .
      - **b:** true
      - **b:** false
    - **example** Example usage:
             
             
             
             Then to access the argument named "Name" in the Python script:
             
             
             To specify a result for the "onScriptComplete" action, set a "result" variable in the script:
      - **code:** var scriptParams = new Dictionary<string, object>();
             scriptParams.Add("Name", "Testing");
             Application.RunScriptAsync(@"c:\Test.py", scriptParams, (pass, result) => {
            		if (pass)
            			MessageBox.Show(result.ToString())
             });
      - **code:** value = argsDict["Name"]
      - **code:** result = "Hello World"

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Application.RunPerformanceTest(System.Boolean,System.Int32)`
    - **summary:** Runs a graphics performance test.
    - **param:** Whether to show the performance report window.
      - *@name:* `showReport`
    - **param:** The number of times to rotate the model. Each rotation is 36 frames.
      - *@name:* `numRotations`
    - **returns:** The frame rate (fps)

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.SelectionResult`
    - **summary:** Describes a selection result which appears in the Selection panel.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SelectionResult.Create(System.String,System.Collections.Generic.ICollection{SpaceClaim.Api.V22.IDocObject})`
    - **summary** Creates data for a selection result. .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.SelectionHandler`1.CreateSelectionResults(`0)`
    - **param:** Text to show in the result.
      - *@name:* `label`
    - **param:** A list of items to include in the result.
      - *@name:* `items`
    - **returns:** A selection result.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.SelectionHandler`1`
    - **summary:** Abstract base class for a selection handler.
    - **typeparam:** The type of object to which this handler is bound.
      - *@name:* `TDocObject`
    - **remarks** This handler can be used to modify selection behavior for a type of object, specified using
            .
      - **typeparamref**
        - *@name:* `TDocObject`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SelectionHandler`1.CreateSelectionResults(`0)`
    - **summary:** Creates additional results for display in the Selection panel.
    - **param:** The object to be used as a seed for the results.
      - *@name:* `selectedObject`
    - **returns** A collection of  results. Collection may be empty.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.SelectionResult`
    - **remarks:** The code within this method may be executed in a separate worker thread, so it should only read data and not modify.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SelectionHandler`1.GetToolbarLayout(System.Collections.Generic.ICollection{`0})`
    - **summary:** Gets the mini-toolbar to be shown when objects of a type are selected
    - **param**
      - *@name:* `selectedObjects`
    - **returns**
    - **remarks:** The toolbar layout is only available in SpaceClaim. Overriding this method does not anything in Discovery.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SelectionHandler`1.ActivateToolOnSelection(`0)`
    - **summary:** Controls whether an object-specific tool is activated on selection.
    - **param**
      - *@name:* `selectedObject`
    - **returns**
    - **remarks** An example of a tool that may be started automatically is the Notes Edit Tool.
            
            If this method is not overridden, the default value is true.
      - **br**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.SelectionHandler`1.GetToolOnFullEdit(`0)`
    - **summary** Determines the tool to set when full edit mode is enabled for an object of type .
      - **typeparamref**
        - *@name:* `TDocObject`
    - **param:** The object for which full edit mode has been enabled.
      - *@name:* `selectedObject`
    - **returns:** The tool to be set.
    - **remarks:** Full edit mode is only available in Discovery. Overriding this method does not do anything in SpaceClaim.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Internal.AnsysMethods.EnableDragDropPreSelection(System.String)`
    - **summary:** Enable preselection when dragging files into scene
    - **param:** Extensions separated by ";", example = ".txt;.csv"
      - *@name:* `filter`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Unsupported.IScriptSelection.Items`
    - **summary:** Gets the list of DocObjects in selection

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.Application.OverrideOpenFileFilter(System.String,System.Int32)`
    - **summary:** OverrideOpenFileFilter
    - **param:** Gets or sets the current file name filter string, which determines the choices that appear in the "Files of type" box in the dialog box.
      - *@name:* `filterString`
    - **param:** A value containing the index of the filter currently selected in the file dialog box. The filter index starts at 1 so the default value is 1.
      - *@name:* `defaultFilterIndex`
    - **remarks:** For each filtering option, the filter string contains a description of the filter, followed by the vertical bar (|) and the filter pattern. The strings for different filtering options are separated by the vertical bar.
             The following is an example of a filter string:
            
             Text files(*.txt)|*.txt|All files(*.*)|*.*
            
             You can add several filter patterns to a filter by separating the file types with semicolons, for example:
             
             Image Files(*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files(*.*)|*.*

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Unsupported.Application.SetSelectionToolOn3D`
    - **summary:** On the change of mode to 3D, set the selection tool instead of the pull tool

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Unsupported.UnsupportedApplicationStatic.TerminateCommand`
    - **summary:** Only terminates readable commands

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.SelectionOrder`
    - **summary:** Selection hit-test ordering

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionOrder.ForceTop`
    - **summary:** Custom objects are always at the top of the hit list.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionOrder.ByDistance`
    - **summary:** Custom objects appear in the hit list based on distance.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.LightweightCustomWrapper.AdjustTransformToWindow`
    - **summary:** Gets whether Move Tool handles should be repositioned to ensure they are visible in the window.
    - **remarks** Return  if the handles should be repositioned (default), or  if they should be left in the position returned by .
      - **b:** true
      - **b:** false
      - **see:** TryGetTransformFrame
        - *@cref:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper.TryGetTransformFrame(SpaceClaim.Api.V22.Geometry.Frame@,SpaceClaim.Api.V22.Geometry.Transformations@)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.LightweightCustomWrapper.SelectionOrder`
    - **summary:** Gets or sets the selection ordering method.
    - **remarks:** SelectionOrder.ForceTop is the default.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper`1.#ctor(SpaceClaim.Api.V22.Window)`
    - **summary:** Constructs a new custom object and a wrapper for it.
    - **param**
      - *@name:* `window`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LightweightCustomWrapper`1.GetChildren(SpaceClaim.Api.V22.Window)`
    - **summary:** Gets custom wrappers for child custom objects.
    - **param**
      - *@name:* `window`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WorkbenchImportOptions.ImportNamedSelections`
    - **summary** Gets or sets Workbench preference to import Named Selections (default = ).
      - **b:** false
    - **exclude**

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WorkbenchImportOptions.namedSelectionKey`
    - **summary** Gets or sets Workbench preference for Named Selection prefix key (default = ).
      - **b:** ""
    - **exclude**

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DesignWindowOptions`
    - **summary:** An object containing design window options.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DrawingWindowOptions`
    - **summary:** A object containing drawing window options.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.DrawingWindowOptions.AllowRotation`
    - **summary** Gets or sets whether to allow drawing sheets to be rotated so that they are not flat-on (default = ).
      - **b:** true

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.SelectionFilterType`
    - **Summary:** A bitmask for defining a selection filter for a window

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Smart`
    - **summary:** Smart selection is on.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Planes`
    - **summary:** Select planes.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Axes`
    - **summary:** Select axes.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Images`
    - **summary:** Select images.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Vertices`
    - **summary:** Select vertices.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Bodies`
    - **summary:** Select bodies.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Notes`
    - **summary:** Select notes.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.Dimensions`
    - **summary:** Select dimensions.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.OtherAnnotations`
    - **summary:** Select annotation types other than notes and dimensions.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.AllAnnotations`
    - **summary:** Select all annotation types.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.SelectionFilterType.All`
    - **summary:** Selects all types.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.WindowSplit`
    - **summary:** Base class describing how a window has been split into multiple panes.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.WindowTab`
    - **summary:** A custom window tab.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.WindowTab.ActiveTabChanged`
    - **summary** Occurs when the  has changed.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.WindowTab.ActiveTab`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WindowTab.Create(SpaceClaim.Api.V22.Command,System.Windows.Forms.Control,SpaceClaim.Api.V22.WindowTabHandler)`
    - **summary:** Creates a custom window tab.
    - **param:** The command to supply the image and text for the tab.
      - *@name:* `command`
    - **param:** The contents to be displayed.
      - *@name:* `control`
    - **param** A handler to receive notifications, or .
      - *@name:* `handler`
      - **b:** null
    - **returns:** A window tab.
    - **remarks** This method adds a custom window tab to the user interface, whose contents are defined by a Windows Forms .
            
            The  supplies the  and  for the tab,
            and its  property controls the visibility of the tab.
      - **see**
        - *@cref:* `T:System.Windows.Forms.Control`
      - **para**
      - **paramref**
        - *@name:* `command`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.Image`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.Text`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.IsVisible`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.WindowTab.ActiveTab`
    - **summary:** Gets the active window tab.
    - **remarks** If no custom window tab is active, the value is .
            
            A  can be activated by calling .
            
            Since other add-ins may also use custom window tabs, you should never assume that
            the  was created by your add-in.
            Always test the  to see whether the window tab is one of yours.
      - **b:** null
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.WindowTab`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tab.Activate`
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.WindowTab.ActiveTab`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Tab.Command`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WindowTab.GetTabs(SpaceClaim.Api.V22.Command)`
    - **summary:** Gets window tabs for a command.
    - **param:** A command.
      - *@name:* `command`
    - **returns:** Window tabs for that command.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.WindowTabHandler`
    - **summary:** A notification handler for a custom window tab.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WindowTabHandler.OnActivated(SpaceClaim.Api.V22.WindowTab)`
    - **summary:** Called when a window tab is activated.
    - **param:** The window tab that was activated.
      - *@name:* `tab`
    - **remarks** A custom window tab can display any kind of content, e.g. a graph, a spreadsheet, or a web page.
            So in general a custom window is foreign to built-in commands.  Therefore, the default implementation
            of  sets the  to .
            
            If your custom window tab embeds a  using ,
            you should activate that window in your override instead of calling the base implementation;
            otherwise you should call the base implementation, followed by whatever else you might want to
            do when the window tab is activated (e.g. change its display style to indicate that it is active).
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.WindowTabHandler.OnActivated(SpaceClaim.Api.V22.WindowTab)`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.ActiveWindow`
      - **b:** null
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Window`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.CreateEmbedded(SpaceClaim.Api.V22.Part,SpaceClaim.Api.V22.EmbeddedWindowHandler)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WindowTabHandler.OnDeactivated(SpaceClaim.Api.V22.WindowTab)`
    - **summary:** Called when a window tab is deactivated.
    - **param:** The window tab that was deactivated.
      - *@name:* `tab`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WindowTabHandler.OnClosing(SpaceClaim.Api.V22.WindowTab)`
    - **summary:** Called when a window tab is closing.
    - **param:** The window tab being closed.
      - *@name:* `tab`
    - **returns** to proceed with closing the window tab, or  to cancel.
      - **b:** true
      - **b:** false

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.WindowTabHandler.GetRelatedWindow(SpaceClaim.Api.V22.WindowTab)`
    - **summary:** Gets the related built-in window for a window tab.
    - **param:** The window tab.
      - *@name:* `tab`
    - **returns** The related window, or  if there is no related window.
      - **b:** null
    - **remarks** If the custom window embeds a  using ,
            then  should be overridden so that the embedded  is
            activated when the custom window tab is activated.
            
            Sometimes a custom window does not embed a window, but it displays information, which is related to a built-in window.
            In this case,  can be overridden, so that the Save command is
            available when the custom window tab is active.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Window`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.CreateEmbedded(SpaceClaim.Api.V22.Part,SpaceClaim.Api.V22.EmbeddedWindowHandler)`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.WindowTabHandler.OnActivated(SpaceClaim.Api.V22.WindowTab)`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Window`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.WindowTabHandler.GetRelatedWindow(SpaceClaim.Api.V22.WindowTab)`

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.EmbeddedWindowHandler`
    - **summary:** Provides control for an embedded window.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.EmbeddedWindowHandler.OnCreate(SpaceClaim.Api.V22.Window,System.Windows.Forms.Control)`
    - **summary:** Called when the embedded window is being created.
    - **param:** The embedded window.
      - *@name:* `window`
    - **param:** The control to embed.
      - *@name:* `control`
    - **remarks** This method is called when  is called.
            
            It is also called when a  command causes the embedded window to be re-created,
            or the  command causes it to be un-deleted.
            In either case a new  is created for the ,
            and the window becomes alive again ( now returns ).
            
            This method should be overridden to start hosting the control in some user interface.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.CreateEmbedded(SpaceClaim.Api.V22.Part,SpaceClaim.Api.V22.EmbeddedWindowHandler)`
      - **para**
      - **b:** Redo
      - **b:** Undo
      - **paramref**
        - *@name:* `control`
      - **paramref**
        - *@name:* `window`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.IsDeleted`
      - **b:** false
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.EmbeddedWindowHandler.OnDelete(SpaceClaim.Api.V22.Window)`
    - **summary:** Called when the embedded window is being deleted.
    - **param:** The embedded window.
      - *@name:* `window`
    - **remarks** This method is called when the  method is called on the window.
            
            It is also called when a  command causes the embedded window to be un-created,
            or the  command causes it to be re-deleted.
            
            This method should be overridden to stop hosting the control.
            
            The  method should be called to delete the control.
            If the control is hosted in a  and the form is closed,
            the control will be disposed automatically.
            
            The control must only be disposed inside this method.
            It must not be disposed at any other time.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.Delete`
      - **para**
      - **b:** Undo
      - **b:** Redo
      - **para**
      - **para**
      - **see**
        - *@cref:* `M:System.Windows.Forms.Control.Dispose(System.Boolean)`
      - **see**
        - *@cref:* `T:System.Windows.Forms.Form`
      - **para**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.EmbeddedWindowHandler.OnActivate(SpaceClaim.Api.V22.Window)`
    - **summary:** Called when the embedded window is activated.
    - **param:** The embedded window.
      - *@name:* `window`
    - **remarks** The default implementation does nothing.
            
            Override this method to indicate to the user that the embedded window is now the .
            For example, if the control hosted in a , you might call  to
            bring that form to the front.
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.ActiveWindow`
      - **see**
        - *@cref:* `T:System.Windows.Forms.Form`
      - **see**
        - *@cref:* `M:System.Windows.Forms.Control.BringToFront`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.FileOpenHandler.OpenFile(System.String,SpaceClaim.Api.V22.Window)`
    - **summary:** Opens the file.
    - **param:** Full path to the file.
      - *@name:* `path`
    - **param:** The target window, if this is a drag and drop operation.
      - *@name:* `targetWindow`
    - **remarks:** Override this method to open a file matching the file filter.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.OptionsPage.OnLoad(System.Windows.Forms.Control)`
    - **summary:** Called when the options page needs to be populated.
    - **param:** The control displayed in the options page.
      - *@name:* `control`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.OptionsPage.OnSave(System.Windows.Forms.Control)`
    - **summary:** Called when the options page needs to be saved.
    - **param:** The control displayed in the options page.
      - *@name:* `control`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Session.MainWindowTitle`
    - **summary:** Gets the title of the main window of the process.
    - **remarks:** This property might be used to distinguish between multiple SpaceClaim sessions on the same machine.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.StartupOptions.ShowApplication`
    - **summary** Gets or sets whether to show the application (default = ).
      - **b:** true
    - **remarks** If the value is , the application is started in an invisible state.
            The  property of the  class
            can be used to change the visibility of the application after it has started.
      - **b:** false
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Application.IsVisible`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Application`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.StartupOptions.WindowState`
    - **summary** Gets or sets the window location and size to use (default = ).
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LengthConverter.#ctor(SpaceClaim.Api.V22.Window)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.LengthConverter.#ctor(SpaceClaim.Api.V22.Window,System.Boolean)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.LengthConverter.#ctor(SpaceClaim.Api.V22.Window,System.Boolean)`
    - **summary:** Constructs a length converter.
    - **param:** The window that will provide units conversion.
      - *@name:* `window`
    - **param:** Whether the formatted value is forced to be positive.
      - *@name:* `absolute`
    - **remarks** When used with a , the  should be the  of the tool.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.ReadoutField`
      - **paramref**
        - *@name:* `window`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Window`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AngleConverter.#ctor(SpaceClaim.Api.V22.Window)`
    - **inheritdoc**
      - *@cref:* `M:SpaceClaim.Api.V22.AngleConverter.#ctor(SpaceClaim.Api.V22.Window,System.Boolean)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.AngleConverter.#ctor(SpaceClaim.Api.V22.Window,System.Boolean)`
    - **summary:** Constructs an angle converter.
    - **param:** The window that will provide units conversion.
      - *@name:* `window`
    - **param:** Whether the formatted value is forced to be positive.
      - *@name:* `absolute`
    - **remarks** When used with a , the  should be the  of the tool.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.ReadoutField`
      - **paramref**
        - *@name:* `window`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Window`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.Panel.Selection`
    - **summary:** The selection panel.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ProgressTracker.UsePopupWindow`
    - **summary:** Gets or sets whether to use the progress popup window.
    - **remarks** If , the progress popup window will be shown approximately 3 seconds after a long operation has begun.
            
            The default value is .
      - **b:** true
      - **para**
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.CustomWrapper.SelectionOrder`
    - **summary:** Gets or sets the selection ordering method.
    - **remarks:** SelectionOrder.ForceTop is the default.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.ApplicationVersion`
    - **summary:** The version information for the application.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ApplicationVersion.MajorReleaseNumber`
    - **summary:** Gets the major release number of the application.
    - **remarks** The major release number is a simple integer that increases for each major release of SpaceClaim,
            but which is the same for each minor release and service pack.
            Here are some example minor release numbers:
            
            SpaceClaim 2014 = 11
            SpaceClaim 2015 = 12
            SpaceClaim 2016 = 17
            
            Note that there was a jump from 12 to 17 at SpaceClaim 2016 to align with ANSYS release numbers.
      - **para**
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ApplicationVersion.MinorReleaseNumber`
    - **summary:** Gets the minor release number of the application.
    - **remarks** The minor release number is a simple integer that increases for each minor release of SpaceClaim,
            but which is the same for each service pack.
            Here are some example minor release numbers:
            
            SpaceClaim 2016 = 0
            SpaceClaim 2016.1 = 1
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.ApplicationVersion.ServicePack`
    - **summary:** Get the service pack of the application.
    - **remarks:** The initial release has a service pack of zero.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.ApplicationWindowState`
    - **summary:** Specifies the location and size to use when starting a session.
    - **remarks** See  for more information.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.StartupOptions.WindowState`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.InteractionContext.Window`
    - **summary:** Gets the window to which this interaction context belongs.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.InteractionContext.Selection`
    - **summary:** Gets or sets the selection in the window, in context-space.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.InteractionContext.SecondarySelection`
    - **summary:** Gets or sets the secondary selection in the window, in context-space.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.InteractionContext.GetSelection``1`
    - **summary:** Gets the selected objects of the specified type, in context-space.
    - **typeparam:** The type of objects desired.
      - *@name:* `TDocObject`
    - **returns:** Selected objects of the specified type.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.InteractionContext.SingleSelection`
    - **summary:** Gets or sets the current single selection in the window, in context-space.
    - **remarks** In general, many objects can be selected,
            however, it is common to test whether a single object is selected, and if so, obtain that object.
            This property returns the single selection, or  if either no objects are selected, or more than one object is selected.
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Options.ResetSelectionFilterOnToolChange`
    - **summary** Gets or sets whether to reset the selection filter when a tool changes (default = ).
      - **b:** true

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Options.DesignWindow`
    - **summary:** Gets the design window options.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Options.DrawingWindow`
    - **summary:** Gets the drawing window options.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Tool.SelectionTypes`
    - **summary:** Gets or sets the types of object that can be selected by the user.
    - **remarks** The value is a collection of types, which may be interfaces or doc object classes.
            Only objects that satisfy one of these types can be selected by the user.
            
            The default value is one type, , which effectively means no filtering is done.
            
            If the value is set to an empty collection, no objects can be selected.
            
            To filter the selection by criteria other than type,  can be overridden.
            See that method for more information.
      - **para**
      - **c** typeof()
        - **see**
          - *@cref:* `T:SpaceClaim.Api.V22.IDocObject`
      - **para**
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.AdjustSelection(SpaceClaim.Api.V22.IDocObject)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Tool.AdjustSelection(SpaceClaim.Api.V22.IDocObject)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Tool.AdjustSelection(SpaceClaim.Api.V22.IDocObject)`
    - **summary:** Adjusts or filters objects being selected.
    - **param:** The object to be tested.
      - *@name:* `docObject`
    - **returns** The object to select, or  to filter out this object.
      - **b:** null
    - **remarks** To filter objects by type,  should be set.
            After filtering by type,  is called to determine the object to be selected.
            
            The default implementation simply returns the incoming  so that no filtering is done.
            Override this method to perform filtering so that only desired objects are selected.
            
            Filtering is done on the preselection so that only suitable objects are prehighlighted.
            The method can return  to filter out an object;
            it can return the same object in order to allow that object;
            or it can return a different object, for example to preselect a design body when the user hovers over a design face or design edge.
            
            Filtering is also done on the current selection when the tool is activated,
            and it is done when the Select All command is chosen.
            In these situations, the selection is merely filtered, and not adjusted.
            If the method returns the same object, the object is accepted, otherwise it is filtered out.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Tool.SelectionTypes`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Tool.AdjustSelection(SpaceClaim.Api.V22.IDocObject)`
      - **para**
      - **paramref**
        - *@name:* `docObject`
      - **para**
      - **b:** null
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Tool.Window`
    - **summary:** Gets the window to which this tool is assigned.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Command.GetCommand(System.Windows.Forms.Keys)`
    - **summary:** Gets the command with the specified shortcut.
    - **param:** The shortcut.
      - *@name:* `shortcut`
    - **returns** The command with the specified shortcut; else  if no such command exists.
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.PanelTab.Create(SpaceClaim.Api.V22.Command,System.Windows.Forms.Control,SpaceClaim.Api.V22.Panel)`
    - **summary:** Creates a custom panel tab.
    - **param:** A command to supply the image and text for the tab.
      - *@name:* `command`
    - **param:** The content to be displayed.
      - *@name:* `content`
    - **param:** A built-in panel used to identify the panel group for the custom panel.
      - *@name:* `companionPanel`
    - **returns:** The new panel.
    - **remarks** This method adds a custom panel tab to the user interface, whose contents are defined by a Windows Forms .
            
            The panel is created in the same panel group as the existing .
            
            The  supplies the  and  for the tab,
            and its  property controls the visibility of the tab.
            
            Built-in panels do not show images on their tabs.
            Supplying a command with a  image will achieve this standard appearance.
      - **see**
        - *@cref:* `T:System.Windows.Forms.Control`
      - **para**
      - **paramref**
        - *@name:* `companionPanel`
      - **para**
      - **paramref**
        - *@name:* `command`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.Image`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.Text`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.IsVisible`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.PanelTab.Create(SpaceClaim.Api.V22.Command,System.Windows.Forms.Control,SpaceClaim.Api.V22.DockLocation,System.Int32,System.Boolean)`
    - **summary:** Creates a custom panel tab.
    - **param:** A command to supply the image and text for the tab.
      - *@name:* `command`
    - **param:** The content to be displayed.
      - *@name:* `content`
    - **param:** The docking location.
      - *@name:* `dockLocation`
    - **param:** The width or height of the docking bar.
      - *@name:* `size`
    - **param** to lock the panel and prevent undocking; otherwise
      - *@name:* `isLocked`
      - **b:** true
      - **b:** false
    - **returns:** The new panel.
    - **remarks** This method adds a custom panel tab to the user interface, whose contents are defined by a Windows Forms .
            
            The  supplies the  and  for the tab,
            and its  property controls the visibility of the tab.
            
            Built-in panels do not show images on their tabs.
            Supplying a command with a  image will achieve this standard appearance.
      - **see**
        - *@cref:* `T:System.Windows.Forms.Control`
      - **para**
      - **paramref**
        - *@name:* `command`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.Image`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.Text`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Command.IsVisible`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.Window`
    - **summary:** A graphical interaction window, showing a part or a drawing sheet.
    - **remarks** Some information about the scene in the window, such as the current selection and the section plane,
            is presented by an  object.
             is typically used to obtain the interaction context,
            but  and  may also be used.
            
            See  for more information.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.InteractionContext`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.ActiveContext`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.SceneContext`
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.GetContext(SpaceClaim.Api.V22.IDocObject)`
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.InteractionContext`
    - **seealso**
      - *@cref:* `T:SpaceClaim.Api.V22.InteractionContext`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.ActiveWindowChanged`
    - **summary** Occurs when the  has changed.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.ActiveWindow`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.SelectionChanged`
    - **summary:** Occurs when the selection changes.
    - **remarks** This event is raised when the  of the  has changed.
            The selection in any other  for this window is the subset of the scene selection
            that can be mapped into context-space, so this subset may not have changed even though the selection in the overall scene has.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.Selection`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.SceneContext`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.InteractionContext`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.WindowSelectionChanged`
    - **summary:** Occurs when the selection of the active window changes.
    - **remarks** This event is raised when the selection has changed, either because it has changed in
            the , or because another window has become active.
            The second argument of the event handler has a  property,
            which returns the window that contains the new selection.
            
            If the event was raised because the last window was closed, then the subject will be .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.ActiveWindow`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SubjectEventArgs`1.Subject`
      - **para**
      - **b:** null

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.PreselectionChanged`
    - **summary:** Occurs when the preselection changes.
    - **remarks** This event is raised when the  of the  has changed.
            The preselection in any other  for this window may not have changed.
            See  for on why this is.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.Preselection`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.SceneContext`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.InteractionContext`
      - **see**
        - *@cref:* `E:SpaceClaim.Api.V22.Window.SelectionChanged`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.WindowPreselectionChanged`
    - **summary:** Occurs when the preselection of any window changes.
    - **remarks** The second argument of the event handler has a  property,
            which returns the window that contains the new preselection.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SubjectEventArgs`1.Subject`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.WindowOpened`
    - **summary:** Occurs when a window is opened.
    - **remarks** The second argument of the event handler has a  property,
            which returns the window that was opened.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SubjectEventArgs`1.Subject`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.WindowCloseProposed`
    - **summary:** Occurs when it is proposed that a window should close.
    - **remarks** The second argument of the event handler has a  property,
            which returns the window to be closed.
            
            An event handler can cancel the operation by calling .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SubjectEventArgs`1.Subject`
      - **para**
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.CancelStatus.Cancel`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.WindowCloseAgreed`
    - **summary:** Occurs when a window is about to be closed.
    - **remarks** The second argument of the event handler has a  property,
            which returns the window to be closed.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SubjectEventArgs`1.Subject`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.WindowClosed`
    - **summary:** Occurs when a window is closed.
    - **remarks** The second argument of the event handler has a  property,
            which returns the window that was closed.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.SubjectEventArgs`1.Subject`

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.ActiveToolChanged`
    - **summary:** Occurs when an active tool in the window has changed.

---
  - **member**
    - *@name:* `E:SpaceClaim.Api.V22.Window.InteractionModeChanged`
    - **summary:** Occurs when the section mode in the window has changed.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.Create(SpaceClaim.Api.V22.DrawingSheet)`
    - **summary:** Creates a window showing a drawing sheet.
    - **param:** A drawing sheet to be used as the window scene.
      - *@name:* `scene`
    - **returns:** A new window.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Split`
    - **summary:** Gets or sets the window split arrangement.
    - **remarks** Returns a , a , or a  object;
            or  if the window is not split.
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.LeftRightSplit`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.TopBottomSplit`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.FourWaySplit`
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.IsVisible`
    - **summary:** Gets or sets whether the window is visible.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.AllowDragDrop`
    - **summary:** Gets or set whether the window will allow a user to drop an object in the window.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.IsViewProjectionLocked`
    - **summary:** Gets or sets whether window's view projection is locked
    - **remarks:** When a window's view projection is locked, all commands for manipulating the view are disabled.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.AllWindows`
    - **summary:** Gets all windows in the session.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.GetWindows(SpaceClaim.Api.V22.Document)`
    - **summary:** Gets all windows with scenes belonging to the specified document.
    - **param:** The document for which windows are sought.
      - *@name:* `doc`
    - **returns:** Zero or more windows with scenes belonging to the specified document.
    - **remarks** If a document has been loaded using  or it has been 
            loaded implicitly, e.g. because an assembly was opened and one of its components
            has a template part in another document, then the document may not have any windows
            open.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Document.Load(System.String)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.GetWindows(SpaceClaim.Api.V22.DrawingSheet)`
    - **summary:** Gets all windows having the specified drawing sheet as their scene.
    - **param:** The window scene.
      - *@name:* `scene`
    - **returns:** Zero or more windows having the specified drawing sheet as their scene.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Document`
    - **summary:** Gets the document to which this window belongs.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.ActiveWindow`
    - **summary:** Gets or sets the active window.
    - **remarks** If the last window has been closed, so that there are no longer any windows,  returns .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.ActiveWindow`
      - **b:** null

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.SelectionFilter`
    - **summary:** Gets or sets the selection filter for the window.
    - **remarks:** The selection filter can either be set to use SpaceClaim smart selection or 
            can be set to filter selection to specific types by using a logical OR operator
            to combine particular types.
    - **example** The following examples show some of the ways to set the selection filter.
      - **code:** // Select only faces and edges
            Window.ActiveWindow.SelectionFilter = SelectionFilterType.Faces | SelectionFilterType.Edges;
            
            // Select everything but annotations
            Window.ActiveWindow.SelectionFilter = SelectionFilterType.All & ~SelectionFilterType.AllAnnotations;
            
            // Turn on smart selection
            Window.ActiveWindow.SelectionFilter = SelectionFilterType.Smart;

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.Copy`
    - **summary** Creates a new window that shows the same  as this window.
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.Scene`
    - **returns:** A new window.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.ZoomExtents`
    - **summary:** Zooms and pans so as to fit the scene to the window.
    - **remarks:** The operation does not happen until the end of the command being executed.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.ZoomSelection`
    - **summary** Zooms so as to fit the current selection to the window.
            If nothing is selected, the behavior is the same as .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.ZoomExtents`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.HomeProjection`
    - **summary:** Gets or sets the home projection for the active view.
    - **remarks:** The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Projection`
    - **summary:** Gets the view projection matrix for the active view.
    - **remarks:** The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Scene`
    - **summary:** Gets the scene shown in the window, either a part or a drawing sheet.
    - **remarks** The scene is a  object.
            
            This property is equivalent to .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DocObject.Root`
      - **para**
      - **c** window..
        - **see**
          - *@cref:* `P:SpaceClaim.Api.V22.Window.SceneContext`
        - **see**
          - *@cref:* `P:SpaceClaim.Api.V22.InteractionContext.Root`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.SceneBox`
    - **summary:** Gets the scene box.
    - **remarks:** The scene box is the bounding box of the visible objects in the scene.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Camera`
    - **summary:** Gets the camera for the scene.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.ActiveLayer`
    - **summary:** Gets or sets the active layer of the window.
    - **exception:** The layer belongs to the wrong document.
      - *@cref:* `T:System.ArgumentException`
    - **remarks:** The active layer is the layer to which newly created objects are assigned.
            Different windows of the same subject matter can have a different active layer.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.DeleteLayers(System.String)`
    - **summary:** Deletes layers in the window that match the specified name.
    - **param:** The layer name.
      - *@name:* `name`
    - **remarks** In general, the scene in a window shows parts that live in more than one document.
            In the user interface, the union of layer names is presented.
            This method deletes all layers in any documents in the scene that have the specified name.
            
            The  cannot be deleted.
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Document.DefaultLayer`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.CreateBitmap(System.Drawing.Size)`
    - **summary:** Creates a bitmap image of the current scene shown in the window.
    - **param:** The size of the bitmap.
      - *@name:* `size`
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
    - *@name:* `M:SpaceClaim.Api.V22.Window.Export(SpaceClaim.Api.V22.WindowExportFormat,System.String)`
    - **summary:** Exports the scene in a particular file format.
    - **param:** The file format to use.
      - *@name:* `format`
    - **param:** The path of the file to write to.
      - *@name:* `path`
    - **exception:** This copy of SpaceClaim is not licensed for the specified operation.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks** A standard file extension will be added according to the file type specified.
            
            Both  and  have methods to export to a particular file format.
             export translates the model, which does not need to be open in a window,
            whereas  export translates the graphics, which is why a window is required.
            
            There are three window export methods:
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Window`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Part`
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.Window`
      - **para**
      - **list**
        - *@type:* `bullet`
        - **item** works for any window.
          - **see**
            - *@cref:* `M:SpaceClaim.Api.V22.Window.Export(SpaceClaim.Api.V22.WindowExportFormat,System.String)`
        - **item** works for a window that shows a part.
          - **see**
            - *@cref:* `M:SpaceClaim.Api.V22.Window.ExportPart(SpaceClaim.Api.V22.PartWindowExportFormat,System.String)`
        - **item** works for a window that shows a drawing sheet.
          - **see**
            - *@cref:* `M:SpaceClaim.Api.V22.Window.ExportDrawingSheet(SpaceClaim.Api.V22.DrawingSheetWindowExportFormat,SpaceClaim.Api.V22.DrawingSheetBatch,System.String)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Part.Export(SpaceClaim.Api.V22.PartExportFormat,System.String,System.Boolean,SpaceClaim.Api.V22.ExportOptions)`

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.ExportDrawingSheet(SpaceClaim.Api.V22.DrawingSheetWindowExportFormat,SpaceClaim.Api.V22.DrawingSheetBatch,System.String)`
    - **summary:** Exports the drawing sheet in a particular file format.
    - **param:** The file format to use.
      - *@name:* `format`
    - **param:** Which drawing sheet windows to export.
      - *@name:* `batch`
    - **param:** The path of the file to write to.
      - *@name:* `path`
    - **exception:** This copy of SpaceClaim is not licensed for the specified operation.
      - *@cref:* `T:System.InvalidOperationException`
    - **exception:** The window does not show a drawing sheet.
      - *@cref:* `T:System.InvalidOperationException`
    - **remarks**
      - **inheritdoc**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.Export(SpaceClaim.Api.V22.WindowExportFormat,System.String)`
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Part.Export(SpaceClaim.Api.V22.PartExportFormat,System.String,System.Boolean,SpaceClaim.Api.V22.ExportOptions)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Groups`
    - **summary:** Gets the groups belonging to the scene shown in the window.
    - **remarks:** If the window shows an assembly, the groups of the top-level part are returned.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.SelectedGroups`
    - **summary:** Gets or sets the groups currently selected in the groups panel.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.ActiveTool`
    - **summary:** Gets the active tool, if that tool is using this API version.
    - **remarks** If the active tool is a custom tool implemented using this version of the API,
            then that tool is returned; otherwise  is returned.
            
            The purpose of this property is to determine whether your custom tool is active.
            The purpose is not to provide access to built-in tools, or tools provided by
            other add-ins.
            
             is typically use to set IsChecked for the command that activates a custom tool.
      - **b:** null
      - **para**
      - **para**
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.ActiveTool`
      - **code**
        ``` 
        
            Window window = Window.ActiveWindow;
            command.IsEnabled = window != null;
            command.IsChecked = window != null && window.ActiveTool is CustomTool;
            
        ```

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.SceneContext`
    - **summary:** Gets the interaction context for the scene.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.ActiveContext`
    - **summary:** Gets the interaction context in which the user is currently working.
    - **remarks:** This property returns a live context, i.e. if the user changes context, this interaction context changes too.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.GetContext(SpaceClaim.Api.V22.IDocObject)`
    - **summary:** Gets an interaction context for the specified root object.
    - **param:** Root object describing the context.
      - *@name:* `sceneSpaceRoot`
    - **returns:** The new interaction context.
    - **exception:** The object does not belong to the scene.
      - *@cref:* `T:System.ArgumentException`
    - **exception:** The master is not a root object.
      - *@cref:* `T:System.ArgumentException`
    - **remarks** The  must be an object in scene-space whose master is a root object.
            A root object is an object whose  is .
            
            See  for more information.
      - **paramref**
        - *@name:* `sceneSpaceRoot`
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.DocObject.Parent`
      - **b:** null
      - **para**
      - **see**
        - *@cref:* `T:SpaceClaim.Api.V22.InteractionContext`
    - **seealso**
      - *@cref:* `T:SpaceClaim.Api.V22.InteractionContext`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.InteractionMode`
    - **summary:** Gets or sets the interaction mode of the window.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Size`
    - **summary:** Gets the width and height of the active view in pixels.
    - **remarks:** The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.CursorPosition`
    - **summary:** Gets the position of the cursor in the active view.
    - **remarks** The coordinate space of the view is in pixels,
            with  as the top-left pixel and  as the bottom-right pixel.
            The property can be used to obtain the width and height of the view.
            
            The cursor might be outside the view, in which case the cursor position will be outside this range.
            
            The window can be split into two or four panes.
            The active view is the pane in which the user last clicked.
      - **c:** (0, 0)
      - **c:** (width - 1, height - 1)
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.Size`
      - **para**
      - **para**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Rendering`
    - **summary:** Gets or sets the temporary graphics rendering.

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.ClearClipVolume`
    - **summary:** Clears the current clipping volume for the window.
    - **seealso**
      - *@cref:* `M:SpaceClaim.Api.V22.Window.SetClipVolume(SpaceClaim.Api.V22.Window.ClipViewShape,SpaceClaim.Api.V22.Geometry.Frame,System.Double)`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.IsSketchConversionEnabled`
    - **summary:** Gets or sets whether conversion between sketches and surfaces is enabled.
    - **remarks** The default is .
      - **b:** true

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.ExtendConstructionLines`
    - **summary:** Gets or sets whether construction lines should be rendered with extensions.
    - **remarks** The lines are extended relative to the bounding box of the visible objects in the scene. 
            
            The default is
      - **br**
      - **b:** false

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.Units`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.Close`
    - **summary:** Closes the window.
    - **remarks** The window is closed.
            If this is the last window of the document, and the document needs saving, the user will  be prompted to save changes.
      - **i:** not

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.Delete`
    - **summary:** Deletes the window.
    - **remarks** Same as .
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.Close`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.IsDeleted`
    - **inheritdoc**

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.LifetimeLease`
    - **inheritdoc**

---
  - **member**
    - *@name:* `M:SpaceClaim.Api.V22.Window.RefreshRendering`
    - **summary** Forces the window to repaint the graphics specified in .
      - **see**
        - *@cref:* `P:SpaceClaim.Api.V22.Window.Rendering`

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.FontName`
    - **summary:** Gets the window font name.

---
  - **member**
    - *@name:* `P:SpaceClaim.Api.V22.Window.FontSize`
    - **summary:** Gets the window font size.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.WindowExportFormat`
    - **summary** Specifies an export format for use with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.Export(SpaceClaim.Api.V22.WindowExportFormat,System.String)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.AutoCadDwg`
    - **summary:** An AutoCAD DWG (".dwg") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.AutoCadDxf`
    - **summary:** An AutoCAD DXF (".dxf") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Bmp`
    - **summary:** A Windows bitmap (".bmp") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Jpeg`
    - **summary:** A JPEG image (".jpg") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Png`
    - **summary:** A PNG image (".png") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Tiff`
    - **summary:** A TIFF image (".tif") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Gif`
    - **summary:** A GIF image (".gif") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Amf`
    - **summary:** An AMF (".amf") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Pov`
    - **summary:** A POV-Ray (".pov") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Anf`
    - **summary:** An ANSYS Neutral File (".anf") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.Amm`
    - **summary:** An ANSYS Modeler Mesh (".amm") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.IcepakModel`
    - **summary:** An ANSYS Icepak model ("model") file.
    - **exclude**

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.QIF`
    - **summary:** A QIF (".qif") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.MSH`
    - **summary:** A Fluent mesh (".msh") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.INP`
    - **summary:** An ANSYS mesh (".inp") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.TGF`
    - **summary:** A Fluent mesh (".tgf") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.TIN`
    - **summary:** An ICEM CFD (".tin") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.STL`
    - **summary:** An STL (".stl") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.FMD`
    - **summary:** A FM database (".fmd") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.WindowExportFormat.DISCO`
    - **summary:** A Disco (".dsco") file.

---
  - **member**
    - *@name:* `T:SpaceClaim.Api.V22.DrawingSheetWindowExportFormat`
    - **summary** Specifies an export format for use with the  method.
      - **see**
        - *@cref:* `M:SpaceClaim.Api.V22.Window.ExportDrawingSheet(SpaceClaim.Api.V22.DrawingSheetWindowExportFormat,SpaceClaim.Api.V22.DrawingSheetBatch,System.String)`

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DrawingSheetWindowExportFormat.Pdf`
    - **summary:** A 2D PDF (".pdf") file.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DrawingSheetBatch.SingleWindow`
    - **summary:** A single drawing sheet window.

---
  - **member**
    - *@name:* `F:SpaceClaim.Api.V22.DrawingSheetBatch.AllWindows`
    - **summary:** All drawing sheet windows currently open.

---
