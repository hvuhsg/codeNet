from cx_Freeze import setup, Executable

#base = "Win32GUI"
base = None

executables = [Executable("mainServer.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "mainServer",
    options = options,
    version = "3.2",
    description = 'mainServer',
    executables = executables
)
