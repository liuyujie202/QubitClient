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
    dir_path: str = "data/t1fit",
    batch_size: int = 5,
    task_type: TaskName = TaskName.T1FIT,
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
                task_type=task_type,
            )
        except Exception as e:
            print(f"批次 [{start_idx + 1}-{end_idx}] 请求失败: {e}")
            continue

        raw_result = client.get_result(response)
        server_results = parse_server_results(raw_result)
        if not server_results:
            print(f"批次 [{start_idx + 1}-{end_idx}] 服务器返回为空，跳过")
            continue

        for local_idx, file_name in enumerate(batch_files):
            if local_idx >= len(server_results):
                print(f"[{file_name}] 服务器未返回结果，跳过绘图")
                continue

            result_item = server_results[local_idx]
            status = result_item.get("status", "unknown")

            if status == "failed":
                print(f"[{file_name}] 服务器处理失败: {result_item.get('error', '未知错误')}")
                continue
            if status != "success":
                print(f"[{file_name}] 状态异常: {status}，跳过绘图")
                continue

            #params_list 为空时直接跳过绘图
            params_list = result_item.get("params_list", [])
            if not params_list:
                print(f"[{file_name}] params_list 为空，无需绘图，跳过")
                continue

            file_path = batch_paths[local_idx]
            try:
                data_ndarray = load_npy_file(file_path)
            except Exception as e:
                print(f"[{file_name}] 加载本地数据失败: {e}")
                continue

            base_name = os.path.splitext(file_name)[0]
            save_path_prefix = f"./tmp/client/result_{task_type.value}_{base_name}"
            save_path_png  = save_path_prefix + ".png"
            save_path_html = save_path_prefix + ".html"

            try:
                # Matplotlib
                plt_manager.plot_quantum_data(
                    data_type='npy',
                    task_type=task_type.value,
                    save_path=save_path_png,
                    result=result_item,
                    data_ndarray=data_ndarray,
                    file_name=file_name
                )

                # Plotly
                ply_manager.plot_quantum_data(
                    data_type='npy',
                    task_type=task_type.value,
                    save_path=save_path_html,
                    result=result_item,
                    data_ndarray=data_ndarray,
                    file_name=file_name
                )

                print(f"{file_name} → {os.path.basename(save_path_html)} 和 {os.path.basename(save_path_png)} 已生成")
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
        dir_path="data/t1_1d_test",      
        batch_size=5,
        task_type=TaskName.T1FIT    
    )


if __name__ == "__main__":
    main()