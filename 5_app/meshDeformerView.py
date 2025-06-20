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
def run():
    """ Creates the UI.

    :return: The UI instance.
    :rtype: MeshDeformerWnd.
    """

    mdw = UI_launcherUtils.run_floating(MeshDeformerWnd)
    return mdw
    
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
        

    def __init__(self, parent=None):
        super(MeshDeformerWnd, self).__init__(parent)
        
        self.setObjectName(self.windowName())
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(800, 800)

        self.setup_layout()
        self.create_widgets()
        self.buildMainLayout()
        self.create_connections()

    def setup_layout(self):
        
        self.main_frame = QtWidgets.QVBoxLayout(self)
        self.main_frame.setContentsMargins(5, 5, 5, 5)
        
        # Create a QWidget to hold the horizontal layout
        self.main_layout = QtWidgets.QWidget()

        # Create a horizontal layout for side-by-side panels
        self.content_layout = QtWidgets.QHBoxLayout(self.main_layout)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        # --------------------------
        # Right SIDE:
        self.rightSide_widget = QtWidgets.QWidget()
        self.rightSide_layout = QtWidgets.QVBoxLayout(self.rightSide_widget)
        self.rightSide_layout.setContentsMargins(0, 0, 0, 0)

        self.button_1 = QtWidgets.QPushButton("Option 1")
        self.rightSide_layout.addWidget(self.button_1)
        
        # --------------------------
        # RIGHT SIDE:
        self.leftSide_widget = QtWidgets.QWidget()
        self.leftSide_layout = QtWidgets.QVBoxLayout(self.leftSide_widget)
        self.leftSide_layout.setContentsMargins(0, 0, 0, 0)
        
        self.button_2 = QtWidgets.QPushButton("Option 2")
        self.leftSide_layout.addWidget(self.button_2)

    def buildMainLayout(self):
        
        self.main_frame.addWidget(self.main_layout)
        
        self.content_layout.addWidget(self.rightSide_widget)
        self.content_layout.addWidget(self.leftSide_widget)

    def create_widgets(self):
        pass

        
    def create_connections(self):
        pass


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
    run()


