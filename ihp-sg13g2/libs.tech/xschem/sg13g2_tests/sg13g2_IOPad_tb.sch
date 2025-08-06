v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Ctrl-Click to execute launcher} 1000 -1190 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 1000 -1090 0 0 0.3 0.3 {layer=11}
N 100 -930 100 -910 {lab=VDD1V5}
N 100 -930 360 -930 {lab=VDD1V5}
N 90 -1770 90 -1750 {lab=VDD3V3}
N 90 -1770 360 -1770 {lab=VDD3V3}
N 90 -1610 90 -1590 {lab=GND}
N 90 -1680 90 -1670 {lab=VSS3V3}
N 140 -2110 140 -2090 {lab=GND}
N 140 -2190 140 -2170 {lab=pad1}
N 600 -2100 750 -2100 {lab=padres1}
N 570 -2370 570 -360 {lab=VSS3V3}
N 560 -2390 560 -350 {lab=VDD3V3}
N 600 -2200 780 -2200 {lab=pad1}
N 140 -2190 350 -2190 {lab=pad1}
N 140 -1900 140 -1880 {lab=GND}
N 140 -1980 140 -1960 {lab=p2c1_pad}
N 140 -1980 360 -1980 {lab=p2c1_pad}
N 580 -2350 580 -370 {lab=VDD1V5}
N 590 -2330 590 -380 {lab=VSS1V5}
N 150 -1350 350 -1350 {lab=c2p1_pad}
N 680 -1180 680 -1160 {lab=GND}
N 680 -1260 680 -1240 {lab=c2p1}
N 600 -1260 680 -1260 {lab=c2p1}
N 200 -1560 360 -1560 {lab=VSS3V3}
N 100 -770 100 -750 {lab=GND}
N 100 -840 100 -830 {lab=VSS1V5}
N 600 -1890 750 -1890 {lab=p2c1}
N 90 -1680 200 -1680 {lab=VSS3V3}
N 90 -1690 90 -1680 {lab=VSS3V3}
N 200 -1680 200 -1560 {lab=VSS3V3}
N 190 -720 360 -720 {lab=VSS1V5}
N 190 -840 190 -720 {lab=VSS1V5}
N 100 -840 190 -840 {lab=VSS1V5}
N 100 -850 100 -840 {lab=VSS1V5}
N 150 -510 350 -510 {lab=c2p2_pad}
N 680 -340 680 -320 {lab=GND}
N 680 -420 680 -400 {lab=c2p2}
N 600 -420 680 -420 {lab=c2p2}
N 150 -300 350 -300 {lab=c2p3_pad}
N 680 -130 680 -110 {lab=GND}
N 680 -210 680 -190 {lab=c2p3}
N 600 -210 680 -210 {lab=c2p3}
N 1030 -920 1030 -900 {lab=sub!}
N 1030 -1000 1030 -980 {lab=GND}
N 990 -1000 1030 -1000 {lab=GND}
C {code_shown.sym} 975 -2015 0 0 {
name=TT_MODELS
only_toplevel=true
value="
** IHP models
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.lib cornerHBT.lib hbt_typ
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
"
spice_ignore=false
      }
C {simulator_commands_shown.sym} 985 -1705 0 0 {name=OP_TRAN
simulator=ngspice
only_toplevel=false 
value="
.param temp=27

.control

save all
op
write sg13g2_IOPad_tb.raw
set appendwrite
tran 10p 1n
write sg13g2_IOPad_tb.raw
plot VDD3V3
plot VSS3V3
plot VDD1V5
plot VSS1V5
plot pad1
plot padres1
plot p2c1
plot p2c1_pad
plot c2p1
plot c2p1_pad
plot c2p2
plot c2p2_pad
plot c2p3
plot c2p3_pad
.endc
"
}
C {devices/launcher.sym} 1060 -1120 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {vsource.sym} 90 -1720 0 0 {name=V1 value=3.3 savecurrent=false}
C {vsource.sym} 100 -880 0 0 {name=V2 value=1.5 savecurrent=false}
C {gnd.sym} 90 -1590 0 0 {name=l1 lab=GND}
C {gnd.sym} 100 -750 0 0 {name=l2 lab=GND}
C {lab_wire.sym} 580 -2350 0 1 {name=p2 sig_type=std_logic lab=VDD1V5}
C {vsource.sym} 90 -1640 0 0 {name=V3 value=-0.05 savecurrent=false}
C {gnd.sym} 140 -2090 0 0 {name=l3 lab=GND}
C {vsource.sym} 140 -2140 0 0 {name=V4 value=1.3 savecurrent=false}
C {lab_wire.sym} 610 -2100 0 1 {name=p5 sig_type=std_logic lab=padres1}
C {lab_wire.sym} 640 -2200 0 1 {name=p6 sig_type=std_logic lab=pad1}
C {launcher.sym} 1060 -1150 0 0 {name=h4
descr=SimulateNGSPICE
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults
puts $sim(spice,1,cmd) 

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,1,cmd) \{ngspice  \\"$N\\" -a\}

# change the simulator to be used (Xyce)
set sim(spice,default) 0

# run netlist and simulation
xschem netlist
simulate
"}
C {gnd.sym} 750 -2040 0 0 {name=l4 lab=GND}
C {gnd.sym} 780 -2140 0 0 {name=l5 lab=GND}
C {gnd.sym} 750 -1830 0 0 {name=l6 lab=GND}
C {gnd.sym} 140 -1880 0 0 {name=l7 lab=GND}
C {vsource.sym} 140 -1930 0 0 {name=V5 value=3.3 savecurrent=false}
C {res.sym} 750 -1860 0 0 {name=R1
value=1G
footprint=1206
device=resistor
m=1}
C {res.sym} 750 -2070 0 0 {name=R2
value=1G
footprint=1206
device=resistor
m=1}
C {res.sym} 780 -2170 0 0 {name=R3
value=1G
footprint=1206
device=resistor
m=1}
C {gnd.sym} 150 -1290 0 0 {name=l9 lab=GND}
C {res.sym} 150 -1320 0 0 {name=R4
value=1G
footprint=1206
device=resistor
m=1}
C {gnd.sym} 680 -1160 0 0 {name=l10 lab=GND}
C {vsource.sym} 680 -1210 0 0 {name=V7 value=1.5 savecurrent=false}
C {lab_wire.sym} 610 -1260 0 1 {name=p12 sig_type=std_logic lab=c2p1}
C {lab_wire.sym} 560 -2390 0 1 {name=p14 sig_type=std_logic lab=VDD3V3}
C {lab_wire.sym} 570 -2370 0 1 {name=p15 sig_type=std_logic lab=VSS3V3}
C {vsource.sym} 100 -800 0 0 {name=V9 value=0.05 savecurrent=false}
C {lab_wire.sym} 590 -2330 0 1 {name=p16 sig_type=std_logic lab=VSS1V5}
C {lab_wire.sym} 160 -1980 0 1 {name=p17 sig_type=std_logic lab=p2c1_pad}
C {lab_wire.sym} 220 -1350 0 0 {name=p20 sig_type=std_logic lab=c2p1_pad}
C {lab_wire.sym} 630 -1890 0 1 {name=p4 sig_type=std_logic lab=p2c1}
C {gnd.sym} 150 -450 0 0 {name=l13 lab=GND}
C {res.sym} 150 -480 0 0 {name=R6
value=1G
footprint=1206
device=resistor
m=1}
C {gnd.sym} 680 -320 0 0 {name=l14 lab=GND}
C {vsource.sym} 680 -370 0 0 {name=V10 value=1.5 savecurrent=false}
C {lab_wire.sym} 610 -420 0 1 {name=p1 sig_type=std_logic lab=c2p2}
C {lab_wire.sym} 220 -510 0 0 {name=p3 sig_type=std_logic lab=c2p2_pad}
C {gnd.sym} 150 -240 0 0 {name=l15 lab=GND}
C {res.sym} 150 -270 0 0 {name=R7
value=1G
footprint=1206
device=resistor
m=1}
C {gnd.sym} 680 -110 0 0 {name=l16 lab=GND}
C {vsource.sym} 680 -160 0 0 {name=V11 value=1.5 savecurrent=false}
C {lab_wire.sym} 610 -210 0 1 {name=p7 sig_type=std_logic lab=c2p3}
C {lab_wire.sym} 220 -300 0 0 {name=p8 sig_type=std_logic lab=c2p3_pad}
C {title.sym} 160 -30 0 0 {name=l17 author="Patrick Fath"}
C {code_shown.sym} 975 -1845 0 0 {
name=PAD_MODELS
only_toplevel=true
value="tcleval(
.include diodes.lib
.include $::PDK_ROOT/$::PDK/libs.ref/sg13g2_io/spice/sg13g2_io.spi
"
spice_ignore=false
      }
C {sg13g2_pr/sub.sym} 1030 -900 0 0 {name=l24 lab=sub!}
C {sg13g2_pr/ptap1.sym} 1030 -950 0 0 {name=R9
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {gnd.sym} 990 -1000 0 0 {name=l8 lab=GND}
C {sg13g2_io/sg13g2_IOPadAnalog.sym} 250 -2300 1 0 {name=x1}
C {sg13g2_io/sg13g2_IOPadIn.sym} 250 -2090 1 0 {name=x2}
C {sg13g2_io/sg13g2_IOPadIOVdd.sym} 250 -1880 1 0 {name=x3}
C {sg13g2_io/sg13g2_IOPadIOVss.sym} 250 -1670 1 0 {name=x4}
C {sg13g2_io/sg13g2_IOPadOut4mA.sym} 250 -1460 1 0 {name=x5}
C {sg13g2_io/sg13g2_IOPadVdd.sym} 250 -1040 1 0 {name=x6}
C {sg13g2_io/sg13g2_IOPadVss.sym} 250 -830 1 0 {name=x7}
C {sg13g2_io/sg13g2_IOPadOut16mA.sym} 250 -620 1 0 {name=x8}
C {sg13g2_io/sg13g2_IOPadOut30mA.sym} 250 -410 1 0 {name=x9}
