from typing import Dict, List
from .pltplotter import QuantumDataPltPlotter
from .spectrum2dpltplotter import Spectrum2DDataPltPlotter
from .s21vfluxpltplotter import S21VfluxDataPltPlotter
from .singleshotpltplotter import SingleShotDataPltPlotter
from .spectrum2dscopepltplotter import Spectrum2DScopeDataPltPlotter
from .s21peakpltplotter import S21PeakDataPltPlotter

from .optpipulsepltplotter import OptPiPulseDataPltPlotter
from .rabipltplotter import RabiDataPltPlotter
from .t1fitpltplotter import T1FitDataPltPlotter
from .t2fitpltplotter import T2FitDataPltPlotter
from .rabicospltplotter import RabiCosDataPltPlotter

class QuantumPlotPltManager:
    def __init__(self):
        self.plotters: Dict[str, QuantumDataPltPlotter] = {}
        self.register_plotters()

    def register_plotters(self):
        self.plotters["spectrum2d"] = Spectrum2DDataPltPlotter()
        self.plotters["s21vflux"] = S21VfluxDataPltPlotter()
        self.plotters["singleshot"] = SingleShotDataPltPlotter()
        self.plotters["spectrum2dscope"] = Spectrum2DScopeDataPltPlotter()
        self.plotters["optpipulse"] = OptPiPulseDataPltPlotter()
        self.plotters["rabicos"] = RabiCosDataPltPlotter()
        self.plotters["t1fit"] = T1FitDataPltPlotter()
        self.plotters["t2fit"] = T2FitDataPltPlotter()
        self.plotters["rabi"] = RabiDataPltPlotter()
        self.plotters["s21peak"] = S21PeakDataPltPlotter()

    def get_plotter(self, task_type: str) -> QuantumDataPltPlotter:
        if task_type not in self.plotters:
            raise ValueError(f"未找到任务 '{task_type}' 的绘图器")
        return self.plotters[task_type]

    def list_available_tasks(self) -> List[str]:
        return list(self.plotters.keys())

    def plot_quantum_data(self, data_type: str, task_type: str, save_format: str = "png", save_name: str = "tmp0bf97fdf.py_1536", **kwargs):
        plotter = self.get_plotter(task_type)
        if data_type=='npy':
            fig = plotter.plot_result_npy(**kwargs)
        if data_type=='npz':
            fig = plotter.plot_result_npz(**kwargs)
        plotter.save_plot(fig, task_type,save_name,save_format)
