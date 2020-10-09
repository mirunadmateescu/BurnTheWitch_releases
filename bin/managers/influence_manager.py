import random
from copy import deepcopy
from functools import partial
import pymel.core as pm
from maya import cmds

from bin.classes.classes import SelectableInfluence, InfluenceColumn, InfluenceWindow


class InfluenceManager:
    global_work_space = {}
    helper = None

    def __init__(self, global_work_space, helper):
        self.global_work_space = global_work_space
        self.helper = helper

    def heyWitch_externalInfWinPicker(self, *args):
        cmds.window(title='Skincluster Picker', widthHeight=(400, 300))
        cmds.scrollLayout()
        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(125, 25))
        sknClstrLst = cmds.ls(type='skinCluster')
        for sknClstr in sknClstrLst:
            sknClstrGeo = cmds.skinCluster(sknClstr, query=True, geometry=True)
            mshNme = sknClstrGeo[0].replace('Shape', '')
            newButton = cmds.button(label=sknClstr, height=25, backgroundColor=[0.3, 0.3, 0.3],
                                    command=partial(self.heyWitch_makeInfluenceWindow, mshNme, sknClstr))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.showWindow()

    def heyWitch_scanForInfWinds(self, infMshObj):
        inf_grid_layout = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(125, 25))
        for infWin in infMshObj.influence_windows:
            for k0, v0 in self.global_work_space['miscData']['infWindowStorage'].items():
                if k0 == infWin:
                    cmds.button(label=infWin, height=25, backgroundColor=[0.3, 0.3, 0.3],
                                command=partial(self.heyWitch_launchInfSetup, k0, v0))
        cmds.setParent('..')
        return inf_grid_layout

    def heyWitch_selInfluence(self, infJnt, infWinSetup, *args):
        pm.mel.setSmoothSkinInfluence(infJnt.joint_name)
        self.global_work_space['miscData']['infJntSelect']["jntSlot0"] = deepcopy(
            self.global_work_space['miscData']['infJntSelect']["jntSlot1"])
        self.global_work_space['miscData']['infJntSelect']["jntSlot1"] = deepcopy(
            self.global_work_space['miscData']['infJntSelect']["jntSlot2"])
        self.global_work_space['miscData']['infJntSelect']["jntSlot2"] = infJnt
        for lstdJnt in infWinSetup.full_influence_list:
            for k0, v0 in self.global_work_space['miscData']['infJntSelect'].items():
                if k0 == 'jntSlot0':
                    if v0 != {} and lstdJnt == v0.joint_name:
                        cmds.button(v0.joint_button, edit=True, backgroundColor=[0.3, 0.3, 0.3])
                        cmds.setAttr(v0.joint_name + '.lockInfluenceWeights', 1)
                elif k0 == 'jntSlot1':
                    if v0 != {} and lstdJnt == v0.joint_name:
                        cmds.button(v0.joint_button, edit=True, backgroundColor=[0.5, 0.5, 0.3])
                        cmds.setAttr(v0.joint_name + '.lockInfluenceWeights', 0)
                elif k0 == 'jntSlot2':
                    if v0 != {} and lstdJnt == v0.joint_name:
                        cmds.button(v0.joint_button, edit=True, backgroundColor=[1.0, 1.0, 0.0])
                        cmds.setAttr(v0.joint_name + '.lockInfluenceWeights', 0)

    def heyWitch_addCheckedInfToList(self, infJnt, infToAdd, *args):
        infToAdd.append(infJnt)

    def heyWitch_removeCheckedInfToList(self, infJnt, infToAdd, *args):
        infToAdd.remove(infJnt)

    def heyWitch_addCheckedInfsToCol(self, infToAdd, colPick, infPickColumn, *args):
        selInfList = []
        infColList = []
        infColLbl = cmds.columnLayout(colPick, query=True, annotation=True)
        infColObj = InfluenceColumn()
        infColObj.inf_col_label = infColLbl
        infWinSetup = self.global_work_space['miscData']['infWindowStorage']['temp']
        for infJnt in infToAdd:
            infJntName = infJnt
            infJnt = SelectableInfluence()
            infJnt.joint_name = infJntName
            newInfBtn = cmds.button(label=infJnt.joint_name, parent=colPick)
            infJnt.joint_button = newInfBtn
            cmds.button(infJnt.joint_button, edit=True, height=25, backgroundColor=[0.3, 0.3, 0.3],
                        command=partial(self.heyWitch_selInfluence, infJnt, infWinSetup))
            selInfList.append(infJnt)
        infColObj.selectable_infs = deepcopy(selInfList)
        infColList = deepcopy(self.global_work_space['miscData']['infWindowStorage']['temp'].inf_columns)
        infColList.append(infColObj)
        self.global_work_space['miscData']['infWindowStorage']['temp'].inf_columns = deepcopy(infColList)
        #
        checkboxList = cmds.columnLayout(infPickColumn, query=True, ca=True)
        for chkBox in checkboxList:
            cmds.checkBox(chkBox, edit=True, value=0)
        del infToAdd[:]
        

    def heyWitch_makeInfluenceWindow(self, infMshName, infMshSknClstr, *args):
        tempInfWindow = InfluenceWindow()
        tempInfWindow.skin_cluster = infMshSknClstr
        tempInfWindow.inf_mesh_name = infMshName
        self.global_work_space['miscData']['infWindowStorage']['temp'] = tempInfWindow
        infWindowBld = cmds.window(title='Influence Window Builder', widthHeight=(500, 400))
        infScroll = cmds.scrollLayout()
        infWinRows = cmds.rowLayout(numberOfColumns=100)
        self.helper.heyWitch_tidyRows(infWinRows)
        cmds.setParent('..')
        utilityFrame = cmds.frameLayout(label='Influence Picker for ' + tempInfWindow.skin_cluster, collapsable=True)
        infToAdd = []
        infList = cmds.skinCluster(tempInfWindow.skin_cluster, query=True, influence=True)
        tempInfWindow.full_influence_list = infList
        infPickRows = cmds.rowLayout(numberOfColumns=2)
        self.helper.heyWitch_tidyRows(infPickRows)
        infPickColumn = cmds.columnLayout()
        for infJnt in infList:
            cmds.checkBox(label=infJnt, onc=partial(self.heyWitch_addCheckedInfToList, infJnt, infToAdd),
                          ofc=partial(self.heyWitch_removeCheckedInfToList, infJnt, infToAdd))
            cmds.setAttr(infJnt + '.lockInfluenceWeights', 1)
        cmds.setParent('..')
        cmds.columnLayout()
        cmds.text(label='Enter New Influence Window Name:')
        infWinTxtFld = cmds.textField()
        cmds.button(label='+SaveSetup', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_saveTempInfStorage, infWinTxtFld, tempInfWindow))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        infColA = cmds.columnLayout(parent=infWinRows, annotation='infColA')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColA, infPickColumn))
        cmds.setParent('..')
        infColB = cmds.columnLayout(parent=infWinRows, annotation='infColB')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColB, infPickColumn))
        cmds.setParent('..')
        infColC = cmds.columnLayout(parent=infWinRows, annotation='infColC')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColC, infPickColumn))
        cmds.setParent('..')
        infColD = cmds.columnLayout(parent=infWinRows, annotation='infColD')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColD, infPickColumn))
        cmds.setParent('..')
        infColE = cmds.columnLayout(parent=infWinRows, annotation='infColE')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColE, infPickColumn))
        cmds.setParent('..')
        infColF = cmds.columnLayout(parent=infWinRows, annotation='infColF')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColF, infPickColumn))
        cmds.setParent('..')
        infColG = cmds.columnLayout(parent=infWinRows, annotation='infColG')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColG, infPickColumn))
        cmds.setParent('..')
        infColH = cmds.columnLayout(parent=infWinRows, annotation='infColH')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColH, infPickColumn))
        cmds.setParent('..')
        infColI = cmds.columnLayout(parent=infWinRows, annotation='infColI')
        cmds.button(label='+AddInfs', height=25, backgroundColor=[0.35, 0.35, 0.35],
                    command=partial(self.heyWitch_addCheckedInfsToCol, infToAdd, infColI, infPickColumn))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.showWindow(infWindowBld)
        

    def heyWitch_saveTempInfStorage(self, infWinTxtFld, tempInfWindow, *args):
        infWinLbl = cmds.textField(infWinTxtFld, query=True, text=True)
        randomNo = random.randint(100, 999)
        if infWinLbl == "":
            infWinLbl = str(randomNo)
        storageSearch = ['chopMeshStorage', 'targetStorage']
        tempInfWinList = []
        isWinHomeless = True
        for storage in storageSearch:
            for k0, v0 in self.global_work_space[storage].items():
                if k0 == tempInfWindow.inf_mesh_name:
                    tempInfWinList = deepcopy(v0.influence_windows)
                    tempInfWinList.append(infWinLbl)
                    v0.influence_windows = deepcopy(tempInfWinList)
                    isWinHomeless = False
                    self.global_work_space['miscData']['infWindowStorage'][infWinLbl] = deepcopy(tempInfWindow)
                    saved_inf_win = self.global_work_space['miscData']['infWindowStorage'][infWinLbl]
                    cmds.button(label=infWinLbl, height=25, backgroundColor=[0.3, 0.3, 0.3], parent=v0.inf_grid_layout,
                                command=partial(self.heyWitch_launchInfSetup, infWinLbl, saved_inf_win))
        if isWinHomeless == True:
            self.global_work_space['miscData']['homelessInfWins'][infWinLbl] = deepcopy(tempInfWindow)
        

    def heyWitch_launchInfSetup(self, infWinKey, infWinObj, *args):
        infWindow = cmds.window(title='Influence Window')
        for infJnt in infWinObj.full_influence_list:
            cmds.setAttr(infJnt + '.lockInfluenceWeights', 1)
        cmds.columnLayout()
        cmds.text(label="Influence Set: " + infWinKey + " skinCluster: " + infWinObj.skin_cluster)
        cmds.separator()
        cmds.setParent('..')
        svdInfWinRows = cmds.rowLayout(numberOfColumns=100)
        self.helper.heyWitch_tidyRows(svdInfWinRows)
        for infColObj in infWinObj.inf_columns:
            cmds.columnLayout()
            cmds.text(label=str(infColObj.inf_col_label))
            for selInfObj in infColObj.selectable_infs:
                newInfBtn = cmds.button(label=selInfObj.joint_name)
                selInfObj.joint_button = newInfBtn
                cmds.button(newInfBtn, edit=True, height=25, backgroundColor=[0.3, 0.3, 0.3],
                            command=partial(self.heyWitch_selInfluence, selInfObj, infWinObj))
                self.heyWitch_selInfluence(selInfObj, infWinObj)
            cmds.setParent('..')
        cmds.setParent('..')
        cmds.showWindow(infWindow)
        