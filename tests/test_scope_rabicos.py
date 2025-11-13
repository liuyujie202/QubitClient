# -*- coding: utf-8 -*-
# tests/test_scope_rabicos.py
# Author: yaqiangsun
# Created Time: 2025/11/13
"""
测试 RabiCos 峰值检测服务器接口（分批提交路径）
- 读取 ./data/rabicos 目录下的 .npy 文件
- 分批发送文件路径
- 使用服务器返回的 peaks/confs 绘图（Plotly HTML + Matplotlib PNG）
"""

import os
import sys
import json
import logging
from typing import List

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitScopeClient, TaskName
from qubitclient.scope.utils.data_parser import load_npy_file
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager


def batch_send_npy_to_server(
    url: str,
    api_key: str,
    dir_path: str = "data/rabicos",
    batch_size: int = 5,
):
    file_names = [f for f in os.listdir(dir_path) if f.endswith(".npy")]
    if not file_names:
        print(f"目录 {dir_path} 中未找到 .npy 文件")
        return

    file_path_list = [os.path.join(dir_path, f) for f in file_names]
    client = QubitScopeClient(url=url, api_key=api_key)

    ply_manager = QuantumPlotPlyManager()
    plt_manager = QuantumPlotPltManager()

    total = len(file_names)
    for start_idx in range(0, total, batch_size):
        end_idx = min(start_idx + batch_size, total)
        batch_files = file_names[start_idx:end_idx]
        batch_paths = file_path_list[start_idx:end_idx]

        print(f"\n正在处理批次: [{start_idx + 1}-{end_idx}/{total}] 文件: {batch_files}")

        try:
            response = client.request(
                file_list=batch_paths,
                task_type=TaskName.RABICOS,  # 关键
            )
        except Exception as e:
            print(f"批次请求失败: {e}")
            continue

        raw_result = client.get_result(response)
        server_results = parse_server_results(raw_result)
        if not server_results:
            print(f"批次返回为空，跳过")
            continue

        for local_idx, file_name in enumerate(batch_files):
            if local_idx >= len(server_results):
                print(f"[{file_name}] 无结果，跳过")
                continue

            result_item = server_results[local_idx]
            status = result_item.get("status", "unknown")

            if status == "failed":
                print(f"[{file_name}] 服务器失败: {result_item.get('error')}")
                continue
            if status != "success":
                print(f"[{file_name}] 状态异常: {status}")
                continue

            # 加载本地原始数据用于绘图
            try:
                data_ndarray = load_npy_file(batch_paths[local_idx])
            except Exception as e:
                print(f"[{file_name}] 加载失败: {e}")
                continue

            base_name = os.path.splitext(file_name)[0]
            save_name = f"rabicos_{base_name}"

            try:
                ply_manager.plot_quantum_data(
                    data_type="npy",
                    task_type="rabicos",
                    save_format="html",
                    save_name=save_name,
                    results=result_item,
                    data_ndarray=data_ndarray,
                    file_name=file_name,
                )
                plt_manager.plot_quantum_data(
                    data_type="npy",
                    task_type="rabicos",
                    save_format="png",
                    save_name=save_name,
                    results=result_item,
                    data_ndarray=data_ndarray,
                    file_name=file_name,
                )
                print(f"{file_name} → result_{save_name}.html/png 已生成")
            except Exception as e:
                print(f"[{file_name}] 绘图异常: {e}")

    print(f"\n所有批次处理完成，共 {total} 个文件。")


def parse_server_results(raw_result) -> List[dict]:
    if isinstance(raw_result, str):
        try:
            return json.loads(raw_result).get("results", [])
        except json.JSONDecodeError as e:
            logging.error(f"JSON 解析失败: {e}")
            return []
    elif isinstance(raw_result, dict):
        return raw_result.get("results", [])
    return []


def main():
    from config import API_URL, API_KEY
    batch_send_npy_to_server(
        url=API_URL,
        api_key=API_KEY,
        dir_path="./data/rabi_in_group",
        batch_size=5,
    )


if __name__ == "__main__":
    main()