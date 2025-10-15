import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import sys
import csv
from datetime import datetime
import json

LOG_CSV_FILE = 'execution_log.csv'
execution_counter = 0

def setup_csv():
    """CSVファイルが存在しない場合にヘッダーを書き込む"""
    if not os.path.exists(LOG_CSV_FILE):
        with open(LOG_CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['execution_count', 'timestamp', 'status', 'return_code', 'output', 'error'])

def log_to_csv(count, status, return_code, output, error):
    """実行結果をCSVに記録する"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([count, timestamp, status, return_code, output, error])

def run_controller():
    """
    controller.pyを実行し、結果をUIとCSVに記録する関数
    """
    global execution_counter
    execution_counter += 1

    # 結果表示エリアをクリア
    result_text.delete('1.0', tk.END)
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 実行回数とコマンド数を表示
        commands_path = os.path.join(script_dir, 'commands.json')
        try:
            with open(commands_path, 'r', encoding='utf-8') as f:
                commands = json.load(f)
                num_commands = len(commands)
                result_text.insert(tk.END, f"▶ {execution_counter}回目の実行: {num_commands}個のコマンドを開始します...\n")
        except FileNotFoundError:
            result_text.insert(tk.END, f"▶ {execution_counter}回目の実行: 警告: commands.json が見つかりません。\n")
        except Exception as e:
            result_text.insert(tk.END, f"▶ {execution_counter}回目の実行: 警告: commands.json の読み込みエラー: {e}\n")

        root.update_idletasks() # UIを強制的に更新

        # controller.py を実行
        controller_path = os.path.join(script_dir, 'controller.py')
        python_executable = sys.executable

        result = subprocess.run(
            [python_executable, controller_path],
            cwd=script_dir,
            capture_output=True,
            text=True,
            check=False,
            encoding='utf-8'
        )

        # 実行が完了したことを示すために、一度表示をクリア
        result_text.delete('1.0', tk.END)

        if result.returncode == 0:
            status = 'success'
            
            # stdoutから「動いている数値」に関する情報を抽出
            filtered_output = []
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if '角度' in line or '停止' in line:
                        filtered_output.append(f"  - {line.strip()}")
            
            output_content = "\n".join(filtered_output) if filtered_output else "  - done"
            
            display_output = f"▶ {execution_counter}回目の実行完了 (ステータス: 成功)\n\n詳細:\n{output_content}"
            log_to_csv(execution_counter, status, result.returncode, result.stdout, result.stderr)
        else:
            status = 'failure'
            error_details = result.stderr or 'No error output'
            display_output = f"▶ {execution_counter}回目の実行完了 (ステータス: エラー)\n\n詳細:\n{error_details}"
            log_to_csv(execution_counter, status, result.returncode, result.stdout, result.stderr)
        
        result_text.insert(tk.END, display_output)

    except Exception as e:
        error_message = f"▶ {execution_counter}回目の実行: 致命的なエラー:\n{e}"
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, error_message)
        log_to_csv(execution_counter, 'critical_failure', '', '', str(e))


# --- UIセットアップ ---
root = tk.Tk()
root.title("Controller Runner")
root.geometry("600x400")

# ボタンフレーム
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

run_button = tk.Button(button_frame, text="Run controller.py", command=run_controller)
run_button.pack()

# 結果表示フレーム
result_frame = tk.Frame(root, padx=10, pady=10)
result_frame.pack(expand=True, fill=tk.BOTH)

result_label = tk.Label(result_frame, text="実行状況:")
result_label.pack(anchor='w')

result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=15)
result_text.pack(expand=True, fill=tk.BOTH)

# --- 初期化処理 ---
setup_csv()

# --- イベントループ開始 ---
root.mainloop()
