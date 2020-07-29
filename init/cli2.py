import os
import importlib.util
homedir = os.path.dirname(os.path.dirname(__file__))
main_dir = os.path.join(homedir,"main2.py")
spec = importlib.util.spec_from_file_location("main2.wind_calcs.cd_cs", main_dir)
mymod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mymod)

#import inspect
#print(inspect.getsource(mymod))
#input("press any button")