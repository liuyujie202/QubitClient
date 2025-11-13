# -*- coding: utf-8 -*-
# tests/test_scope_opt_pipulse.py
# Author: yaqiangsun
# Created Time: 2025/11/12
"""
测试 OptPiPulse-fit 服务器接口（分批提交路径）
- 读取 ./data/opt_pipulse 目录下的 .npy 文件
- 分批发送 **文件路径**（避免一次性太多导致断开）
- 使用服务器返回的拟合结果绘图（Plotly HTML + Matplotlib PNG）
"""

import os
import sys
import json
import logging
from typing import List

# 把项目根目录加入 sys.path
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
    dir_path: str = "data/opt_pipulse",
    batch_size: int = 5,
    task_type: TaskName = TaskName.OPTPIPULSE,
):
    """
    分批提交 .npy 文件路径到服务器并绘图
    """
    file_names = [f for f in os.listdir(dir_path) if f.endswith(".npy")]
    if not file_names:
        print(f"目录 {dir_path} 中未找到 .npy 文件")
        return

    file_path_list = [os.path.join(dir_path, f) for f in file_names]
    client = QubitScopeClient(url=url, api_key=api_key)

    # 绘图管理器（一次性创建，后面复用）
    ply_manager = QuantumPlotPlyManager()
    plt_manager = QuantumPlotPltManager()

    total = len(file_names)
    for start_idx in range(0, total, batch_size):
        end_idx = min(start_idx + batch_size, total)
        batch_files = file_names[start_idx:end_idx]
        batch_paths = file_path_list[start_idx:end_idx]

        print(f"\n正在处理批次: [{start_idx + 1}-{end_idx}/{total}] 文件: {batch_files}")

        # ---------- 1. 发送请求（只传路径） ----------
        try:
            response = client.request(
                file_list=batch_paths,          # 关键：传文件路径字符串列表
                task_type=task_type,
            )
        except Exception as e:
            print(f"批次 [{start_idx + 1}-{end_idx}] 请求失败: {e}")
            continue

        # ---------- 2. 解析服务器返回 ----------
        raw_result = client.get_result(response)
        server_results = parse_server_results(raw_result)

        if not server_results:
            print(f"批次 [{start_idx + 1}-{end_idx}] 服务器返回为空，跳过")
            continue

        # ---------- 3. 逐文件绘图 ----------
        for local_idx, file_name in enumerate(batch_files):
            if local_idx >= len(server_results):
                print(f"[{file_name}] 服务器未返回结果，跳过绘图")
                continue

            result_item = server_results[local_idx]

            # ---- status 检查 ----
            status = result_item.get("status", "unknown")
            if status == "failed":
                error_msg = result_item.get("error", "未知错误")
                print(f"[{file_name}] 服务器处理失败: {error_msg}")
                continue
            if status != "success":
                print(f"[{file_name}] 状态异常: {status}，跳过绘图")
                continue

            # ---- 绘图时加载本地原始数据 ----
            file_path = batch_paths[local_idx]
            try:
                data_ndarray = load_npy_file(file_path)
            except Exception as e:
                print(f"[{file_name}] 绘图失败，加载本地数据异常: {e}")
                continue

            base_name = os.path.splitext(file_name)[0]
            save_name = f"optpipulse_{base_name}"

            try:
                # Plotly HTML
                ply_manager.plot_quantum_data(
                    data_type="npy",
                    task_type="optpipulse",     # 注意：这里是 'optpipulse'
                    save_format="html",
                    save_name=save_name,
                    results=result_item,
                    data_ndarray=data_ndarray,
                    file_name=file_name,
                )
                # Matplotlib PNG
                plt_manager.plot_quantum_data(
                    data_type="npy",
                    task_type="optpipulse",
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
    """统一解析服务器返回"""
    if isinstance(raw_result, str):
        try:
            parsed = json.loads(raw_result)
            return parsed.get("results", [])
        except json.JSONDecodeError as e:
            logging.error(f"JSON 解析失败: {e}")
            return []
    elif isinstance(raw_result, dict):
        return raw_result.get("results", [])
    else:
        return []


def main():
    from config import API_URL, API_KEY

    # 可自行修改
    base_dir = "data/opt_pipulse"      # 数据目录
    batch_size = 5                     # 每批提交数量（路径模式下可设更大）
    task_type = TaskName.OPTPIPULSE    # OptPiPulse 任务

    batch_send_npy_to_server(
        url=API_URL,
        api_key=API_KEY,
        dir_path=base_dir,
        batch_size=batch_size,
        task_type=task_type,
    )


if __name__ == "__main__":
    main()