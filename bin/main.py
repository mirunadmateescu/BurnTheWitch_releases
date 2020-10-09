from maya import cmds

from bin.managers.influence_manager import InfluenceManager
from bin.managers.chop_mesh_manager import ChopMeshManager
from bin.managers.burn_group_manager import BurnGroupManager
from bin.managers.clone_manager import CloneManager
from bin.managers.main_tabs_manager import MainTabsManager
from bin.managers.utility_mesh_manager import UtilityMeshManager
from bin.managers.bind_joint_cluster_manager import BindJointClusterManager
from bin.managers.main_window_manager import MainWindowManager
from bin.managers.magic_maps_manager import MagicMapsManager
from bin.utilities.data_stash import get_pickle_dict_path, get_global_work_space
from bin.utilities.helper import Helper

BTW_ALL_JNTS_GRP = 'btw_AllJnts_grp'
BTW_ALL_GEO_GRP = 'btw_AllGeo_grp'
BTW_WORK_SPACE_GRP = 'btw_WorkSpace_grp'


class Main:

    def create_outliner_groups(self):
        if not cmds.objExists(BTW_WORK_SPACE_GRP):
            cmds.group(empty=True, name=BTW_WORK_SPACE_GRP)
            cmds.group(empty=True, name=BTW_ALL_GEO_GRP)
            cmds.group(empty=True, name=BTW_ALL_JNTS_GRP)
            cmds.parent(BTW_ALL_GEO_GRP, BTW_ALL_JNTS_GRP, BTW_WORK_SPACE_GRP)

    def execute(self):
        pickle_dict_path = get_pickle_dict_path()
        print("Pickle file path = " + str(pickle_dict_path))
        global_work_space = get_global_work_space(pickle_dict_path)
        print("Global workspace = " + str(global_work_space))
        self.create_outliner_groups()

        helper = Helper()
        bind_joint_cluster_manager = BindJointClusterManager(global_work_space, helper)
        clone_manager = CloneManager(global_work_space, bind_joint_cluster_manager, helper)
        influence_manager = InfluenceManager(global_work_space, helper)
        chop_mesh_manager = ChopMeshManager(helper, bind_joint_cluster_manager, global_work_space)
        utility_mesh_manager = UtilityMeshManager(global_work_space, helper)
        burn_group_manager = BurnGroupManager(global_work_space, bind_joint_cluster_manager, utility_mesh_manager,
                                              chop_mesh_manager, influence_manager, clone_manager, helper)
        magic_maps_manager = MagicMapsManager(global_work_space, helper)
        main_tabs_manager = MainTabsManager(global_work_space, influence_manager, chop_mesh_manager,
                                                burn_group_manager,bind_joint_cluster_manager, utility_mesh_manager,
                                                magic_maps_manager, helper)
        main_window_manager = MainWindowManager(global_work_space, influence_manager, chop_mesh_manager,
                                                burn_group_manager,bind_joint_cluster_manager, utility_mesh_manager,
                                                magic_maps_manager, main_tabs_manager, helper)

        main_window_manager.create_main_window()
