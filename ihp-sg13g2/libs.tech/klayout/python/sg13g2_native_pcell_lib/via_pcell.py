########################################################################
#
# Copyright 2024 IHP PDK Authors
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

import math
import pya


class ViaPCell(pya.PCellDeclarationHelper):
    def __init__(self):
        super().__init__()

        # Endpoints
        self.param("from_layer", self.TypeString, "From (GATPOLY, ACTIV, M1..M5, TM1, TM2)", default="M1")
        self.param("to_layer",   self.TypeString, "To   (GATPOLY, ACTIV, M1..M5, TM1, TM2)", default="M2")
		
	 # Optional array override
        self.param("nx", self.TypeInt, "nx", default=0)
        self.param("ny", self.TypeInt, "ny", default=0)

        # Optional plane sizes
        self.param("w_bottom", self.TypeDouble, "Bottom width [um]", default=0.0)
        self.param("h_bottom", self.TypeDouble, "Bottom height [um]", default=0.0)
        self.param("w_top",    self.TypeDouble, "Top width [um]",    default=0.0)
        self.param("h_top",    self.TypeDouble, "Top height [um]",   default=0.0)

        # GDS layer map
        self.lymap = {
            "ACTIV": pya.LayerInfo(1,0),
            "GATPOLY": pya.LayerInfo(5,0),
            "CONT": pya.LayerInfo(6,0),
            "M1": pya.LayerInfo(8,0),
            "V1": pya.LayerInfo(19,0),
            "M2": pya.LayerInfo(10,0),
            "V2": pya.LayerInfo(29,0),
            "M3": pya.LayerInfo(30,0),
            "V3": pya.LayerInfo(49,0),
            "M4": pya.LayerInfo(50,0),
            "V4": pya.LayerInfo(66,0),
            "M5": pya.LayerInfo(67,0),
            "TV1": pya.LayerInfo(125,0),
            "TM1": pya.LayerInfo(126,0),
            "TV2": pya.LayerInfo(133,0),
            "TM2": pya.LayerInfo(134,0),
        }

        # Per-hop rules (µm)
        self.steps = {
            ("GATPOLY","M1"): dict(cut="CONT", vwidth=0.16, vspace=0.18, bottom="GATPOLY", top="M1",  enc_bottom=0.07,  enc_top=0.05),
            ("ACTIV","M1"): dict(cut="CONT", vwidth=0.16, vspace=0.18, bottom="ACTIV", top="M1",  enc_bottom=0.07,  enc_top=0.05),
            ("M1","M2"):   dict(cut="V1",   vwidth=0.19, vspace=0.22, bottom="M1",   top="M2",  enc_bottom=0.05, enc_top=0.05),
            ("M2","M3"):   dict(cut="V2",   vwidth=0.19, vspace=0.22, bottom="M2",   top="M3",  enc_bottom=0.05, enc_top=0.05),
            ("M3","M4"):   dict(cut="V3",   vwidth=0.19, vspace=0.22, bottom="M3",   top="M4",  enc_bottom=0.05, enc_top=0.05),
            ("M4","M5"):   dict(cut="V4",   vwidth=0.19, vspace=0.22, bottom="M4",   top="M5",  enc_bottom=0.05, enc_top=0.05),
            ("M5","TM1"):  dict(cut="TV1",  vwidth=0.42, vspace=0.42, bottom="M5",   top="TM1", enc_bottom=0.10,  enc_top=0.42),
            ("TM1","TM2"): dict(cut="TV2",  vwidth=0.90, vspace=1.06, bottom="TM1",  top="TM2", enc_bottom=0.50,  enc_top=0.50),
        }

        # Wire tool via types (single-hop)
        self.via_type_list = []
        def add_vt(name, desc, bottom, cut, top, vwidth, vspace, enc_b, enc_t):
            vt = pya.ViaType(name, desc)
            vt.bottom = self.lymap[bottom]; vt.cut = self.lymap[cut]; vt.top = self.lymap[top]
            vt.bottom_grid = 0.005; vt.top_grid = 0.005
            vt.wbmin = vt.hbmin = 0.2; vt.wtmin = vt.htmin = 0.2
            vt.enc_bottom = enc_b; vt.enc_top = enc_t; vt.vwidth = vwidth; vt.vspace = vspace
            self.via_type_list.append(vt)

        add_vt("SG13G2_VIA_GATPOLY_M1","Via GATPOLY_M1","GATPOLY","CONT","M1",0.16,0.18,0.07,0.05)
        add_vt("SG13G2_VIA_ACTIV_M1","Via ACTIV_M1","ACTIV","CONT","M1",0.16,0.18,0.07,0.05)
        add_vt("SG13G2_VIA_M1_M2","Via M1_M2","M1","V1","M2",0.19,0.22,0.05,0.05)
        add_vt("SG13G2_VIA_M2_M3","Via M2_M3","M2","V2","M3",0.19,0.22,0.05,0.05)
        add_vt("SG13G2_VIA_M3_M4","Via M3_M4","M3","V3","M4",0.19,0.22,0.05,0.05)
        add_vt("SG13G2_VIA_M4_M5","Via M4_M5","M4","V4","M5",0.19,0.22,0.05,0.05)
        add_vt("SG13G2_VIA_M5_TM1","Via M5_TM1","M5","TV1","TM1",0.42,0.42,0.10,0.42)
        add_vt("SG13G2_VIA_TM1_TM2","Via TM1","TM2","TV2","TM2",0.90,1.06,0.50,0.50)

    # Wire tool support
    def via_types(self): return self.via_type_list
    def display_text_impl(self): return f"SG13G2_ViaStack({self.from_layer}->{self.to_layer})"

    def coerce_parameters_impl(self):
        alias = {
            "GATPOLY":"GATPOLY","ACTIV":"ACTIV",
            "M1":"M1","M2":"M2","M3":"M3","M4":"M4","M5":"M5","TM1":"TM1","TM2":"TM2"
        }
        fl = alias.get(self.from_layer.strip().upper(), "M1")
        tl = alias.get(self.to_layer.strip().upper(),   "M2")
        order = ["GATPOLY","ACTIV","M1","M2","M3","M4","M5","TM1","TM2"]
        if order.index(fl) >= order.index(tl):
            fl, tl = "M1", "M2"
        self.from_layer, self.to_layer = fl, tl

    def can_create_from_shape_impl(self): return False
    def parameters_from_shape_impl(self): pass
    def transformation_from_shape_impl(self): return pya.Trans()

    # Helpers
    def _min_dim_after_enc(self, a, b, da, db):
        if a < 1e-10 and b < 1e-10: return 0.0
        if a < 1e-10: return b - 2.0 * max(da, db)
        if b < 1e-10: return a - 2.0 * max(da, db)
        return min(a - 2.0 * da, b - 2.0 * db)

    def _get_stack_steps(self):
        start, end = self.from_layer, self.to_layer
        next_map = {
            "GATPOLY":"M1", "ACTIV":"M1",
            "M1":"M2", "M2":"M3", "M3":"M4", "M4":"M5",
            "M5":"TM1", "TM1":"TM2"
        }
        hops = []
        cur = start
        while cur != end:
            nxt = next_map.get(cur)
            if nxt is None: return []
            hop = self.steps.get((cur, nxt))
            if hop is None: return []
            hops.append(hop)
            cur = nxt
        return hops

    def _compute_nxy(self, hops):
        enc_b = hops[0]["enc_bottom"]; enc_t = hops[-1]["enc_top"]
        w_eff = self._min_dim_after_enc(self.w_bottom, self.w_top, enc_b, enc_t)
        h_eff = self._min_dim_after_enc(self.h_bottom, self.h_top, enc_b, enc_t)
        pitch = min(h["vwidth"] + h["vspace"] for h in hops)
        vsize = min(h["vwidth"] for h in hops)
        nx = self.nx if self.nx > 0 else (max(1, int(math.floor((w_eff + (pitch - vsize)) / pitch + 1e-10))) if w_eff > 0 else 1)
        ny = self.ny if self.ny > 0 else (max(1, int(math.floor((h_eff + (pitch - vsize)) / pitch + 1e-10))) if h_eff > 0 else 1)
        return nx, ny

    def _insert_dbox_centered(self, shapes, w, h):
        shapes.insert(pya.DBox(-0.5*w, -0.5*h, 0.5*w, 0.5*h))

    def produce_impl(self):
        hops = self._get_stack_steps()
        if not hops: return
        nx, ny = self._compute_nxy(hops)

        for idx, hop in enumerate(hops):
            bottom_ly = self.layout.layer(self.lymap[hop["bottom"]])
            top_ly    = self.layout.layer(self.lymap[hop["top"]])
            cut_ly    = self.layout.layer(self.lymap[hop["cut"]])

            v = hop["vwidth"]; s = hop["vspace"]
            wcut = nx * v + (nx - 1) * s
            hcut = ny * v + (ny - 1) * s

            wbot = max(self.w_bottom if idx == 0 else 0.0, 2.0*hop["enc_bottom"] + wcut)
            hbot = max(self.h_bottom if idx == 0 else 0.0, 2.0*hop["enc_bottom"] + hcut)
            wtop = max(self.w_top    if idx == len(hops)-1 else 0.0, 2.0*hop["enc_top"] + wcut)
            htop = max(self.h_top    if idx == len(hops)-1 else 0.0, 2.0*hop["enc_top"] + hcut)

            self._insert_dbox_centered(self.cell.shapes(bottom_ly), wbot, hbot)
            self._insert_dbox_centered(self.cell.shapes(top_ly),    wtop, htop)

            scut = self.cell.shapes(cut_ly)
            x0 = -0.5 * (nx - 1) * (v + s)
            y0 = -0.5 * (ny - 1) * (v + s)
            for ix in range(nx):
                cx = x0 + ix * (v + s)
                for iy in range(ny):
                    cy = y0 + iy * (v + s)
                    scut.insert(pya.DBox(cx - 0.5*v, cy - 0.5*v, cx + 0.5*v, cy + 0.5*v))

class SG13G2_ViaLib(pya.Library):
    def __init__(self):
        self.description = "SG13G2 Via Stack Library"
        self.layout().register_pcell("ViaStack", ViaPCell())
        self.register("SG13_ViaLib")
        self.technology = 'sg13g2'


SG13G2_ViaLib()
