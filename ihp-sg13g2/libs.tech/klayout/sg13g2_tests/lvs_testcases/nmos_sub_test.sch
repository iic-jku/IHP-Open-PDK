v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 1 190 -390 {}
N 200 -280 200 -220 {lab=ndrain}
N 200 -160 200 -110 {lab=nsource}
N 100 -190 160 -190 {lab=ngate}
N 370 -270 370 -250 {lab=vss}
N 200 -190 260 -190 {lab=sub!}
C {iopin.sym} 370 -270 0 0 {name=p1 lab=vss}
C {ipin.sym} 100 -190 0 0 {name=p3 lab=ngate}
C {iopin.sym} 200 -280 3 0 {name=p4 lab=ndrain}
C {iopin.sym} 200 -110 1 0 {name=p5 lab=nsource}
C {sg13g2_pr/sg13_lv_nmos.sym} 180 -190 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/ptap1_ring.sym} 370 -220 2 0 {name=R1
model=ptap1
spiceprefix=X
w=2.87e-6
l=2.51e-6
rw=0.3e-6
}
C {sg13g2_pr/sub.sym} 370 -190 0 1 {name=l1 lab=sub!}
C {sg13g2_pr/sub.sym} 260 -190 0 0 {name=l2 lab=sub!}
