# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/15 10:31:23
########################################################################
import os
import requests
import io
import numpy as np


def file_request(file_path_list,url,api_key):
    files = []
    for file_path in file_path_list:
        if file_path.endswith('.npz'):
            file_name = os.path.basename(file_path)
            files.append(("request", (file_name, open(file_path, "rb"), "image/jpeg")))
    headers = {'Authorization': f'Bearer {api_key}'}  # 添加API密钥到请求头
    response = requests.post(url, files=files, headers=headers)
    return response

def file_request_with_dict(dict_list,url,api_key):
    files = []
    for index,dict_obj in enumerate(dict_list):
        with io.BytesIO() as buffer:
            np.savez(buffer, **dict_obj)
            bytes_obj = buffer.getvalue()
        files.append(("request", ("None"+str(index)+".npz", bytes_obj, "application/octet-stream")))
    headers = {'Authorization': f'Bearer {api_key}'}  # 添加API密钥到请求头
    response = requests.post(url, files=files, headers=headers)
    return response