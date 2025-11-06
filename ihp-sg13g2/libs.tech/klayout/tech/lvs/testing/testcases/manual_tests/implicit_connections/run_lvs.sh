#!/bin/bash
# ==============================================================
# Run LVS for SP6TCClockGenerator
# ==============================================================
# This script runs the LVS check with specified layout, netlist,
# and implicit nets.
# ==============================================================

python3 ../../../../run_lvs.py \
  --layout=SP6TCClockGenerator.gds \
  --netlist=SP6TCClockGenerator.cdl \
  --implicit_nets=vdd
