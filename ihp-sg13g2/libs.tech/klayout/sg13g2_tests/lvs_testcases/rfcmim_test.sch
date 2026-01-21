v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 190 -390 {}
N 200 -180 200 -160 {lab=c2}
N 200 -100 200 -80 {lab=c1}
N 110 -130 170 -130 {lab=vss}
C {iopin.sym} 200 -180 3 0 {name=p4 lab=c2}
C {iopin.sym} 200 -80 1 0 {name=p5 lab=c1}
C {iopin.sym} 110 -130 2 0 {name=p1 lab=vss}
C {sg13g2_pr/cap_rfcmim.sym} 200 -130 0 0 {name=C1 
model=cap_rfcmim
w=7.0e-6
l=7.0e-6
wfeed=3.0e-6
spiceprefix=X}
