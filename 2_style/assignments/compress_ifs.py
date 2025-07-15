# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2025-03-07
# email   = contact@alexanderrichtertd.com
#**********************************************************************************


# COMMENT --------------------------------------------------
# Not optimal

from maya import cmds

def set_color(ctrl_list, color_index):
    """
    Set the override color of the given controls to the specified color index.
    
    :param ctrl_list: List of control names to set the color for.
    :param color_index: Color index to apply to the controls.
    """
    color_map = {
                1: 4,
                2: 13,
                3: 25,
                4: 17,
                5: 17,
                6: 15,
                7: 6,
                8: 16
                }

    color = color_map.get(color_index)
    if color is None:
        cmds.warning(f"Color index {color_index} is not valid.")
        return

    for control in ctrl_list:
        shape_name = f"{control}Shape"
        if control and cmds.objExists(shape_name):
            cmds.setAttr(f"{shape_name}.overrideEnabled", 1)
            cmds.setAttr(f"{shape_name}.overrideColor", color)
        else:
            cmds.warning(f"Control '{shape_name}' does not exist.")


            
set_color(['circle', 'circle1'], 8)
         

# EXAMPLE
# set_color(['circle','circle1'], 8)
