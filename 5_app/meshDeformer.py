import sys
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class SampleUI(QtWidgets.QDialog):

    WINDOW_TITLE = "Sample UI"


    def __init__(self, parent=maya_main_window()):
        super(SampleUI, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(200, 100)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.apply_button = QtWidgets.QPushButton("Apply")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addStretch()
        main_layout.addWidget(self.apply_button)

    def create_connections(self):
        self.apply_button.clicked.connect(self.on_clicked)

    def on_clicked(self):
        print("Button Clicked")


if __name__ == "__main__":

    try:
        sample_ui.close() # pylint: disable=E0601
        sample_ui.deleteLater()
    except:
        pass

    sample_ui = SampleUI()
    sample_ui.show()
