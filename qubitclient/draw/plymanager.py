
from typing import Dict, List
from .plyplotter import QuantumDataPlyPlotter
from .spectrum2dplyplotter import Spectrum2DDataPlyPlotter
from .s21vfluxplyplotter import S21VfluxDataPlyPlotter
from .singleshotplyplotter import SingleShotDataPlyPlotter
from .spectrum2dscopeplyplotter import Spectrum2DScopeDataPlyPlotter


class QuantumPlotPlyManager:


    def __init__(self):
        self.plotters: Dict[str, QuantumDataPlyPlotter] = {}
        self.register_plotters()

    def register_plotters(self):

        self.plotters["spectrum2d"] = Spectrum2DDataPlyPlotter()
        self.plotters["s21vflux"] = S21VfluxDataPlyPlotter()
        self.plotters["singleshot"] = SingleShotDataPlyPlotter()
        self.plotters["spectrum2dscope"] = Spectrum2DScopeDataPlyPlotter()

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
