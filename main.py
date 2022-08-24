import os
import time
import threading
import selenium
import json
import undetected_chromedriver.v2 as uc

from selenium import webdriver
from GUI import Ui_MainWindow
from PyQt5 import QtWidgets
from create_account_dialog import Ui_Dialog as Ui_create_account_dialog
from user_agents.main import get_user_agent
from html_editor.main import create_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from qt_material import apply_stylesheet
from list_widget import Ui_Form as Ui_Custom_widget


class WebBrowser:
    def __init__(self, path, account_name):
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
        options.add_extension(f'./extension/chrome_extension_fcc-master.crx')
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
        with open(fr'{path}\config.json', 'r') as f:
            data = json.load(f)
            user_agent_ = data["user-agent"]
        print(f"Read user agent: {user_agent_}")
        return user_agent_

    @staticmethod
    def write_to_file(path: str) -> str:
        with open(f'{path}/config.json', 'w') as f:
            user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
            data = {
                'user-agent': user_agent_
            }
            try:
                json.dump(data, f)
                print(f"Created user agent: {user_agent_}")
            except Exception as e:
                print(e)
        return user_agent_

# class QListCustomWidget(QtWidgets.QListWidgetItem, Ui_Custom_widget):
#     def __init__(self, parent=None):
#         super(QListCustomWidget, self).__init__(parent)
#         self.setupUi(parent)

class CreateAccountDialog(Ui_create_account_dialog, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CreateAccountDialog, self).__init__(parent)
        self.setupUi(self)


class QListCustomWidget(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None):
        super(QListCustomWidget, self).__init__(parent)
        self.name = None
        self.status: bool = False
        self.thread: threading.Thread or None = None


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.browsers_names = os.listdir(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles")
        self.list_widget_arr = []
        for i in self.browsers_names:
            w = QListCustomWidget()
            w.setText(i)
            w.name = i
            self.list_widget_arr.append(w)
            self.listWidget.addItem(w)
        self.add_functions()
        self.start_threads_watcher()

    def add_functions(self):
        self.listWidget.itemClicked.connect(self.item_click)
        self.CreateAccountButton.clicked.connect(lambda: self.create_profile())

    def create_profile(self):
        dlg = CreateAccountDialog()
        dlg.show()
        result = dlg.exec()
        account_name = dlg.lineEdit.text()
        if result:

            w = QListCustomWidget()
            w.setText(account_name)
            w.name = account_name
            self.list_widget_arr.append(w)
            self.listWidget.addItem(w)
            os.makedirs(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\{account_name}")
        print(result)
        print(dlg.lineEdit.text())

    def item_click(self, item: QListCustomWidget):
        print(f"item {item.name} clicked")
        if item.status is True:
            pass
        else:
            t = threading.Thread(target=self.run_browser, args=(item.text(),))
            item.thread = t
            t.start()

    def run_browser(self, name):
        d = WebBrowser(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\{name}", name)

    def start_threads_watcher(self):
        t = threading.Thread(target=self.threads_watcher)
        t.start()

    def threads_watcher(self):
        while True:
            for i in self.list_widget_arr:
                try:
                    if i.thread.is_alive():
                        i.setText(f'{i.name} running...')
                        i.status = True
                    else:
                        i.setText(f'{i.name}')
                        i.status = False
                except AttributeError:
                    pass

            time.sleep(1)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    m = MainWindow()
    # apply_stylesheet(app, theme='light_blue.xml')
    m.show()
    sys.exit(app.exec_())
    # d = WebBrowser(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\2")
