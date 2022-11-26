from cx_Freeze import setup, Executable
import shutil
import os

try:
    shutil.rmtree('build')
    shutil.rmtree('dist')
except:
    pass
base = None

executables = [Executable("main.py",
                          target_name='Accounts manager.exe',
                          base=base)
               ]

# includes = ['chromedriver.exe']
includes = ['extension', 'icons', './settings.json']

packages = ["os", "threading", "time", "PyQt5", "selenium", "json", "user_agents", "undetected_chromedriver",
            "html_editor", "autoreg"]
options = {
    'build_exe': {
        'packages': packages,
        'include_files': includes,
    }
}

setup(
    name="accounts_manager",
    options=options,
    version=1.0,
    description='',
    executables=executables
)
os.makedirs('./build/exe.win-amd64-3.9/profiles')