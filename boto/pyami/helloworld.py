# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#
#
from boto.pyami.scriptbase import ScriptBase

class HelloWorld(ScriptBase):

    def main(self):
        self.log('Hello World!!!')
