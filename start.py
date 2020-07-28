import sys
import types


def reload_package(root_module):
    package_name = root_module.__name__

    loaded_package_modules = dict([
        (key, value) for key, value in sys.modules.items()
        if key.startswith(package_name) and isinstance(value, types.ModuleType)])

    for key in loaded_package_modules:
        del sys.modules[key]

    for key in loaded_package_modules:
        print('loading %s' % key)
        new_module = __import__(key)
        old_module = loaded_package_modules[key]
        old_module.__dict__.clear()
        old_module.__dict__.update(new_module.__dict__)


PROJECT_PATH = "C:/Users/Miruna/Documents/PythonProjects/BurnTheWitch"

sys.path.append(PROJECT_PATH)
reload_package(bin)
from bin.main import Main

script = Main()
print(u"\u0028\u256F\u00B0\u25A1\u00B0\u0029\u256F\uFE35\u0020\u253B\u2501\u253B")
script.execute()
sys.path.remove(PROJECT_PATH)
