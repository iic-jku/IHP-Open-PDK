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

from __future__ import annotations
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
import subprocess
from typing import *


def lvs_script_path() -> str:
    directory_containing_this_script = os.path.realpath(os.path.dirname(__file__))
    parent_directory = os.path.dirname(directory_containing_this_script)
    script_path = os.path.join(parent_directory, 'tech', 'lvs', 'run_lvs.py')
    return script_path


@dataclass
class LVSResult:
    testcase: LVSTestCase
    return_code: Optional[int]
    report_path: Optional[Path]
    passed: bool
    messages: List[str]

    @classmethod
    def error_before_test_execution(cls, testcase: LVSTestCase, msg: str):
        return LVSResult(testcase=testcase,
                         return_code=None,
                         report_path=None,
                         passed=False,
                         messages=[msg])


_LVSDB_RE = re.compile(r"runset output at:\s*(?P<path>\S+)")
_ERROR_RE = re.compile(r"\bERROR\b\s*:\s*(?P<msg>.*)")
_SUCCESS_RE = re.compile(r"\bINFO\b\s*:\s*Congratulations!", re.IGNORECASE)


def parse_lvs_output(stdout: str, stderr: str) -> Tuple[Optional[Path], bool, List[str]]:
    lvsdb_path: Optional[Path] = None
    success = False
    messages: List[str] = []

    combined = stdout.splitlines() + stderr.splitlines()

    for line in combined:
        if m := _LVSDB_RE.search(line):
            lvsdb_path = Path(m.group("path"))

        if m := _ERROR_RE.search(line):
            messages.append(m.group("msg"))
            success = False  # ERROR always dominates

        if _SUCCESS_RE.search(line):
            success = True

    return lvsdb_path, success, messages


@dataclass
class LVSTestCase:
    name: str
    top_cell_name: str
    layout_path: Path
    schematic_path: Optional[Path]
    netlist_path: Path   # expected netlist

    def run(self,
            run_dir_base: Optional[Path],
            verbose: bool) -> LVSResult:
        fs_test_name = self.name.replace(' ', '_').replace('/', '-').lower()
        run_dir = Path(run_dir_base).resolve() / fs_test_name
        
        layout_path = Path(self.layout_path).resolve()
        netlist_path = Path(self.netlist_path).resolve()

        args = [
            '--run_dir', str(run_dir),
            '--layout', str(layout_path),
            '--netlist', str(netlist_path),
            '--topcell', self.top_cell_name,
        ]
        
        cmd_args = ['python3', lvs_script_path()] + args
        if verbose:
            print(f"Calling subprocess with: {' '.join(cmd_args)}")
        
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ERROR: LVS script terminated with exit code {result.returncode}")

        lvsdb_path, passed, messages = parse_lvs_output(result.stdout, result.stderr)

        result = LVSResult(
            testcase=self,
            return_code=result.returncode,
            report_path=run_dir / f"{self.top_cell_name}.lvsdb",
            passed=passed,
            messages=messages
        )

        return result
