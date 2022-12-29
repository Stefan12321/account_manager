import os
import autoreg.autoreg_main
from PyQt5 import QtWidgets, QtGui, QtCore
from dialogs.settings_dialog import Ui_Dialog as Ui_settings_dialog
from dialogs.settings_main import Ui_Dialog as Ui_main_settings_dialog

DEBUG = (os.getenv("DEBUG_ACCOUNT_MANAGER", default='False') == 'True')
print(f"DEBUG in settings: {DEBUG}")

settings_file = os.environ["ACCOUNT_MANAGER_PATH_TO_SETTINGS"]


class QlistExtensionsWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None):
        super(QlistExtensionsWidgetItem, self).__init__(parent)
        self.extension_name = None


class SettingsDialog(Ui_settings_dialog, QtWidgets.QDialog):
    def __init__(self, parent=None, user_agent="", account_name=""):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        if DEBUG:
            self.CheckGSButton = QtWidgets.QPushButton(self)
            self.CheckGSButton.setStyleSheet("")
            self.CheckGSButton.setObjectName("CheckGSButton")
            self.verticalLayout.addWidget(self.CheckGSButton)
            self.CheckGSButton.setText("CheckGS")
            self.CheckGSButton.clicked.connect(autoreg.autoreg_main.test_google_sheet)
        self.items = []
        self.name = account_name
        self.user_agent_line.setText(user_agent)
        extension_list = os.listdir(fr'{os.environ["ACCOUNT_MANAGER_BASE_DIR"]}\extension')
        for extension_name in extension_list:
            text = extension_name
            item = QlistExtensionsWidgetItem()
            item.setText(text)
            item.extension_name = extension_name
            item.setCheckState(QtCore.Qt.Unchecked)
            self.items.append(item)
            self.listWidgetExtensions.addItem(item)


class MainSettings(Ui_main_settings_dialog, QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.pages_list = []
        self.pages_dict = {}
        self.add_functions()
        self.lineEditAddPage.setText("index")

    def add_one_page_onload(self, page_url):
        try:
            # print(page_url)
            horizontalLayout_2 = QtWidgets.QHBoxLayout()
            horizontalLayout_2.setObjectName("horizontalLayout_2")
            lineEditAddPage = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(lineEditAddPage.sizePolicy().hasHeightForWidth())
            lineEditAddPage.setSizePolicy(sizePolicy)
            lineEditAddPage.setObjectName("lineEditAddPage")
            horizontalLayout_2.addWidget(lineEditAddPage)
            pushButton_remove_page = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            pushButton_remove_page.setEnabled(True)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(pushButton_remove_page.sizePolicy().hasHeightForWidth())
            pushButton_remove_page.setSizePolicy(sizePolicy)
            pushButton_remove_page.setMaximumSize(QtCore.QSize(30, 30))
            pushButton_remove_page.setObjectName("pushButton_remove_page")
            pushButton_remove_page.setText("-")
            pushButton_remove_page.clicked.connect(lambda: self.deleteItemsOfLayout(horizontalLayout_2))
            horizontalLayout_2.addWidget(pushButton_remove_page)
            self.verticalLayout_2.addLayout(horizontalLayout_2)
            if page_url:
                lineEditAddPage.setText(page_url)

            self.pages_list.append(lineEditAddPage)
            self.pages_dict.update({horizontalLayout_2: lineEditAddPage})


        except Exception as e:
            print(e)

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)

                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
            try:
                self.pages_dict.pop(layout)
                # print(self.pages_dict)
            except Exception as e:
                print(e)

    def add_functions(self):
        self.pushButton_add_page.clicked.connect(self.add_one_page_onload)
