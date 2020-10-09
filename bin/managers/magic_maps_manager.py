import random
from functools import partial

import pymel.core as pm
from maya import cmds

from bin.classes.classes import Map


class MagicMapsManager:
    global_work_space = {}
    helper = None

    def __init__(self, global_work_space, helper):
        self.global_work_space = global_work_space
        self.helper = helper

    def mapStash(self, mapsTreeView, mapNameTxtFld, stashedMapsScroll, stashedMapsLayout, sourceVar, *args):
        self.mapHighlight(mapsTreeView, stashedMapsScroll, stashedMapsLayout)
        mapName = cmds.textField(mapNameTxtFld, query=True, text=True)
        if mapName == "":
            mapName = 'stsh_' + str(random.randint(100, 999))
        selItem = cmds.treeView(mapsTreeView, query=True, si=True)
        self.global_work_space['miscData']['mapOps']['stashed_maps'][str(selItem[0])][mapName] = self.global_work_space['miscData']['mapOps'][sourceVar].copy()
        self.mapHighlight(mapsTreeView, stashedMapsScroll, stashedMapsLayout)
        mapContainer = self.global_work_space['miscData']['mapOps']['stashed_maps'][str(selItem[0])][mapName]
        # self.mapTest(mapContainer)

    def openSlot(self, oneTwo, opnSlotCharge, clsdSlotCharge, *args):
        self.global_work_space['miscData']['mapOps']['open_slot']['slot_no'] = oneTwo
        self.global_work_space['miscData']['mapOps']['open_slot']['open_slot'] = opnSlotCharge
        self.global_work_space['miscData']['mapOps']['open_slot']['closed_slot'] = clsdSlotCharge
        cmds.text(opnSlotCharge, edit=True, label='open')
        clsdSlotCheck = cmds.text(clsdSlotCharge, query=True, label=True)
        if clsdSlotCheck == 'open':
            cmds.text(clsdSlotCharge, edit=True, label='closed')

    def loadToSlot(self, mapKey, mapVal, *args):
        openSlot = self.global_work_space['miscData']['mapOps']['open_slot']['slot_no']
        self.global_work_space['miscData']['mapOps'][openSlot] = mapVal.copy()
        openCharge = self.global_work_space['miscData']['mapOps']['open_slot']['open_slot']
        cmds.text(openCharge, edit=True, label=mapKey)
        self.global_work_space['miscData']['mapOps']['aftermath_label'][openSlot] = mapKey

    def mapMaths(self, mapMathsCol, aftermathCharge, *args):
        mapMathsList = cmds.columnLayout(mapMathsCol, query=True, ca=True)
        for chkBox in mapMathsList:
            chkBoxVal = cmds.checkBox(chkBox, query=True, value=True)
            if chkBoxVal == 1:
                chkBoxOp = cmds.checkBox(chkBox, query=True, label=True)
                break
        slotOne = self.global_work_space['miscData']['mapOps']['aftermath_label']['slot_one']
        slotTwo = self.global_work_space['miscData']['mapOps']['aftermath_label']['slot_two']
        cmds.text(aftermathCharge, edit=True, label=slotOne + ' ' + chkBoxOp + ' ' + slotTwo)
        self.global_work_space['miscData']['mapOps']['math_map'] = {}
        if chkBoxOp == 'invert':
            for k, v in self.global_work_space['miscData']['mapOps']['slot_one'].items():
                mthVal = 1 - v
                self.global_work_space['miscData']['mapOps']['math_map'][k] = mthVal
        elif chkBoxOp == '+':
            for k, v in self.global_work_space['miscData']['mapOps']['slot_one'].items():
                plusVal = float(self.global_work_space['miscData']['mapOps']['slot_two'][k])
                mthVal = v + plusVal
                if mthVal > 1:
                    mthVal = 1
                self.global_work_space['miscData']['mapOps']['math_map'][k] = mthVal
        elif chkBoxOp == '-':
            for k, v in self.global_work_space['miscData']['mapOps']['slot_one'].items():
                minVal = float(self.global_work_space['miscData']['mapOps']['slot_two'][k])
                mthVal = v - minVal
                if mthVal < 0:
                    mthVal = 0
                self.global_work_space['miscData']['mapOps']['math_map'][k] = mthVal

    def overwriteSelected(self, mapsTreeView, sourceVar, *args):
        selItem = cmds.treeView(mapsTreeView, query=True, si=True)
        greenlight = False
        for k0, v0 in self.global_work_space['miscData']['mapOps']['crt_scene_maps'].items():
            if k0 == selItem[0]:
                greenlight = True
                selItemObj = v0
        if greenlight == False:
            print('match not found for ' + selItem[0])
        else:
            baseMesh = cmds.listConnections(selItemObj.parent_node + '.outputGeometry[0]')
            baseMesh = self.find_basemesh_nodetype(baseMesh)
            vertsNo = int(cmds.polyEvaluate(baseMesh, v=True))
            if selItemObj.map_type == 'blend':
                cmds.setToolTo('artAttrBlendShapeContext')
                pm.mel.artBlendShapeSelectTarget('artAttrCtx', selItemObj.inf_or_tgt)
                for vtxNo in range(vertsNo):
                    vtxKey = '.vtx[' + str(vtxNo) + ']'
                    newVtxVal = float(self.global_work_space['miscData']['mapOps'][sourceVar][vtxKey])
                    cmds.select(baseMesh[0] + vtxKey)
                    cmds.artAttrCtx('artAttrBlendShapeContext', edit=True, val=newVtxVal, opacity=1.0, sao="absolute")
                    cmds.artAttrCtx('artAttrBlendShapeContext', edit=True, clr=True)
            elif selItemObj.map_type == 'skn_clstr':
                for vtxNo in range(vertsNo):
                    vtxKey = '.vtx[' + str(vtxNo) + ']'
                    newVtxVal = float(self.global_work_space['miscData']['mapOps'][sourceVar][vtxKey])
                    cmds.skinPercent(selItemObj.parent_node, baseMesh[0] + vtxKey,
                                     transformValue=(selItemObj.inf_or_tgt, newVtxVal))

    def mapHighlight(self, mapsTreeView, stashedMapsScroll, stashedMapsLayout, *args):
        self.global_work_space['miscData']['mapOps']['temp_map'] = {}
        stashedMapsGrid = self.global_work_space['miscData']['mapOps']['crt_sel_layout']
        cmds.deleteUI(stashedMapsGrid, layout=True)
        stashedMapsGrid = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(120, 25), parent=stashedMapsScroll)
        self.global_work_space['miscData']['mapOps']['crt_sel_layout'] = stashedMapsGrid
        selItem = cmds.treeView(mapsTreeView, query=True, si=True)
        greenlight = False
        for k0, v0 in self.global_work_space['miscData']['mapOps']['crt_scene_maps'].items():
            if k0 == selItem[0]:
                greenlight = True
                selItemObj = v0
        if greenlight == False:
            print('match not found for ' + selItem[0])
        else:
            cmds.frameLayout(stashedMapsLayout, edit=True, label='Maps Library for ' + selItemObj.inf_or_tgt)
            for k1, v1 in self.global_work_space['miscData']['mapOps']['stashed_maps'].items():
                if k1 == selItemObj.crt_map_id:
                    for k2, v2 in v1.items():
                        cmds.button(label=k2, parent=stashedMapsGrid, backgroundColor=[0.3, 0.3, 0.3],
                                    command=partial(self.loadToSlot, k2, v2))
            baseMesh = cmds.listConnections(selItemObj.parent_node + '.outputGeometry[0]')
            baseMesh = self.find_basemesh_nodetype(baseMesh)
            vertsNo = int(cmds.polyEvaluate(baseMesh, v=True))
            if selItemObj.map_type == 'blend':
                for vtxNo in range(vertsNo):
                    vtxKey = '.vtx[' + str(vtxNo) + ']'
                    vtxVal = cmds.getAttr(
                        selItemObj.parent_node + '.it[0].itg[' + selItemObj.index + '].tw[' + str(vtxNo) + ']')
                    self.global_work_space['miscData']['mapOps']['temp_map'][vtxKey] = vtxVal
            else:
                for vtxNo in range(vertsNo):
                    vtxKey = '.vtx[' + str(vtxNo) + ']'
                    vtxVal = cmds.skinPercent(selItemObj.parent_node, baseMesh[0] + vtxKey,
                                              transform=selItemObj.inf_or_tgt, query=True)
                    self.global_work_space['miscData']['mapOps']['temp_map'][vtxKey] = vtxVal
        mapContainer = self.global_work_space['miscData']['mapOps']['temp_map']
        # self.mapTest(mapContainer)

    def find_basemesh_nodetype(self, baseMesh):
        for og_node in baseMesh:
            og_node_type = cmds.nodeType(og_node)
            if og_node_type == 'polyColorPerVertex':
                baseMesh = cmds.listConnections(og_node + '.output')
            elif og_node_type == 'mesh':
                baseMesh = og_node
        return baseMesh