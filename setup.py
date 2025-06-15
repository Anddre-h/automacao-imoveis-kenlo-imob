import sys
from cx_Freeze import setup, Executable

# Criar uma interface gráfica pro Windows
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
setup(
    name='Kenlo Imob - Automação',
    version='1.0',
    description='Esse é um programa com interface gráfica que automatiza site.',
    author='Anddré Henrique',
    options={'build_exe':{
        'includes': ['tkinter'],
        'include_msvcr': True
    }},
    executables=[Executable('main.py', base=base, icon='logo-kenlo-imob.ico')]
    )