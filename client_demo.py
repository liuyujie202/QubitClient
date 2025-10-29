# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/15 10:04:35
########################################################################

import os
# import cv2
import numpy as np

# from qubitclient.utils.data_parser import load_npz_to_images
from qubitclient.nnscope.utils.data_parser import load_npz_file
from qubitclient import QubitSegClient
from qubitclient.nnscope.utils.data_convert import convert_spectrum_npy2npz,convert_spectrum_dict2npz

import matplotlib.pyplot as plt  # 引入 matplotlib 绘图库
from qubitclient import CurveType

def send_spectrum_npy_to_server(url, api_key):
    file_path = "tmp/npyfile/tmp0ffc025b.py_4905.npy"
    # Method 1. load from file_path
    dict_list, name_list = convert_spectrum_npy2npz(file_path)
    # Method 2. data has been loaded, converted from dict 
    # data = np.load(file_path, allow_pickle=True)
    # data = data.item() if isinstance(data, np.ndarray) else data
    # dict_list, name_list = convert_spectrum_dict2npz(data)


    client = QubitSegClient(url=url, api_key=api_key,curve_type=CurveType.COSINE)

    response = client.request(file_list=dict_list)
    results = client.get_result(response=response)
    plot_result(results,dict_list,name_list,index=0)


def send_npz_to_server(url, api_key):

    dir_path = "data/33137"
    # get all file in dir
    file_names = os.listdir(dir_path)
    
    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npz'):
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    


    client = QubitSegClient(url=url, api_key=api_key,curve_type=CurveType.COSINE)
    
    # Method 1. load from file_path
    # 使用文件路径，格式为str，形成list
    # response = client.request(file_list=file_path_list)

    # Method 2. data has been loaded, converted from dict 
    dict_list = []
    for file_path in file_path_list:
        content = load_npz_file(file_path)
        dict_list.append(content)    
    #使用从文件路径加载后的对象，格式为dict[str,np.ndarray]，多个组合成list
    response = client.request(file_list=dict_list)
    

    # images = load_npz_to_images(file_path_list)
    # result_images = client.parser_result_with_image(response=response, images=images)
    # for i, image in enumerate(result_images):
    #     cv2.imwrite(f"./tmp/client/result_{i}.jpg", image)

    results = client.get_result(response=response)
    plot_result(results,dict_list,file_names,index=0)


def plot_result(results,dict_list,file_names,index = 0):
    result = results[index]
    print(result["params_list"])
    print(result["linepoints_list"])
    print(result["confidence_list"])
    file_name = file_names[index]
    
    
    # 增加结果坐标映射
    # frequency = dict_list[index]["frequency"] # 750
    # bias = dict_list[index]["bias"] # 42
    # reflection_points_lst = []
    # for i in range(len(result["linepoints_list"])):
    #     reflection_points = client.convert_axis(result["linepoints_list"][i], bias,frequency)
    #     reflection_points_lst.append(reflection_points)
    # points_list = reflection_points_lst

    points_list = []
    for i in range(len(result["linepoints_list"])):
        points_list.append(result["linepoints_list"][i])

    plt.figure(figsize=(10, 6))
    plt.pcolormesh(dict_list[index]["bias"], dict_list[index]["frequency"],  dict_list[index]["iq_avg"], shading='auto', cmap='viridis')
    plt.colorbar(label='IQ Average')  # 添加颜色条
    colors = plt.cm.rainbow(np.linspace(0, 1, len(result["linepoints_list"])))
    for i in range(len(points_list)):
        reflection_points = points_list[i]
        reflection_points = np.array(reflection_points)
        xy_x = reflection_points[:, 0]  # 提取 x 坐标
        xy_y = reflection_points[:, 1]  # 提取 y 坐标
        plt.scatter(xy_x, xy_y, color=colors[i], label=f'XY Points{i}-conf:{round(result["confidence_list"][i],2)}', s=5, alpha=0.1)  # 绘制散点图
    # 图形设置
    plt.title(f"File: {file_name}")
    plt.xlabel("Bias")
    plt.ylabel("Frequency (GHz)")
    plt.legend()
    plt.show()
    save_path = "./tmp/client/result.png"
    # save_path = f"./tmp/client/result_{file_name}.png"
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(save_path)


    pass

def main():
    from config import API_URL, API_KEY

    send_npz_to_server(API_URL, API_KEY)  # 传递API密钥
    # send_spectrum_npy_to_server(API_URL, API_KEY)  # 传递API密钥

if __name__ == "__main__":
    main()