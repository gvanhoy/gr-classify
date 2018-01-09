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
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class CumulantTransformer(BaseEstimator, TransformerMixin):
    """Extract cumulant features"""

    def fit(self, x, y=None):
        return self

    def transform(self, samples):
        return [(self.cumulant_40(sample), self.cumulant_42(sample), self.cumulant_63(sample)) for sample in samples]

    def cumulant_40(self, sample):  # C_40 = mean(y^4) - 3*mean(y^2)^2
        second_term = np.multiply(sample, sample)
        first_term = np.mean(np.multiply(second_term, second_term))
        second_term = np.mean(second_term)
        return np.abs(first_term - 3 * second_term * second_term)

    def cumulant_42(self, sample):  # C_42 = mean(abs(y^4)) - abs(mean(y^2))^2 - 2*mean(abs(y^2))^2
        first_term = np.multiply(np.abs(sample), np.abs(sample))
        first_term = np.mean(np.multiply(first_term, first_term))
        second_term = np.mean(np.multiply(sample, sample))
        third_term = np.mean(np.multiply(np.abs(sample), np.abs(sample)))
        return np.abs(first_term - np.abs(second_term * second_term) - 2 * third_term * third_term)

    def cumulant_63(self, sample):
        '''
        C_63 = mean(abs(y)^6)) - 9*mean(abs(y)^4)*mean(abs(y)^2) +
        12*abs(mean(y^2))^2*mean(abs(y)^2) + 12*mean(abs(y)^2)
        :param sample:
        :return:
        '''

        abs_y = np.abs(sample)
        first_term = np.zeros((np.size(sample)))
        # mean(abs(y)^6)
        for x in range(len(first_term)):
            first_term[x] = pow(abs_y[x], 6)

        first_term = np.mean(first_term)

        # abs(y)^2
        mean_abs_y_squared = np.mean(np.multiply(abs_y, abs_y))

        # mean(abs(y)^4)
        second_term = np.mean(np.multiply(np.multiply(abs_y, abs_y), np.multiply(abs_y, abs_y)))

        # mean(y^2)
        third_term = np.mean(np.multiply(sample, sample))

        # abs(mean(y^2))^2
        third_term = np.abs(third_term)*np.abs(third_term)

        print first_term - (9*second_term + 12*third_term + 12)*mean_abs_y_squared

        return first_term - (9*second_term + 12*third_term + 12)*mean_abs_y_squared