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
    from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
    from shiboken2 import wrapInstance
except: # newer DCC versions
    from PySide6 import QtWidgets, QtGui, QtUiTools, QtCore
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

def horizontal_divider():
    """
    Create a horizontal divider line.
    :return:
    """
    divider = QtWidgets.QFrame()
    divider.setFrameShape(QtWidgets.QFrame.HLine)
    divider.setFrameShadow(QtWidgets.QFrame.Plain)
    divider.setLineWidth(1)
    divider.setMidLineWidth(1)
    return divider

def addText(message, alignement=QtCore.Qt.AlignCenter, height=15, bold=False, color="color: white"):
    """
    Create global text management.
    :param message: Text displayed
    :param alignement: Alignment, left, right ,center ...
    :param height: height of text
    :param bold: expect boolean value
    :param color: default text color
    :return:
    """
    myFont = QtGui.QFont()
    myFont.setBold(bold)
    text = QtWidgets.QLabel(message)
    text.setAlignment(alignement)
    text.setFixedHeight(height)
    text.setFont(myFont)
    text.setStyleSheet(color)
    return text

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

        self.base_layout()
        self.create_menu_action()
        self.widgetsAndLayouts()
        self.create_header_layout_wdg()
        self.create_mid_layout_wdg()
        self.create_button()
        self.buildMainLayout()
        self.create_connections()

    def base_layout(self):
        
        ## -----------------------------
        ## ---  Main frame Layout
        self.main_window = QtWidgets.QVBoxLayout(self)
        self.main_window.setContentsMargins(3, 8, 3, 8)
        self.main_window.setSpacing(3)

        
    def widgetsAndLayouts(self):
        self.vLayoutAndFunctions = [
            #Name,                   Margins
            ["BodyCore",           [5,0,5,0]],
            ["TopCore",            [5,0,5,0]],
            ["MidCore",            [5,0,5,0]],
            ]

        self.vLayout = {}
        for layoutName, margins, in self.vLayoutAndFunctions:
            self.vLayout[layoutName] = QtWidgets.QVBoxLayout()
            self.vLayout[layoutName].setContentsMargins(*margins)

        self.hLayoutAndFunctions = [
            # name,
            ['Header_Layout',      [0,0,0,0]],
            ['Mid_Layout',         [0,0,0,0]],
            ['Left_Layout',        [0,0,0,0]],
            ['Right_Layout',       [0,0,0,0]],
            ]
        self.hLayout = {}
        for layoutName, margins in self.hLayoutAndFunctions:
            self.hLayout[layoutName] = QtWidgets.QHBoxLayout()
            self.hLayout[layoutName].setContentsMargins(*margins)
            
        ##-----------------------------
        ##---  Create divider widget
        self.divider_widget = {"Divider_0{}".format(i):horizontal_divider() for i in range(1,9)}
        
        ##-----------------------------
        ##---  Create Menu bar and action
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar_Help = self.menu_bar.addMenu("Help")
        self.menu_bar_Help.addAction(self.about_action)
        
        ##-----------------------------
        ##---  Create Left tree widget
        # self.left_Qtree_wdg = QTreeWidget()
        # self.left_Qtree_wdg.setHeaderHidden(True)
        
        
        


    def create_button(self):
        """
        Dictionnary of all button
        :return:
        """
        self.colorWhite = '#FFFFFF'
        self.colorBlack = '#190707'

        self.colorGrey = '#606060'
        self.colorLightGrey = '#F2F2F2'

        self.colorDarkGrey2 = '#373737'
        self.colorDarkGrey3 = '#2E2E2E'
        self.colorGrey2 = '#4A4949'

        self.buttonAndFunctions = [
            # name,                   function ,        group number,   labelColor,      backgroundColor,                layout,                 layout_coordinate     width   Height
            ['Option 1',              self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['Header_Layout'],         '0,1,0,0',         125,   ''],
            ['Option 2',              self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['Header_Layout'],           '0,1,0,0',         125,   ''],
            ['Option 3',              self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['Right_Layout'],          '0,1,0,0',         125,   ''],
            ]

        # Build Buttons
        self.buttons = {}
        for buttonName, buttonFunction, _, labColor, bgColor, layout, layout_coord, width, height in self.buttonAndFunctions:
            
            self.buttons[buttonName] = QtWidgets.QPushButton(buttonName)
            self.buttons[buttonName].clicked.connect(buttonFunction)

            if width != '':
                self.buttons[buttonName].setFixedWidth(width)

            if height != '':
                self.buttons[buttonName].setFixedHeight(height)

            self.buttons[buttonName].setStyleSheet(
                'padding:3px; text-align:center; font: normal; color:{};  background-color:{};'.format(labColor, bgColor))
             
            layout.addWidget(self.buttons[buttonName]) 

        ## Build and customize Buttons
        self.buttons0 = [button for button, _, groupNumber, labColor, bgColor, layout, layout_coord, width, height, in self.buttonAndFunctions if groupNumber == 0] #<--- GroupNumber0 > main button

    def create_header_layout_wdg(self):
        
        self.header_widget = QtWidgets.QWidget()
        self.header_widget.setLayout(self.vLayout["TopCore"]) 
        self.header_widget.setStyleSheet("background-color: #373737;")
        self.header_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.vLayout["TopCore"].addWidget(self.divider_widget["Divider_01"])
        self.vLayout["TopCore"].addLayout(self.hLayout["Header_Layout"])
        self.vLayout["TopCore"].addSpacing(11)
  
    def create_mid_layout_wdg(self):
        
        self.midCore_widget = QtWidgets.QWidget()
        self.midCore_widget.setLayout(self.hLayout["Mid_Layout"])
        
        # Left container
        # self.left_widget = QtWidgets.QWidget()
        # self.left_widget.setLayout(self.hLayout["Left_Layout"])
        # self.left_widget.setStyleSheet("background-color: #606060;")

        self.left_Qtree_wdg = QtWidgets.QTreeWidget()
        self.left_Qtree_wdg.setHeaderHidden(False)
        self.left_Qtree_wdg.setItemsExpandable(True)
        self.left_Qtree_wdg.setHeaderLabel("Geometries")
        self.left_Qtree_wdg.setMaximumWidth(400)

        # Right container
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setLayout(self.hLayout["Right_Layout"])
        self.right_widget.setStyleSheet("background-color: #4A4949;")


        # Add both to the mid layout
        self.hLayout["Mid_Layout"].addWidget(self.left_Qtree_wdg)
        self.hLayout["Mid_Layout"].addWidget(self.right_widget)


    def buildMainLayout(self):
        
        self.main_window.addLayout(self.vLayout["BodyCore"])
        self.main_window.setMenuBar(self.menu_bar)
        
        self.vLayout["BodyCore"].addWidget(self.header_widget)
        self.vLayout["BodyCore"].addWidget(self.midCore_widget)

    def create_menu_action(self):

        self.about_action = QtWidgets.QAction("About", self)
        self.about_action.setIcon(QtGui.QIcon(":help.png"))
        
    def create_connections(self):
        self.about_action.triggered.connect(self.about)


    # def on_clicked(self):
    #     print("Button Clicked")
    
    def temp(self):
        pass
        
    
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
        
        
    ##-----------------------------
    ##---  Help Menu subMenu configuration
    def about(self):
        QtWidgets.QMessageBox.about(self, "About meshDeformer", "Version 1.0 \
                                            \nFunctionality: \
                                            \n      Tool to help manage deformer on a selected mesh")


# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------------- MAIN-- #

if __name__ == "__main__":
    run()


