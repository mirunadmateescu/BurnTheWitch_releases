import random
from functools import partial

from maya import cmds

from bin.classes.classes import Map


class MainWindowManager:
    global_work_space = {}
    influence_manager = None
    chop_mesh_manager = None
    utility_mesh_manager = None
    burn_group_manager = None
    bind_joint_cluster_manager = None
    magic_maps_manager = None
    main_tabs_manager = None
    helper = None

    # default constructor
    def __init__(self, global_work_space, influence_manager, chop_mesh_manager, burn_group_manager,
                 bind_joint_cluster_manager, utility_mesh_manager, magic_maps_manager, main_tabs_manager,
                 helper):
        self.global_work_space = global_work_space
        self.influence_manager = influence_manager
        self.chop_mesh_manager = chop_mesh_manager
        self.utility_mesh_manager = utility_mesh_manager
        self.burn_group_manager = burn_group_manager
        self.bind_joint_cluster_manager = bind_joint_cluster_manager
        self.magic_maps_manager = magic_maps_manager
        self.main_tabs_manager = main_tabs_manager
        self.helper = helper

    def refresh_main_window(self, main_window, witch_dock, *args):
        if cmds.window(main_window, ex=True):
            # cmds.deleteUI(witch_dock, control=True)
            cmds.deleteUI(main_window, window=True)
            self.create_main_window()
        else:
            self.create_main_window()

    def create_main_window(self):
        main_window = cmds.window(title=".Burn the witch "+u"\u0028\u256F\u00B0\u25A1\u00B0\u0029\u256F\uFE35\u0020\u253B\u2501\u253B", widthHeight=(500, 560), tlc=(450, 1100))
        cmds.scrollLayout()
        # witch_dock = cmds.dockControl(label=".Burn the witch", area='right', content=main_window, fl=True, width=510,
        #                               height=570)
        cmds.text(label='Pickle path is: ' + str(self.global_work_space['miscData']['picklePath']))
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(100, 25))
        cmds.button(label='SaveData', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.helper.heyWitch_stashDictionary, self.global_work_space))
        cmds.button(label='Refresh', height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.refresh_main_window, main_window))
        cmds.setParent('..')
        tab_layout = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

        toolkit_column_layout = self.main_tabs_manager.toolkit_tab_builder()

        mswPane = self.main_tabs_manager.msw_tab_builder()
        mapsPane = self.main_tabs_manager.magic_maps_tab_builder()
        bjcCol = self.main_tabs_manager.bjc_tab_builder()

        cmds.tabLayout(tab_layout, edit=True, tabLabel=(
            (toolkit_column_layout, 'Toolkit'), (mswPane, 'Mesh Skinning Workspace'), (mapsPane, 'Magic Maps'), (bjcCol, 'Bind Joint Clusters')))
        # cmds.setParent('..')
        cmds.setParent('..')
        # end of scroll and row layouts for both
        cmds.showWindow(main_window)
        cmds.window(main_window, edit=True, visible=True)

