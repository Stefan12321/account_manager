from multiprocessing import freeze_support

freeze_support()

import os
import time
import threading
import selenium
import json
import undetected_chromedriver as uc
import shutil
import zipfile

from selenium import webdriver
from GUI import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from user_agents.main import get_user_agent
from html_editor.main import create_html
from list_widget import Ui_Form as Ui_Custom_widget
from create_account_dialog import Ui_Dialog as Ui_create_account_dialog
from dialogs.settings_dialog import Ui_Dialog as Ui_settings_dialog
from dialogs.about_dialog import Ui_Dialog as Ui_about_dialog
from dialogs.progress_bar import Ui_Dialog as Ui_progress_bar
from password_decryptor.passwords_decryptor import do_decrypt
from zipfile import ZipFile


def serialize(path, data: dict):
    """

    :param path: path to config.json
    :param data: dict of settings
    :return: None
    """
    with open(f'{path}/config.json', 'w') as f:
        try:
            json.dump(data, f)
            print(f"Serialized data: {data}")
        except Exception as e:
            print(e)


def deserialize(path) -> dict:
    """

    :param path: path to config.json
    :return: list of deserialized data from config.json
    """
    with open(fr'{path}\config.json', 'r') as f:
        data = json.load(f)

    return data


class WebBrowser:
    def __init__(self, path, account_name):
        print(f"PATH {path}")
        self.start_undetected_chrome(path, account_name)

    def start_undetected_chrome(self, path, account_name):
        if os.path.isdir(path):
            try:
                data = deserialize(path)
                user_agent_ = data["user-agent"]
            except FileNotFoundError:
                user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
                data = {
                    'user-agent': user_agent_
                }
                serialize(path, data)
                user_agent_ = self.write_to_file(path)
            except KeyError as e:
                if str(e).replace("'", "") == "user-agent":
                    user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
                    data.update({"user-agent": user_agent_})
        else:
            user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
            data = {
                'user-agent': user_agent_
            }

            os.makedirs(path)
            serialize(path, data)

        index = f"{path}/init.html"
        base_dir = os.path.dirname(os.path.realpath(__file__))
        options = uc.ChromeOptions()
        try:
            extensions = ','.join(
                fr'{base_dir}\extension\{key}' for key in data["extensions"].keys() if data["extensions"][key] is True)
            options.add_argument(fr'--load-extension={extensions}')
        except KeyError:
            pass
        options.add_argument(f'--user-data-dir={path}')
        options.add_argument(f"--user-agent={user_agent_}")
        options.add_argument(f"-enable-features=PasswordImport")
        # options.add_argument(f'--password-store=gnome')
        try:
            driver = uc.Chrome(options=options)
        except Exception as e:
            print(e)
        if os.path.exists(index):
            driver.get(index)
        else:
            create_html(index, account_name)
            driver.get(index)
        # driver.switch_to.new_window('tab')
        # driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        driver.switch_to.new_window('tab')
        driver.get("https://whoer.net/")
        # driver.get("https://proxyleak.com/")
        # driver.switch_to.new_window('tab')
        # driver.get("chrome://settings/passwords")
        # driver.implicitly_wait(2)
        # shadow_host = driver.find_element(By.CSS_SELECTOR, '#shadow-root')
        # shadow_root = shadow_host.shadow_root
        # shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '#shadow-root')
        # shadow_content.find_element(By.ID, "menuImportPassword").click()
        try:
            while len(driver.window_handles) > 0:
                time.sleep(1)
        except selenium.common.exceptions.WebDriverException:
            driver.quit()
            print('driver quit')

    def start_standart_chrome(self, path, account_name):
        if os.path.isdir(path):
            try:
                user_agent_ = self.read_from_file(path)
            except FileNotFoundError:
                user_agent_ = self.write_to_file(path)
        else:
            try:
                user_agent_ = self.write_to_file(path)
            except FileNotFoundError:
                os.makedirs(path)
                user_agent_ = self.write_to_file(path)

        index = f"{path}/init.html"
        chromedriver = './chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-data-dir={path}')
        options.add_extension(f'./extension/FoxyProxy-Standard.crx')
        # options.add_extension(f'./extension/chrome_extension_fcc-master.crx')
        options.add_argument(f"user-agent={user_agent_}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        driver = webdriver.Chrome(chromedriver, options=options)
        if os.path.exists(index):
            driver.get(index)
        else:
            create_html(index, account_name)
            driver.get(index)
        driver.switch_to.new_window('tab')
        driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        driver.switch_to.new_window('tab')
        driver.get("https://proxyleak.com/")
        try:
            while len(driver.window_handles) > 0:
                time.sleep(1)
        except selenium.common.exceptions.WebDriverException:
            driver.quit()
            print('driver quit')

    @staticmethod
    def read_from_file(path: str) -> str:
        data = deserialize(path)
        user_agent_ = data["user-agent"]
        print(f"Read user agent: {user_agent_}")
        return user_agent_

    @staticmethod
    def write_to_file(path: str) -> str:
        user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
        data = {
            'user-agent': user_agent_
        }
        serialize(path, data)
        return user_agent_


class QListCustomWidgetNew(QtWidgets.QWidget, Ui_Custom_widget):
    def __init__(self, parent=None):
        super(QListCustomWidgetNew, self).__init__(parent)
        self.setupUi(parent)


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.name = None

        self.textQVBoxLayout = QtWidgets.QHBoxLayout()
        self.account_name_label = QtWidgets.QLabel()
        self.running_status_label = QtWidgets.QLabel()
        self.pushButtonSettings = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSettings.sizePolicy().hasHeightForWidth())
        self.pushButtonSettings.setSizePolicy(sizePolicy)
        self.pushButtonSettings.setMaximumSize(32, 32)
        self.pushButtonSettings.setIcon(QtGui.QIcon("./icons/icons8-settings.svg"))
        self.pushButtonSettings.setIconSize(QtCore.QSize(32, 32))
        self.pushButtonSettings.clicked.connect(lambda: self.open_settings())

        self.checkBox = QtWidgets.QCheckBox()
        self.textQVBoxLayout.addWidget(self.checkBox)
        self.textQVBoxLayout.addWidget(self.account_name_label)
        self.textQVBoxLayout.addWidget(self.running_status_label)
        self.textQVBoxLayout.addWidget(self.pushButtonSettings)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.account_name_label.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.running_status_label.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def open_settings(self):
        path = fr'{os.path.dirname(os.path.realpath(__file__))}\profiles\{self.name}'
        try:
            data = deserialize(path)
            user_agent = data["user-agent"]
        except FileNotFoundError:
            data = {}
            user_agent = ""
        except KeyError:
            data = deserialize(path)
            user_agent = ""
        try:
            extensions = data["extensions"]
        except Exception as e:
            extensions = {}
        checked = 2
        dlg = SettingsDialog(user_agent=user_agent, account_name=self.name)
        try:
            passwords = do_decrypt(path)
            dlg.passwords_textBrowser.setText(passwords)
        except:
            pass
        for item in dlg.items:
            if item.extension_name in extensions:
                if extensions[item.extension_name] is True:
                    item.setCheckState(QtCore.Qt.Checked)
        dlg.show()
        result = dlg.exec()
        if result:
            for item in dlg.items:
                if item.checkState() == checked:
                    print(item.extension_name)
                    extensions.update({item.extension_name: True})
                else:
                    extensions.update({item.extension_name: False})
            data.update({"extensions": extensions})
            if dlg.user_agent_line.text() != user_agent:
                data.update({"user-agent": dlg.user_agent_line.text()})
            serialize(path, data)

    def setTextUp(self, text):
        self.account_name_label.setText(text)


class QListAccountsWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None):
        super(QListAccountsWidgetItem, self).__init__(parent)
        self.name = None
        self.status: bool = False
        self.thread: threading.Thread or None = None


class QlistExtensionsWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None):
        super(QlistExtensionsWidgetItem, self).__init__(parent)
        self.extension_name = None


class CreateAccountDialog(Ui_create_account_dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CreateAccountDialog, self).__init__(parent)
        self.setupUi(self)


class SettingsDialog(Ui_settings_dialog, QtWidgets.QDialog):
    def __init__(self, parent=None, user_agent="", account_name=""):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.items = []
        self.name = account_name
        self.user_agent_line.setText(user_agent)
        extension_list = os.listdir(fr"{os.path.dirname(os.path.realpath(__file__))}\extension")
        for extension_name in extension_list:
            text = extension_name
            item = QlistExtensionsWidgetItem()
            item.setText(text)
            item.extension_name = extension_name
            item.setCheckState(QtCore.Qt.Unchecked)
            self.items.append(item)
            self.listWidgetExtensions.addItem(item)


class AboutDlg(Ui_about_dialog, QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.label_bild_number.setText('0.2')


class ProgressBarDialog(Ui_progress_bar, QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

    @QtCore.pyqtSlot(int)
    def progress(self, value: int):
        self.progressBar.setValue(value)

    @QtCore.pyqtSlot(str)
    def filename(self, name: str):
        self.label_file.setText(name)

    @QtCore.pyqtSlot()
    def exit(self):
        self.close()


class ProgressBarDialogThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.dlg = ProgressBarDialog()
        self.dlg.show()
        self.dlg.exec()


class QListCustomWidget(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None):
        super(QListCustomWidget, self).__init__(parent)
        self.name = None
        self.status: bool = False
        self.thread: threading.Thread or None = None


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    progress_signal = QtCore.pyqtSignal(int)
    progress_exit_signal = QtCore.pyqtSignal()
    progress_filename_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.base_path = fr"{os.path.dirname(os.path.realpath(__file__))}"
        self.profiles_path = fr"{os.path.dirname(os.path.realpath(__file__))}\profiles"
        self.browsers_names = [item for item in os.listdir(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles")
                               if os.path.isdir(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\{item}")]
        self.list_item_arr = []
        for i in self.browsers_names:
            self.create_list_item(i)

        self.add_functions()
        self.start_threads_watcher()

    def add_functions(self):
        self.listWidget.itemClicked.connect(self.item_click)
        self.CreateAccountButton.clicked.connect(self.create_profile)
        self.pushButtonDeleteAccounts.clicked.connect(self.delete_profiles)
        self.exportProfileButton.clicked.connect(self.export_profiles)
        self.importProfileButton.clicked.connect(self.import_profiles)
        self.checkBoxCkeckAll.stateChanged.connect(self.set_all_checkbox)
        self.actionAbout.triggered.connect(self.open_about)

    def set_all_checkbox(self, state):
        for item in self.list_item_arr:
            widget = self.listWidget.itemWidget(item)
            item_state = widget.checkBox.checkState()
            if item_state != 2 and state == 2:
                widget.checkBox.setCheckState(QtCore.Qt.Checked)

            elif item_state != 0 and state == 0:
                widget.checkBox.setCheckState(QtCore.Qt.Unchecked)

    def create_list_item(self, name):
        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.setTextUp(name)
        myQCustomQWidget.name = name
        myQListWidgetItem = QListAccountsWidgetItem(self.listWidget)
        myQListWidgetItem.name = name
        # Set size hint
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        # Add QListWidgetItem into QListWidget
        self.listWidget.addItem(myQListWidgetItem)
        self.listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.list_item_arr.append(myQListWidgetItem)

    def extract_zip(self, path, forbidden=[]):

        with ZipFile(path, 'r') as zipObj:
            counter = 0
            length = len(zipObj.filelist)
            # TODO if forbidden is not empty then length should be shorter
            # print(zipObj.filelist[0].filename.split('/')[0])
            for file in zipObj.filelist:
                if file.filename.split('/')[0] not in forbidden:
                    zipObj.extract(file, './profiles')
                    counter += 1
                    self.progress_signal.emit(int(counter / (length / 100)))
                    self.progress_filename_signal.emit(file.filename)
                    # print(f"{counter / (length / 100)}%")
        self.progress_exit_signal.emit()

    def progress_bar_thread(self, target, title, *args):
        """

        :param target: target function
        :param title: title for progress window
        :param args: args for target function
        :return:
        """
        progress_bar = ProgressBarDialog()
        progress_bar.show()
        progress_bar.setWindowTitle(title)
        self.progress_signal.connect(progress_bar.progress)
        self.progress_exit_signal.connect(progress_bar.exit)
        self.progress_filename_signal.connect(progress_bar.filename)
        t = threading.Thread(target=target, args=args)
        t.start()
        progress_bar.exec()

    def export_profiles(self):
        checked_items = self.get_checked_items()
        export_path = fr"{self.base_path}\export.zip"
        if os.path.isfile(export_path):
            os.remove(export_path)
        if len(checked_items) > 0:
            self.progress_bar_thread(self.zip_directory, "Exporting",
                                     [fr'{self.profiles_path}\{profile.name}' for profile in checked_items],
                                     export_path)
            # self.zip_directory([fr'{self.profiles_path}\{profile.name}' for profile in checked_items],
            #                    export_path)
        print("EXPORTED")

    def import_profiles(self):
        profile_names = os.listdir(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles")
        dlg = QtWidgets.QFileDialog()
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            if len(filenames) == 1:
                pth = zipfile.Path(filenames[0])
                profiles = list(pth.iterdir())
                imported_accounts = [folder.name for folder in profiles]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(f"Are y sure you want to import accounts: {imported_accounts}")
                msg.setWindowTitle("Warning")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                retval = msg.exec()
                if retval == 1024:
                    same_items = [item for item in profile_names if item in imported_accounts]

                    if len(same_items) > 0:
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setText(f"Accounts {same_items} is already exist. Overwrite?")
                        msg.setWindowTitle("Warning")
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No)
                        retval = msg.exec()
                        if retval == 1024:
                            self.progress_bar_thread(self.extract_zip, "Importing", filenames[0])
                            self.update_item_list()
                            print("IMPORTED")
                        else:
                            self.progress_bar_thread(self.extract_zip, "Importing", filenames[0], same_items)
                            self.update_item_list()
                            print("IMPORTED")
                    else:
                        self.progress_bar_thread(self.extract_zip, "Importing", filenames[0])
                        self.update_item_list()
                        print("IMPORTED")

    def zip_directory(self, folders_path: list, zip_path: str):

        counter = 1
        with zipfile.ZipFile(zip_path, mode='w') as zipf:
            length = len(folders_path)
            for folder_path in folders_path:
                base_folder = folder_path.split('\\')[-1]
                # print(base_folder)
                self.progress_signal.emit(int(counter / (length / 100)))
                self.progress_filename_signal.emit(base_folder)
                len_dir_path = len(folder_path)
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, f'{base_folder}/{file_path[len_dir_path:]}')
                counter += 1
        self.progress_exit_signal.emit()
        # progress_bar.done(0)

    def get_checked_items(self):
        checked_items = []
        for item in self.list_item_arr:
            widget = self.listWidget.itemWidget(item)
            if widget.checkBox.checkState() == 2:
                checked_items.append(item)
        return checked_items

    def delete_profiles(self):
        checked_items = self.get_checked_items()
        if len(checked_items) > 0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)

            msg.setText(f"Are y sure you want to delete accounts: {[i.name for i in checked_items]}")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

            retval = msg.exec()
            if retval == 1024:
                self.progress_bar_thread(self.delete_profiles_thread, "Deleting", checked_items)
                self.update_item_list()

    def delete_profiles_thread(self, checked_items):
        counter = 1
        length = len(checked_items)
        for profile in checked_items:
            shutil.rmtree(path=fr'{self.profiles_path}\{profile.name}')
            self.listWidget.removeItemWidget(profile)
            self.progress_signal.emit(int(counter / (length / 100)))
            # print(type(profile.name))
            self.progress_filename_signal.emit(profile.name)
            counter += 1

        # time.sleep(2)
        self.progress_exit_signal.emit()



    def update_item_list(self):
        self.browsers_names = [item for item in os.listdir(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles")
                               if os.path.isdir(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\{item}")]
        self.list_item_arr = []
        self.listWidget.clear()
        for i in self.browsers_names:
            self.create_list_item(i)

    def open_progress_bar(self):
        dlg = ProgressBarDialog()
        self.progressbar_signal = dlg.signal
        dlg.show()
        dlg.exec()

    def open_about(self):
        dlg = AboutDlg()
        dlg.show()
        dlg.exec()

    def create_profile(self):
        dlg = CreateAccountDialog()
        dlg.show()
        result = dlg.exec()
        account_name = dlg.lineEdit.text()
        if result:
            self.create_list_item(account_name)
            path = fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\{account_name}"
            os.makedirs(path)
            user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
            data = {
                'user-agent': user_agent_
            }
            serialize(path, data)
            # passwords = do_decrypt(path)

    def item_click(self, item: QListAccountsWidgetItem):
        account_name = self.listWidget.itemWidget(item).name
        if item.status is True:
            pass
        else:
            t = threading.Thread(target=self.run_browser, args=(account_name,))
            item.thread = t
            t.start()
            print("Thread created")

    def run_browser(self, name):
        path = fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\{name}"
        d = WebBrowser(path=path, account_name=name)
        print(f"Browser {name} started")
        passwords = do_decrypt(path)

    def start_threads_watcher(self):
        t = threading.Thread(target=self.threads_watcher)
        t.start()

    def threads_watcher(self):
        while True:
            for i in self.list_item_arr:
                try:
                    widget = self.listWidget.itemWidget(i)
                    if i.thread.is_alive():

                        widget.running_status_label.setText(f'running...')
                        widget.status = True
                    else:
                        widget.running_status_label.setText(f'')
                        widget.status = False
                except AttributeError:
                    pass
            time.sleep(1)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(app.exec_())
