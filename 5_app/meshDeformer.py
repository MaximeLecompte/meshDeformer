# ---------------------------------------------------------------------------- #
# ------------------------------------------------------------------ HEADER -- #
"""

:Authors:
    Maxime Lecompte, maxime.lecompte10@gmail.com

:Organization:
    
:Departments:
    - Rigging

:Description:
    Provides an interface for many common actions related to
    deformer weight, BlendShape, Wrap, DeltaMush and SkinCluster.
    Select at least one mesh to display the deformers in the UI.

:How to: (how to execute the core of this module)

:Dependencies:
    - maya
    

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


def run():
    # Close previous instances
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.objectName() == MeshDeformerWnd.__name__:
            widget.close()
            widget.deleteLater()

    ui = MeshDeformerWnd()
    ui.show()
    return ui
    
# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------- FUNCTIONS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- WIDGETS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- CLASSES -- #

class MeshDeformerWnd(QtWidgets.QDialog):

    WINDOW_TITLE = "Mesh Deformer"

    @classmethod
    def windowName(cls):
        return cls.__name__

    def __init__(self, parent=maya_main_window()):
        super(MeshDeformerWnd, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setObjectName(self.__class__.__name__)
        self.setMinimumSize(300, 150)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        pass
        # self.apply_button = QtWidgets.QPushButton("Apply")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addStretch()
        # main_layout.addWidget(self.apply_button)

    def create_connections(self):
        pass
        # self.apply_button.clicked.connect(self.on_clicked)

    # def on_clicked(self):
    #     print("Button Clicked")


# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------------- MAIN-- #

if __name__ == "__main__":
    run()
