from copy import deepcopy

from maya import cmds


class CloneManager:
    global_work_space = {}
    bind_joint_cluster_manager = None
    helper = None

    def __init__(self, global_work_space, bind_joint_cluster_manager, helper):
        self.global_work_space = global_work_space
        self.bind_joint_cluster_manager = bind_joint_cluster_manager
        self.helper = helper

    def heyWitch_cloneSkinCluster(self, cloneKey, cloneVal, *args):
        sknClstrToClonePrompt = cmds.promptDialog(
            message="Skin cluster to clone: ",
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

        if sknClstrToClonePrompt == 'OK':
            extSknClstr = cmds.promptDialog(query=True, text=True)
            # figure out if vertices match
            shapeToClone = cmds.skinCluster(extSknClstr, query=True, geometry=True)
            transformToClone = shapeToClone[0].replace('Shape', '')
            if cmds.objExists(transformToClone):
                tempVertBook = {}
                if cmds.polyCompare(transformToClone, cloneKey) == 0:
                    vertMatch = True
                    for k5, v5 in cloneVal.vert_vals.items():
                        extInfList = cmds.skinCluster(extSknClstr, query=True, inf=True)
                        for joint in extInfList:
                            skinVal = cmds.skinPercent(extSknClstr, (transformToClone + '.' + k5), transform=joint,
                                                       query=True)
                            tempVertBook[k5] = {joint: skinVal}
                    print('Vertices match, copying skinweights done vert to vert')
                else:
                    print('Not all vertices match, copying skinweights may not give precise results')
                    extInfList = cmds.skinCluster(extSknClstr, query=True, inf=True)
                    vertMatch = False
            else:
                print('Could not find transform node')
                extInfList = cmds.skinCluster(extSknClstr, query=True, inf=True)
                vertMatch = False
            # create bjc and bind to clone
            for k0, v0 in self.global_work_space['bindJointClustersStorage'].items():
                if v0.bind_joints_list == extInfList:
                    cmds.select(cloneKey)
                    self.bind_joint_cluster_manager.heyWitch_bindToSelectedMsh(k0, v0)
            if cmds.objExists(cloneKey + '_sknClstr'):
                print('Skincluster found')
            else:
                cmds.select(extInfList)
                self.bind_joint_cluster_manager.heyWitch_makeBindJointCluster()
                bjcList = []
                for x in extInfList:
                    if 'btw_' in x:
                        bjcList.append(x)
                    else:
                        bjcList.append('btw_' + x)
                for k1, v1 in self.global_work_space['bindJointClustersStorage'].items():
                    if v1.bind_joints_list == bjcList:
                        cmds.select(cloneKey)
                        self.bind_joint_cluster_manager.heyWitch_bindToSelectedMsh(k1, v1)
                if cmds.objExists(cloneKey + '_sknClstr'):
                    print('Skincluster found')
            # assign values to clone
            if vertMatch == True:
                cloneVal.vert_vals = deepcopy(tempVertBook)
                for k3, v3 in cloneVal.vert_vals.items():
                    for k4, v4 in v3.items():
                        if 'btw_' in k4:
                            cloneJnt = k4
                        else:
                            cloneJnt = 'btw_' + k4
                        cmds.skinPercent(cloneVal.skin_cluster, cloneKey + '.' + k3, transformValue=(cloneJnt, v4))
            elif vertMatch == False:
                cmds.select(shapeToClone[0], cloneKey)
                cmds.CopySkinWeights()
        