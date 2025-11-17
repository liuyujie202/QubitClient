from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os


class OptPiPulseDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("optpipulse")

    def plot_result_npy(self, **kwargs):
        result      = kwargs.get('result')
        data_ndarray = kwargs.get('data_ndarray')
        file_name    = kwargs.get('file_name', 'unknown')

        if not result or not data_ndarray:
            fig = go.Figure()
            fig.add_annotation(text="Missing data", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        # 解析 .npy 数据
        data = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        image_dict = data.get("image", {})
        if not isinstance(image_dict, dict) or not image_dict:
            fig = go.Figure()
            fig.add_annotation(text="No image data", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        qubit_names = list(image_dict.keys())
        n_qubits = len(qubit_names)
        cols = min(3, n_qubits)
        rows = (n_qubits + cols - 1) // cols

        # 创建子图
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f"{q}" for q in qubit_names],
            vertical_spacing=0.08,
            horizontal_spacing=0.08,
        )

        # 颜色循环
        wave_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                       '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

        # 服务器返回的共峰
        params_list = result.get("params", [])  # [[p1,p2,...], ...]
        confs_list  = result.get("confs", [])   # [[c1,c2,...], ...]

        # 图例控制标志
        wave_legend_shown = False
        peak_legend_shown = False

        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1

            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            waveforms = np.asarray(item[0])  # (n_wave, n_pts)
            x_axis    = np.asarray(item[1])  # (n_pts,)

            # --- 绘制所有波形 ---
            for w_idx, wave in enumerate(waveforms):
                show_wave_legend = (not wave_legend_shown) and (w_idx == 0)
                fig.add_trace(
                    go.Scatter(
                        x=x_axis, y=wave,
                        mode='lines',
                        line=dict(color=wave_colors[w_idx % len(wave_colors)], width=1.2),
                        name='wave',
                        legendgroup='wave',
                        showlegend=show_wave_legend
                    ),
                    row=row, col=col
                )
            if not wave_legend_shown:
                wave_legend_shown = True

            # --- 绘制共峰：垂直线 + 文字标注（x + conf）---
            if q_idx < len(params_list):
                peaks = params_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else []
                for p_idx, (peak, conf) in enumerate(zip(peaks, confs)):
                    show_peak_legend = (not peak_legend_shown) and (p_idx == 0)

                    # 垂直虚线
                    fig.add_trace(
                        go.Scatter(
                            x=[peak, peak],
                            y=[waveforms.min(), waveforms.max()],
                            mode='lines',
                            line=dict(color='red', width=2, dash='dash'),
                            name='peak',
                            legendgroup='peak',
                            showlegend=show_peak_legend
                        ),
                        row=row, col=col
                    )
                    if not peak_legend_shown:
                        peak_legend_shown = True

                    # 文字标注：x=... + conf:...
                    fig.add_trace(
                        go.Scatter(
                            x=[peak],
                            y=[waveforms.max() * 1.08],  # 略高于波形顶部
                            mode='text',
                            text=[f"x={peak:.4f}<br>conf:{conf:.3f}"],
                            textposition="top center",
                            showlegend=False,
                            textfont=dict(size=10, color="red", family="Arial")
                        ),
                        row=row, col=col
                    )

            # 坐标轴标题（仅最底行、最左列）
            if row == rows:
                fig.update_xaxes(title_text="Time", row=row, col=col)
            if col == 1:
                fig.update_yaxes(title_text="Amp", row=row, col=col)

        # 全局布局
        fig.update_layout(
            height=400 * rows,
            width=520 * cols,
            title_text=f"Opt-Pi-Pulse – {os.path.splitext(file_name)[0]}",
            title_x=0.5,
            legend=dict(
                font=dict(size=10),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="gray",
                borderwidth=1
            ),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        
        return fig