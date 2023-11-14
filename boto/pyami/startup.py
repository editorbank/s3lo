# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#
#
import sys
import boto
from boto.utils import find_class
from boto import config
from boto.pyami.scriptbase import ScriptBase


class Startup(ScriptBase):

    def run_scripts(self):
        scripts = config.get('Pyami', 'scripts')
        if scripts:
            for script in scripts.split(','):
                script = script.strip(" ")
                try:
                    pos = script.rfind('.')
                    if pos > 0:
                        mod_name = script[0:pos]
                        cls_name = script[pos + 1:]
                        cls = find_class(mod_name, cls_name)
                        boto.log.info('Running Script: %s' % script)
                        s = cls()
                        s.main()
                    else:
                        boto.log.warning('Trouble parsing script: %s' % script)
                except Exception as e:
                    boto.log.exception('Problem Running Script: %s. Startup process halting.' % script)
                    raise e

    def main(self):
        self.run_scripts()
        self.notify('Startup Completed for %s' % config.get('Instance', 'instance-id'))

if __name__ == "__main__":
    if not config.has_section('loggers'):
        boto.set_file_logger('startup', '/var/log/boto.log')
    sys.path.append(config.get('Pyami', 'working_dir'))
    su = Startup()
    su.main()
