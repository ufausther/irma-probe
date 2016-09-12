#
# Copyright (c) 2013-2016 Quarkslab.
# Copyright (c) 2016 Teclib'
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.

import logging
import re

from ..base import Antivirus

log = logging.getLogger(__name__)


class ArmaditoAV(Antivirus):
    _name = "Armadito Antivirus"

    # ==================================
    #  Constructor and destructor stuff
    # ==================================

    def __init__(self, *args, **kwargs):
        # class super class constructor
        super(ArmaditoAV, self).__init__(*args, **kwargs)        
        
        # scan tool variables
        self._scan_args = (
            "--no-summary"  # disable summary at end of scanning            
        )
        self._scan_patterns = [
            re.compile(r'(?P<file>.*): malware (?P<name>([^\s]+ - [^\s]+))', re.IGNORECASE)            
        ]

    # ==========================================
    #  Antivirus methods (need to be overriden)
    # ==========================================

    def get_version(self):
        """return the version of the antivirus"""
        result = None
        if self.scan_path:
            cmd = self.build_cmd(self.scan_path, '--version')
            retcode, stdout, stderr = self.run_cmd(cmd)
            if not retcode:                
                matches = re.search(r'(?P<version>\d+(\.\d+)+)',
                                    stdout,
                                    re.IGNORECASE)
                if matches:
                    result = matches.group('version').strip()        
        return result

    def get_database(self):
        """return list of files in the database"""
        # TODO: modules databases files.
        return None        

    def get_scan_path(self):
        """return the full path of the scan tool"""
        paths = self.locate("armadito-scan", "/usr/local/bin/")
        return paths[0] if paths else None
