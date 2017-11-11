#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from classify import constellations
import numpy as np


class ModulationAndCodingScheme(gr.top_block):
    def __init__(self,
                 modulation,
                 code_rate,
                 num_samples,
                 code_type="convolutional"
                 ):
        gr.top_block.__init__(self, "Modulation and Coding Scheme")

        ##################################################
        # Variables
        ##################################################
        self.modulation = modulation
        self.code_rate = code_rate
        self.num_samples = num_samples
        self.code_type = code_type
        self.enc_cc = enc_cc = fec.cc_encoder_make(2048, 7, 2, ([79, 109]), 0, fec.CC_STREAMING, False)
        self.const = digital.constellation_bpsk().base()
        self.puncpat = '11'
        self.snr_db = 10

        self.get_constellation_from_string(modulation)
        self.get_puncpat_from_string(code_rate)


        ##################################################
        # Blocks
        ##################################################
        self.fec_extended_encoder_0 = fec.extended_encoder(encoder_obj_list=enc_cc, threading='capillary', puncpat=self.puncpat)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.blocks_probe_signal_vx_0 = blocks.probe_signal_vc(self.num_samples)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, self.num_samples)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, np.random.randint(0, 256, 10000)), True)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=np.sqrt(10.0**(-self.snr_db/10.0)),
            frequency_offset=0.0,
            epsilon=1.0,
            taps=(1.0, ),
            noise_seed=0,
            block_tags=False
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.fec_extended_encoder_0, 0))
        self.connect((self.fec_extended_encoder_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_probe_signal_vx_0, 0))

    def get_num_samples(self):
        return self.num_samples

    def set_num_samples(self, num_samples):
        self.num_samples = num_samples
        self.blocks_head_0.set_length(self.num_samples)

    def get_enc_cc(self):
        return self.enc_cc

    def set_enc_cc(self, enc_cc):
        self.enc_cc = enc_cc

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def set_snr_db(self, snr_db):
        self.snr_db = snr_db
        self.channels_channel_model_0.set_noise_voltage(np.sqrt(10.0**(-self.snr_db/10.0)/2))

    def get_constellation_from_string(self, const_string):
        self.const = {
            'bpsk': digital.constellation_bpsk().base(),
            'qpsk': digital.constellation_qpsk().base(),
            '8psk': digital.constellation_8psk().base(),
            '8qam_cross': constellations.constellation_8qam_cross(),
            '16qam': digital.constellation_16qam().base(),
            '32qam_cross': constellations.constellation_32qam_cross(),
            '64qam': constellations.constellation_64qam(),
        }.get(const_string, digital.constellation_bpsk().base())

    def get_puncpat_from_string(self, code_rate_string):
        '''
            The puncpat comes from the "puncturing matrix" that is
            shown for convolutional codes on wikipedia:
            https://en.wikipedia.org/wiki/Convolutional_code
            Where a matrix: 1 0 1
                            1 1 0
            becomes puncpat: '110110'
        '''
        self.puncpat = {
            '1/2': '11',
            '2/3': '1101',
            '3/4': '110110',
            '5/6': '1101100110'
        }.get(code_rate_string, '11')
