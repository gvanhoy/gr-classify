#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Constellation Modulator
# Author: Garrett Vanhoy
# Generated: Tue Sep 19 19:27:04 2017
##################################################

from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import gr
import logging
import numpy


class constellation_modulator(gr.top_block):

    def __init__(self, modulation_string):
        gr.top_block.__init__(self, "Constellation Modulator")

        ##################################################
        # Variables
        ##################################################
        self.snr_db = snr_db = 10
        self.signal_len = signal_len = 1024
        self.samp_rate = samp_rate = 100000
        self.logger = logging.getLogger()

        if modulation_string == 'BPSK':
            self.const = digital.constellation_bpsk().base()
        elif modulation_string == 'QPSK':
            self.const = digital.constellation_qpsk().base()
        elif modulation_string == '8PSK':
            self.const = digital.constellation_8psk().base()
        elif modulation_string == '16QAM':
            self.const = digital.constellation_16qam().base()
        else:
            self.logger.warn("Got an incorrect modulation string, defaulting to BPSK.")
            self.const = digital.onstellation_bpsk().base()


        ##################################################
        # Blocks
        ##################################################
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=numpy.sqrt(10.0**(-snr_db/10.0)/2),
        	frequency_offset=0.0,
        	epsilon=1.0,
        	taps=(1.0, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, signal_len)
        self.blocks_probe_signal_vx_0 = blocks.probe_signal_vc(signal_len)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, self.const.arity(), 10000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_probe_signal_vx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.channels_channel_model_0, 0))

    def get_snr_db(self):
        return self.snr_db

    def set_snr_db(self, snr_db):
        self.snr_db = snr_db
        self.channels_channel_model_0.set_noise_voltage(numpy.sqrt(10.0**(-self.snr_db/10.0)/2))

    def get_signal_len(self):
        return self.signal_len

    def set_signal_len(self, signal_len):
        self.signal_len = signal_len

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const


def main(top_block_cls=constellation_modulator, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
