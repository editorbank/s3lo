# Copyright 2010 Google Inc.
#


class User(object):
    def __init__(self, parent=None, id='', name=''):
        if parent:
            parent.owner = self
        self.type = None
        self.id = id
        self.name = name

    def __repr__(self):
        return self.id

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'Name':
            self.name = value
        elif name == 'ID':
            self.id = value
        else:
            setattr(self, name, value)

    def to_xml(self, element_name='Owner'):
        if self.type:
            s = '<%s type="%s">' % (element_name, self.type)
        else:
            s = '<%s>' % element_name
        s += '<ID>%s</ID>' % self.id
        if self.name:
            s += '<Name>%s</Name>' % self.name
        s += '</%s>' % element_name
        return s
