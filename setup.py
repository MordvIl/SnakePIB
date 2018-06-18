import sys
import os.path
from cx_Freeze import setup, Executable



PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib', 'xml',
            'unicodedata', 'bz2', 'select']
zip_include_packages = ['collections', 'encodings', 'importlib', 'wx']

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
           }
}

    
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "snake8v1",
        version = "1.1",
        description = "Snake",
        options = options,
        executables = [Executable("snake8v1.py", base = base)])
