import cPickle

from maya import cmds


class Helper:

    def heyWitch_stashDictionary(self, global_work_space, *args):
        scenePath = cmds.file(query=True, location=True)
        if '.mb' in scenePath:
            pickleDictPath = scenePath.replace('.mb', '.pkl')
        else:
            pickleDictPath = scenePath.replace('.ma', '.pkl')
        cPickle.dump(global_work_space, open(pickleDictPath, "wb"))
        global_work_space['miscData']['picklePath'] = pickleDictPath

    def heyWitch_blankSlate(self, meshToBlank):
        cmds.delete(meshToBlank, ch=True)
        cmds.makeIdentity(meshToBlank, apply=True, t=1, r=1, s=1, n=0)

    def heyWitch_tidyRows(self, rowVar):
        columnsNo = cmds.rowLayout(rowVar, query=True, numberOfColumns=True)
        for x in range(columnsNo):
            cmds.rowLayout(rowVar, edit=True, rowAttach=(x + 1, 'top', 0))

    def heyWitch_selectListOf(self, container, addVar, *args):
        if addVar == 'single':
            cmds.select(clear=True)
        if type(container) == dict:
            for ctKey in container.keys():
                cmds.select(ctKey, add=True)
        elif type(container) == list:
            for ctItem in container:
                cmds.select(ctItem, add=True)
        else:
            print('Not a dict or list')

    def heyWitch_selectRawMesh(self, meshName, *args):
        cmds.select(str(meshName))

    def heyWitch_grabMesh(self, toGrabKey, toGrabValue, global_work_space, *args):
        for k0, v0 in global_work_space.items():
            for k1, v1 in v0.items():
                if hasattr(v1, 'mesh_spawn_name') and v1.mesh_spawn_name == toGrabValue.mesh_spawn_name:
                    if k1 == toGrabKey:
                        cmds.setAttr(k1 + '.visibility', 1)
                        cmds.select(k1)
                    else:
                        cmds.setAttr(k1 + '.visibility', 0)

    def execute_string_command(self, string_to_execute, *args):
        print('attempting to execute')
        print(string_to_execute)
        exec(string_to_execute)