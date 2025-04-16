# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/15 10:04:35
########################################################################

import os
import cv2

from qubitclient.utils.data_parser import load_npz_to_images,load_npz_file
from qubitclient.QubitSeg import QubitSegClient


def send_npz_to_server(url, api_key):

    dir_path = "data/33137"
    # get all file in dir
    file_names = os.listdir(dir_path)
    
    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npz'):
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    


    client = QubitSegClient(url=url, api_key=api_key)
    
    # 使用文件路径，格式为str，形成list
    # response = client.request(file_list=file_path_list)

    dict_list = []
    for file_path in file_path_list:
        content = load_npz_file(file_path)
        dict_list.append(content)
    #使用从文件路径加载后的对象，格式为dict[str,np.ndarray]，多个组合成list
    response = client.request(file_list=dict_list)
    

    images = load_npz_to_images(file_path_list)
    result_images = client.parser_result_with_image(response=response, images=images)
    for i, image in enumerate(result_images):
        cv2.imwrite(f"./tmp/client/result_{i}.jpg", image)

    result = client.get_result(response=response)
    print(result[0]["params_list"])
    print(result[0]["linepoints_list"])
    print(result[0]["confidence_list"])
    
    
    # 增加结果坐标映射
    # TODO

def main():
    from config import API_URL, API_KEY

    send_npz_to_server(API_URL, API_KEY)  # 传递API密钥

if __name__ == "__main__":
    main()