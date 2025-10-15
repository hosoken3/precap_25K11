import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

def run_controller():
    """
    controller.pyを実行する関数
    """
    try:
        # UI.py があるディレクトリを取得
        script_dir = os.path.dirname(os.path.abspath(__file__))
        controller_path = os.path.join(script_dir, 'controller.py')
        
        # 実行するPythonのパスを特定 (UI.pyを実行しているPythonと同じものを使用)
        python_executable = sys.executable

        # controller.py を、そのファイルがあるディレクトリを作業ディレクトリとして実行
        result = subprocess.run(
            [python_executable, controller_path],
            cwd=script_dir,
            capture_output=True,
            text=True,
            check=False  # check=Trueにすると0以外の終了コードで例外が発生する
        )

        # 実行結果をチェック
        if result.returncode == 0:
            # 成功した場合、標準出力を表示 (任意)
            output = result.stdout if result.stdout else "実行が完了しました。"
            messagebox.showinfo("成功", output)
        else:
            # エラーが発生した場合、標準エラー出力を表示
            error_message = f"エラーが発生しました。\n\n終了コード: {result.returncode}\n\nエラー出力:\n{result.stderr}"
            messagebox.showerror("エラー", error_message)

    except Exception as e:
        messagebox.showerror("実行エラー", f"controller.pyの実行中に予期せぬエラーが発生しました:\n{e}")


# メインウィンドウの作成
root = tk.Tk()
root.title("Controller Runner")

# ボタンの作成
run_button = tk.Button(root, text="Run controller.py", command=run_controller)
run_button.pack(pady=20, padx=50)

# イベントループの開始
root.mainloop()
