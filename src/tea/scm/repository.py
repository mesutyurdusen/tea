__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '01 January 2009'
__copyright__ = 'Copyright (c) 2009 Viktor Kerkez'

import re
import urllib2
import urlparse


# tea imports
from .hg import Hg

NETLOC_RE = re.compile('^(?:(?P<username>[^:]+)(?:\:(?P<password>[^@]+))?@)?(?P<netloc>.*)$')

def set_uri(uri, **kwargs):
    try:
        parsed = urlparse.urlparse(uri)
        match = NETLOC_RE.match(parsed.netloc)
        if match:
            gd = match.groupdict()
            for key, value in kwargs.items():
                gd[key] = value
            if gd['username'] and gd['password']:
                netloc = '%(username)s:%(password)s@%(netloc)s' % gd
            elif gd['username']:
                netloc = '%(username)s@%(netloc)s' % gd
            else:
                netloc = '%(netloc)s' % gd
            parsed = parsed._replace(netloc=netloc)
        return urlparse.urlunparse(parsed)
    except:
        return uri


class Repository(object):
    def __init__(self, name, path=None, source=None, username=None, password=None):
        self.name     = name
        self.path     = path
        self.source   = source
        self.username = urllib2.quote(username)
        self.password = urllib2.quote(password)
        self._uri     = None
        self._muri    = None
        self.hg       = Hg(self)

    @property
    def uri(self):
        '''Returns the full URI with username and password'''
        if self._uri is None:
            self._uri = set_uri(self.source, username=self.username, password=self.password)
        return self._uri

    @property
    def muri(self):
        '''Returns a full URI with username, but password is massked'''
        if self._muri is None:
            self._muri = set_uri(self.source, username=self.username, password='*****')
        return self._muri

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Repository <%s>' % self.name

    def __serialize__(self):
        return {
            'name'   : self.name,
            'type'   : 'Repository',
            'path'   : self.path,
            'source' : self.source,
        }