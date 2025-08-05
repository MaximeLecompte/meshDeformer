# ---------------------------------------------------------------------------- #
# ------------------------------------------------------------------ HEADER -- #
"""
Authors:   Maxime Lecompte, maxime.lecompte10@gmail.com
   
Departments:    Rigging TD

Description:
    Provides an interface for many common actions related to
    importing/exporting/transferring deformers under one roof.

How to: (how to execute the core of this module)

Dependencies:  maya
"""

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- IMPORTS -- #

import pprint
from maya import cmds

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- GLOBALS -- #

# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------- FUNCTIONS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- CLASSES -- #

class DeformerUtils:
    # Constants as class attributes
    BLENDSHAPE = "blendShape"
    SKINCLUSTER = "skinCluster"
    CLUSTER = "cluster"
    WRAP = "wrap"
    PROXIMITYWRAP = "proximityWrap"
    DELTAMUSH = "deltaMush"
    LATTICE = "ffd"
    WIRE = "wire"

    VALID_DEFORMERS_TYPES = [
        BLENDSHAPE,
        SKINCLUSTER,
        CLUSTER,
        WRAP,
        PROXIMITYWRAP,
        DELTAMUSH,
        LATTICE,
        WIRE
    ]

    @classmethod
    def get_deformers_from_object(cls, obj):
        """ Get deformers from a given object by checking its history.
            Returns a dictionary with deformer types as keys and lists of deformer names as values."""
        result = {deformer: [] for deformer in cls.VALID_DEFORMERS_TYPES}
        
        if not obj or not cmds.objExists(obj):
            return result
        
        object_history = cmds.listHistory(obj, pruneDagObjects=True) or []
        
        for node in object_history:
            node_type = cmds.nodeType(node)
            
            if node_type in cls.VALID_DEFORMERS_TYPES:
                if node_type == cls.SKINCLUSTER:
                    joints = cmds.skinCluster(node, query=True, influence=True) or []
                    result[node_type].append({"name": node, "joints": joints})
                    
                elif node_type == cls.BLENDSHAPE:
                    aliases = cmds.aliasAttr(node, query=True) or []
                    # aliases is a flat list: [alias1, attr1, alias2, attr2, ...]
                    # We want only the alias names for weight attributes
                    targets = []

                    for i in range(0, len(aliases), 2):
                        if aliases[i] and aliases[i] != '':
                            targets.append(aliases[i])
                    result[node_type].append({"name": node, "targets": targets})
                                    
                else:
                    result[node_type].append(node)
                
        return result

    @classmethod
    def get_deformers_from_selection(cls, selection=None):
        """ Get deformers from the current selection or a provided selection.
            Returns a dictionary with object names as keys and lists of deformer names as values."""
        if selection is None:
            selection = cmds.ls(selection=True, long=True)
        results = {}
        
        if not selection:
            return results
        
        valid_types = {"mesh", "nurbsSurface"}
        filtered_selection = []

        for obj in selection:
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []

            for shape in shapes:
                if cmds.nodeType(shape) in valid_types:
                    filtered_selection.append(obj)
                    break

        for obj in filtered_selection:
            deformers = cls.get_deformers_from_object(obj)
            results[obj] = deformers

        pprint.pprint(results)

        return results



