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
from gnuradio import digital


def constellation_64qam():
    # points are separated as such
    real, imaginary = np.meshgrid(np.linspace(-7, 7, 8), np.linspace(-7, 7, 8))
    constellation_points = real + np.multiply(imaginary, 1j)
    gray_code = [
        4, 12, 28, 20, 52, 60, 44, 36,
        5, 13, 29, 21, 53, 61, 45, 37,
        7, 15, 31, 23, 55, 63, 47, 39,
        6, 14, 30, 22, 54, 62, 46, 39,
        2, 10, 26, 18, 50, 58, 42, 34,
        3, 11, 27, 19, 51, 59, 43, 35,
        1, 9, 25, 17, 49, 57, 41, 33,
        0, 8, 24, 16, 48, 56, 40, 32
    ]
    return digital.constellation_rect(
        constellation_points,
        gray_code,
        4, # rotational symmetry
        8, # real sectors
        8, # imaginary sectors
        2, # real sector width
        2  # imaginary sector width
    ).base()
