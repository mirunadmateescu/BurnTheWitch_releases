import json


class ChopShader():
    short_name = ""
    red = ""
    green = ""
    blue = ""
    set_label = ""
    vert_vals = {}
    single_sel_command = ""
    add_to_sel_command = ""

class ChopMesh():
    mesh_spawn_name = ""
    set_label = ""
    all_shaders = {}
    utl_wkshp_label = ""
    skin_cluster = ""
    bind_joint_cluster = ""
    influence_windows = []
    object_type = "ChopMesh"
    inf_grid_layout = ""
    int_config = {}


class HomelessChop():
    set_label = ""
    all_shaders = {}


class BindJointCluster():
    bind_joints_list = []
    influenced_meshes = []
    influenced_meshes_switch_layout = ''


class OutputMesh():
    mesh_spawn_name = ""
    burn_group_label = ""
    object_type = "OutputMesh"
    mesh_label = ""
    vert_vals = {}
    skin_cluster = ""
    bind_joint_cluster = ""
# not sure if it should inherit influence windows from previous targets


class TargetMesh():
    mesh_spawn_name = ""
    burn_group_label = ""
    object_type = "TargetMesh"
    mesh_label = ""
    vert_vals = {}
    utility_nest = []
    skin_cluster = ""
    bind_joint_cluster = ""
    influence_windows = []
    set_label = ""
    all_shaders = {}
    inf_grid_layout = ""
    int_config = {}


class BurnBaseMesh():
    mesh_spawn_name = ""
    object_type = "BurnBaseMesh"
    burn_group_label = ""
    burn_group_home = ""
    mesh_label = ""
    vert_vals = {}
    targets_nest = {}
    outputs_nest = {}
    set_label = ""
    all_shaders = {}
    int_config = {}


class MeshSkinningWorkspace():
    mesh_spawn_name = ""
    object_type = "MeshSkinningWorkspace"
    utility_nest = []

    def __str__(self):
        return "mesh_spawn_name: " + str(self.mesh_spawn_name) + "\nobject_type: " + str(self.object_type)


class Spawn:
    mesh_spawn_name = ""
    mesh_label = ""
    object_type = "Spawn"
    vert_vals = {}
    mesh_skinning_workspace = MeshSkinningWorkspace()

    def __init__(self, mesh_spawn_name):
        self.mesh_spawn_name = mesh_spawn_name

    def __str__(self):
        return "mesh_spawn_name: " + str(self.mesh_spawn_name) + "\nvert_vals: " + str(
            json.dumps(self.vert_vals, indent=2)) + "\nmesh_skinning_workspace: " + str(self.mesh_skinning_workspace)

    def heyWitch_buildMeshSkinningWorkspace(self):
        # creates a mesh skinning workspace object from a spawn and updates dictionary stash
        self.mesh_skinning_workspace.mesh_spawn_name = self.mesh_spawn_name
    # btwStorageString=json.dumps(globalWorkSpace)
    # heyWitch_stashDictionary(btwStorageString)


class SelectableInfluence():
    joint_name = ""
    joint_button = ""


class InfluenceWindow():
    inf_columns = []
    full_influence_list = []
    skin_cluster = ""
    inf_mesh_name = ""


class InfluenceColumn():
    inf_col_label = ""
    selectable_infs = []

class Map():
    parent_node = ""
    map_type = ""
    crt_map_id = ""
    inf_or_tgt = ""
    index = ""
