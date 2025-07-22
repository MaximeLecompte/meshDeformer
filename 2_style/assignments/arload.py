# STYLE ***************************************************************************
# content = 2_style assignment
#
# date    = 2025-07-01
# author  = Maxime Lecompte
#************************************************************************************

# ---------------------------------------------------------------------------- #
# ------------------------------------------------------------------ HEADER -- #
"""
:Authors:
    - Arnaud Reiser (arnaud.reiser@example.com)

:Organization:
    - Freelance (example)

:Departments:
    - Rigging TD

:Description:
    - This module is responsible for loading assets in the application.
      It provides a user interface to select and load files from a specified directory.
      The module also handles metadata display and file selection logic.

:How to: (how to execute the core of this module)
    - To execute the core functionality of this module, call the `execute_the_class_ar_load` function.
      This will initialize the loading interface and allow users to select files.

:Dependencies:
    - maya
    - Qt
    - arUtil
"""

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- IMPORTS -- #

import os
import re
import sys
import shutil
import getpass
import datetime
import subprocess

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import libLog
import libData
import libFunc
import arNotice

from arUtil import ArUtil
from tank import Tank

# ---------------------------------------------------------------------------- #
# ----------------------------------------------------------------- CLASSES -- #
TITLE = "load"
LOG = libLog.init(script=TITLE)

class ArLoad(ArUtil):
    """ArLoad is a class that provides functionality to load assets in the application.
       It includes methods for selecting files, displaying metadata, and managing the 
       user interface for loading assets.
    """
    
    def __init__(self):
        super(ArLoad, self).__init__()
        path_ui = "/".join([os.path.dirname(__file__), "ui", TITLE + ".ui"])
        self.wgLoad = QtCompat.loadUi(path_ui)

        self.load_dir = ''
        self.load_file = ''
        self.software_format = {y:x.upper() for x,y in self.data
                                ['software']
                                ['EXTENSION'].items()}
        self.software_keys = list(self.software_format.keys())

        self.wgLoad.lstScene.clear()
        self.wgLoad.lstStatus.clear()
        self.wgLoad.lstSet.clear()

        self.clear_meta()
        self.resize_widget(self.wgLoad)
        self.wgLoad.show()
        LOG.info('START : ArLoad')
    
    def press_btnAccept(self):
        """Handles the acceptance of the selected file 
           and updates the application state.
        """
        if not os.path.exists(self.load_file):
            self.set_status('FAILED LOADING : Path doesn\'t exists: {}'.format(
                self.load_file), msg_type=3)
            
            return False
    
    def press_menuItemAddFolder(self):
        """Adds a new folder to the list of scenes."""
        import arSaveAs
        self.save_as = arSaveAs.start(new_file=False)
    
    def press_menuSort(self, list_widget, reverse=False):
        """Sorts the items in the specified list widget.

           :list_widget: The list widget to sort.
           :reverse: If True, sorts in descending order.
        """
        file_list = []
        for index in xrange(list_widget.count()):
             file_list.append(list_widget.item(index).text())
        list_widget.clear()
        list_widget.addItems(sorted(file_list, reverse=reverse))
    
    def change_lstScene(self):
        """Changes the current scene based on the 
           selected item in the list.
        """
        self.load_dir = self.data['project']['PATH'][self.wgLoad.lstScene.currentItem().text()]
        tmp_content = libFunc.get_file_list(self.load_dir)
        self.scene_steps = len(self.data['rules']['SCENES']
                               [self.wgLoad.lstScene.currentItem().text()].split('/'))

        if self.scene_steps < 5:
            self.wgLoad.lstAsset.hide()

        else:
            self.wgLoad.lstAsset.itemSelectionChanged.connect(self.change_lstAsset)
            self.wgLoad.lstAsset.show()

        self.wgLoad.lstSet.clear()

        if tmp_content:
            self.wgLoad.lstSet.addItems(sorted(tmp_content))
            self.wgLoad.lstSet.setCurrentRow(0)
    
    def change_lstSet(self):
        """Changes the current set based on the 
           selected item in the list.
        """
        new_path = self.load_dir + '/' + self.wgLoad.lstSet.currentItem().text()
        tmp_content = libFunc.get_file_list(new_path)

        if self.scene_steps < 5:
            self.wgLoad.lstTask.clear()

            if tmp_content:
                self.wgLoad.lstTask.addItems(sorted(tmp_content))
                self.wgLoad.lstTask.setCurrentRow(0)

        else:
            self.wgLoad.lstAsset.clear()

            if tmp_content:
                self.wgLoad.lstAsset.addItems(sorted(tmp_content))
                self.wgLoad.lstAsset.setCurrentRow(0)
    
    def change_lstAsset(self):
        """Changes the current asset based on the 
           selected item in the list.
        """
        new_path = self.load_dir + '/' + self.wgLoad.lstSet.currentItem().text() \
                   + '/' + self.wgLoad.lstAsset.currentItem().text()
        tmp_content = libFunc.get_file_list(new_path)
        self.wgLoad.lstTask.clear()

        if tmp_content:
            self.wgLoad.lstTask.addItems(sorted(tmp_content))
            self.wgLoad.lstTask.setCurrentRow(0)
    
    def fill_meta(self):
        """Fills the metadata fields with information 
           about the currently selected file.
        """
        self.wgPreview.lblTitle.setText(self.file_name)
        self.wgPreview.lblDate.setText(str(datetime.datetime.fromtimestamp(
            os.path.getmtime(self.load_file))).split(".")[0])
        self.wgPreview.lblSize.setText(str("{0:.2f}".format(
            os.path.getsize(self.load_file)/(1024*1024.0)) + " MB"))
   
    def clear_meta(self):
        """Clears the metadata fields in the preview widget."""
        self.wgPreview.lblUser.setText('')
        self.wgPreview.lblTitle.setText('')
        self.wgPreview.lblDate.setText('')
        self.wgPreview.lblSize.setText('')


# ---------------------------------------------------------------------------- #
# --------------------------------------------------------------------- Run -- #
def execute_the_class_ar_load():
    global main_widget
    main_widget = ArLoad()
