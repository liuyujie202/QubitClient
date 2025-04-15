# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/15 10:36:23
########################################################################

import logging

from qubitclient.utils.request_tool import request
from qubitclient.utils.result_parser import parser_result


logging.basicConfig(level=logging.INFO)


class QubitSegClient(object):
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
    def request(self, file_path_list):
        response = request(file_path_list=file_path_list,url=self.url,api_key=self.api_key)
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