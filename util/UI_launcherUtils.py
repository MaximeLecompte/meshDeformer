# ---------------------------------------------------------------------------- #
# ------------------------------------------------------------------ HEADER -- #
"""

:Authors:
    Maxime Lecompte, maxime.lecompte10@gmail.com

:Organization:
    
:Departments:
    Rigging TD

:Description:
        This module provides shared utility functions for launching custom Maya UI tools
        dockable windows (integrated in Maya UI panels)
        floating windows (independent popup dialogs)

:How to: (how to execute the core of this module)

:Dependencies:
    maya
    

"""

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- IMPORTS -- #
import sys

try:    # older DCC versions
    from PySide2 import QtWidgets, QtGui, QtUiTools
    from shiboken2 import wrapInstance
except: # newer DCC versions
    from PySide6 import QtWidgets, QtGui, QtUiTools
    from shiboken6 import wrapInstance

from maya import cmds
import maya.OpenMayaUI as omui

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- GLOBALS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------- FUNCTION UTIL -- #
def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def run_dockable(UI_class):
    
    window_name = UI_class.windowName()
    workspace_name = f"{window_name}WorkspaceControl"
    
    if cmds.workspaceControl(workspace_name, exists=True):
        cmds.deleteUI(workspace_name, control=True)
    
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.objectName() == window_name:
            widget.close()
            widget.deleteLater()

    ui = UI_class(parent=maya_main_window())
    ui.setObjectName(window_name)
    
    ptr = omui.MQtUtil.findControl(ui.objectName())
    if ptr is not None:
        cmds.workspaceControl(
            workspace_name,
            label=UI_class.WINDOW_TITLE,
            floating=True,
        )
    else:
        ui.show()
    return ui


def run_floating(UI_class):
    
    window_name = UI_class.windowName()
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.objectName() == window_name:
            widget.close()
            widget.deleteLater()

    ui = UI_class(parent=maya_main_window())
    ui.setObjectName(window_name)
    ui.show()
    return ui
    
# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------- FUNCTIONS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- WIDGETS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- CLASSES -- #

# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------------- MAIN-- #

