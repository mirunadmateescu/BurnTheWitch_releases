# BurnTheWitch

Skinning tool prototype ment to create a faster and non-destructive weight-painting 
workflow. 

Some of the functions will work with +25k meshes but it's not recommended to use 
this tool on anything over 10k until improvements are made to the scripts. Backup 
your work before running Burn The Witch and save your dictionary frequently. Some 
of the scripts will use the hierarchy created in the Outliner, for best results do 
not delete or reorder anything in 'btw_WorkSpace_grp' until the skinning process 
is over. 

A bunch of the terminology used in this guide might not make a lot of sense without 
reading the "Concept" section in "Mesh Skinning Workspaces", although learning to 
use that part of the tool is not essential for using the Magic Maps maths and storage,
the independent colour sets and influence windows or just storing Bind Joint Clusters.

##  How to run the script for the first time

1. Move the "BurnTheWitch" folder wherever you want to store it, open the folder in 
the Windows File Explorer and copy its path.

2. Open "start.py" in a text editor and replace the PROJECT_PATH string (currently 
"C:/Users/Miruna/Documents/PythonProjects/BurnTheWitch") with the new path you've 
copied.

3. Run the modified "start.py" script in Maya's text editor, feel free to add it to 
your shelf or make a runtime command for quicker access.

## The Main Window

- Dictionary path

    This is there Burn The Witch stores all the data it creates in relation to that Maya scene, it will be saved in the same location as your .mb or .ma file.

- Save

    Save as often as possible, the external file does not update automatically. This will overwrite your current dictionary file. Keep in mind that if you've renamed your Maya scene the dictionary should be saved right after that, if the scene is closed without saving an empty dictionary file will be created next time you attempt to run the script. If that happened, look for the old dictionary file and rename it accordingly.

- Refresh

    Some functions will automatically update the main window but not all of them are at that stage yet. Magic maps won't be updated with newly created blendnodes and skinclusters unless it has been refreshed.

## Toolkit

**Buttons**

- +MshSknWks

    Makes selected mesh into a spawn so Burn Groups and Utility Workshops can be added to it inside the Mesh Skinning Workspace.

- +BndJntClstr

    Creates a set for all of the selected joints that can be quickly selected for either regular or chop skinning, bind joints will be created from the originals so they can be reparented if the rig has to be modified at any point in the future. All the joints and the influenced meshes of a Bind Joint Cluster will be listed in the "Bind Joint Clusters" tab. The Burn Groups and Utility Workshops will need Bind Joint Clusters to function correctly, skinning meshes to jointchains that aren't stored that way will lead to unpredictable results.

- +JntFromLoop

    Creates a joint in the middle of the selected edgeflow and detaches the mesh at those edges, useful for creating a Chop Mesh (see the Mesh Skinning Workspace section) and a skeleton at the same time.

- NameChopByJoint

    If two objects are selected, the second one will be renamed to match the first. The '_geoChp' suffix should be kept where it is if this is done with the intention to fuse all geometry into a Chop Mesh later.

- +MkeInfWin

    Launches the Influence Window Builder for skinclusters that aren't inside the Mesh Skinning Workspace, if a window is saved it will appear in the "Homeless Influence Windows" frame.

- +MkeChpClrSet

    Will store the selected mesh into the "Homeless Chop Sets" frame so different groups of vertices can be quickly selected when painting skinweights or deformer weights outside the Mesh Skinning Workspace. 

**Homeless Influence Windows**

Shows buttons that launch all homeless influence windows that have been saved after the Main Window has been refreshed.

**Homeless Chop Sets**

Shows each mesh that has been given a Homeless Chop Set with the following buttons:

- Select

    Selects the entire mesh.

- +AddChpShdr

    Adds a Chop Shader to the selected polygons.

- SelByChopShader

    Launches a window with all chop shaders that belong to that mesh ready to be selected.

## Mesh Skinning Workspace

**Concept**

This is where everything comes together, think of this as a workshop where 
you can use a bunch of different techniques on multiple clones of the Spawn 
Mesh and then merge all the different bits you are happy with at the end rather
than having to skin perfectly one single mesh from start to finish and lose parts
you initially got right while attempting to change the ones that weren't working :)

- **Burn Groups**

    A Burn Group consists of a Burn Base Mesh that gets its information from a bunch 
    of blend targets (Target Meshes) that can all be skinned in different ways to one 
    or more Bind Joint Clusters. The blend map weights on the Burn Base will act as a 
    mask that decides which Target Mesh will affect different regions. When you are 
    happy with the result, you can "burn" everything into one single mesh with one 
    single skincluster that gets stored separately (so the Burn Group will not be 
    destroyed). If the Target Meshes are skinned to more than one Bind Joint Cluster,
    a new one that contains all the influences will be created for the Output or 
     Burnout Mesh. Burn Base, Target and Burnout Meshes are always perfect copies of
     their Spawn.

- **Utility Workshops**

    Utility Workshops hold meshes with altered geometry that would not be a perfect
    match for the Spawn Mesh but can still be lifesavers in certain contexts. 
    Skinweights can be copied to a mesh with the correct geometry afterwards.
    
    - **Raw Meshes**
    
        Any piece of geometry inside an Utility Workshop's Outliner group is selectable
        as a Raw Mesh in the Utility Workshop's menu, it can be modified and then
        labeled as any other sort of utility mesh.

    - **Chop Meshes**
    
        Chop Meshes are meshes that have all their vertices in the correct location,
        but have been separated and merged back together to create a bunch of Chop
        Shaders that can be used to quickly select vertex sets and intersect them 
        while skinning the mesh. If any Chop Shaders have joints that match their
        name and those joints have been stored as a Bind Joint Cluster, all the 
        vertices that belong to a Chop Shader can be skinned automatically with a
        weight value of 1 to their corresponding joints. (see Bind Joint Clusters
        section)
    
    - **Gulp Meshes**
    
        Gulp Meshes haven't been implemented yet but they are essentially versions of
        the spawn mesh that are more like an all-engulfing blob where detail is ment 
        to be (for example hair or fur strands that are ment to deform like a single, 
        bigger mass) and has all the gaps closed (so a character's hood or sleeves 
        that have manifold geometry would be a closed, more general shape instead).
        Primitives like a cilinder can act as a Gulp Mesh too.
    
Both Burn Groups and Utility Workshops can be added to either Mesh Skinning 
Workspaces or to Target Meshes, although the Main Window might have to be refreshed
for the hierarchy to shop up correctly.

- **Weightpainting aids**

    - **Chop Colour Sets**
    
        A slightly less destructive way to bring in some of the functionality of Chop
        Meshes to a Burn Group without altering the geometry or the vertex order. They
        can be assigned by selecting polygons and clicking "+AddChpShdr" inside the
        menu of the relevant mesh.
    
    - **Influence Windows**
    
        When skinning a mesh with a long list of influences that has to be constantly
        scrolled through, especially when going back and forth between joints that are
        really far away in the hierarchy or overlap too much to be easily selected from
        the viewport, navigating Maya's weightpainting tool can be unnecessarily time
        consuming. This function allows for building your own windows from which you 
        can select influences later, they can be grouped in rows or columns and you
        can tag each setup. All influences get locked up automatically, with only the
        last two joints that were clicked staying unlocked. It won't update Maya's 
        skinning menu automatically, but you're still painting on the correct influence
        and the elbow room is worth it. Trust the process :)

**Interface**

Left - Hierarchy displaying all Spawn meshes with their Burn Groups and Utility Workshops if 
any were added. All Target and Burnout Meshes are nested under their respective 
Burn Base Mesh, all Chop Meshes are nested under their Utility Workshops.

Upper Right - Actions that can be performed on the mesh you have selected in the
hierarchy

Lower Right - Storage space for Influence Windows, Raw Meshes etc.

- **Available actions**

    - **>Grab** _(Spawn Mesh, Burn Base Mesh, Target Mesh, Burnout Mesh, Chop Mesh)_
    
        Selects the active mesh you've picked from the hierarchy and makes the rest
        of the contents of that Mesh Skinning Workspace invisible. A bit buggy with
        Utility Workshops but should work fine with Burn Groups.
        
    - **+AddBrnGrp** _(Spawn Mesh, Target Mesh)_
    
        Adds a Burn Base Mesh to the Mesh Skinning Workspace or the Target Mesh that
        was currently active in the menu.
        
    - **+AddTgtMsh** _(Burn Base Mesh)_
    
        Adds a Target Mesh to the active Burn Base.
    
    - **BURN** _(Burn Base Mesh)_
    
        Creates a Burnout Mesh that combines all Target Meshes of that Burn Group 
        according to the blend maps that have been painted on the Burn Base Mesh.
    
    - **+AddUtlMsh** _(Spawn Mesh, Target Mesh)_
    
        Adds an Utility Workshop with a duplicate of the Spawn Mesh inside it. If
        applied to a Mesh Skinning Workspace an Utility Base Mesh will also be 
        created, if applied to a Target Mesh then that mesh will act as a Base.

    - **+ChopColorize** _(Utility Workshop)_
    
        If a mesh has been sliced into separately named bits ending in "_geoChp", 
        selecting all of them in the Outliner and hitting this button will remerge
        the geometry with color selection sets assigned according to the sliced
        geometry pieces and all their names. This will not automatically skin the mesh
        to a skeleton.
          
    - **CloneSkin** _(Target Mesh)_
    
        Clones a specific skincluster into the active Target Mesh. Nothing has to 
        be selected, a pop-up will ask for the skincluster node's name. If the meshes
        match perfectly it will copy using vertex values, otherwise it will use Maya's
        Copy SkinWeights function, which might be slightly less precise depending on
        your setup.
    
    - **+AddChpShdr** _(Burn Base Mesh, Target Mesh)_
    
        Adds a new Chop Shader to the selected polygons.
    
    - **SelByChopShader** _(Burn Base Mesh, Target Mesh, Chop Mesh)_
    
        Launches the "Select by Chop Shader" window (see "Weightpainting windows" 
        for the interface)
    
    - **+MkeInfWin** _(Target Mesh, Chop Mesh)_
    
        Only appears if the active mesh has been skinned, launches the "Influence 
        Builder" window (see "Weightpainting windows" for the interface)
    
    - **+BlndPaint**
    
        Shortcut to the "Paint Blend Shape Weights Tool", click ">Grab" first or 
        select the mesh in the Viewport.
    
    - **+SkinPaint** 
    
        Shortcut to the "Paint Skin Weights Tool", click ">Grab" first or 
        select the mesh in the Viewport. 
    
- **Weightpainting windows**

    - **Select by Chop Shader**
    
        - **Single select**
        
            Selects all vertices from the Chop Shader that has been clicked.
        
        - **Add to selection**
        
            Adds all the vertices from the Chop Shader that has been clicked to the
            existing selection.
        
        - **Intersect**
        
            If two or more Chop Shaders are currently selected, this will deselect 
            all the vertices that aren't included in all those shaders. It's ment as 
            an easy way to select all the vertices on the edge between two Chop Shaders.
            Can get very slow on highpoly meshes.
        
        - **Configure intersection data stash**
        
            Not operational yet, function ment to create string commands for all the possible
            intersections between existing Chop Shaders inside that Chop Colour Set as a way
            to get around the speed issue the "Intersect" button currently has.
    
    - **Influence Window Builder**
    
        - **+AddInfs**
        
            Adds all the joints you have checked in the Influence Picker to that 
            respective column.
        
        - **+SaveSetup**
        
            Saves a ready to launch Influence Window with the selection layout you
            have created and the name you typed inside the text field above.
    
    - **Influence Window**
    
        Window with your saved selection layout. The "Paint Skin Weights Tool" has to
        be activated for the window to work. The active influence is bright yellow and
        the other unlocked influence is in a darker shade, all other influences should 
        be locked.

## Magic Maps

Offers blend map and skinweight map storage independent from the Mesh Skinning 
Workspace for all the blendshape and skincluster nodes that can be found in the 
scene. Simple maths can be done with the weight values for each vertex and then 
transferred to other meshes if the geometry is identical. Will add a function that 
can store everything in batch in the future and make the scripts for assigning 
weight values faster when time allows, until then it might not be a good idea to 
use this function on models that exceed a 10k polycount.

**Interface**

Left - Hierarchy displaying all BlendShape and SkinCluster nodes in the scene with
all their blend targets or influences. Select a target or influence to make it active.

Upper right - Maps library with all the maps you've saved previously for that target 
or influence.

Lower right - "Map Maths" interface

- **OpenSlot**

    Opens that respective slot so a map can be loaded into it. Clicking a map from the
    library will load it into that slot.

- **+/-/invert checkbox**
    
    Only check one box, this will not do anything until "=" is clicked:
    
    - **+**
    
        Slot1 map vertex value + Slot2 map vertex value, will be clamped if it goes higher
        than 1
    
    - **-**
    
        Slot1 map vertex value - Slot2 map vertex value, will be clamped if it goes lower
        than 0
    
    - **invert**
    
        1 - Slot1 vertex value

- **=**

    Creates new map according to the operation that was checked and loads it into a 
    third slot, if the third slot is loaded text will appear stating the names of the
    contributing maps and the operation that was used.

- **Stash**

    Will save the current map of the active influence or target in its Maps Library. 
    The "Stash" button inside the Math Maps interface will save the last map that was
    created with the Map Maths tool instead.

- **MakeCrt**

    Overwrites the current map of the active influence or target. This is very slow in 
    the current version.

- **LoadToSlot**

    Loads the newly created map into whichever slot is currently open.

## Bind Joint Clusters

Each Bind Joint Cluster has its own labeled section with:

- **Influenced meshes**

    List with every mesh that was skinned to this Bind Joint Cluster.

- **Joints list**

- **Available actions**

    - **Select**
    
        Selects all joints that belong to the Bind Joint Cluster.
    
    - **+BndToSelMesh**
    
        Binds the selected mesh to the Bind Joint Cluster using Maya's "Bind Skin" 
        function.
        
    - **+ChopBndToSelMesh**
    
        If a Chop Mesh is selected and joints from this Bind Joint Cluster are matching
        its Chop Shaders, the mesh will be skinned so all verts belonging to a Chop
        Shader will have a weight value of 1 coming from the respective influence.
