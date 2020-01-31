#!/usr/bin/python3

import os
import sys
from time import sleep

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from api import *
from shell import check_py_version


class DDNS():
    def __init__(self, domain, subdomain="@"):
        self.domain = domain
        self.subdomain = subdomain
        self.recordid = None
        self.currentip = None
        self.recordip = None

    def run(self):
        check_py_version()
        self.currentip = get_ip()
        self.recordid = get_record_id(self.domain, self.subdomain)
        info = get_info(self.domain, self.recordid)
        if info:
            if info["value"] == self.currentip:
                self.currentip = self.recordip
                print("A record %s exist." % self.currentip)
        else:
            self.recordid = add_record(self.domain, subdomain=self.subdomain)
        while True:
            if self.recordip != self.currentip:
                update(self.currentip, self.domain, self.recordid, self.subdomain)
            sleep(5)
            self.currentip = get_ip()

