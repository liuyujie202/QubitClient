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
from qubitclient.utils.data_parser import load_npz_file
from qubitclient.QubitSeg import QubitSegClient

import matplotlib.pyplot as plt  # 引入 matplotlib 绘图库
from qubitclient import CurveType


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
    
    # 使用文件路径，格式为str，形成list
    # response = client.request(file_list=file_path_list)

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

    result = client.get_result(response=response)
    print(result[0]["params_list"])
    print(result[0]["linepoints_list"])
    print(result[0]["confidence_list"])
    
    
    # 增加结果坐标映射
        
    frequency = dict_list[0]["frequency"] # 750
    bias = dict_list[0]["bias"] # 42
    reflection_points = client.convert_axis(result[0]["linepoints_list"][0], bias,frequency)

    plt.figure(figsize=(10, 6))
    plt.pcolormesh(dict_list[0]["bias"], dict_list[0]["frequency"],  dict_list[0]["iq_avg"], shading='auto', cmap='viridis')
    plt.colorbar(label='IQ Average')  # 添加颜色条
    reflection_points = np.array(reflection_points)
    xy_x = reflection_points[:, 0]  # 提取 x 坐标
    xy_y = reflection_points[:, 1]  # 提取 y 坐标
    plt.scatter(xy_x, xy_y, color='blue', label='XY Points', s=5, alpha=0.1)  # 绘制散点图
    # 图形设置
    plt.title(f"File: {file_name}")
    plt.xlabel("Bias")
    plt.ylabel("Frequency (GHz)")
    plt.legend()
    plt.show()
    save_path = "./tmp/client/result.png"
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(save_path)


    pass

def main():
    from config import API_URL, API_KEY

    send_npz_to_server(API_URL, API_KEY)  # 传递API密钥

if __name__ == "__main__":
    main()