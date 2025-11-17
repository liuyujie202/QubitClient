# src/draw/rabicospltplotter.py
from .pltplotter import QuantumDataPltPlotter
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.lines import Line2D


class RabiCosDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("rabicos")

    def plot_result_npy(self, **kwargs):
        result      = kwargs.get('result')
        data_ndarray = kwargs.get('data_ndarray')
        file_name    = kwargs.get('file_name', 'unknown')

        if not result or not data_ndarray:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data", ha='center', transform=ax.transAxes)
            plt.close(fig)
            return fig

        data = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        n_qubits = len(qubit_names)
        if n_qubits == 0:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No qubits", ha='center', transform=ax.transAxes)
            plt.close(fig)
            return fig

        cols = min(3, n_qubits)
        rows = (n_qubits + cols - 1) // cols

        fig = plt.figure(figsize=(5.8 * cols, 4.5 * rows))
        fig.suptitle(f"RabiCos Peak Detection – {os.path.splitext(file_name)[0]}", fontsize=14, y=0.96)

        peaks_list = result.get("peaks", [])
        confs_list = result.get("confs", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = fig.add_subplot(rows, cols, q_idx + 1)
            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x = np.asarray(item[0])
            y = np.asarray(item[1])

            # 绘制信号曲线
            signal_line, = ax.plot(x, y, 'b-', alpha=0.7, linewidth=1.5)

            # 手动创建图例元素（每图都有）
            legend_elements = [
                Line2D([0], [0], color='blue', lw=1.5, label='Signal'),
            ]

            # 绘制所有峰
            if q_idx < len(peaks_list):
                peaks = peaks_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else []
                for p_idx, (p, c) in enumerate(zip(peaks, confs)):
                    idx = np.argmin(np.abs(x - p))
                    ax.scatter(x[idx], y[idx], color='red', s=80, zorder=5)
                    ax.axvline(p, color='red', linestyle='--', alpha=0.8, linewidth=1.2)

                    # 标注：横坐标 + 置信度
                    ax.annotate(f"x={p:.4f}\nconf={c:.3f}",
                                (x[idx], y[idx]),
                                xytext=(8, 8), textcoords='offset points',
                                fontsize=8, color='darkred',
                                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
                                ha='left')

                    # 第一个峰才加图例（避免重复）
                    if p_idx == 0:
                        legend_elements.append(
                            Line2D([0], [0], color='red', linestyle='--', lw=1.2, label='Peak')
                        )

            # 设置坐标轴
            ax.set_title(q_name, fontsize=11, pad=10)
            ax.set_xlabel("Time (µs)")
            ax.set_ylabel("P(|1>)")
            ax.grid(True, linestyle='--', alpha=0.5)

            # 每张子图都显示图例
            ax.legend(handles=legend_elements, fontsize=8, loc='upper right', framealpha=0.9)
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.close(fig)
        return fig