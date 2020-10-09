import random
from functools import partial

from maya import cmds

from bin.classes.classes import Map


class MainTabsManager:
    global_work_space = {}
    influence_manager = None
    chop_mesh_manager = None
    utility_mesh_manager = None
    burn_group_manager = None
    bind_joint_cluster_manager = None
    magic_maps_manager = None
    helper = None

    # default constructor
    def __init__(self, global_work_space, influence_manager, chop_mesh_manager, burn_group_manager,
                 bind_joint_cluster_manager, utility_mesh_manager, magic_maps_manager, helper):
        self.global_work_space = global_work_space
        self.influence_manager = influence_manager
        self.chop_mesh_manager = chop_mesh_manager
        self.utility_mesh_manager = utility_mesh_manager
        self.burn_group_manager = burn_group_manager
        self.bind_joint_cluster_manager = bind_joint_cluster_manager
        self.magic_maps_manager = magic_maps_manager
        self.helper = helper

    def add_to_tree(self, tree_layout, child, parent):
        cmds.treeView(tree_layout, edit=True, addItem=(child, parent))

    def send_utility_scout(self, homePass, mswTreeView, parent):
        for utility_shop in homePass.utility_nest:
            self.add_to_tree(mswTreeView, utility_shop, parent)
            self.send_chop_scout(mswTreeView, utility_shop)
            self.send_gulp_scout(mswTreeView, utility_shop)

    def send_chop_scout(self, mswTreeView, utility_shop):
        for k, v in self.global_work_space['chopMeshStorage'].items():
            if v.utl_wkshp_label == utility_shop:
                self.add_to_tree(mswTreeView, k, utility_shop)
    
    def send_gulp_scout(self, mswTreeView, utility_shop):
        print('gulp scout out of order')
        
    def send_target_scout(self, mswTreeView, baseMesh):
        for k, v in self.global_work_space['targetStorage'].items():
            if v.burn_group_label == baseMesh.burn_group_label:
                self.add_to_tree(mswTreeView, v.target_mesh_label, v.burn_group_label)
                self.send_burn_group_scout(v, mswTreeView, v.target_mesh_label)
                self.send_utility_scout(v, mswTreeView, v.target_mesh_label)
                
    def send_burnout_scout(self, mswTreeView, baseMesh):
        for k, v in self.global_work_space['outMeshStorage'].items():
            if v.burn_group_label == baseMesh.burn_group_label:
                self.add_to_tree(mswTreeView, k, v.burn_group_label)

    def send_burn_group_scout(self, homePass, mswTreeView, parent):
        for k, v in self.global_work_space['burnGroupStorage'].items():
            if v.burn_group_home == homePass:
                self.add_to_tree(mswTreeView, v.burn_group_label, parent)
                self.send_burnout_scout(mswTreeView, v)
                self.send_target_scout(mswTreeView, v)
        
    def toolkit_tab_builder(self):
        toolkit_column_layout = cmds.columnLayout(adjustableColumn=True, width=490)
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(100, 25))
        cmds.button(label='+MshSknWks', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.burn_group_manager.heyWitch_makeSpawn))
        cmds.button(label='+BndJntClstr', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.bind_joint_cluster_manager.heyWitch_makeBindJointCluster))
        cmds.button(label='+JntFromLoop', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_jntFromLoop))
        cmds.button(label='NameChopByJnt', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_nameGeoChopByJnt))
        cmds.button(label='+MkeInfWin', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.influence_manager.heyWitch_externalInfWinPicker))
        cmds.button(label='+MkeChpClrSet', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.chop_mesh_manager.heyWitch_addHomelessChopClrSet))
        cmds.setParent('..')
        cmds.frameLayout(label='Homeless Influence Windows', collapsable=True)
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(100, 25))
        for k0, v0 in self.global_work_space['miscData']['homelessInfWins'].items():
            cmds.button(label=k0, height=25, backgroundColor=[0.3, 0.3, 0.3],
                        command=partial(self.influence_manager.heyWitch_launchInfSetup, k0, v0))
        cmds.setParent('..')
        cmds.frameLayout(label='Homeless Chop Sets', collapsable=True)
        for k1, v1 in self.global_work_space['miscData']['homelessChopClrSets'].items():
            cmds.rowLayout(numberOfColumns=4)
            cmds.text(label=k1)
            cmds.button(label="SelectMesh", height=25, backgroundColor=[0.3, 0.3, 0.3],
                        command=partial(self.helper.heyWitch_selectRawMesh, k1))
            cmds.button(label="+AddChpShdr", height=25, backgroundColor=[0.3, 0.3, 0.3],
                        command=partial(self.chop_mesh_manager.heyWitch_addChopShader, k1, v1))
            cmds.button(label="SelByChopShader", height=25, backgroundColor=[0.3, 0.3, 0.3],
                        command=partial(self.chop_mesh_manager.heyWitch_selByChopShader, k1, v1))
            cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        return toolkit_column_layout
    
    def msw_tab_builder(self):
        mswPane = cmds.paneLayout(configuration='right3', st=1, height=455)
        mswFormLayout = cmds.formLayout(parent=mswPane)
        mswTreeView = cmds.treeView(parent=mswFormLayout, abr=False)
        cmds.formLayout(mswFormLayout, e=True, attachForm=(mswTreeView, 'top', 2))
        cmds.formLayout(mswFormLayout, e=True, attachForm=(mswTreeView, 'left', 2))
        cmds.formLayout(mswFormLayout, e=True, attachForm=(mswTreeView, 'bottom', 2))
        cmds.formLayout(mswFormLayout, e=True, attachForm=(mswTreeView, 'right', 2))
        msw_switch_Layout = cmds.frameLayout(parent=mswPane, label='Mesh Skinning Workspace Toolkit')
        msw_switch_Scroll = cmds.scrollLayout(backgroundColor=[0.2, 0.2, 0.2])
        msw_switch_Grid = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(120, 25))
        self.global_work_space['miscData']['switch_layouts']['msw_switch'] = msw_switch_Grid
        self.global_work_space['miscData']['switch_layouts']['msw_tree_layout'] = mswTreeView
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        msw_grab_tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, parent=mswPane)
        testtext = cmds.text(label='nothing to see here')
        cmds.tabLayout(msw_grab_tabs, edit=True, tabLabel=(testtext, ''))
        self.global_work_space['miscData']['switch_layouts']['msw_grab_tabs'] = msw_grab_tabs
        cmds.setParent('..')
        cmds.setParent('..')

        spwnScan = self.global_work_space['spawnStorage']
        for k, v in spwnScan.items():
            if v.object_type == "Spawn":
                msw_name = k + "'s Mesh Skinning Workspace"
                self.add_to_tree(mswTreeView, msw_name, '')
                homePass = v.mesh_skinning_workspace
                self.send_burn_group_scout(homePass, mswTreeView, msw_name)
                self.send_utility_scout(homePass, mswTreeView, msw_name)
        cmds.treeView(mswTreeView, edit=True,
                      scc=partial(self.burn_group_manager.sort_skinning_mingler, mswTreeView, msw_switch_Scroll,
                                  msw_switch_Layout, mswPane))
        return mswPane

    def magic_maps_tab_builder(self):
        mapsPane = cmds.paneLayout(configuration='right3', st=1)
        mapsFormLayout = cmds.formLayout(parent=mapsPane)
        mapsTreeView = cmds.treeView(parent=mapsFormLayout, abr=False)
        cmds.formLayout(mapsFormLayout, e=True, attachForm=(mapsTreeView, 'top', 2))
        cmds.formLayout(mapsFormLayout, e=True, attachForm=(mapsTreeView, 'left', 2))
        cmds.formLayout(mapsFormLayout, e=True, attachForm=(mapsTreeView, 'bottom', 2))
        cmds.formLayout(mapsFormLayout, e=True, attachForm=(mapsTreeView, 'right', 2))
        stashedMapsLayout = cmds.frameLayout(parent=mapsPane, label='Maps Library')
        stashedMapsScroll = cmds.scrollLayout(backgroundColor=[0.2, 0.2, 0.2])
        stashedMapsGrid = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(120, 25))
        self.global_work_space['miscData']['mapOps']['crt_sel_layout'] = stashedMapsGrid
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.columnLayout(parent=mapsPane)
        stash_bar_rows = cmds.rowLayout(numberOfColumns=3)
        self.helper.heyWitch_tidyRows(stash_bar_rows)
        mapNameTxtFld = cmds.textField(width=200)
        cmds.button(label='Stash',
                    command=partial(self.magic_maps_manager.mapStash, mapsTreeView, mapNameTxtFld, stashedMapsScroll,
                                    stashedMapsLayout,
                                    'temp_map'))
        # cmds.button(label='LoadToSlot')
        cmds.setParent('..')
        cmds.frameLayout(label='Map Maths')
        map_maths_rows = cmds.rowLayout(numberOfColumns=5)
        self.helper.heyWitch_tidyRows(map_maths_rows)
        slotOneCol = cmds.columnLayout()
        slotOneCharge = cmds.text(label='closed')
        slotOneButton = cmds.button(label='OpenSlot')
        cmds.button(label='MakeCrt',
                    command=partial(self.magic_maps_manager.overwriteSelected, mapsTreeView, 'slot_one'))
        cmds.setParent('..')
        mathsCol = cmds.columnLayout()
        cmds.checkBox(label='+')
        cmds.checkBox(label='-')
        cmds.checkBox(label='invert')
        cmds.setParent('..')
        slotTwoCol = cmds.columnLayout()
        slotTwoCharge = cmds.text(label='closed')
        slotTwoButton = cmds.button(label='OpenSlot')
        cmds.button(label='MakeCrt',
                    command=partial(self.magic_maps_manager.overwriteSelected, mapsTreeView, 'slot_two'))
        cmds.setParent('..')
        cmds.button(slotOneButton, edit=True,
                    command=partial(self.magic_maps_manager.openSlot, 'slot_one', slotOneCharge, slotTwoCharge))
        cmds.button(slotTwoButton, edit=True,
                    command=partial(self.magic_maps_manager.openSlot, 'slot_two', slotTwoCharge, slotOneCharge))
        cmds.columnLayout()
        doMathsBtn = cmds.button(label='=')
        cmds.setParent('..')
        aftermathCol = cmds.columnLayout()
        aftermathCharge = cmds.text(label='')
        aftermathTxtFld = cmds.textField()
        cmds.button(label='Stash',
                    command=partial(self.magic_maps_manager.mapStash, mapsTreeView, aftermathTxtFld, stashedMapsScroll,
                                    stashedMapsLayout,
                                    'math_map'))
        cmds.button(label='MakeCrt',
                    command=partial(self.magic_maps_manager.overwriteSelected, mapsTreeView, 'math_map'))
        mapVals = self.global_work_space['miscData']['mapOps']['math_map'].copy()
        cmds.button(label='LoadToSlot', command=partial(self.magic_maps_manager.loadToSlot, 'math_map', mapVals))
        cmds.button(doMathsBtn, edit=True, command=partial(self.magic_maps_manager.mapMaths, mathsCol, aftermathCharge))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.paneLayout(mapsPane, edit=True, shp=3)
        cmds.showWindow()
        blndNodeList = cmds.ls(type='blendShape')
        cmds.treeView(mapsTreeView, edit=True, addItem=("Blend Maps", ""))
        cmds.treeView(mapsTreeView, edit=True, addItem=("Skinweight Maps", ""))
        for blndNode in blndNodeList:
            cmds.treeView(mapsTreeView, edit=True, addItem=(blndNode, "Blend Maps"))
            targetList = cmds.listConnections(blndNode + '.it[0].iti')
            for blndTgt in targetList:
                unique_item = blndNode+'_'+blndTgt
                new_map = Map()
                new_map.crt_map_id = unique_item
                new_map.parent_node = blndNode
                new_map.map_type = "blend"
                new_map.inf_or_tgt = blndTgt
                tgtIndex = 0
                while tgtIndex < 10:
                    crtTgt = cmds.listConnections(blndNode + '.it[0].itg[' + str(tgtIndex) + '].iti[6000].igt')
                    if crtTgt != None:
                        if blndTgt == crtTgt[0]:
                            break
                        else:
                            tgtIndex += 1
                    else:
                        tgtIndex += 1
                new_map.index = str(tgtIndex)
                cmds.treeView(mapsTreeView, edit=True, addItem=(unique_item, blndNode))
                cmds.treeView(mapsTreeView, edit=True, dl=[unique_item, blndTgt])
                self.global_work_space['miscData']['mapOps']['crt_scene_maps'][unique_item] = new_map
                if not unique_item in self.global_work_space['miscData']['mapOps']['stashed_maps']:
                    self.global_work_space['miscData']['mapOps']['stashed_maps'][unique_item] = {}
        sknClstrList = cmds.ls(type='skinCluster')
        for sknClstr in sknClstrList:
            cmds.treeView(mapsTreeView, edit=True, addItem=(sknClstr, "Skinweight Maps"))
            infList = cmds.skinCluster(sknClstr, query=True, inf=True)
            for infJnt in infList:
                unique_item = sknClstr + '_' + infJnt
                new_map = Map()
                new_map.crt_map_id = unique_item
                new_map.parent_node = sknClstr
                new_map.map_type = "skn_clstr"
                new_map.inf_or_tgt = infJnt
                cmds.treeView(mapsTreeView, edit=True, addItem=(unique_item, sknClstr))
                cmds.treeView(mapsTreeView, edit=True, dl=[unique_item, infJnt])
                self.global_work_space['miscData']['mapOps']['crt_scene_maps'][unique_item] = new_map
                if not unique_item in self.global_work_space['miscData']['mapOps']['stashed_maps']:
                    self.global_work_space['miscData']['mapOps']['stashed_maps'][unique_item] = {}
        cmds.treeView(mapsTreeView, edit=True,
                      scc=partial(self.magic_maps_manager.mapHighlight, mapsTreeView, stashedMapsScroll,
                                  stashedMapsLayout))
        return mapsPane

    def bjc_tab_builder(self):
        bjcCol = cmds.columnLayout(adj=True)
        for k, v in self.global_work_space['bindJointClustersStorage'].items():
            self.bind_joint_cluster_manager.add_bjc_mingler(k, v, bjcCol)
        self.global_work_space['miscData']['switch_layouts']['bjc_switch'] = bjcCol
        # end of row layout
        # cmds.setParent('..')
        cmds.setParent('..')
        return bjcCol