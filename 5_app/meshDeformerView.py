# ---------------------------------------------------------------------------- #
# ------------------------------------------------------------------ HEADER -- #
"""

:Authors:
    Maxime Lecompte, maxime.lecompte10@gmail.com

:Organization:
    
:Departments:
    - Rigging TD

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
from MeshDeformer.util import UI_launcherUtils


# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- GLOBALS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------- FUNCTION UTIL -- #
# def maya_main_window():
#     """
#     Return the Maya main window widget as a Python object
#     """
#     main_window_ptr = omui.MQtUtil.mainWindow()
#     if sys.version_info.major >= 3:
#         return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
#     else:
#         return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    
# def run():
#     # Close previous instances
#     for widget in QtWidgets.QApplication.topLevelWidgets():
#         if widget.objectName() == MeshDeformerWnd.__name__:
#             widget.close()
#             widget.deleteLater()

#     ui = MeshDeformerWnd()
#     ui.show()
#     return ui
    
# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------- FUNCTIONS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- WIDGETS -- #

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- CLASSES -- #

class MeshDeformerWnd(QtWidgets.QDialog):

    WINDOW_TITLE = "Mesh Deformer"
    DOCKABLE= True

    @classmethod
    def windowName(cls):
        return cls.__name__
        
    @classmethod
    def killScriptJobs(cls, func=None, event=None):
        if callable(func):
            func = func.__name__

        jobs = set()
        ids = set()
        for job in cmds.scriptJob(listJobs=True):
            'bound method {}.'.format(cls.__name__)
            if cls.__name__ not in job:
                continue

            id, _, remaining = job.partition(':')
            if event:
                # Parses the job string to extract the event name
                if 'event=' not in remaining:
                    continue

                _event, _, remaining = job.partition('event=')[-1][1:].partition(' ') # Parse and clean the event name
                _event = _event.strip('"\',')
                if event != _event:
                    continue

            if func:
                if ' {}.{} '.format(cls.__name__, func) not in remaining:
                    continue

            jobs.add(job)
            ids.add(id)

        if ids:
            cmnds = ['cmds.scriptJob(kill={}, force=True)'.format(i) for i in ids]
            cmndsStr = '; '.join(cmnds)

            cmds.evalDeferred(cmndsStr)

        return jobs
        

    def __init__(self, parent=maya_main_window()):
        super(MeshDeformerWnd, self).__init__(parent)
        
        self.setObjectName(self.windowName())
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(800, 800)

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
    
    def killAllCallBacks(self):
        return self.killScriptJobs()
        
    #---------- Event Overrides ----------
    def closeEvent(self, event):
        #Cannot use super because Mayas dockable system wraps my dialog, which can break the super(). 
        #The wrapped widget is no longer considered a true instance of my class. 
        #return super(MeshDeformerWnd, self).closeEvent(*args, **kwargs)
        
        self.killAllCallBacks()
        QtWidgets.QDialog.closeEvent(self, event) 
        
    def showEvent(self, event):
        QtWidgets.QDialog.showEvent(self, event)
        


# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------------- MAIN-- #

if __name__ == "__main__":
    # run()
    UI_launcherUtils.run_floating(MeshDeformerWnd)

