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

__version__ = '$Revision: #1 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *
import math


class cap_mfringe(DloGen):
    """Interdigitated metal fringe capacitor PCell.

    Generates a capacitor by interdigitating metal fingers across M1..M4.
    Finger orientation alternates between metal layers. Connected via
    stacks join fingers on alternating sides to form two terminals (c1, c2).

    Ported from the Magic generator (ihp-sg13cmos5l-cap.tcl, PR #31).
    """

    # Metal layer names indexed 1..4
    METAL_NAMES = {1: 'Metal1', 2: 'Metal2', 3: 'Metal3', 4: 'Metal4'}
    VIA_NAMES   = {1: 'Via1',   2: 'Via2',   3: 'Via3'}

    # Design rules per metal layer (from SG13CMOS5L DRM)
    # M1.a = 0.16, M1.b = 0.18; Mn.a = 0.20, Mn.b = 0.21
    METAL_RULES = {
        1: {'mw': 0.16, 'ms': 0.18, 'widem': 0.30, 'extras': 0.04},
        2: {'mw': 0.20, 'ms': 0.21, 'widem': 0.39, 'extras': 0.03},
        3: {'mw': 0.20, 'ms': 0.21, 'widem': 0.39, 'extras': 0.03},
        4: {'mw': 0.20, 'ms': 0.21, 'widem': 0.39, 'extras': 0.03},
    }

    # Via rules (from SG13CMOS5L DRM)
    # V1.a = Vn.a = 0.19 (min AND max -- square vias only)
    # V1.b = Vn.b = 0.22 (min spacing)
    # V1.c = 0.01 (Metal1 enclosure of Via1)
    # Mn.c = 0.005 (Metal(n) enclosure of Via(n-1))
    VIA_CUT = 0.19          # via cut size (square)
    VIA_SPACING = 0.22      # via minimum edge-to-edge spacing
    VIA_WIDTH = 0.20        # metal-enclosed via width for edge sizing (VIA_CUT + 2*Mn.c)
    VIA1_BOT_ENC = 0.005    # extra M1 enclosure beyond standard (V1.c - Mn.c)

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()
#ifdef KLAYOUT
        specs('model', 'cap_mfringe', 'Model name')
        specs('w', '2.0u', 'Width', RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '2.0u', 'Length', RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 4=M4)',
              ChoiceConstraint([1, 2, 3, 4]))
        specs('mmax', 4, 'Top metal (1=M1 .. 4=M4)',
              ChoiceConstraint([1, 2, 3, 4]))
        specs('subblock', 0, 'Add substrate isolation block',
              ChoiceConstraint([0, 1]))
#else
        specs('model', 'cap_mfringe', 'Model name')
        specs('w', '2.0u', 'Width', RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '2.0u', 'Length', RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 4=M4)',
              ChoiceConstraint([1, 2, 3, 4]))
        specs('mmax', 4, 'Top metal (1=M1 .. 4=M4)',
              ChoiceConstraint([1, 2, 3, 4]))
        specs('subblock', 0, 'Add substrate isolation block',
              ChoiceConstraint([0, 1]))
#endif

    def setupParams(self, params):
        self.params = params
        self.w_um = Numeric(params['w']) * 1e6      # width in microns
        self.l_um = Numeric(params['l']) * 1e6      # length in microns
        self.mmin = int(params['mmin'])
        self.mmax = int(params['mmax'])
        self.subblock = int(params['subblock'])

        # Enforce mmax >= mmin
        if self.mmax < self.mmin:
            self.mmax = self.mmin

    def _paint_via_array(self, via_layer, llx, lly, urx, ury):
        """Paint an array of square vias within the given bounding box.

        Vias are VIA_CUT x VIA_CUT squares at VIA_SPACING edge-to-edge.
        The array is centered within the region.
        """
        via_cut = self.VIA_CUT
        via_pitch = via_cut + self.VIA_SPACING
        region_w = urx - llx
        region_h = ury - lly
        if region_w < via_cut or region_h < via_cut:
            return
        nx = max(1, int((region_w - via_cut) / via_pitch) + 1)
        ny = max(1, int((region_h - via_cut) / via_pitch) + 1)
        array_w = (nx - 1) * via_pitch + via_cut
        array_h = (ny - 1) * via_pitch + via_cut
        x0 = llx + (region_w - array_w) / 2.0
        y0 = lly + (region_h - array_h) / 2.0
        for i in range(nx):
            for j in range(ny):
                vx = GridFix(x0 + i * via_pitch)
                vy = GridFix(y0 + j * via_pitch)
                dbCreateRect(self, via_layer,
                             Box(vx, vy, GridFix(vx + via_cut),
                                 GridFix(vy + via_cut)))

    def genLayout(self):
        w = self.w_um
        l = self.l_um
        mmin = self.mmin
        mmax = self.mmax

        # Layer objects
        metal_layers = {}
        for m in range(mmin, mmax + 1):
            metal_layers[m] = Layer(self.METAL_NAMES[m], 'drawing')

        via_layers = {}
        for v in range(mmin, mmax):
            via_layers[v] = Layer(self.VIA_NAMES[v], 'drawing')

        recog_layer = Layer('Recog', 'mom')     # GDS 99/39
        text_layer = Layer('TEXT', 'drawing')

        # Track edge sizes from previous layer for via placement
        last_edge = {'l': 0, 'r': 0, 't': 0, 'b': 0}

        orient = 0  # 0 = vertical fingers, 1 = horizontal fingers
        for m in range(mmin, mmax + 1):
            rules = self.METAL_RULES[m]
            mw = rules['mw']
            ms = rules['ms']
            widem = rules['widem']
            extras = rules['extras']

            viabe = self.VIA1_BOT_ENC if m == 1 else 0.0

            # Extra spacing adjustments for run-length rules
            msxl = msxr = msxt = msxb = 0.0

            # Via parameters for the layer below
            viaw1 = self.VIA_WIDTH
            viabe1 = self.VIA1_BOT_ENC if m == 2 else 0.0
            viate1 = 0.0

            pitch = mw + ms
            viaw = self.VIA_WIDTH

            # -- Determine edge widths --
            if m == 1:
                edge_base = mw
                if mmax >= 2:
                    edge_base = viaw + 2 * viabe
                edgel = edger = edget = edgeb = edge_base
            elif m == 2:
                edge_base = viaw
                if mmin == 1:
                    edge_base = mw + viabe1
                edgel = edger = edget = edgeb = edge_base
            else:
                edgel = edger = edget = edgeb = viaw

            # -- Compute finger count and distribute remainder --
            if orient == 0:     # Vertical fingers
                wbase = edgel + edger
                nfxi = int((w - (wbase + ms)) / pitch)
                xdelta = (w - (nfxi * pitch + ms + wbase)) / 2.0
                edgel += xdelta
                edger += xdelta

                if edgel > widem:
                    msxl = extras
                    edgel -= msxl
                if edger > widem:
                    msxr = extras
                    edger -= msxr
            else:               # Horizontal fingers
                lbase = edget + edgeb
                nfyi = int((l - (lbase + ms)) / pitch)
                ydelta = (l - (nfyi * pitch + ms + lbase)) / 2.0
                edget += ydelta
                edgeb += ydelta

                if edget > widem:
                    msxt = extras
                    edget -= msxt
                if edgeb > widem:
                    msxb = extras
                    edgeb -= msxb

            # -- Paint vias to layer below --
            if m > mmin:
                maxel = max(edgel, last_edge['l'])
                maxer = max(edger, last_edge['r'])
                maxeb = max(edgeb, last_edge['b'])
                maxet = max(edget, last_edge['t'])
                via_lyr = via_layers[m - 1]

                # Bottom via region
                vb_llx = GridFix(maxel + pitch)
                vb_urx = GridFix(w - (maxer + pitch))
                vb_lly = GridFix(viabe1)
                vb_ury = GridFix(vb_lly + viaw1)
                if vb_urx > vb_llx:
                    self._paint_via_array(via_lyr,
                                         vb_llx, vb_lly, vb_urx, vb_ury)

                # Left via region
                vl_lly = GridFix(maxeb + ms)
                vl_ury = GridFix(l - (maxet + pitch))
                vl_llx = GridFix(viabe1 + viate1)
                vl_urx = GridFix(vl_llx + viaw1)
                if vl_ury - vl_lly < viaw1:
                    vl_ury = GridFix(vl_lly + viaw1)
                if vl_ury > vl_lly:
                    self._paint_via_array(via_lyr,
                                         vl_llx, vl_lly, vl_urx, vl_ury)

                # Right via region
                vr_lly = GridFix(maxeb + pitch)
                vr_ury = GridFix(l - (maxet + ms))
                vr_urx = GridFix(w - viabe1)
                vr_llx = GridFix(vr_urx - viaw1)
                if vr_ury > vr_lly:
                    self._paint_via_array(via_lyr,
                                         vr_llx, vr_lly, vr_urx, vr_ury)

                # Top via region
                vt_ury = GridFix(l - (viabe1 + viate1))
                vt_lly = GridFix(vt_ury - viaw1)
                vt_llx = GridFix(maxel + pitch)
                vt_urx = GridFix(w - (maxer + ms))
                if vt_urx - vt_llx < viaw1:
                    vt_urx = GridFix(vt_llx + viaw1)
                if vt_urx > vt_llx:
                    self._paint_via_array(via_lyr,
                                         vt_llx, vt_lly, vt_urx, vt_ury)

            # -- Paint metal fingers --
            met = metal_layers[m]

            if orient == 0:     # Vertical fingers
                # Left edge (full height)
                dbCreateRect(self, met, Box(0, 0, GridFix(edgel), l))

                # Interior fingers
                for x in range(int(nfxi)):
                    f_llx = GridFix(x * pitch + edgel + msxl + ms)
                    f_urx = GridFix(f_llx + mw)
                    f_lly = 0.0
                    f_ury = l

                    if x % 2 == 0:
                        # Shorten from top (connect to bottom/left = c1)
                        inset = edget + ms + msxt + viabe1
                        f_ury = GridFix(l - inset)
                    else:
                        # Shorten from bottom (connect to top/right = c2)
                        inset = edgeb + ms + msxb + viabe1
                        f_lly = GridFix(inset)

                    dbCreateRect(self, met,
                                 Box(f_llx, f_lly, f_urx, f_ury))

                # Right edge (full height)
                re_llx = GridFix(nfxi * pitch + edgel + msxl + msxr + ms)
                dbCreateRect(self, met, Box(re_llx, 0, GridFix(w), l))

                # Bottom connecting bar (c1 side)
                bb_urx = GridFix(w - (edger + ms + msxr))
                dbCreateRect(self, met,
                             Box(0, 0, bb_urx, GridFix(edgeb)))

                # Top connecting bar (c2 side)
                tb_llx = GridFix(edgel + ms + msxl)
                dbCreateRect(self, met,
                             Box(tb_llx, GridFix(l - edget), GridFix(w), l))

            else:               # Horizontal fingers
                # Bottom edge (full width)
                dbCreateRect(self, met,
                             Box(0, 0, w, GridFix(edgeb)))

                # Interior fingers
                for y in range(int(nfyi)):
                    f_llx = 0.0
                    f_urx = w
                    f_lly = GridFix(y * pitch + edgeb + ms + msxb)
                    f_ury = GridFix(f_lly + mw)

                    if y % 2 == 0:
                        # Shorten from left (connect to right = c2)
                        inset = edgel + ms + msxl + viabe1
                        f_llx = GridFix(inset)
                    else:
                        # Shorten from right (connect to left = c1)
                        inset = edger + ms + msxr + viabe1
                        f_urx = GridFix(w - inset)

                    dbCreateRect(self, met,
                                 Box(f_llx, f_lly, f_urx, f_ury))

                # Top edge (full width)
                te_lly = GridFix(nfyi * pitch + edgeb + ms + msxb + msxt)
                dbCreateRect(self, met, Box(0, te_lly, w, l))

                # Left connecting bar (c1 side)
                lb_ury = GridFix(l - (edget + ms + msxt))
                dbCreateRect(self, met,
                             Box(0, 0, GridFix(edgel), lb_ury))

                # Right connecting bar (c2 side)
                rb_lly = GridFix(edgeb + ms + msxb)
                dbCreateRect(self, met,
                             Box(GridFix(w - edger), rb_lly, w, l))

            # Save edge sizes for next layer's via placement
            last_edge = {'l': edgel, 'r': edger, 't': edget, 'b': edgeb}

            # Alternate orientation for next layer
            orient = 1 - orient

        # -- Recognition marker --
        dbCreateRect(self, recog_layer, Box(0, 0, GridFix(w), GridFix(l)))

        # -- Substrate isolation block --
        if self.subblock:
            pwb_layer = Layer('PWell', 'block')
            dbCreateRect(self, pwb_layer, Box(0, 0, GridFix(w), GridFix(l)))

        # -- Pins on top metal --
        top_metal_name = self.METAL_NAMES[mmax]
        # c1 pin: left side of device
        c1_box = Box(0, GridFix(l / 2.0 - 0.1),
                     GridFix(0.2), GridFix(l / 2.0 + 0.1))
        MkPin(self, 'c1', 1, c1_box, top_metal_name)

        # c2 pin: top side of device
        c2_box = Box(GridFix(w / 2.0 - 0.1), GridFix(l - 0.2),
                     GridFix(w / 2.0 + 0.1), GridFix(l))
        MkPin(self, 'c2', 2, c2_box, top_metal_name)

        # LVS terminal identification:
        # The MkPin shapes on the metal pin layer are used by the LVS extractor
        # to identify c1 (left side, lower x) and c2 (top side, higher y).

        # -- Capacitance label --
        areacap = 0.67 if mmin == 1 else 0.55
        areacap += (mmax - mmin) * 0.55
        cval = areacap * w * l
        label_text = 'cap_mfringe C={:.3f}fF'.format(cval)
        dbCreateLabel(self, text_layer, Point(0, GridFix(-0.5)),
                      label_text, 'centerLeft', 'R0',
                      Font.EURO_STYLE, 0.25)
