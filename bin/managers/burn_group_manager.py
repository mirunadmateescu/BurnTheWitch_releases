import random
from copy import deepcopy
from functools import partial

from maya import cmds

from bin.classes.classes import MeshSkinningWorkspace, Spawn, BurnBaseMesh, TargetMesh, OutputMesh


class BurnGroupManager:
    global_work_space = {}
    helper = None
    bind_joint_cluster_manager = None
    utility_mesh_manager = None
    chop_mesh_manager = None
    influence_manager = None
    clone_manager = None

    def __init__(self, global_work_space, bind_joint_cluster_manager, utility_mesh_manager, chop_mesh_manager,
                 influence_manager, clone_manager, helper):
        self.global_work_space = global_work_space
        self.bind_joint_cluster_manager = bind_joint_cluster_manager
        self.utility_mesh_manager = utility_mesh_manager
        self.chop_mesh_manager = chop_mesh_manager
        self.influence_manager = influence_manager
        self.clone_manager = clone_manager
        self.helper = helper

    def add_chop_mingler(self, k, v, msw_switch_Layout, mswPane):
        cmds.frameLayout(msw_switch_Layout, edit=True, label=k + ' Chop Mesh Toolkit')
        cmds.button(label=">Grab", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.helper.heyWitch_grabMesh, k, v, self.global_work_space))
        cmds.button(label="SelByChopShader", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_selByChopShader, k, v))
        cmds.button(label="+SkinPaint", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command='cmds.ArtPaintSkinWeightsToolOptions()')
        # cmds.text(label='crap_'+str(v.skin_cluster))
        if not v.skin_cluster == "":
            cmds.button(label="+MkeInfWin", height=25, backgroundColor=[0.3, 0.3, 0.3],
                        command=partial(self.influence_manager.heyWitch_makeInfluenceWindow, k, v.skin_cluster))
        msw_grab_tabs = self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs']
        if cmds.layout(msw_grab_tabs, ex=True):
            cmds.deleteUI(msw_grab_tabs, layout=True)
        msw_grab_tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, parent=mswPane)
        self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs'] = msw_grab_tabs
        inf_grid_layout = self.influence_manager.heyWitch_scanForInfWinds(v)
        v.inf_grid_layout = inf_grid_layout
        cmds.tabLayout(msw_grab_tabs, edit=True, tabLabel=(inf_grid_layout, 'Influence Windows'))

    def add_utility_mingler(self, k, v, msw_switch_Layout, mswPane):
        cmds.frameLayout(msw_switch_Layout, edit=True, label=k+ ' Utility Shop Toolkit')
        cmds.button(label='+ChopColorize', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_geoChopRandomColourSet, k))
        msw_grab_tabs = self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs']
        if cmds.layout(msw_grab_tabs, ex=True):
            cmds.deleteUI(msw_grab_tabs, layout=True)
        msw_grab_tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, parent=mswPane)
        self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs'] = msw_grab_tabs
        raw_mesh_grid_layout = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(125, 25))
        cmds.select(k + '_grp', hierarchy=True)
        cmds.select(k + '_grp', deselect=True)
        rawMeshList = cmds.ls(sl=True, type='transform')
        for raw_mesh in rawMeshList:
            cmds.button(label=raw_mesh, command=partial(self.helper.heyWitch_selectRawMesh, raw_mesh))
        cmds.setParent('..')
        cmds.tabLayout(msw_grab_tabs, edit=True, tabLabel=(raw_mesh_grid_layout, 'Raw Meshes'))

    def add_burnout_mingler(self, k, v, msw_switch_Layout):
        cmds.frameLayout(msw_switch_Layout, edit=True, label=v.mesh_label + ' Output Mesh Toolkit')
        cmds.button(label=">Grab", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.helper.heyWitch_grabMesh, k, v, self.global_work_space))

        msw_grab_tabs = self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs']
        if cmds.layout(msw_grab_tabs, ex=True):
            cmds.deleteUI(msw_grab_tabs, layout=True)

    def add_target_mingler(self, k, v, msw_switch_Layout, mswPane):
        cmds.frameLayout(msw_switch_Layout, edit=True, label=v.mesh_label + ' Target Mesh Toolkit')
        cmds.button(label=">Grab", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.helper.heyWitch_grabMesh, k, v, self.global_work_space))
        cmds.button(label="+AddUtlMsh", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.utility_mesh_manager.heyWitch_addUtlMshWindow, v))
        cmds.button(label="+AddBrnGrp", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.heyWitch_addBrnGrpWindow, v))
        cmds.button(label="+AddChpShdr", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_addChopShader, k, v))
        cmds.button(label="SelByChopShader", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_selByChopShader, k, v))
        cmds.button(label="+SkinPaint", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command='cmds.ArtPaintSkinWeightsToolOptions()')
        if not v.skin_cluster == '':
            cmds.button(label="+MkeInfWin", height=25, backgroundColor=[0.3, 0.3, 0.3],
                        command=partial(self.influence_manager.heyWitch_makeInfluenceWindow, k, v.skin_cluster))
        cmds.button(label="CloneSkin", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.clone_manager.heyWitch_cloneSkinCluster, k, v))
        msw_grab_tabs = self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs']
        if cmds.layout(msw_grab_tabs, ex=True):
            cmds.deleteUI(msw_grab_tabs, layout=True)
        msw_grab_tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, parent=mswPane)
        self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs'] = msw_grab_tabs
        inf_grid_layout = self.influence_manager.heyWitch_scanForInfWinds(v)
        v.inf_grid_layout = inf_grid_layout
        cmds.tabLayout(msw_grab_tabs, edit=True, tabLabel=(inf_grid_layout, 'Influence Windows'))

    def add_burn_base_mingler(self, k, v, msw_switch_Layout):
        cmds.frameLayout(msw_switch_Layout, edit=True, label=v.mesh_label + ' Burn Base Toolkit')
        cmds.button(label=">Grab", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.helper.heyWitch_grabMesh, k, v, self.global_work_space))
        cmds.button(label="+AddTgtMsh", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.heyWitch_addTgtMshWindow, v))
        cmds.button(label="+AddChpShdr", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_addChopShader, k, v))
        cmds.button(label="SelByChopShader", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_selByChopShader, k, v))
        cmds.button(label="+BlndPaint", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command='cmds.ArtPaintBlendShapeWeightsToolOptions()')
        cmds.button(label="BURN", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.heyWitch_burn, k, v))

        msw_grab_tabs = self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs']
        if cmds.layout(msw_grab_tabs, ex=True):
            cmds.deleteUI(msw_grab_tabs, layout=True)

    def add_msw_mingler(self, k, v, msw_switch_Layout):
        homePass = v.mesh_skinning_workspace
        cmds.frameLayout(msw_switch_Layout, edit=True, label=k + ' Spawn Toolkit')
        cmds.button(label=">Grab", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.helper.heyWitch_grabMesh, k, v, self.global_work_space))
        cmds.button(label="+AddBrnGrp", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.heyWitch_addBrnGrpWindow, homePass))
        cmds.button(label="+AddUtlMsh", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.utility_mesh_manager.heyWitch_addUtlMshWindow, homePass))
        msw_grab_tabs = self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs']
        if cmds.layout(msw_grab_tabs, ex=True):
            cmds.deleteUI(msw_grab_tabs, layout=True)
        
    def sort_skinning_mingler(self, msw_tree_layout, msw_switch_Scroll, msw_switch_Layout, mswPane):
        selItem = cmds.treeView(msw_tree_layout, query=True, si=True)
        if "'s Mesh Skinning Workspace" in selItem[0]:
            itemKey=selItem[0].replace("'s Mesh Skinning Workspace", "")
        else:
            itemKey=selItem[0]
        mingler_type = 'Abort'
        for k0, v0 in self.global_work_space.items():
            for k1, v1 in v0.items():
                if hasattr(v1, 'object_type'):

                    if k1 == itemKey:
                        mingler_type = v1.object_type
                        mingler_value = v1
                        break
                    elif hasattr(v1, 'utility_nest') and itemKey in v1.utility_nest:
                        mingler_type = 'UtilityShop'
                        mingler_value = v1
                        break
                    elif v1.object_type == 'Spawn' and itemKey in v1.mesh_skinning_workspace.utility_nest:
                        mingler_type = 'UtilityShop'
                        mingler_value = v1.mesh_skinning_workspace
                    else:
                        print('found nothing for '+itemKey+' in '+k1)
        if mingler_type != 'Abort':
            msw_switch_Grid = self.global_work_space['miscData']['switch_layouts']['msw_switch']
            cmds.deleteUI(msw_switch_Grid, layout=True)
            msw_switch_Grid = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(120, 25), parent=msw_switch_Scroll)
            self.global_work_space['miscData']['switch_layouts']['msw_switch'] = msw_switch_Grid
            if mingler_type == 'Spawn':
                self.add_msw_mingler(itemKey, mingler_value, msw_switch_Layout)
            elif mingler_type == 'BurnBaseMesh':
                self.add_burn_base_mingler(itemKey, mingler_value, msw_switch_Layout)
            elif mingler_type == 'TargetMesh':
                self.add_target_mingler(itemKey, mingler_value, msw_switch_Layout, mswPane)
            elif mingler_type == 'OutputMesh':
                self.add_burnout_mingler(itemKey, mingler_value, msw_switch_Layout)
            elif mingler_type == 'UtilityShop':
                self.add_utility_mingler(itemKey, mingler_value, msw_switch_Layout, mswPane)
            elif mingler_type == 'ChopMesh':
                self.add_chop_mingler(itemKey, mingler_value, msw_switch_Layout, mswPane)
            else:
                print('unrecognized')


    def heyWitch_makeSpawn(self, *args):
        # makes selected geometry into spawn class objects and sends them to the mesh skinning workspace proc
        to_make_into_spawn = cmds.ls(selection=True, type='transform')
        vert_vals = {}
        for mesh in to_make_into_spawn:
            self.helper.heyWitch_blankSlate(mesh)
            mesh_vert_count = cmds.polyEvaluate(mesh, v=True)
            cmds.select(clear=True)
            cmds.group(empty=True, name=(mesh + '_msw_grp'))
            cmds.parent(mesh, (mesh + '_msw_grp'))
            cmds.parent((mesh + '_msw_grp'), 'btw_AllGeo_grp')
            the_spawn = Spawn(mesh)
            for current_vertex in range(mesh_vert_count):
                current_vertex_str = "vtx[" + str(current_vertex) + "]"
                # must remember to make proc that actually assigns values to the vertex of a mesh,
                # keeping it nameless in the dict right now for easier maths
                vert_vals[current_vertex_str] = {}
            the_spawn.vert_vals = vert_vals.copy()
            the_spawn.mesh_skinning_workspace = MeshSkinningWorkspace()
            the_spawn.heyWitch_buildMeshSkinningWorkspace()
            self.global_work_space['spawnStorage'][the_spawn.mesh_spawn_name] = the_spawn
            tree_layout = self.global_work_space['miscData']['switch_layouts']['msw_tree_layout']
            cmds.treeView(tree_layout, edit=True, addItem=(the_spawn.mesh_spawn_name+"'s Mesh Skinning Workspace", ""))
            vert_vals.clear()
            

    def heyWitch_addBrnGrpWindow(self, homePass, *args):
        # homeString=homePass.mesh_label
        randomNo = random.randint(100, 999)
        # timeOfCreation=cmds.date(time=True, format='hhmmss')
        brnGrpLabelPrompt = cmds.promptDialog(
            message=("Enter Burn Group Label for " + homePass.mesh_spawn_name if isinstance(homePass, MeshSkinningWorkspace) else homePass.target_mesh_label),
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        if brnGrpLabelPrompt == 'OK':
            brnGrpLabelTextFld = cmds.promptDialog(query=True, text=True)
            if brnGrpLabelTextFld == "":
                brnGrpLabelTextFld = str(randomNo)
                self.heyWitch_addBurnGroup(homePass, brnGrpLabelTextFld)
            else:
                self.heyWitch_addBurnGroup(homePass, brnGrpLabelTextFld)

    def heyWitch_addBurnGroup(self, homePass, brnGrpLabelTextFld):
        spwnScan = self.global_work_space['spawnStorage']
        for x in spwnScan.values():
            if x.mesh_spawn_name == homePass.mesh_spawn_name:
                spawnMesh = x
        burnBaseMeshName = "brnBseMsh_" + brnGrpLabelTextFld
        # making the burn base mesh
        cmds.duplicate(str(spawnMesh.mesh_spawn_name), name=burnBaseMeshName)
        self.helper.heyWitch_blankSlate(burnBaseMeshName)
        # outliner group
        cmds.select(clear=True)
        if homePass.object_type == 'MeshSkinningWorkspace':
            homeGroup = homePass.mesh_spawn_name + "_msw_grp"
            tree_parent = homePass.mesh_spawn_name + "'s Mesh Skinning Workspace'"
        else:
            homeGroup = homePass.burn_group_label + '_tgt_grp'
            tree_parent = homePass.mesh_label
        burnGroupName = burnBaseMeshName
        cmds.group(empty=True, name=burnGroupName + '_brn_grp')
        cmds.group(empty=True, name=(burnGroupName + '_tgt_grp'))
        cmds.group(empty=True, name=(burnGroupName + '_out_grp'))
        cmds.parent(burnBaseMeshName, (burnGroupName + '_tgt_grp'), (burnGroupName + '_out_grp'),
                    (burnGroupName + '_brn_grp'))
        cmds.parent((burnGroupName + '_brn_grp'), homeGroup)
        # object bookkeeping
        burnBaseMesh = BurnBaseMesh()
        burnBaseMesh.burn_group_label = burnBaseMeshName
        burnBaseMesh.vert_vals = spawnMesh.vert_vals
        burnBaseMesh.mesh_spawn_name = spawnMesh.mesh_spawn_name
        burnBaseMesh.burn_group_home = homePass
        self.global_work_space['burnGroupStorage'][burnBaseMeshName] = burnBaseMesh
        tree_layout = self.global_work_space['miscData']['switch_layouts']['msw_tree_layout']
        cmds.treeView(tree_layout, edit=True,
                      addItem=(burnBaseMesh.burn_group_label, tree_parent), cs=True)
        cmds.treeView(tree_layout, edit=True, selectItem=(burnBaseMesh.burn_group_label, True))
        self.helper.heyWitch_grabMesh(burnBaseMeshName, burnBaseMesh, self.global_work_space)
        

    def heyWitch_addTgtMshWindow(self, basePass, *args):
        randomNo = random.randint(100, 999)
        tgtMshLabelPrompt = cmds.promptDialog(
            message=("Enter Target Mesh Label for " + str(basePass.burn_group_label)),
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        if tgtMshLabelPrompt == 'OK':
            tgtMshLabelTextFld = cmds.promptDialog(query=True, text=True)
            if tgtMshLabelTextFld == "":
                tgtMshLabelTextFld = str(randomNo)
                self.heyWitch_addTargetMesh(basePass, tgtMshLabelTextFld)
            else:
                self.heyWitch_addTargetMesh(basePass, tgtMshLabelTextFld)

    def heyWitch_addTargetMesh(self, basePass, tgtMshLabelTextFld):
        spawnMesh = basePass.mesh_spawn_name
        baseMesh = basePass.burn_group_label
        targetMeshName = "tgtMsh_" + tgtMshLabelTextFld
        cmds.duplicate(spawnMesh, name=targetMeshName)
        self.helper.heyWitch_blankSlate(targetMeshName)
        # outliner group
        cmds.select(clear=True)
        cmds.parent(targetMeshName, (baseMesh + '_tgt_grp'))
        ###CHECK IF BLEND NODE EXISTS FIRST!
        if cmds.objExists(baseMesh + "_blndNde"):
            tgtNo = len(cmds.listConnections(baseMesh + "_blndNde.it[0].iti")) + 1
            cmds.blendShape((baseMesh + "_blndNde"), edit=True, t=(baseMesh, tgtNo, targetMeshName, 1))
        else:
            cmds.blendShape(targetMeshName, baseMesh, n=(baseMesh + "_blndNde"))
        cmds.setAttr(baseMesh + "_blndNde." + targetMeshName, 1)
        targetMesh = TargetMesh()
        targetMesh.mesh_spawn_name = spawnMesh
        targetMesh.burn_group_label = baseMesh
        targetMesh.vert_vals = basePass.vert_vals
        targetMesh.target_mesh_label = str(targetMeshName)
        self.global_work_space['targetStorage'][targetMeshName] = targetMesh
        tree_layout = self.global_work_space['miscData']['switch_layouts']['msw_tree_layout']
        cmds.treeView(tree_layout, edit=True,
                      addItem=(targetMeshName, targetMesh.burn_group_label), cs=True)
        cmds.treeView(tree_layout, edit=True, selectItem=(targetMeshName, True))
        self.helper.heyWitch_grabMesh(targetMeshName, targetMesh, self.global_work_space)
        

    def heyWitch_burn(self, baseKey, baseValue, *args):
        allJntList = []

        # vert val datasort
        tmpVrtValsDict = deepcopy(baseValue.vert_vals)
        targetList = cmds.listConnections(baseKey + '_blndNde.it[0].iti')
        for k1, v1 in baseValue.vert_vals.items():
            vertNoTemp = k1.replace('vtx[', '')
            vertNo = vertNoTemp.replace(']', '')
            for targetNo in range(len(targetList)):
                targetMesh = targetList[targetNo]
                blendVal = cmds.getAttr(baseKey + '_blndNde.it[0].itg[' + str(targetNo) + '].tw[' + vertNo + ']')
                tmpVrtValsDict[k1][targetMesh] = {'blend_val': blendVal, 'joint_influences': {}}
                for k2, v2 in self.global_work_space['targetStorage'].items():
                    # could avoid this by storing the target mesh objects directly into the base mesh
                    if k2 == targetMesh:
                        for k3, v3 in self.global_work_space['bindJointClustersStorage'].items():
                            if k3 == v2.bind_joint_cluster:
                                tmpJntInfDict = {}
                                for bindJoint in v3.bind_joints_list:
                                    skinVal = cmds.skinPercent(v2.skin_cluster, (targetMesh + '.vtx[' + vertNo + ']'),
                                                               transform=bindJoint, query=True)
                                    tmpJntInfDict[bindJoint] = skinVal
                                    if bindJoint not in allJntList:
                                        allJntList.append(bindJoint)
                                tmpVrtValsDict[k1][targetMesh]['joint_influences'] = deepcopy(tmpJntInfDict)
                                tmpJntInfDict.clear()

        baseValue.vert_vals = deepcopy(tmpVrtValsDict)
        # tmpVrtValsDict.clear()

        # vert val maths
        outMeshVertVals = {}
        for k4, v4 in baseValue.vert_vals.items():
            outMeshVertVals[k4] = {}
            jntsInVertex = []
            blendValList = []
            blendTgtList = []
            for k5, v5 in v4.items():
                blendTgtList.append(k5)
                blendValList.append(v5['blend_val'])
            targetSum = sum(float(blendVal) for blendVal in blendValList)
            if targetSum > 1:
                for k6, v6 in v4.items():
                    oldVal = v6['blend_val']
                    v6['blend_val'] = oldVal / targetSum
            for lstJnt in allJntList:
                lstJntValList = []
                for k7, v7 in v4.items():
                    if lstJnt in v7['joint_influences']:
                        jntsInVertex.append(lstJnt)
                        lstJntValList.append((v7['joint_influences'][lstJnt]) * (v7['blend_val']))
                lstJntSum = sum(float(lstJntVal) for lstJntVal in lstJntValList)
                if lstJnt in jntsInVertex:
                    outMeshVertVals[k4][lstJnt] = lstJntSum

        # outmesh creation
        spawnMesh = baseValue.mesh_spawn_name
        outMesh = baseKey.replace('brnBseMsh', 'brnOutMsh')
        cmds.duplicate(spawnMesh, name=outMesh)
        outMeshName = str(outMesh)
        outMesh = OutputMesh()
        outMesh.mesh_spawn_name = spawnMesh
        outMesh.burn_group_label = baseKey
        cmds.parent(outMeshName, (baseKey + '_out_grp'))
        self.global_work_space['outMeshStorage'][outMeshName] = outMesh
        self.helper.heyWitch_grabMesh(outMeshName, outMesh, self.global_work_space)
        # bjc creation
        cmds.select(clear=True)
        for k9, v9 in self.global_work_space['bindJointClustersStorage'].items():
            if v9.bind_joints_list == allJntList:
                cmds.select(outMeshName)
                self.bind_joint_cluster_manager.heyWitch_bindToSelectedMsh(k9, v9)
        if cmds.objExists(outMeshName + "_sknClstr"):
            print('Skincluster found')
        else:
            for x in allJntList:
                cmds.select(x, add=True)
            self.bind_joint_cluster_manager.heyWitch_makeBindJointCluster()
            cmds.select(outMeshName)
            for k10, v10 in self.global_work_space['bindJointClustersStorage'].items():
                if v10.bind_joints_list == allJntList:
                    self.bind_joint_cluster_manager.heyWitch_bindToSelectedMsh(k10, v10)
        # #outmesh value transfer
        for k11, v11 in outMeshVertVals.items():
            vertNoTemp = k11.replace('vtx[', '')
            vertNo = vertNoTemp.replace(']', '')
            for k12, v12 in v11.items():
                cmds.skinPercent(outMesh.skin_cluster, outMeshName + '.vtx[' + vertNo + ']', transformValue=(k12, v12))
        tree_layout = self.global_work_space['miscData']['switch_layouts']['msw_tree_layout']
        cmds.treeView(tree_layout, edit=True,
                      addItem=(outMeshName, outMesh.burn_group_label), cs=True)
        cmds.treeView(tree_layout, edit=True, selectItem=(outMeshName, True))
        