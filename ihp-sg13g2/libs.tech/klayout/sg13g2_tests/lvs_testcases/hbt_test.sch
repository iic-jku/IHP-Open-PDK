v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 190 -350 {}
N 200 -190 260 -190 {lab=vss}
N 200 -160 200 -140 {lab=nemitter}
N 140 -190 160 -190 {lab=nbase}
N 200 -240 200 -220 {lab=ncollector}
C {ipin.sym} 140 -190 0 0 {name=p3 lab=nbase}
C {iopin.sym} 200 -240 3 0 {name=p4 lab=ncollector}
C {iopin.sym} 200 -140 1 0 {name=p5 lab=nemitter}
C {sg13g2_pr/npn13G2.sym} 180 -190 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1
}
C {iopin.sym} 260 -190 0 0 {name=p1 lab=vss}
