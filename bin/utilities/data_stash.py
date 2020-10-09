import cPickle

from maya import cmds


def get_pickle_dict_path():
    scene_path = cmds.file(query=True, location=True)
    extension = '.mb' if '.mb' in scene_path else '.ma'
    return scene_path.replace(extension, '.pkl')


def get_global_work_space(pickle_dict_path):
    if cmds.file(pickle_dict_path, query=True, ex=True):
        global_work_space = cPickle.load(open(pickle_dict_path, 'rb'))
    else:
        global_work_space = {"spawnStorage": {}, "burnGroupStorage": {}, "targetStorage": {},
                             "utilityBurnShopStorage": {}, "utilityBuildShopStorage": {}, "chopMeshStorage": {},
                             "bindJointClustersStorage": {}, "outMeshStorage": {},
                             'miscData': {"infJntSelect": {"jntSlot0": {}, "jntSlot1": {}, "jntSlot2": {}},
                                          'mapOps': {
                                 'crt_scene_maps': {},
                                 'open_slot': {
                                     'slot_no': ''
                                 },
                                 'aftermath_label': {
                                     'slot_one': '',
                                     'slot_two': ''
                                 }
                             }, 'switch_layouts':{
                                     'bjc_switch':'',
                                     'msw_switch':''
                                 }}}

        global_work_space['miscData']['picklePath'] = pickle_dict_path
        global_work_space['miscData']['infWindowStorage'] = {}
        global_work_space['miscData']['homelessInfWins'] = {}
        global_work_space['miscData']['homelessChopClrSets'] = {}
        global_work_space['miscData']['mapOps']['crt_scene_maps'] = {}
        global_work_space['miscData']['mapOps']['stashed_maps'] = {}
        global_work_space['miscData']['mapOps']['crt_sel_layout'] = {}
        global_work_space['miscData']['mapOps']['slot_one'] = {}
        global_work_space['miscData']['mapOps']['slot_two'] = {}
        global_work_space['miscData']['mapOps']['math_map'] = {}

    return global_work_space
