########################################################################
#
# Copyright 2026 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

#
# To test this code, 
#   - Either run it in the KLayout Macro Development environment
#   - Or use the shell comamnd (bash syntax):
#       (in the location of this file):
#       KLAYOUT_PATH=$(pwd)/.. klayout -zz -r pycell_lvs_test.py
#

import os
from pathlib import Path
import sys
from typing import *

directory_containing_this_script = os.path.realpath(os.path.dirname(__file__))

try:
    from lvs_testcase import (LVSTestCase, LVSResult)
except ModuleNotFoundError:
    sys.path.append(directory_containing_this_script)
    from lvs_testcase import (LVSTestCase, LVSResult)


PCELL_LIB_NAME = 'SG13_dev'
TECH_NAME = 'sg13g2'


def find_lvs_testcases() -> List[LVSTestCase]:
    testcases = []

    testdata_dir = Path(directory_containing_this_script) / 'lvs_testcases'
    for suffix in ('.gds.gz',):
        absolute_layout_paths = [f.resolve() for f in testdata_dir.glob(f"*{suffix}")]
        for lp in absolute_layout_paths:
            parent = lp.parent
            cell_name = str(lp.name)[0:-len(suffix)]
            testcases.append(
                LVSTestCase(
                    name=cell_name,
                    top_cell_name=cell_name,
                    layout_path=lp,
                    netlist_path=parent / f"{cell_name}.spice"
                )
            )
    return testcases

    
if __name__ == "__main__":
    lvs_testcases = find_lvs_testcases()
    run_dir_base = 'pcell_lvs_test_run_dir'

    passed_tests = []
    failed_tests = []

    for testcase in lvs_testcases:
        print(f"\n[{testcase.name}] Running LVS check …")

        result = testcase.run(run_dir_base=run_dir_base)

        if result.passed:
            passed_tests.append(result)
        else:
            failed_tests.append(result)

    print("\n")
    if len(failed_tests) == 0:
        print(f"PASS: {len(passed_tests)} of {len(lvs_testcases)} testcases passed")
        for result in passed_tests:
            print(f"\t✅ {result.testcase.name}")
        sys.exit(0)
    else:
        print(f"FAIL: {len(failed_tests)} of {len(lvs_testcases)} testcases failed:")
        for result in passed_tests:
            print(f"\t✅ {result.testcase.name}")
        for result in failed_tests:
            print(f"\t❌ {result.testcase.name} ({' '.join(result.messages)})")
            print(f"\t\tLVSDB: {result.report_path}")
        sys.exit(1)
