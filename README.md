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

3.  **結果を確認する (`rotation_log.csv`)**
    プログラムが動くと、モーターの動きが`rotation_log.csv`というファイルに記録されます。このファイルを開くと、いつ、どのような指示でモーターが動いたかを確認できます。

## ファイルの役割

-   `controller.py`: メインのプログラムです。このファイルを実行します。
-   `commands.json`: モーターの動きの指示を書き込む設定ファイルです。
-   `rotation_log.csv`: モーターの動きの記録が保存されるログファイルです。
-   `README.md`: このファイルです。プログラムの使い方が書かれています。

## 安全機能：非常停止ボタン

このシステムには、GPIOピン23に接続された非常停止ボタンがあります。万が一の際には、このボタンを押すことで、ただちにすべての動作を停止し、安全にプログラムを終了できます。

---

# How to Use the Servo Motor Control Program

This program simplifies controlling the movement of a servo motor. Simply write the desired movements into a file named `commands.json`, and it will move the motor accordingly while automatically saving a log of the movements.

## How to Use

1.  **Configure Movement (`commands.json`)**
    Open the `commands.json` file and describe the desired motor movements in JSON format. You can freely set the angle (`angle`) and speed (`speed`).

    **Example configuration:**
```json
[
  {
    “mode”: “rotate”,
    “angle”: 90,
    “angle_unit”: “degrees”,
    “speed”: 50,
    “speed_unit”: “%”
      },
      {
        “mode”: “rotate”,
        “angle”: 0,
        “angle_unit”: “degrees”,
        “speed”: 30,
        “speed_unit”: “%”
      }
    ]
    ```
    - `mode`: Choose either `“rotate”` or `“stop”`.
    - `angle`: Specify the motor angle between 0 and 180 degrees.
    - `speed`: Specify the motor speed as a percentage between 0 and 100.

2.  **Run the program (`controller.py`)**
    Running `controller.py` will start the motor according to the commands written in `commands.json`.

3.  **Check the results (`rotation_log.csv`)**
    When the program runs, the motor's movements are recorded in a file named `rotation_log.csv`. Opening this file allows you to see when and under what instructions the motor moved.

## File Roles

-   `controller.py`: The main program. This is the file you run.
-   `commands.json`: A configuration file where you write instructions for the motor's movements.
-   `rotation_log.csv`: The log file where motor movement records are saved.
-   `README.md`: This file. It describes how to use the program.

## Safety Feature: Emergency Stop Button

This system includes an emergency stop button connected to GPIO pin 23. In case of an emergency, pressing this button immediately stops all operations and safely terminates the program.
