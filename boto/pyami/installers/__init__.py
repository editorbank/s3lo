# Copyright (c) 2006,2007,2008 Mitch Garnaat http://garnaat.org/
#
#
from boto.pyami.scriptbase import ScriptBase


class Installer(ScriptBase):
    """
    Abstract base class for installers
    """

    def add_cron(self, name, minute, hour, mday, month, wday, who, command, env=None):
        """
        Add an entry to the system crontab.
        """
        raise NotImplementedError

    def add_init_script(self, file):
        """
        Add this file to the init.d directory
        """

    def add_env(self, key, value):
        """
        Add an environemnt variable
        """
        raise NotImplementedError

    def stop(self, service_name):
        """
        Stop a service.
        """
        raise NotImplementedError

    def start(self, service_name):
        """
        Start a service.
        """
        raise NotImplementedError

    def install(self):
        """
        Do whatever is necessary to "install" the package.
        """
        raise NotImplementedError
