# Naming conventions

Since the schematic contains `sg13g2_pr/` string in the instance reference 
we use symbolic links to ensure schematic portability between G2 and CMOS5L.

In the `xschemrc` file the global variable were change for the same reason. 

SG13G2_MODELS -> MODELS_NGSPICE
SG13G2_MODELS_XYCE -> MODELS_XYCE

same for SG13CMOS5L

# IO pad symbols (sg13cmos5l_io)

The IO pad cells are renamed in CMOS5L (`sg13g2_IOPadIn` -> `sg13cmos5l_IOPadIn`,
see `libs.ref/sg13cmos5l_io`). The symbols in `sg13cmos5l_io/` are therefore
*renamed* symbolic links to the G2 symbols in `ihp-sg13g2/libs.tech/xschem/sg13g2_io/`:
the drawing and pins are shared with G2, while xschem derives the netlisted
subcircuit name (`@symname`) from the local file name, which matches the
subcircuits in `libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spi`.

The corresponding testbench `tests/sg13cmos5l_IOPad_tb.sch` is a local copy of
the G2 `sg13g2_tests/sg13g2_IOPad_tb.sch` adapted to the CMOS5L cell names and
model paths (no HBT corner lib, since CMOS5L has no HBT devices).
