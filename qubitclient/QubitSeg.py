# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/15 10:36:23
########################################################################

import logging
import numpy as np

from qubitclient.utils.request_tool import file_request,file_request_with_dict
from qubitclient.utils.result_parser import parser_result


logging.basicConfig(level=logging.INFO)


class QubitSegClient(object):
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
    def request(self, file_list:list[str|dict[str,np.ndarray]]):
        if len(file_list)>0:
            if type(file_list[0]) == str:
                response = file_request(file_path_list=file_list,url=self.url,api_key=self.api_key)
            elif type(file_list[0]) == dict:# 多个content字典
                response = file_request_with_dict(dict_list=file_list,url=self.url,api_key=self.api_key)
            else:
                raise ValueError("file_list must be a list of str or dict")
        else:
            raise ValueError("file_list must not be empty")
        return response
    def parser_result_with_image(self,response,images):
        if response.status_code == 200:
            # logging.info("Result: %s", response.json())
            result = response.json()
            result = result["result"]
            result_images = parser_result(result=result,images=images)
            # for image in result_images:
            #     cv2.imwrite("tmp/client/test.jpg",image)
            return result_images
        else:
            logging.error("Error: %s %s", response.status_code, response.text)
            return []
    def get_result(self,response):
        if response.status_code == 200:
            # logging.info("Result: %s", response.json())
            result = response.json()
            result = result["result"]
            return result
        else:
            logging.error("Error: %s %s", response.status_code, response.text)
            return []