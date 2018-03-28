from __future__ import unicode_literals

import base64
import re
from functools import reduce


key_whitelist = ['$or', '$and', '$exists', '$in', '$gt', '$gte',
                 '$lt', '$lte', '$regex', '$options', '$all']


def _decode_from_mongo(key):
    re_dollar = re.compile(r'^%s' % base64.b64encode(b'$').decode('utf-8'))
    re_dot = re.compile(r'%s' % base64.b64encode(b'.').decode('utf-8'))
    return reduce(lambda s, c: c[0].sub(c[1], s),
                  [(re_dollar, '$'), (re_dot, '.')], key)


def _is_invalid_for_mongo(key):
    return key not in\
        key_whitelist and (key.startswith('$') or key.count('.') > 0)
