import urllib2, base64
import json, time, re
from datetime import datetime, timedelta
import logging
from toolz.functoolz import memoize

class hbquery:
    def __init__(self):
        self.is_resolved = False
        self.is_ignored  = False
        self.env = "production"

    def build(self, created_after=None):
        #TODO: hard-coded now
        q = "?q=-is%3Aresolved+-is%3Aignored+environment%3Aproduction"

        if created_after is not None:
            timestamp = time.mktime(created_after.timetuple())
            return q + "&created_after=%i"%timestamp

        return q

class honeybadger:
    def __init__(self, project_id, username, password = ''):
        self.username = username
        self.password = password
        self.project_id = project_id

    def project(self, q, created_after=None):
        #"?q=-is%3Aresolved+-is%3Aignored+environment%3Aproduction"
        host = "https://app.honeybadger.io/v2/projects/%s"%self.project_id
        return self.query(host, q)

    def faults(self, q):
        host = "https://app.honeybadger.io/v2/projects/%s/faults"%self.project_id
        return self.query(host, q)

    def fault(self, fault_id):
        host = "https://app.honeybadger.io/v2/projects/45598/faults/%s/notices"%fault_id
        return self.query(host)

    @memoize
    def query(self, host, query = ''):
        self.logger().debug(host + query)
        request = urllib2.Request(host + query)
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        result = urllib2.urlopen(request).read()
        return json.loads(result)

    def logger(self):
        return logging.getLogger(self.__class__.__name__)

    def next(self, result):
        nxt = result['links']['next']
        return self.query(nxt)
