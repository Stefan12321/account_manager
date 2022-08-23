from cx_Freeze import setup, Executable
import shutil

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
includes = ['chromedriver.exe','profiles', 'extension']

packages = ["os", "threading",  "time", "PyQt5", "selenium"]
options = {
    'build_exe': {
        'packages': packages,
        'include_files': includes,
    }
}

setup(
    name="accounts_manager",
    options=options,
    version=1.1,
    description='',
    executables=executables
)