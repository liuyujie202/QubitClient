from .pltplotter import QuantumDataPltPlotter
import matplotlib.pyplot as plt
import numpy as np
import os


class T1FitDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("t1fit")

    def plot_result_npy(self, **kwargs):
        result      = kwargs.get('result')
        data_ndarray = kwargs.get('data_ndarray')
        file_name    = kwargs.get('file_name', 'unknown')

        if not result or not data_ndarray:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data", ha='center', transform=ax.transAxes)
            return fig

        # ---------- 解析 .npy ----------
        data = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        n_qubits = len(qubit_names)
        cols = min(3, n_qubits)
        rows = (n_qubits + cols - 1) // cols

        fig = plt.figure(figsize=(5.8 * cols, 4.5 * rows))
        fig.suptitle(f"T1-Fit – {os.path.splitext(file_name)[0]}", fontsize=14, y=0.96)

        # ---------- 服务器返回 ----------
        params_list = result.get("params_list", [])   # [[A, T1, B], ...]
        r2_list     = result.get("r2_list", [])
        fit_data_list = result.get("fit_data_list", [])   # 每个 qubit 的拟合曲线

        for q_idx, q_name in enumerate(qubit_names):
            ax = fig.add_subplot(rows, cols, q_idx + 1)
            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x_raw = np.asarray(item[0])          # 时间
            y_raw = np.asarray(item[1])          # |1> 概率

            # 原始点
            ax.plot(x_raw, y_raw, 'o', color='orange', markersize=4,
                    label='Data', alpha=0.7)

            # 拟合曲线（服务器已经给出）
            if q_idx < len(fit_data_list):
                fit_y = np.asarray(fit_data_list[q_idx])
                ax.plot(x_raw, fit_y, '-', color='blue', linewidth=2,
                        label='Fit')

            # 参数文字
            if q_idx < len(params_list):
                A, T1, B = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                txt = f"A={A:.3f}\nT1={T1:.1f}µs\nB={B:.3f}\nR²={r2:.3f}"
                ax.text(0.05, 0.95, txt, transform=ax.transAxes,
                        verticalalignment='top', fontsize=8,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

            ax.set_title(q_name, fontsize=11, pad=10)
            ax.set_xlabel("Time")
            ax.set_ylabel("Amp")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(fontsize=8, loc='upper right', framealpha=0.9)

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.close(fig)
        return fig