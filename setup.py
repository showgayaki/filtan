import sys
from cx_Freeze import setup, Executable


base = 'Win32GUI' if sys.platform == 'win32' else None
name = 'filtan'
# icon = 'icon/filtan.ico'
includes = ['pathlib', 'os', 'subprocess']
exe = [
    Executable(
        script='run.py'
        , base=base
        , targetName=name
        # , icon=icon
    )
]

setup(
    name=name
    , version='0.1.0'
    , description='Create Gmail label and filter'
    , options={'build_exe': {'includes': includes}}
    , executables=exe
)
