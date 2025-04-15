# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/15 10:23:27
########################################################################

import cv2

def parser_result(result, images):
    result_images = []
    for i in range(len(result)):
        image = images[i]
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        input_image_reshape = (512, 512)
        image = cv2.resize(image, input_image_reshape, interpolation=cv2.INTER_NEAREST)
        
        image_result = result[i]
        linepoints_list = image_result["linepoints_list"]
        for linepoints in linepoints_list:
            for j in range(len(linepoints) - 1):
                cv2.line(image, tuple(linepoints[j]), tuple(linepoints[j + 1]), (0, 255, 0), 2)
        
        # cv2.imwrite(f"tmp/client/result_{i}.jpg", image)
        result_images.append(image)
    return result_images