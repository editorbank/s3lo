# Copyright 2010 Google Inc.
#


"""
Implements plugin related api.

To define a new plugin just subclass Plugin, like this.

class AuthPlugin(Plugin):
    pass

Then start creating subclasses of your new plugin.

class MyFancyAuth(AuthPlugin):
    capability = ['sign', 'vmac']

The actual interface is duck typed.
"""

import glob
import imp
import os.path


class Plugin(object):
    """Base class for all plugins."""

    capability = []

    @classmethod
    def is_capable(cls, requested_capability):
        """Returns true if the requested capability is supported by this plugin
        """
        for c in requested_capability:
            if c not in cls.capability:
                return False
        return True


def get_plugin(cls, requested_capability=None):
    if not requested_capability:
        requested_capability = []
    result = []
    for handler in cls.__subclasses__():
        if handler.is_capable(requested_capability):
            result.append(handler)
    return result


def _import_module(filename):
    (path, name) = os.path.split(filename)
    (name, ext) = os.path.splitext(name)

    (file, filename, data) = imp.find_module(name, [path])
    try:
        return imp.load_module(name, file, filename, data)
    finally:
        if file:
            file.close()

_plugin_loaded = False


def load_plugins(config):
    global _plugin_loaded
    if _plugin_loaded:
        return
    _plugin_loaded = True

    if not config.has_option('Plugin', 'plugin_directory'):
        return
    directory = config.get('Plugin', 'plugin_directory')
    for file in glob.glob(os.path.join(directory, '*.py')):
        _import_module(file)
