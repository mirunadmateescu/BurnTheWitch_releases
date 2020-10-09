import random
from copy import deepcopy
from functools import partial

from maya import cmds

from bin.classes.classes import BindJointCluster


class BindJointClusterManager:
    global_work_space = None
    helper = None

    def __init__(self, global_work_space, helper):
        self.global_work_space = global_work_space
        self.helper = helper

    def heyWitch_makeBindJointCluster(self, *args):
        bindJointsList = []
        jointsToCluster = cmds.ls(sl=True, type='transform')

        randomNo = random.randint(100, 999)
        bndJntClstrLabelPrompt = cmds.promptDialog(
            message="Enter Bind Joint Cluster Label for Selected",
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        bndJntClstrLabelTextFld = ""
        if bndJntClstrLabelPrompt == 'OK':
            bndJntClstrLabelTextFld = cmds.promptDialog(query=True, text=True)
            if bndJntClstrLabelTextFld == "":
                bndJntClstrLabelTextFld = str(randomNo)

        bndJntClstrName = bndJntClstrLabelTextFld + '_bndJntClstr'
        bndJntClstr = BindJointCluster()
        self.global_work_space['bindJointClustersStorage'][bndJntClstrName] = bndJntClstr
        for x in jointsToCluster:
            if 'btw_' in x:
                bindJointsList.append(x)
            elif cmds.objExists('btw_' + x):
                bindJointsList.append('btw_' + x)
            else:
                cmds.select(clear=True)
                bndJnt = 'btw_' + x
                cmds.joint(name=bndJnt)
                cmds.parentConstraint(x, bndJnt)
                cmds.parent(bndJnt, 'btw_AllJnts_grp')
                bindJointsList.append('btw_' + x)
            # not useful for now
            # self.global_work_space['bindJointStorage'][bndJnt]
        bndJntClstr.bind_joints_list = deepcopy(bindJointsList)
        switch_layout = self.global_work_space['miscData']['switch_layouts']['bjc_switch']
        self.add_bjc_mingler(bndJntClstrName, bndJntClstr, switch_layout)
        
    
    def add_bjc_mingler(self, k, v, switch_layout):
        bjc_rows_unit = cmds.rowLayout(numberOfColumns=4, parent=switch_layout)
        self.helper.heyWitch_tidyRows(bjc_rows_unit)

        cmds.columnLayout()
        cmds.text(label=k)
        cmds.setParent('..')

        cmds.columnLayout()
        bjc_influenced_meshes_layout = cmds.frameLayout(label='Influenced meshes')
        for m in v.influenced_meshes:
            cmds.text(label=m)
        cmds.setParent('..')
        cmds.setParent('..')
        v.influenced_meshes_switch_layout = bjc_influenced_meshes_layout
        cmds.columnLayout()
        cmds.frameLayout(label='Joints list', collapsable=True, collapse=True)
        for j in v.bind_joints_list:
            cmds.text(label=j)
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(120, 25))
        cmds.button(label="Select", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.heyWitch_selectBindJointCluster, k, v))
        cmds.button(label="+BndToSelMesh", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.heyWitch_bindToSelectedMsh, k, v))
        cmds.button(label="+ChopBndToSelMesh", height=25, backgroundColor=[0.3, 0.3, 0.3],
                    command=partial(self.heyWitch_chopBindSelectedMsh, k, v))
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.separator()
        
    def heyWitch_selectBindJointCluster(self, bjcKey, bjcValue, *args):
        cmds.select(clear=True)
        for jntToSel in bjcValue.bind_joints_list:
            cmds.select(jntToSel, add=True)

    def heyWitch_bindToSelectedMsh(self, clusterKey, clusterObj, *args):
        meshToBind = cmds.ls(sl=True, type='transform')
        meshName = str(meshToBind[0])
        cmds.select(clusterObj.bind_joints_list, add=True)
        cmds.skinCluster(n=meshName + '_sknClstr')
        tempInfMshList = []
        tempInfMshList = deepcopy(clusterObj.influenced_meshes)
        tempInfMshList.append(meshName)
        clusterObj.influenced_meshes = deepcopy(tempInfMshList)
        cmds.text(label=meshName, parent=clusterObj.influenced_meshes_switch_layout)
        for k0, v0 in self.global_work_space.items():
            for k1, v1 in v0.items():
                if hasattr(v1, 'mesh_spawn_name') and k1 == meshName:
                    v1.skin_cluster = meshName + '_sknClstr'
                    v1.bind_joint_cluster = str(clusterKey)
                # figure out if it's worth keeping the influenced mesh data on the bjc object as well
        

    def heyWitch_chopBindSelectedMsh(self, clusterKey, clusterObj, *args):
        pickedMesh = cmds.ls(sl=True, type='transform')
        cmds.select(clusterObj.bind_joints_list)
        cmds.select(pickedMesh, add=True)
        chopSknClstr = pickedMesh[0] + "_sknClstr"
        cmds.skinCluster(name=chopSknClstr)
        tempInfMshList = []
        tempInfMshList = deepcopy(clusterObj.influenced_meshes)
        tempInfMshList.append(pickedMesh[0])
        cmds.text(label=pickedMesh[0], parent=clusterObj.influenced_meshes_switch_layout)
        clusterObj.influenced_meshes = deepcopy(tempInfMshList)
        for k0, v0 in self.global_work_space['chopMeshStorage'].items():
            if k0 == pickedMesh[0]:
                v0.skin_cluster = chopSknClstr
                v0.bind_joint_cluster = clusterKey
                for bndJnt in clusterObj.bind_joints_list:
                    origJnt = bndJnt.replace('btw_', '')
                    for k1, v1 in v0.all_shaders.items():
                        if origJnt in k1:
                            for k2, v2 in v1.vert_vals.items():
                                cmds.skinPercent(chopSknClstr, k2, transformValue=(bndJnt, 1))
        