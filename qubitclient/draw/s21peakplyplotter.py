from .plyplotter import QuantumDataPlyPlotter
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class S21PeakDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("s21peak")


    def plot_result_npy(self, **kwargs):

        result_param = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        dict_param = dict_param.item()

        image = dict_param["image"]
        q_list = image.keys()
        x_list = []
        amp_list = []
        phi_list = []
        qname_list=[]
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            amp = image_q[1]
            phi = image_q[2]
            x_list.append((x))
            amp_list.append((amp))
            phi_list.append((phi))
            qname_list.append(q_name)




        peaks_list = result_param['peaks']
        confs_list = result_param['confs']

        nums = len(x_list)
        row = (nums // 3) + 1 if nums % 3 != 0 else nums // 3
        col = 3

        fig = make_subplots(
            rows=row, cols=col,
            subplot_titles=qname_list,
            vertical_spacing=0.015,
            horizontal_spacing=0.1
            # x_title="Bias",
            # y_title="Frequency (GHz)"
        )

        for i in range(len(x_list)):
            x = x_list[i]
            y1 = amp_list[i]
            y2 = phi_list[i]
            peaks = peaks_list[i]
            confs = confs_list[i]

            current_row = i // col + 1
            current_col = i % col + 1

            # 添加幅度曲线
            fig.add_trace(
                go.Scatter(x=x, y=y1, mode='lines',
                           name='Amp Curve', line=dict(color='blue', width=2)),
                row=current_row, col=current_col
            )

            # 添加相位曲线
            fig.add_trace(
                go.Scatter(x=x, y=y2, mode='lines',
                           name='Phi Curve', line=dict(color='green')),
                row=current_row, col=current_col
            )

            # 添加峰值点
            for j in range(len(peaks)):
                peak_x = x[peaks[j]]
                peak_y = y1[peaks[j]]
                conf = confs[j]

                fig.add_trace(
                    go.Scatter(x=[peak_x], y=[peak_y], mode='markers',
                               marker=dict(symbol='star', size=12, color='red')),
                               row=current_row, col=current_col
                               )

                # 添加峰值标注
                fig.add_annotation(
                    x=peak_x, y=peak_y,
                    text=f'{conf:.2f}',
                    showarrow=False,
                    ax=0, ay=-30,
                    font=dict(size=10, color='darkred'),
                    row=current_row, col=current_col
                )

                # 添加垂直线
                fig.add_vline(
                    x=peak_x, line_dash="dash",
                    line_color="red", opacity=0.8,
                    row=current_row, col=current_col
                )

                # 更新布局配置
                fig.update_layout(
                    height=500 * row,
                    width=900 * col,
                    margin=dict(r=60, t=60, b=60, l=60),
                    showlegend=False
                )

                fig.update_xaxes(
                    title_text="Bias",
                    title_font=dict(size=10),  # 缩小字体
                    title_standoff=8  # 增加标题与坐标轴的距离（单位：像素）
                )
                fig.update_yaxes(
                    title_text="Frequency (GHz)",
                    title_font=dict(size=10),
                    title_standoff=8
                )
        return fig