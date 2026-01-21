v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 190 -390 {}
N 200 -280 200 -220 {lab=pdrain}
N 200 -160 200 -110 {lab=psource}
N 100 -190 160 -190 {lab=pgate}
N 200 -190 340 -190 {lab=#net1}
N 340 -270 340 -250 {lab=vdd}
N 340 -140 340 -130 {lab=vss}
C {iopin.sym} 340 -270 0 0 {name=p1 lab=vdd}
C {ipin.sym} 100 -190 0 0 {name=p3 lab=pgate}
C {iopin.sym} 200 -280 3 0 {name=p4 lab=pdrain}
C {iopin.sym} 200 -110 1 0 {name=p5 lab=psource}
C {sg13g2_pr/sg13_lv_pmos.sym} 180 -190 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/ntap1_ring.sym} 340 -220 0 0 {name=R1
model=ntap1
spiceprefix=X
w=3.49e-6
l=2.92e-6
rw=0.3e-6
}
C {iopin.sym} 340 -140 0 0 {name=p2 lab=vss}
C {sg13g2_pr/ptap1_ring.sym} 340 -100 0 0 {name=R2
model=ptap1
spiceprefix=X
w=7e-6
l=7e-6
rw=0.3e-6
}
C {sg13g2_pr/sub.sym} 340 -70 0 0 {name=l1 lab=sub!}
