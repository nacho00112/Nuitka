#!/usr/bin/env python
#     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Python test originally created or extracted from other peoples work. The
#     parts from me are licensed as below. It is at least Free Softwar where
#     it's copied from other people. In these cases, that will normally be
#     indicated.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

import os, sys, tempfile, subprocess

os_path = os.path.normcase( os.path.dirname( os.__file__  ) )

print "Using standard library path", os_path

stage_dir = os.path.join( tempfile.gettempdir(), "compile_library" )

blacklist = (
    "__phello__.foo.py", # Triggers error for "." in module name
)

for root, dirnames, filenames in os.walk( os_path ):
    dirnames.sort()

    filenames = [ filename for filename in filenames if filename.endswith( ".py" ) and not filename in blacklist ]

    if not filenames:
        continue

    for filename in sorted( filenames ):
        path = os.path.join( root, filename )

        command = "%s %s --output-dir %s --recurse-none %s" % (
            sys.executable,
            os.path.join( os.path.dirname( __file__ ), "..", "..", "bin", "nuitka" ),
            stage_dir,
            path,
        )

        print path

        subprocess.check_call( command.split() )