# QubitClient

#### 介绍
**qubit-client**
QubitClient 是用于使用Qubit服务的示例。

# 更新日志   

近期更新:

- **增加曲线类型**: 增加cosin类型曲线拟合(20250606).
- **构建基础项目:** 基础功能与结构构建.    


# 使用
#### 使用说明
1.拷贝config.py.example文件为config.py，并修改配置参数。
```
cp config.py.example config.py
```
2.运行
```Python
python client_demo.py
```

#### 请求输入

```python
response = client.request(file_list=dict_list)
```
dict_list格式为：
```json
[
    {
        "bias":np.ndarray shape(A),
        "frequency":np.ndarray shape(B),
        "iq_avg":np.ndarray shape(B,A),
    },
    ...
]
```


#### 返回值
返回请求为response
```python
res = response.json()
```
res格式为：
```json
{
    "state":'success',
    "result":result
}
```
其中result格式：
```json
[
    {
        "params_list":List[List[float]],//每条线段的多项式参数列表
        "linepoints_list":List[List[[row_index,col_index]]],//每条线段的点坐标列表
        "confidence_list":List[float],//每条线段的置信度
    },//每一个npz文件的结果
    {
        ...
    },
    ...
]
```


