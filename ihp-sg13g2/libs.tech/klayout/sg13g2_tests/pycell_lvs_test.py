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

import argparse
import os
from pathlib import Path
import sys
from typing import *


directory_containing_this_script = os.path.realpath(os.path.dirname(__file__))

try:
    from lvs_testcase import (LVSTestCase, LVSResult)
    from xschem_util import xschemrc_default_path, xschem_netlist, NetlistMode
except ModuleNotFoundError:
    sys.path.append(directory_containing_this_script)
    from lvs_testcase import (LVSTestCase, LVSResult)
    from xschem_util import xschemrc_default_path, xschem_netlist, NetlistMode


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
                    schematic_path=parent / f"{cell_name}.sch",
                    netlist_path=parent / f"{cell_name}.spice"
                )
            )
    return testcases


def parse_args(arg_list: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"LVS testcase runner",
                                     add_help=False)

    parser.add_argument("-q", "--quiet", dest="verbose",
                        action='store_true', default=True,
                        help="Quiet mode (show no commands, default is %(not default)s)")

    parser.add_argument("--xschemrc", dest="xschemrc_path",
                        type=str, default=None,
                        help="Path to custom xschemrc")

    return parser.parse_args()


def main(arg_list: List[str]):
    args = parse_args(arg_list)

    def xschemrc_path_or_bail() -> Path:
        if args.xschemrc_path is not None:
            xschemrc_path = args.xschemrc_path
        else:
            try:
                xschemrc_path = xschemrc_default_path()
            except Exception as e:
                print(f"ERROR: failed to netlist xschem schematic, "
                      f"ensure PDK/PDK_ROOT variables are set! Caught exception: {e}")
                sys.exit(1)
        return xschemrc_path

    lvs_testcases = find_lvs_testcases()
    run_dir_base = Path('pcell_lvs_test_run_dir')

    passed_tests = []
    failed_tests = []

    for t in lvs_testcases:
        if not t.layout_path.exists():
            failed_tests.append(
                LVSResult.error_before_test_execution(
                    t, f"layout does not exist at {str(t.layout_path)}"
                )
            )
            continue
        elif t.netlist_path is None:
            failed_tests.append(
                LVSResult.error_before_test_execution(t, f"netlist path is None")
            )
            continue

        if t.schematic_path is not None:
            reason: Optional[str] = None
            if not t.netlist_path.exists():
                reason = "netlist does not yet exist"
            elif t.netlist_path.stat().st_mtime_ns < t.schematic_path.stat().st_mtime_ns:
                reason = "netlist is older than xschem schematic"

            if reason is not None:
                if args.verbose:
                    print(f"\tNetlisting the xschem schematic, as {reason}")
                result = xschem_netlist(rcfile_path=xschemrc_path_or_bail(),
                                        sch_path=t.schematic_path,
                                        output_netlist_path=t.netlist_path,
                                        mode=NetlistMode.LVS,
                                        verbose=args.verbose)
                if result.returncode != 0:
                    print(result.stdout)
                    sys.exit(1)

        print(f"\n[{t.name}] Running LVS check … ", end='')

        result = t.run(run_dir_base=run_dir_base, verbose=args.verbose)

        if result.passed:
            print('PASS')
            passed_tests.append(result)
        else:
            print('FAIL')
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


if __name__ == "__main__":
    main(sys.argv)