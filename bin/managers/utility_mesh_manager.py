import random
from copy import deepcopy
from maya import cmds


class UtilityMeshManager:
    global_work_space = {}
    helper = None
    
    def __init__(self, global_work_space, helper):
        self.global_work_space = global_work_space
        self.helper = helper

    def heyWitch_addUtlMshWindow(self, homePass, *args):
        if homePass.object_type == 'MeshSkinningWorkspace':
            homeString = homePass.mesh_spawn_name + "'s Mesh Skinning Workspace"
            needsBase = True
        else:
            homeString = homePass.target_mesh_label
            needsBase = False
        randomNo = random.randint(100, 999)
        utlMshLabelPrompt = cmds.promptDialog(
            message=("Enter Utility Shop Label for " + homeString),
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        if utlMshLabelPrompt == 'OK':
            utlMshLabelTextFld = cmds.promptDialog(query=True, text=True)
            if utlMshLabelTextFld == "":
                utlMshLabelTextFld = str(randomNo)
                self.heyWitch_addUtilityShop(homePass, utlMshLabelTextFld, needsBase)
            else:
                self.heyWitch_addUtilityShop(homePass, utlMshLabelTextFld, needsBase)
        

    def heyWitch_addUtilityShop(self, homePass, utlMshLabelTextFld, needsBase, *args):
        spwnScan = self.global_work_space['spawnStorage']
        for x in spwnScan.values():
            if x.mesh_spawn_name == homePass.mesh_spawn_name:
                spawnMesh = x
        utlMeshName = "utlMsh_" + utlMshLabelTextFld
        utlBseMeshName = "utlBseMsh_" + utlMshLabelTextFld
        # making the burn base mesh
        # should add function to duplicate other meshes than the spawn
        cmds.duplicate(str(spawnMesh.mesh_spawn_name), name=utlMeshName)
        self.helper.heyWitch_blankSlate(utlMeshName)
        cmds.select(clear=True)
        if needsBase == True:
            cmds.duplicate(str(spawnMesh.mesh_spawn_name), name=utlBseMeshName)
            self.helper.heyWitch_blankSlate(utlBseMeshName)
            homeGroup = homePass.mesh_spawn_name + "_msw_grp"
        else:
            homeGroup = homePass.burn_group_label + '_tgt_grp'
        # outliner group
        utlWkshpNme = 'utlWkshp_' + utlMshLabelTextFld
        cmds.group(empty=True, name=utlWkshpNme + '_grp')
        cmds.parent(utlMeshName, (utlWkshpNme + '_grp'))
        cmds.setAttr(utlMeshName + '.visibility', 1)
        tree_layout = self.global_work_space['miscData']['switch_layouts']['msw_tree_layout']
        if cmds.objExists(utlBseMeshName):
            cmds.parent(utlBseMeshName, (utlWkshpNme + '_grp'))
            cmds.setAttr(utlBseMeshName + '.visibility', 0)
            cmds.treeView(tree_layout, edit=True, addItem=(utlWkshpNme,
                                                           homePass.mesh_spawn_name+"'s Mesh Skinning Workspace"),
                          cs=True)
            cmds.treeView(tree_layout, edit=True, selectItem=(utlWkshpNme, True))
        else:
            cmds.treeView(tree_layout, edit=True, addItem=(utlWkshpNme, homePass.target_mesh_label), cs=True)
            cmds.treeView(tree_layout, edit=True, selectItem=(utlWkshpNme, True))
        cmds.parent((utlWkshpNme + '_grp'), homeGroup)
        # no point in making objects if the type is not really available yet
        unlikelyString = 'veryunlikelynamenothingmustreallybeselected'
        self.helper.heyWitch_grabMesh(unlikelyString, homePass, self.global_work_space)
        cmds.select(utlMeshName)
        tempUtlLst = []
        tempUtlLst = deepcopy(homePass.utility_nest)
        tempUtlLst.append(utlWkshpNme)
        homePass.utility_nest = deepcopy(tempUtlLst)
        