from traceback import format_exc
from importlib import import_module, reload

def load_plugins(folder, reload=False):
    plugs = []
    notplugs = {}
    files = sorted(glob.glob(f"{folder}/*.py"))
    for file in files:
        try:
            filename = file.replace("/", ".").replace(".py" , "")
            if not reload:
                import_module(filename)
            else:
                reload(filename)
            plugs.append(os.path.basename(file))
        except:
            notplugs.update({os.path.basename(file): format_exc()})
    return plugs, notplugs
