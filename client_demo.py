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

from qubitclient.utils.data_parser import load_npz_to_images
from qubitclient.QubitSeg import QubitSegClient


def send_npz_to_server(url, api_key):

    dir_path = "data/1829"
    # get all file in dir
    file_names = os.listdir(dir_path)
    
    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npz'):
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    images = load_npz_to_images(file_path_list)


    client = QubitSegClient(url=url, api_key=api_key)
    response = client.request(file_path_list=file_path_list)

    result_images = client.parser_result_with_image(response=response, images=images)
    for i, image in enumerate(result_images):
        cv2.imwrite(f"tmp/client/result_{i}.jpg", image)

def main():
    from config import API_URL, API_KEY

    send_npz_to_server(API_URL, API_KEY)  # 传递API密钥

if __name__ == "__main__":
    main()