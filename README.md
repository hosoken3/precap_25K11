# サーボモーター制御プログラムの使い方

このプログラムは、サーボモーターの動きをかんたんに制御するためのものです。`commands.json`というファイルに動かしたい内容を書き込むだけで、その通りにモーターを動かし、動きの記録（ログ）を自動で保存してくれます。

## 使い方

1.  **動かし方を設定する (`commands.json`)**
    `commands.json`ファイルを開き、モーターにさせたい動きをJSON形式で記述します。角度（`angle`）や速さ（`speed`）を自由に設定できます。

    **設定例:**
    ```json
    [
      {
        "mode": "rotate",
        "angle": 90,
        "angle_unit": "degrees",
        "speed": 50,
        "speed_unit": "%"
      },
      {
        "mode": "rotate",
        "angle": 0,
        "angle_unit": "degrees",
        "speed": 30,
        "speed_unit": "%"
      }
    ]
    ```
    - `mode`: `"rotate"`（回転）か`"stop"`（停止）を選びます。
    - `angle`: モーターの角度を0度から180度の間で指定します。
    - `speed`: モーターの速さを0から100の間のパーセンテージで指定します。

2.  **プログラムを実行する (`controller.py`)**
    `controller.py`を実行すると、`commands.json`に書かれた内容に従ってモーターが動き始めます。

3.  **結果を確認する (`execution_log.csv`)**
    プログラムが動くと、モーターの動きが`execution_log.csv`というファイルに記録されます。このファイルを開くと、いつ、どのような指示でモーターが動いたかを確認できます。

4.  **GUIから実行する (`UI.py`)**
    `UI.py`を実行すると、GUIウィンドウが立ち上がります。「Run controller.py」ボタンをクリックすると、`controller.py`が実行されます。
    ```bash
    python UI.py
    ```

## ファイルの役割

-   `controller.py`: メインのプログラムです。このファイルを実行します。
-   `commands.json`: モーターの動きの指示を書き込む設定ファイルです。
-   `execution_log.csv`: モーターの動きの記録が保存されるログファイルです。
-   `README.md`: このファイルです。プログラムの使い方が書かれています。

## 安全機能：非常停止ボタン

このシステムには、GPIOピン23に接続された非常停止ボタンがあります。万が一の際には、このボタンを押すことで、ただちにすべての動作を停止し、安全にプログラムを終了できます。

---

# How to Use the Servo Motor Control Program

This program makes it easy to control a servo motor. Write your desired movements into the `commands.json` file, and the motor will execute them automatically while saving a log of all actions.

## How to Use

1. **Configure Movement (`commands.json`)**  
   Open the `commands.json` file and describe the motor's movements in JSON format. Set the angle (`angle`) and speed (`speed`) as needed.

   **Example:**
[
{
"mode": "rotate",
"angle": 90,
"angle_unit": "degrees",
"speed": 50,
"speed_unit": "%"
},
{
"mode": "rotate",
"angle": 0,
"angle_unit": "degrees",
"speed": 30,
"speed_unit": "%"
}
]

text
- `mode`: `"rotate"` or `"stop"`.
- `angle`: Motor angle between 0 and 180 degrees.
- `speed`: Motor speed as a percentage (0–100).

2. **Run the program (`controller.py`)**  
Execute `controller.py` to start the motor according to the instructions in `commands.json`.

3. **Check the results (`execution_log.csv`)**  
The motor's movements are recorded in `execution_log.csv`. Open this file to see when and under what commands the motor moved.

4. **Run from GUI (`UI.py`)**  
   Execute `UI.py` to launch a GUI window. Click the "Run controller.py" button to run `controller.py`.
   ```bash
   python UI.py
   ```

## File Roles

- `controller.py`: Main program to run.
- `commands.json`: Movement instruction file.
- `execution_log.csv`: Log file of motor movements.
- `README.md`: This document.

## Safety Feature: Emergency Stop Button

An emergency stop button is connected to GPIO pin 23. Pressing it instantly stops all operations and safely terminates the program.
