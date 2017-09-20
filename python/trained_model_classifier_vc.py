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

import numpy as np
from gnuradio import gr
import pmt
from sklearn.externals import joblib


class trained_model_classifier_vc(gr.sync_block):
    """
    docstring for block trained_model_classifier_vc
    """
    def __init__(self, vlen, trained_model_filename):
        gr.sync_block.__init__(
            self,
            name="trained_model_classifier_vc",
            in_sig=[(np.complex64, vlen)],
            out_sig=None)
        self.result_map = {
            0: 'BPSK',
            1: 'QPSK',
            2: '8PSK',
            3: '16QAM'
        }
        self.message_port_register_out(pmt.intern('classification_info'))
        self.classifier = joblib.load(trained_model_filename)
        self.vlen = vlen

    def work(self, input_items, output_items):
        in0 = input_items[0]
        for x in range(0, len(input_items), self.vlen):
            result = self.classifier.predict(in0[x:x + self.vlen])
            print result
            # self.message_port_pub(
            #     pmt.intern('classification_info'),
            #     pmt.cons(pmt.intern('modulation'), pmt.to_pmt(self.result_map[result])))

        return len(input_items[0])

