import os
import sys
import traceback
from importlib import import_module
from glob import glob


class SiteManager():

    def __init__(self):
        self.sites = {}

    def add_site(self, sites):
        if not isinstance(sites, list):
            sites = [sites]

        def decorator(fn):
            for arg in sites:
                self.sites[arg] = fn
            return fn
        return decorator

    # noinspection PyMethodMayBeStatic
    def load_site_handlers(self):
        for handle in glob('sites/[!_]*.py'):
            if os.path.basename(handle) == 'manage.py':
                continue
            module_name = handle.replace("/", ".")[:-3]
            print "Module: %s" % module_name
            try:
                import_module(module_name)
            except:
                print "import failed on module %s, module not loaded" % plugin
                print "%s" % sys.exc_info()[0]
                print "%s" % traceback.format_exc()

manage = SiteManager()