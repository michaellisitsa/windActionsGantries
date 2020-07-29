#Use code pyinstaller --onefile --hidden-import=main2 main.py to initialise
import inspect
from importlib import import_module
mymod = import_module('main2')

def getsource():
    print(inspect.getsource(mymod.wind_calcs))
    input("Press any key to exit!!!")