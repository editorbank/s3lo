# Copyright (c) 2012 Amazon.com, Inc. or its affiliates.  All Rights Reserved
#
#
import os

# This allows boto modules to say "from boto.compat import json".  This is
# preferred so that all modules don't have to repeat this idiom.
try:
    import simplejson as json
except ImportError:
    import json


# Switch to use encodebytes, which deprecates encodestring in Python 3
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes


# If running in Google App Engine there is no "user" and
# os.path.expanduser() will fail. Attempt to detect this case and use a
# no-op expanduser function in this case.
try:
    os.path.expanduser('~')
    expanduser = os.path.expanduser
except (AttributeError, ImportError):
    # This is probably running on App Engine.
    expanduser = (lambda x: x)

from boto.vendored import six

from boto.vendored.six import BytesIO, StringIO
from boto.vendored.six.moves import filter, http_client, map, _thread, \
                                    urllib, zip
from boto.vendored.six.moves.queue import Queue
from boto.vendored.six.moves.urllib.parse import parse_qs, quote, unquote, \
                                                 urlparse, urlsplit
from boto.vendored.six.moves.urllib.parse import unquote_plus
from boto.vendored.six.moves.urllib.request import urlopen

if six.PY3:
    # StandardError was removed, so use the base exception type instead
    StandardError = Exception
    long_type = int
    from configparser import ConfigParser, NoOptionError, NoSectionError
    unquote_str = unquote_plus
    parse_qs_safe = parse_qs
else:
    StandardError = StandardError
    long_type = long
    from ConfigParser import SafeConfigParser as ConfigParser
    from ConfigParser import NoOptionError, NoSectionError

    def unquote_str(value, encoding='utf-8'):
        # In python2, unquote() gives us a string back that has the urldecoded
        # bits, but not the unicode parts.  We need to decode this manually.
        # unquote has special logic in which if it receives a unicode object it
        # will decode it to latin1.  This is hard coded.  To avoid this, we'll
        # encode the string with the passed in encoding before trying to
        # unquote it.
        byte_string = value.encode(encoding)
        return unquote_plus(byte_string).decode(encoding)

    # These are the same default arguments for python3's
    # urllib.parse.parse_qs.
    def parse_qs_safe(qs, keep_blank_values=False, strict_parsing=False,
                      encoding='utf-8', errors='replace'):
        """Parse a query handling unicode arguments properly in Python 2."""
        is_text_type = isinstance(qs, six.text_type)
        if is_text_type:
            # URL encoding uses ASCII code points only.
            qs = qs.encode('ascii')
        qs_dict = parse_qs(qs, keep_blank_values, strict_parsing)
        if is_text_type:
            # Decode the parsed dictionary back to unicode.
            result = {}
            for (name, value) in qs_dict.items():
                decoded_name = name.decode(encoding, errors)
                decoded_value = [item.decode(encoding, errors)
                                 for item in value]
                result[decoded_name] = decoded_value
            return result
        return qs_dict
