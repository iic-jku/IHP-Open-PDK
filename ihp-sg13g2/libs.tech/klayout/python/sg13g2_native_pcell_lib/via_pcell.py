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

from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
import math
from typing import *

import pya


def via(name: str, 
        desc: str, 
        bottom: pya.LayerInfo, 
        cut: pya.LayerInfo, 
        top: pya.LayerInfo,
        bottom_grid: float,
        top_grid: float,
        wbmin: float,
        hbmin: float,
        wtmin: float,
        htmin: float,
        enc_bottom: float,
        enc_top: float,
        vwidth: float,
        vspace: float) -> ViaType:
    vt = pya.ViaType(name, desc)
    vt.bottom = bottom
    vt.cut = cut
    vt.top = top
    vt.bottom_grid = bottom_grid
    vt.top_grid = top_grid
    vt.wbmin = wbmin
    vt.hbmin = hbmin
    vt.wtmin = wtmin
    vt.htmin = htmin
    vt.enc_bottom = enc_bottom
    vt.enc_top = enc_top
    vt.vwidth = vwidth
    vt.vspace = vspace
    return vt


@dataclass
class PDKInfo:
    layers: List[pya.LayerInfo]
    vias: List[pya.ViaType]

    @classmethod
    def instance(cls) -> PDKInfo:
        if not hasattr(cls, '_instance'):
            layers = [
                pya.LayerInfo(1, 0, 'Activ'),
                pya.LayerInfo(5, 0, 'GatPoly'),
                pya.LayerInfo(6, 0, 'Cont'),
                pya.LayerInfo(8, 0, 'Metal1'),
                pya.LayerInfo(19, 0, 'Via1'),
                pya.LayerInfo(10, 0, 'Metal2'),
                pya.LayerInfo(29, 0, 'Via2'),
                pya.LayerInfo(30, 0, 'Metal3'),
                pya.LayerInfo(49, 0, 'Via3'),
                pya.LayerInfo(50, 0, 'Metal4'),
                pya.LayerInfo(66, 0, 'Via4'),
                pya.LayerInfo(67, 0, 'Metal5'),
                pya.LayerInfo(125, 0, 'TopVia1'),
                pya.LayerInfo(126, 0, 'TopMetal1'),
                pya.LayerInfo(133, 0, 'TopVia2'),
                pya.LayerInfo(134, 0, 'TopMetal2'),
            ]
            ld: Dict[str, pya.LayerInfo] = {l.name: l for l in layers}
        
            vias = [
                via(name='SG13G2_VIA_GATPOLY_M1', desc='Cont (over GatPoly)', bottom=ld['GatPoly'], cut=ld['Cont'], top=ld['Metal1'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.07, enc_top=0.05, vwidth=0.16, vspace=0.18),
                via(name='SG13G2_VIA_ACTIV_M1', desc='Cont (over Activ)', bottom=ld['Activ'], cut=ld['Cont'], top=ld['Metal1'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.07, enc_top=0.05, vwidth=0.16, vspace=0.18),
                via(name='SG13G2_VIA_M1_M2', desc='Via1 (Metal1→Metal2)', bottom=ld['Metal1'], cut=ld['Via1'], top=ld['Metal2'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.05, enc_top=0.05, vwidth=0.19, vspace=0.22),
                via(name='SG13G2_VIA_M2_M3', desc='Via2 (Metal2→Metal3)', bottom=ld['Metal2'], cut=ld['Via2'], top=ld['Metal3'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.05, enc_top=0.05, vwidth=0.19, vspace=0.22),
                via(name='SG13G2_VIA_M3_M4', desc='Via3 (Metal3→Metal4)', bottom=ld['Metal3'], cut=ld['Via3'], top=ld['Metal4'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.05, enc_top=0.05, vwidth=0.19, vspace=0.22),
                via(name='SG13G2_VIA_M4_M5', desc='Via4 (Metal4→Metal5)', bottom=ld['Metal4'], cut=ld['Via4'], top=ld['Metal5'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.05, enc_top=0.05, vwidth=0.19, vspace=0.22),
                via(name='SG13G2_VIA_M5_TM1', desc='TopVia1 (Metal5→TopMetal1)', bottom=ld['Metal5'], cut=ld['TopVia1'], top=ld['TopMetal1'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.10, enc_top=0.42, vwidth=0.42, vspace=0.42),
                via(name='SG13G2_VIA_TM1_TM2', desc='TopVia2 (TopMetal1→TopMetal2)', bottom=ld['TopMetal1'], cut=ld['TopVia2'], top=ld['TopMetal2'], 
                    bottom_grid=0.005, top_grid=0.005, wbmin=0.2, hbmin=0.2, wtmin=0.2, htmin=0.2,
                    enc_bottom=0.50, enc_top=0.50, vwidth=0.90, vspace=1.06),
            ]        
        
            cls._instance = PDKInfo(layers=layers, vias=vias)
        return cls._instance
    
    def layer_by_name(self, name: str) -> pya.LayerInfo:
        return [l for l in self.layers if l.name == name][0]

    @cached_property
    def via_layers(self) -> Set[pya.LayerInfo]:
        return {v.cut for v in self.vias}

    @cached_property
    def non_via_layers(self) -> List[pya.LayerInfo]:
        return [l for l in self.layers if not l in self.via_layers]
    
    @cached_property
    def layer_choices(self) -> List[Tuple[str, pya.LayerInfo]]:
        return [(l.name, l) for l in self.non_via_layers]
    
    def num_stack_steps(self, bot: pya.LayerInfo, top: pya.LayerInfo) -> int:
        bi = self.layers.index(bot)
        ti = self.layers.index(top)
        return ti - bi

    def get_vias(self, bottom: pya.LayerInfo, top: pya.LayerInfo) -> List[pya.ViaType]:
        bottom_via_found = False
        already_added_cut_layers: Set[pya.LayerInf] = set()
        vias = []
        for via in self.vias:
            if not bottom_via_found:
                if via.bottom == bottom:
                    vias.append(via)
                    already_added_cut_layers.add(via.cut)
                    bottom_via_found = True
                    
            if bottom_via_found:
                if via.cut not in already_added_cut_layers:
                    vias.append(via)
                
                if via.top == top:
                    break

        return vias


class ViaPCell(pya.PCellDeclarationHelper):
    def __init__(self):
        super().__init__()

        self.pdk_info = PDKInfo.instance()

        # Endpoints
        self.param("bottom_layer", self.TypeList, "Bottom Layer", 
                   choices=self.pdk_info.layer_choices, default=self.pdk_info.layer_by_name('Metal1'))
        self.param("top_layer",   self.TypeLayer, "Top Layer", 
                   choices=self.pdk_info.layer_choices, default=self.pdk_info.layer_by_name('Metal2'))
        
	 # Optional array override
        self.param("nx", self.TypeInt, "nx", default=0)
        self.param("ny", self.TypeInt, "ny", default=0)

        # Optional plane sizes
        self.param("w_bottom", self.TypeDouble, "Bottom width [um]",  default=0.0)
        self.param("h_bottom", self.TypeDouble, "Bottom height [um]", default=0.0)
        self.param("w_top",    self.TypeDouble, "Top width [um]",     default=0.0)
        self.param("h_top",    self.TypeDouble, "Top height [um]",    default=0.0)
    
        self.via_type_list = self.pdk_info.vias
    
    # Wire tool support
    def via_types(self): 
        return self.via_type_list
        
    def display_text_impl(self): 
        return f"SG13G2_ViaStack({self.bottom_layer.name}->{self.top_layer.name})"

    def coerce_parameters_impl(self):
        bl_idx = self.pdk_info.layers.index(self.bottom_layer)
        tl_idx = self.pdk_info.layers.index(self.top_layer)
        
        if bl_idx > tl_idx:  # swap layers if the order is wrong
            tmp = self.bottom_layer
            self.bottom_layer = self.top_layer
            self.top_layer = tmp

        error_found = False

        if not error_found and bl_idx == tl_idx:
            error_found = True
        
        if not error_found:
            match (self.bottom_layer.name, self.top_layer.name):
                case ('GatPoly', 'Activ') | ('Activ', 'GatPoly'):
                    error_found = True
                case _:
                    pass
        
        if error_found:
            self.bottom_layer = self.pdk_info.layer_by_name('Metal1')
            self.top_layer = self.pdk_info.layer_by_name('Metal2')
            
    
    def can_create_from_shape_impl(self):
        return False
        
    def parameters_from_shape_impl(self): 
        pass
        
    def transformation_from_shape_impl(self): 
        return pya.Trans()

    # Helpers
    def _min_dim_after_enc(self, a: float, b: float, da: float, db: float) -> float:
        if a < 1e-10 and b < 1e-10: return 0.0
        if a < 1e-10: return b - 2.0 * max(da, db)
        if b < 1e-10: return a - 2.0 * max(da, db)
        return min(a - 2.0 * da, b - 2.0 * db)

    def _compute_nxy(self, vias: List[pya.ViaType]) -> (int, int):
        enc_b = vias[0].enc_bottom
        enc_t = vias[-1].enc_top
        w_eff = self._min_dim_after_enc(self.w_bottom, self.w_top, enc_b, enc_t)
        h_eff = self._min_dim_after_enc(self.h_bottom, self.h_top, enc_b, enc_t)
        pitch = min(v.vwidth + v.vspace for v in vias)
        vsize = min(v.vwidth for v in vias)
        nx = self.nx if self.nx > 0 else (max(1, int(math.floor((w_eff + (pitch - vsize)) / pitch + 1e-10))) if w_eff > 0 else 1)
        ny = self.ny if self.ny > 0 else (max(1, int(math.floor((h_eff + (pitch - vsize)) / pitch + 1e-10))) if h_eff > 0 else 1)
        return nx, ny
    
    def _insert_dbox_centered(self, shapes: pya.Shapes, w: float, h: float):
        shapes.insert(pya.DBox(-0.5*w, -0.5*h, 0.5*w, 0.5*h))
    
    def produce_impl(self):
        vias = self.pdk_info.get_vias(self.bottom_layer, self.top_layer)
        if not vias: 
            return

        nx, ny = self._compute_nxy(vias)
        
        for idx, via in enumerate(vias):
            bottom_ly = self.layout.layer(via.bottom)
            top_ly    = self.layout.layer(via.top)
            cut_ly    = self.layout.layer(via.cut)

            v = via.vwidth
            s = via.vspace
            wcut = nx * v + (nx - 1) * s
            hcut = ny * v + (ny - 1) * s

            wbot = max(self.w_bottom if idx == 0 else 0.0, 2.0*via.enc_bottom + wcut)
            hbot = max(self.h_bottom if idx == 0 else 0.0, 2.0*via.enc_bottom + hcut)
            wtop = max(self.w_top    if idx == len(vias)-1 else 0.0, 2.0*via.enc_top + wcut)
            htop = max(self.h_top    if idx == len(vias)-1 else 0.0, 2.0*via.enc_top + hcut)

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
