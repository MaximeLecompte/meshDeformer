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

import maya.OpenMayaUI as omui
from maya import cmds

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

class LabeledDivider(QtWidgets.QWidget):
    """
        A widget that displays a horizontal line with a label in the center.
    """
    def __init__(self, text="Section", color="4A4949", font_size=10):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        line_left = QtWidgets.QFrame()
        line_left.setFrameShape(QtWidgets.QFrame.HLine)
        line_left.setFrameShadow(QtWidgets.QFrame.Plain)
        line_left.setLineWidth(1)

        self.label = QtWidgets.QLabel(text)
        self.label.setStyleSheet(f"color: {color}; font-size: {font_size}pt; text-decoration: underline;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        line_right = QtWidgets.QFrame()
        line_right.setFrameShape(QtWidgets.QFrame.HLine)
        line_right.setFrameShadow(QtWidgets.QFrame.Plain)
        line_right.setLineWidth(1)

        layout.addWidget(line_left)
        layout.addWidget(self.label)
        layout.addWidget(line_right)

    def setText(self, new_text):
        self.label.setText(new_text)

    def text(self):
        return self.label.text()

def horizontal_divider():
    """
        Creates a reusable QWidget that looks like:
        :return:
    """
    divider = QtWidgets.QFrame()
    divider.setFrameShape(QtWidgets.QFrame.HLine)
    divider.setFrameShadow(QtWidgets.QFrame.Plain)
    divider.setLineWidth(1)
    divider.setMidLineWidth(1)
    return divider

def addText(message, alignement=QtCore.Qt.AlignCenter, height=None, bold=False, color="color: white"):
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
    text.setFont(myFont)
    text.setStyleSheet(color)
    if height:
        text.setMinimumHeight(height)
    return text
    
def radioButton(checked=False):    
    """
        :param checked: Expect boolean value
        :return:
    """
    radio_button = QtWidgets.QRadioButton()
    radio_button.setChecked(checked)
    radio_button.setStyleSheet("QtWidgets.QRadioButton::indicator {width: 60px; height:60px; }")
    return radio_button

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- CLASSES -- #

class MeshDeformerWnd(QtWidgets.QDialog):

    WINDOW_TITLE = "Mesh Deformer"

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
        self.widgets_and_layouts()
        self.create_Header_Layout01_wdg()
        self.create_mid_layout_wdg()
        self.create_button()
        self.build_main_layout()
        self.create_connections()

    def base_layout(self):
        ## ---  Main frame Layout
        self.main_window = QtWidgets.QVBoxLayout(self)
        self.main_window.setContentsMargins(8, 3, 8, 8)
        self.main_window.setSpacing(3)

        
    def widgets_and_layouts(self):
        self.vLayoutAndFunctions = [
            #Name,                        Margins
            ["BodyCore",                 [0,0,0,0]],
            ["TopCore",                  [2,0,2,0]],
            ["Right_Layout",             [5,0,5,0]],
            ]

        self.vLayout = {}
        for layoutName, margins, in self.vLayoutAndFunctions:
            self.vLayout[layoutName] = QtWidgets.QVBoxLayout()
            self.vLayout[layoutName].setContentsMargins(*margins)

        self.hLayoutAndFunctions = [
            # name,                       Margins
            ['Header_Layout01',          [5,0,0,0]],
            ['Header_Layout02',          [5,0,0,0]],
            ['Mid_Layout',               [0,0,0,0]],
            ['Deformer_Layout',          [0,0,0,0]],
            ['SkinCluster_Layout',       [0,0,0,0]],
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
        ##---  Header text and button widget
        self.header_deformer_text = addText("Deformer Visibility :")
        self.header_deformer_text.setStyleSheet("""text-decoration: underline; 
                                                   color: 4A4949; 
                                                   font-size: 10pt"""
                                                   )
        self.header_deformer_text.setAlignment(QtCore.Qt.AlignLeft)    
        self.header_widgets = {}

        rows = [
                ("All :", True),
                ("SkinCluster :", False),
                ("BlendShape :", False),
                ("Wrap :", False),
                ("Delta Mush :", False),
                ]

        for name, is_checked in rows:
            self.label = addText(name)
            self.btn = radioButton(checked=is_checked)
            self.header_widgets[name] = (self.label, self.btn)

    def create_button(self):
        """
        Create buttons and assign functions to them.
        The buttons are grouped by their function and layout.
        """
        self.colorWhite = '#FFFFFF'
        self.colorBlack = '#190707'

        self.colorGrey = '#606060'
        self.colorLightGrey = '#F2F2F2'

        self.colorDarkGrey2 = '#373737'
        self.colorDarkGrey3 = '#2E2E2E'
        self.colorGrey2 = '#4A4949'

        self.buttonAndFunctions = [
            # name,                         function ,       group number,   labelColor,      backgroundColor,                layout,                 layout_coordinate     width   Height
            ['Check Out',                  self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['Deformer_Layout'],         '0,1,0,0',         125,   ''],
            ['Update',                     self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['Deformer_Layout'],         '0,1,0,0',         125,   ''],
            ['Check In',                   self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['Deformer_Layout'],         '0,1,0,0',         125,   ''],
            ['Add SkinCluster',            self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['SkinCluster_Layout'],      '0,1,0,0',         190,   ''],
            ['Transfer SkinCluster',       self.temp,             0,      self.colorWhite,    self.colorGrey,      self.hLayout['SkinCluster_Layout'],      '0,1,0,0',         190,   ''],
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
        self.buttons0 = [button for button, 
                         _, 
                         groupNumber, 
                         labColor, 
                         bgColor, 
                         layout, 
                         layout_coord, 
                         width, 
                         height, 
                         in self.buttonAndFunctions if groupNumber == 0] #<--- GroupNumber0 > main button

    def create_Header_Layout01_wdg(self):
        
        self.header_widget = QtWidgets.QWidget()
        self.header_widget.setLayout(self.vLayout["TopCore"]) 

        self.vLayout["TopCore"].addWidget(self.divider_widget["Divider_01"])
        self.vLayout["TopCore"].addLayout(self.hLayout["Header_Layout01"])
        self.hLayout["Header_Layout01"].addWidget(self.header_deformer_text)
        self.vLayout["TopCore"].addLayout(self.hLayout["Header_Layout02"])
        self.vLayout["TopCore"].addSpacing(5)
        self.vLayout["TopCore"].addWidget(self.divider_widget["Divider_02"])
        
        for self.label, self.btn in self.header_widgets.values():
            self.hLayout["Header_Layout02"].addWidget(self.label)
            self.hLayout["Header_Layout02"].addWidget(self.btn)
        
        self.hLayout["Header_Layout02"].setAlignment(QtCore.Qt.AlignLeft)
        self.vLayout["TopCore"].addSpacing(5)
        # self.vLayout["TopCore"].addWidget(self.divider_widget["Divider_02"])
        self.vLayout["TopCore"].addSpacing(5)

 
  
    def create_mid_layout_wdg(self):
        
        self.midCore_widget = QtWidgets.QWidget()
        self.midCore_widget.setLayout(self.hLayout["Mid_Layout"])

        # Left container   
        self.left_Qtree_wdg = QtWidgets.QTreeWidget()
        self.left_Qtree_wdg.setHeaderHidden(False)
        self.left_Qtree_wdg.setItemsExpandable(True)
        self.left_Qtree_wdg.setHeaderLabel("Geometries")
        self.left_Qtree_wdg.setMaximumWidth(400)

        # Right container
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setLayout(self.vLayout["Right_Layout"])
        self.vLayout["Right_Layout"].addSpacing(5)
        
        self.labeled_divider01_wdg = LabeledDivider("Deformer")
        self.vLayout["Right_Layout"].addWidget(self.labeled_divider01_wdg)
        # self.vLayout["Right_Layout"].addSpacing(5)
        self.vLayout["Right_Layout"].addLayout(self.hLayout["Deformer_Layout"])
        self.vLayout["Right_Layout"].addSpacing(15)
        
        
        self.labeled_divider02_wdg = LabeledDivider("SkinCluster")
        self.vLayout["Right_Layout"].addWidget(self.labeled_divider02_wdg)
        self.vLayout["Right_Layout"].addLayout(self.hLayout['SkinCluster_Layout'])

        
        self.vLayout["Right_Layout"].addStretch(1)


        # Add both to the mid layout
        self.hLayout["Mid_Layout"].addWidget(self.left_Qtree_wdg)
        self.hLayout["Mid_Layout"].addWidget(self.right_widget)


    def build_main_layout(self):
        
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
        """
        Override the close event to ensure all script jobs are killed
            **Cannot use super because Mayas dockable system wraps my dialog, which can break the super(). 
              The wrapped widget is no longer considered a true instance of my class. 
              return super(MeshDeformerWnd, self).closeEvent(*args, **kwargs)**
        """
        
        self.killAllCallBacks()
        QtWidgets.QDialog.closeEvent(self, event) 
        
    def showEvent(self, event):
        QtWidgets.QDialog.showEvent(self, event)
        
        
    ##-----------------------------
    ##---  Help Menu subMenu configuration 
    def about(self):
        """
        To update with final description
        """
        QtWidgets.QMessageBox.about(self, "About meshDeformer", "Version 1.0 \
                                            \nFunctionality: \
                                            \n      Tool to help manage deformer on a selected mesh")


# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------------- MAIN-- #

if __name__ == "__main__":
    run()


