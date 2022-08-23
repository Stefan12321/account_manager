import os
import time
import threading
import selenium
import undetected_chromedriver.v2 as uc

from selenium import webdriver
from GUI import Ui_MainWindow
from PyQt5 import QtWidgets
from create_account_dialog import Ui_Dialog as Ui_create_account_dialog
from list_widget import Ui_Form as Ui_Custom_widget


class WebBrowser:
    def __init__(self, path):
        # options = uc.ChromeOptions()
        chromedriver = './chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-data-dir={path}')
        options.add_extension(f'./extension/FoxyProxy-Standard.crx')
        # options.add_argument(
        #     f'--load-extension={os.path.dirname(os.path.realpath(__file__))}\extension\FoxyProxy-Standard.crx')
        # driver = uc.Chrome(options=options)
        driver = webdriver.Chrome(chromedriver, options=options)
        try:
            while len(driver.window_handles) > 0:
                time.sleep(1)
        except selenium.common.exceptions.WebDriverException:
            driver.quit()
            print('driver quit')


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
        print('aaa')
        dlg = CreateAccountDialog()
        dlg.show()
        result = dlg.exec()
        account_name = dlg.lineEdit.text()
        if result:
            t = threading.Thread(target=self.run_browser, args=(account_name,))
            t.start()
            w = QListCustomWidget()
            w.setText(account_name)
            w.name = account_name
            self.list_widget_arr.append(w)
            self.listWidget.addItem(w)
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
        d = WebBrowser(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\{name}")

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
    m.show()
    sys.exit(app.exec_())
    # d = WebBrowser(fr"{os.path.dirname(os.path.realpath(__file__))}\profiles\2")
