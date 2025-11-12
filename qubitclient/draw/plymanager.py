
from typing import Dict, List
from .plyplotter import QuantumDataPlyPlotter
from .spectrum2dplyplotter import Spectrum2DDataPlyPlotter
from .singleshotplyplotter import SingleShotDataPlyPlotter


class QuantumPlotPlyManager:


    def __init__(self):
        self.plotters: Dict[str, QuantumDataPlyPlotter] = {}
        self.register_plotters()

    def register_plotters(self):

        self.plotters["spectrum2d"] = Spectrum2DDataPlyPlotter()
        self.plotters["singleshot"] = SingleShotDataPlyPlotter()

    def get_plotter(self, task_type: str) -> QuantumDataPlyPlotter:

        if task_type not in self.plotters:
            raise ValueError(f"未找到任务 '{task_type}' 的绘图器")
        return self.plotters[task_type]

    def list_available_tasks(self) -> List[str]:

        return list(self.plotters.keys())

    def plot_quantum_data(self, data_type: str, task_type: str,save_format: str = "html",save_name: str = "tmp0bf97fdf.py_1536",**kwargs):
        plotter = self.get_plotter(task_type)
        if data_type=='npy':
            fig = plotter.plot_result_npy(**kwargs)
        if data_type=='npz':
            fig = plotter.plot_result_npz(**kwargs)

        plotter.save_plot(fig,task_type, save_name,save_format)
