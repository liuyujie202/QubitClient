# RABI 任务接口文档

## 概述

RABI 是 Scope 中的一个任务，用于对量子比特的进行 **指数衰减 + 余弦振荡** 拟合，返回每个量子比特的拟合参数、拟合曲线、R² 拟合优度及处理状态

$$
y = A \cdot e^{-x / T1} \cdot \cos(2\pi w x + \phi) + B
$$

---

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient, TaskName

client = QubitScopeClient(url="http://your-server-address:port", api_key="your-api-key")
```

### 请求参数

| 参数名      | 类型                                      | 必需 | 描述                                                                 |
|-------------|-------------------------------------------|------|----------------------------------------------------------------------|
| `file_list` | `list[str \| dict[str, np.ndarray]]`      | 是   | 数据文件列表，支持 `.npy` 文件路径或 `numpy` 数组                     |
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.RABI`                                    |                             |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [x_array, amp_array],   
            "Q1": [x_array, amp_array],
            ...
        }
    }
    ```

    x_array: 一维 np.ndarray，表示时间点
    amp_array: 一维 np.ndarray，表示信号强度
    每个量子比特对应一个键（如 "Q0"），值为 [x, amp] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/rabi/file1.npy", "data/rabi/file2.npy"],
    task_type=TaskName.RABI
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.RABI
)
```

### 获取结果

```python
results = client.get_result(response=response)
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "t2fit",
  "results": [
    {
      "params_list": [[A, B, T1, T2, w, phi], ...],
      "r2_list": [float, ...],
      "fit_data_list": [[float, ...], ...],
      "status": "success" | "failed"
    },
    ...
  ]
}
```

params_list[i]: 第 i 个量子比特的拟合参数 [A, B, T1, T2, w, phi]
fit_data_list[i]: 第 i 个量子比特在 密集时间点 上的拟合值（用于绘制平滑曲线）
r2_list[i]: 第 i 个量子比特的 R² 拟合优度

### 字段说明

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `params_list`    | `List[List[float]]`    | 每个量子比特的拟合参数 `[A, B, T1, w, phi]`：<br>• `A`: 初始振幅<br>• `B`: 基线偏移<br>• `T1`: 指数衰减时间（µs）<br>• `w`: 振荡角频率（rad/s）<br>• `phi`: 初始相位（rad） |
| `r2_list`        | `List[float]`          | 每个量子比特的 R² 拟合优度，范围 `[0, 1]`，越接近 1 拟合越好 |
| `fit_data_list`  | `List[List[float]]`    | 每个量子比特的拟合曲线值 |
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "rabi",
  "results": [
    {
      "params_list": [
        [0.4220602571148976, 0.6782053429458166, 1021.6257020164796,
         46142276.9097151, 1.075826496551695]
      ],
      "r2_list": [0.9279673627766446],
      "fit_data_list": [
        [0.8786861186854626, 0.7349471964772133, 0.5839287562931449, ...]
      ],
      "status": "success"
    }
  ]
}
```

注意：fit_data_list 中的拟合点对应更密集的时间序列（非原始 x），绘图时需使用 np.linspace(x_min, x_max, len(fit_data)) 生成对应 x_fit。

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

# 使用Plotly绘制（HTML）
plot_manager = QuantumPlotPlyManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type='rabi',
    save_format="html",
    save_name="rabi_result",
    results=results,
    data_ndarray=data_ndarray,
    file_name="example.npy"
)

# 使用Matplotlib绘制（PNG）
plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type='rabi',
    save_format="png",
    save_name="rabi_result",
    results=results,
    data_ndarray=data_ndarray,
    file_name="example.npy"
)
```