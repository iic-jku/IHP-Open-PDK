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
from enum import StrEnum
import os
from pathlib import Path
import subprocess
from subprocess import CompletedProcess
from typing import *


class NetlistMode(StrEnum):
    SIMULATION = 'sim'
    LVS = 'lvs'


def xschemrc_default_path() -> Path:
    path = Path(os.environ['PDK_ROOT']) / os.environ['PDK'] /\
           'libs.tech' / 'xschem' / 'xschemrc'
    return path


def xschem_netlist(rcfile_path: str | Path,
                   sch_path: str | Path,
                   output_netlist_path: str | Path,
                   mode: NetlistMode,
                   verbose: bool) -> CompletedProcess[str]:
    rcfile_path = Path(rcfile_path).resolve()
    sch_path = Path(sch_path).resolve()
    output_netlist_path = Path(output_netlist_path).resolve()

    tcl_command = ""
    match mode:
        case NetlistMode.LVS:
            tcl_command += "xschem set format lvs_format; "
        case NetlistMode.SIMULATION:
            pass  # we leave default 'format' attribute as the source for netlist spice formats

    tcl_command += f"set netlist_dir \"{str(output_netlist_path.parent)}\";"\
                   f" xschem netlist \"{output_netlist_path.name}\""

    args = [
        '-rcfile', str(rcfile_path),
        '-q',
        '-x',
        '--command', tcl_command,
        str(sch_path)
    ]

    cmd_args = ['xschem'] + args
    if verbose:
        print(f"Calling subprocess with: {' '.join(cmd_args)}")

    result = subprocess.run(cmd_args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: xschem terminated with exit code {result.returncode}")

    return result