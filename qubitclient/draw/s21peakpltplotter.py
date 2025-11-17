import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter

class S21PeakDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("s21peak")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        dict_param = dict_param.item()

        image = dict_param["image"]
        q_list = image.keys()
        x_list = []
        amp_list = []
        phi_list = []
        q_name_list =[]
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            amp = image_q[1]
            phi = image_q[2]
            x_list.append((x))
            amp_list.append((amp))
            phi_list.append((phi))
            q_name_list.append(q_name)
        peaks_list = result['peaks']
        confs_list = result['confs']

        nums = len(x_list)
        row = (nums // 3) + 1 if nums % 3 != 0 else nums // 3
        col = 3

        fig = plt.figure(figsize=(20, 20))
        for i in range(len(x_list)):
            x = x_list[i]
            y1 = amp_list[i]
            y2 = phi_list[i]
            peaks = peaks_list[i]
            confs = confs_list[i]

            ax = fig.add_subplot(row, col, i + 1)
            ax.plot(x, y1, 'b-', label='Amp Curve', linewidth=2)
            ax.plot(x, y2, c='green', label='Phi Curve')
            for j in range(len(peaks)):
                ax.scatter(x[peaks[j]], y1[peaks[j]],
                color = 'red', marker = '*', s = 100,
                label = f'peak (conf: {confs[j]:.2f})',
                zorder = 5)
                ax.annotate(f'{confs[j]:.2f}',
                (x[peaks[j]], y1[peaks[j]]),
                textcoords = "offset points",
                xytext = (0, 15), ha = 'center',
                fontsize = 10, color = 'darkred',
                label = f'(final (conf: {confs[j]:.2f})')
                ax.axvline(x[peaks[j]], color="red", linestyle='--', alpha=0.8)
                ax.set_title(f'{q_name_list[i]}', fontsize=14, fontweight='bold', pad=15)
                # ax.legend()
            plt.tight_layout()



        return fig

