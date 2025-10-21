# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/10/20 18:24:01
########################################################################

import os

from qubitclient import QubitScopeClient
from qubitclient import TaskName

from qubitclient.scope.utils.data_parser import load_npz_file



def send_npz_to_server(url, api_key,dir_path = "data/33137"):

    # get all file in dir
    file_names = os.listdir(dir_path)
    
    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npz'):
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    if len(file_path_list)==0:
        return
    
    client = QubitScopeClient(url="http://127.0.0.1:9000",api_key="")

    dict_list = []
    for file_path in file_path_list:
        content = load_npz_file(file_path)
        dict_list.append(content)    
    #使用从文件路径加载后的对象，格式为dict[str,np.ndarray]，多个组合成list
    # response = client.request(file_list=dict_list)
    

    # images = load_npz_to_images(file_path_list)
    # result_images = client.parser_result_with_image(response=response, images=images)
    # for i, image in enumerate(result_images):
    #     cv2.imwrite(f"./tmp/client/result_{i}.jpg", image)

    


    for index in range(len(file_path_list)):
        # 使用文件路径，格式为str，形成list
        response = client.request(file_list=[file_path_list[index]],task_type=TaskName.OPTPIPULSE)
        results = client.get_result(response=response)


def main():
    from config import API_URL, API_KEY

    base_dir = "tmp/convert"
    send_npz_to_server(API_URL, API_KEY, base_dir)


if __name__ == "__main__":
    main()