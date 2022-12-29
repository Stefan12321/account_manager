import os
import time
import selenium
import undetected_chromedriver as uc
import autoreg.autoreg_main

from user_agents.main import get_user_agent
from html_editor.main import create_html
from autoreg.autoreg_main import reg_outlook
from autoreg.namefake_api import Person
from .serializer import serialize, deserialize


class WebBrowser:
    def __init__(self, path, account_name):
        print(f"PATH {path}")
        self.start_undetected_chrome(path, account_name)

    def start_undetected_chrome(self, path, account_name):
        if os.path.isdir(path):
            #  get user agent from config.json
            try:
                data = deserialize(fr'{path}\config.json')
                #  get line number from config.json
                try:
                    line = data["line_number"]
                except KeyError as e:
                    if str(e).replace("'", "") != "line_number":
                        raise KeyError
                user_agent_ = data["user-agent"]
            except FileNotFoundError:
                user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
                data = {
                    'user-agent': user_agent_
                }
                serialize(fr'{path}\config.json', data)
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
            serialize(fr'{path}\config.json', data)
        index = f"{path}/init.html"
        base_dir = os.environ["ACCOUNT_MANAGER_BASE_DIR"]
        print(f"Base directory: {base_dir}")
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
        settings_main = deserialize('./settings.json')
        version_main = settings_main["chrome_version"]
        autoreg_ = settings_main["autoreg"]
        onload_pages = settings_main["onload_pages"]
        autoreg.autoreg_main.spreadsheetId = settings_main["spreadsheetId"]

        try:
            driver = uc.Chrome(options=options, version_main=version_main)
        except Exception as e:
            print(e)
        if os.path.exists(index):
            driver.get(index)
        else:
            create_html(index, account_name)
            driver.get(index)
        for page in onload_pages:
            try:
                driver.switch_to.new_window('tab')
                driver.get(page)
            except Exception as e:
                print(e)
        if autoreg_ == 2:
            person = Person()
            print(person)
            reg_outlook(driver, person, int(line))
        try:
            while len(driver.window_handles) > 0:
                time.sleep(1)
        except selenium.common.exceptions.WebDriverException:
            driver.quit()
            print('driver quit')

    @staticmethod
    def read_from_file(path: str) -> str:
        data = deserialize(fr'{path}\config.json')
        user_agent_ = data["user-agent"]
        print(f"Read user agent: {user_agent_}")
        return user_agent_

    @staticmethod
    def write_to_file(path: str) -> str:
        user_agent_ = get_user_agent(os=("win"), navigator=("chrome"), device_type=("desktop"))
        data = {
            'user-agent': user_agent_
        }
        serialize(fr'{path}\config.json', data)
        return user_agent_
