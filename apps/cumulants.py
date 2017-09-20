from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class Cumulants(BaseEstimator, TransformerMixin):
    """Extract cumulant_40 features"""

    def fit(self, x, y=None):
        return self

    def transform(self, samples):
        return [(self.cumulant_40(sample), self.cumulant_42(sample)) for sample in samples]

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