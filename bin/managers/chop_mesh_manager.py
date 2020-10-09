import random
from copy import deepcopy
from functools import partial

import pymel.core as pm
from maya import cmds

from bin.classes.classes import HomelessChop, ChopShader, ChopMesh

class ChopMeshManager:

    helper = None
    bind_joint_cluster_manager = None
    global_work_space = {}

    def __init__(self, helper, bind_joint_cluster_manager, global_work_space):
        self.helper = helper
        self.bind_joint_cluster_manager = bind_joint_cluster_manager
        self.global_work_space = global_work_space

    def heyWitch_jntFromLoop(self, *args):
        loopyJointPrompt = cmds.promptDialog(
            message="Enter name ",
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        if loopyJointPrompt == 'OK':
            loopyJoint = cmds.promptDialog(query=True, text=True)
            cmds.DetachComponent()
            cmds.CreateCurveFromPoly()
            newCurve = cmds.ls(sl=True, type='transform')
            for x in newCurve:
                cmds.delete(x, ch=True)
                cmds.makeIdentity(x, apply=True, t=1, r=1, s=1, n=0)
                cmds.CenterPivot()
                cmds.select(clear=True)
                cmds.joint(name=loopyJoint)
                cmds.pointConstraint(x, loopyJoint)
                cmds.delete((loopyJoint + "_pointConstraint1"), x)

    def heyWitch_nameGeoChopByJnt(self, *args):

        nameGrp = cmds.ls(sl=True, type='transform')
        cmds.rename(nameGrp[1], nameGrp[0] + "_geoChp")

    def heyWitch_addHomelessChopClrSet(self, *args):
        homelessMeshName = cmds.ls(sl=True, type='transform')
        chpClrSetTextFld = self.heyWitch_makeChopSetWin()
        if chpClrSetTextFld != "cancelset":
            homelessMesh = HomelessChop()
            homelessMesh.set_label = chpClrSetTextFld
            self.global_work_space['miscData']['homelessChopClrSets'][homelessMeshName[0]] = homelessMesh
        

    def heyWitch_makeChopSetWin(self):
        randomNo = random.randint(100, 999)
        chpClrSetLabelPrompt = cmds.promptDialog(
            message=("Enter Set Label"),
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        if chpClrSetLabelPrompt == 'OK':
            chpClrSetTextFld = cmds.promptDialog(query=True, text=True)
            greenlight = True
            if chpClrSetTextFld == "":
                chpClrSetTextFld = str(randomNo)
        else:
            chpClrSetTextFld = "cancelset"
        return chpClrSetTextFld

    def heyWitch_addChopShader(self, meshKey, meshObj, *args):
        if meshObj.set_label == "":
            chpClrSetTextFld = self.heyWitch_makeChopSetWin()
            if chpClrSetTextFld != "cancelset":
                greenlight = True
                meshObj.set_label = chpClrSetTextFld
        else:
            greenlight = True
            chpClrSetTextFld = meshObj.set_label

        if greenlight == True:
            chpShdrLabelPrompt = cmds.promptDialog(
                message=("Enter Label for Chop Shader"),
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')

            if chpShdrLabelPrompt == 'OK':
                chpShdrTextFld = cmds.promptDialog(query=True, text=True)
                if chpShdrTextFld == "":
                    randomNo = random.randint(100, 999)
                    chpShdrTextFld = str(randomNo)

            selPoly = cmds.ls(sl=True, fl=True)
            chopShaderDict = deepcopy(meshObj.all_shaders)
            mtlName = 'btw_' + chpClrSetTextFld + '_' + chpShdrTextFld + "_geoChp_Mtl"
            randRed = random.uniform(0.0, 1.0)
            randGreen = random.uniform(0.0, 1.0)
            randBlue = random.uniform(0.0, 1.0)
            # cmds.shadingNode('lambert', asShader=True, name=mtlName)
            # cmds.setAttr((mtlName + ".color"), randRed, randGreen, randBlue, type='double3')
            cmds.select(selPoly)
            # cmds.hyperShade(a=mtlName)
            cmds.ConvertSelectionToVertices()
            pm.mel.polyColorPerVertex(a=1, cdo=1, rgb=(randRed, randGreen, randBlue))
            # cmds.HypershadeSelectObjectsWithMaterials()
            vertsSelected = cmds.ls(sl=True, fl=True)
            tempVertBook = {}
            sel_add_command_string = "cmds.select("
            arg_count = 0
            for x in vertsSelected:
                tempVertBook[x] = 0
                if arg_count <= 250:
                    temp_scs = sel_add_command_string + '"' + x + '", '
                    sel_add_command_string = temp_scs
                    arg_count+=1
                else:
                    temp_scs = sel_add_command_string + 'add=True)\ncmds.select('
                    sel_add_command_string = temp_scs + '"' + x + '", '
                    arg_count = 0
            temp_scs = sel_add_command_string + 'add=True)'
            sel_add_command_string = temp_scs
            single_sel_command_string = 'cmds.select(clear=True)\n'+sel_add_command_string
            chopShader = ChopShader()
            chopShader.vert_vals = deepcopy(tempVertBook)
            chopShader.set_label = chpClrSetTextFld
            chopShader.red = randRed
            chopShader.green = randGreen
            chopShader.blue = randBlue
            chopShader.short_name = chpShdrTextFld
            chopShader.single_sel_command = single_sel_command_string
            chopShader.add_to_sel_command = sel_add_command_string
            chopShaderDict[mtlName] = chopShader
            meshObj.all_shaders = deepcopy(chopShaderDict)
            cmds.select(meshKey)
            pm.mel.dR_DoCmd("modePoly")
            


    def heyWitch_geoChopRandomColourSet(self, utlWkshpLabel, *args):
        chpClrSetTextFld = self.heyWitch_makeChopSetWin()
        if chpClrSetTextFld != "cancelset":
            choppedBits = cmds.ls(sl=True, type='transform')
            chopShaderDict = {}
            for x in choppedBits:
                mtlName = 'btw_' + chpClrSetTextFld + '_' + x + "_Mtl"
                randRed = random.uniform(0.0, 1.0)
                randGreen = random.uniform(0.0, 1.0)
                randBlue = random.uniform(0.0, 1.0)
                cmds.shadingNode('lambert', asShader=True, name=mtlName)
                cmds.setAttr((mtlName + ".color"), randRed, randGreen, randBlue, type='double3')
                cmds.select(x)
                cmds.hyperShade(a=mtlName)
                cmds.ConvertSelectionToVertices()
                pm.mel.polyColorPerVertex(a=1, cdo=1, rgb=(randRed, randGreen, randBlue))
                chopShader = ChopShader()
                chopShader.set_label = chpClrSetTextFld
                chopShader.red = randRed
                chopShader.green = randGreen
                chopShader.blue = randBlue
                chopShader.short_name = x
                chopShaderDict[mtlName] = chopShader

            cmds.select(clear=True)
            for y in choppedBits:
                cmds.select(y, add=True)
            cmds.CombinePolygons()
            cmds.PolyMerge()
            newChopMeshName = 'chpMsh_' + chpClrSetTextFld
            newChopMeshSel = cmds.ls(sl=True, type='transform')
            cmds.rename(newChopMeshSel[0], newChopMeshName)
            self.helper.heyWitch_blankSlate(newChopMeshName)
            chopMesh = ChopMesh()
            chopMesh.set_label = chpClrSetTextFld
            chopMesh.all_shaders = deepcopy(chopShaderDict)

            for k0, v0 in chopMesh.all_shaders.items():
                tempVertBook = {}
                cmds.select(k0)
                cmds.HypershadeSelectObjectsWithMaterials()
                cmds.ConvertSelectionToVertices()
                vertsSelected = cmds.ls(sl=True, fl=True)
                cmds.delete(k0)
                for x in vertsSelected:
                    tempVertBook[x] = 0
                v0.vert_vals = deepcopy(tempVertBook)

            for chopShader in chopMesh.all_shaders.values():
                sel_add_command_string = "cmds.select("
                arg_count = 0
                for vtx in chopShader.vert_vals.keys():
                    if arg_count <= 250:
                        temp_scs = sel_add_command_string + '"' + vtx + '", '
                        sel_add_command_string = temp_scs
                        arg_count += 1
                    else:
                        temp_scs = sel_add_command_string + 'add=True)\ncmds.select('
                        sel_add_command_string = temp_scs + '"' + vtx + '", '
                        arg_count = 0
                temp_scs = sel_add_command_string + 'add=True)'
                sel_add_command_string = temp_scs
                single_sel_command_string = 'cmds.select(clear=True)\n' + sel_add_command_string
                chopShader.single_sel_command = single_sel_command_string
                chopShader.add_to_sel_command = sel_add_command_string
                cmds.select(clear=True)
            chopMesh.utl_wkshp_label = utlWkshpLabel
            cmds.parent(newChopMeshName, utlWkshpLabel + '_grp')
            storageSearch = ['spawnStorage', 'targetStorage']
            for storage in storageSearch:
                for v1 in self.global_work_space[storage].values():
                    if storage == 'spawnStorage':
                        if chopMesh.utl_wkshp_label in v1.mesh_skinning_workspace.utility_nest:
                            chopMesh.mesh_spawn_name = v1.mesh_spawn_name
                    else:
                        if chopMesh.utl_wkshp_label in v1.utility_nest:
                            chopMesh.mesh_spawn_name = v1.mesh_spawn_name
            self.global_work_space['chopMeshStorage'][newChopMeshName] = chopMesh
            tree_layout = self.global_work_space['miscData']['switch_layouts']['msw_tree_layout']
            cmds.treeView(tree_layout, edit=True,
                          addItem=(newChopMeshName, chopMesh.utl_wkshp_label), cs=True)
            cmds.treeView(tree_layout, edit=True, selectItem=(newChopMeshName, True))
            cmds.shadingNode('lambert', asShader=True, name='btw_chop_Mtl')
            cmds.select(newChopMeshName)
            cmds.hyperShade(a='btw_chop_Mtl')
            pm.mel.dR_DoCmd("modeObject")
            

    def heyWitch_intersectVerts(self, chpMshVal, *args):
        vertsList = cmds.ls(sl=True, fl=True)
        edgeVertsList = []
        shaderDict = {}
        for k0, v0 in chpMshVal.all_shaders.items():
            excludeVar = False
            for k1 in v0.vert_vals.keys():
                if not k1 in vertsList:
                    excludeVar = True
            if excludeVar == False:
                shaderDict[k0] = v0
        for crntVtx in vertsList:
            excludeVar = False
            for k2, v2 in shaderDict.items():
                if not crntVtx in v2.vert_vals.keys():
                    excludeVar = True
            if excludeVar == False:
                edgeVertsList.append(crntVtx)
        addVar = 'single'
        self.helper.heyWitch_selectListOf(edgeVertsList, addVar)

    def configure_intersections(self, chpMshVal, chpMshKey, sel_by_chop_win, *args):
        cmds.deleteUI(sel_by_chop_win, window=True)
        temp_config_dict = {}
        for k0, v0 in chpMshVal.all_shaders.items():
            for k1, v1 in chpMshVal.all_shaders.items():
                temp_config_dict[k0] = {}
                if k1 != k0:
                    sel_add_command_string = 'cmds.select('
                    arg_count = 0
                    for vtx in v0.vert_vals.keys():
                        if vtx in v1.vert_vals.keys():
                            if arg_count < 250:
                                temp_scs = sel_add_command_string + '"' + vtx + '", '
                                sel_add_command_string = temp_scs
                                arg_count += 1
                            else:
                                temp_scs = sel_add_command_string + 'add=True)\ncmds.select('
                                sel_add_command_string = temp_scs + '"' + vtx + '", '
                                arg_count = 0
                            temp_scs = sel_add_command_string + 'add=True)'
                            sel_add_command_string = temp_scs
                            temp_config_dict[k0][k1] = str(sel_add_command_string)
        chpMshVal.int_config = deepcopy(temp_config_dict)
        self.heyWitch_selByChopShader(chpMshKey, chpMshVal)

    def heyWitch_selByChopShader(self, chpMshKey, chpMshVal, *args):
        sel_by_chop_win = cmds.window(title='selByChopShader')
        cmds.scrollLayout()
        cmds.columnLayout()
        cmds.separator()
        cmds.text(label='Select by Chop Shader for Chop Set ' + str(chpMshVal.set_label))
        cmds.separator()
        cmds.frameLayout(label='Single select')
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(125, 25))
        for k0, v0 in chpMshVal.all_shaders.items():
            shortLblTemp = k0.replace('btw_' + chpMshVal.set_label + '_', '')
            shortLbl = shortLblTemp.replace('_geoChp_Mtl', '')
            cmds.button(label=shortLbl, backgroundColor=[v0.red, v0.green, v0.blue],
                        command=partial(self.helper.execute_string_command, v0.single_sel_command))
        cmds.setParent('..')
        cmds.frameLayout(label='Add to selection')
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(125, 25))
        for k0, v0 in chpMshVal.all_shaders.items():
            shortLblTemp = k0.replace('btw_' + chpMshVal.set_label + '_', '')
            shortLbl = shortLblTemp.replace('_geoChp_Mtl', '')
            cmds.button(label=shortLbl, backgroundColor=[v0.red, v0.green, v0.blue],
                        command=partial(self.helper.execute_string_command, v0.add_to_sel_command))
        cmds.setParent('..')
        cmds.button(label='Intersect', command=partial(self.heyWitch_intersectVerts, chpMshVal))
        cmds.button(label='Configure intersection data stash', command=partial(self.configure_intersections, chpMshVal, chpMshKey, sel_by_chop_win))
        if chpMshVal.int_config != {}:
            cmds.frameLayout(label='Currently configured:', collapsable=True)
            for k0, v0 in chpMshVal.int_config.items():
                cmds.rowLayout(numberOfColumns=3)
                cmds.text(label=k0+' + ')
                cmds.columnLayout()
                for k1, v1 in v0.items():
                    if v1 != 'cmds.select(add=True)':
                        string_command = str(chpMshVal.int_config[k0][k1])
                        cmds.button(label=k1, command=partial(self.helper.execute_string_command, string_command))
                cmds.setParent('..')
                cmds.setParent('..')
            cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.showWindow()