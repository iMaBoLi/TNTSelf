from traceback import format_exc
from importlib import import_module, reload

def get_plugins():
    files = sorted(glob.glob(f"FidoSelf/plugins/*.py"))
    return files

def load_plugins(files, reload=False):
    plugs = []
    notplugs = {}
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
