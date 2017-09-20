from constellation_modulator import constellation_modulator
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from python.cumulants import Cumulants
import matplotlib.pyplot as plt
import logging
import numpy as np

NUM_SAMPLES_PER_SNR = 50
SNR_RANGE = range(-5, 15, 1)


class Classifier:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.classes = [constellation_modulator('BPSK'),
                        constellation_modulator('QPSK'),
                        constellation_modulator('8PSK'),
                        constellation_modulator('16QAM')]
        self.accuracy = np.zeros((len(SNR_RANGE),), dtype=np.float32)
        self.features = np.ndarray((len(SNR_RANGE)*len(self.classes)*NUM_SAMPLES_PER_SNR, self.classes[0].get_signal_len()), dtype=np.complex64)
        self.labels = np.zeros((len(SNR_RANGE)*len(self.classes)*NUM_SAMPLES_PER_SNR,), dtype=np.int32)
        self.clf = Pipeline([
            ('cumulants', Cumulants()),
            ('SVM', SVC(kernel='linear', decision_function_shape='ovo'))
        ])
        self.generate_features()
        self.cross_validation()
        self.pcc_v_snr()
        self.save_model()

    def generate_features(self):
        for snr_index, snr in enumerate(SNR_RANGE):
            for tb_index, top_block in enumerate(self.classes):
                top_block.set_snr_db(snr)
                top_block.start()
                logging.info("Generating features for tb:{0} snr: {1}".format(tb_index, snr))
                for x in range(NUM_SAMPLES_PER_SNR):
                    old_sample = top_block.blocks_probe_signal_vx_0.level()
                    new_sample = old_sample
                    while new_sample[0] == old_sample[0]:
                        new_sample = top_block.blocks_probe_signal_vx_0.level()
                    self.features[x + tb_index*NUM_SAMPLES_PER_SNR + snr_index*len(self.classes)*NUM_SAMPLES_PER_SNR, :] = new_sample
                    self.labels[x + tb_index*NUM_SAMPLES_PER_SNR + snr_index*len(self.classes)*NUM_SAMPLES_PER_SNR] = tb_index
                top_block.stop()
        train_features, _, train_labels, _ = train_test_split(self.features, self.labels, test_size = 0.33, random_state = 42)
        self.clf.fit(train_features, train_labels)

    def pcc_v_snr(self):
        for snr_index in range(len(SNR_RANGE)):
            step = NUM_SAMPLES_PER_SNR*len(self.classes)
            y_pred = self.clf.predict(self.features[snr_index*step:(snr_index + 1)*step, :])
            self.accuracy[snr_index] = accuracy_score(self.labels[snr_index*step:(snr_index + 1)*step], y_pred)
        print self.accuracy
        plt.figure(1)
        plt.plot(SNR_RANGE,
                 100*self.accuracy,
                 color='blue',
                 linewidth=3.0,
                 linestyle='--')
        self.save_figure(1, 'Percent Correct Classification', 'pcc_v_snr')

    def cross_validation(self):
        logging.info("Cross Validation Scores: " + str(cross_val_score(self.clf, self.features, self.labels)))

    def save_figure(self, figure_number, figure_title, file_name):
        plt.figure(figure_number)
        plt.xlabel('SNR E_s/N_0(dB)', fontsize=18)
        plt.ylabel('Percent Correct Classification', fontsize=16)
        plt.xlim((min(SNR_RANGE), max(SNR_RANGE)))
        plt.ylim((0, 100))
        plt.title(figure_title)
        plt.grid(True)
        # plt.show()
        plt.savefig(file_name + '.eps', format='eps', dpi=1000)
        plt.savefig(file_name + '.png', format='png', dpi=300)
        plt.clf()

    def save_model(self):
        joblib.dump(self.clf, 'cumulant_classifier.pkl')


if __name__ == '__main__':
    main_class = Classifier()