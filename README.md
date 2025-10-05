# 追加機能定義書：回転ログ CSV 記録と非常停止ボタン

system_name: “RaspberryPi-Servo-Control-With-Logging-And-ESTOP”  
version: “0.2”  
date: “2025-10-05”

components:

- name: “Raspberry Pi 5”  
  role: “中央制御ユニット + ログ記録 + 非常停止監視”  
  language: “Python 3.x”  
  libraries:
  - RPi.GPIO # 標準インストール済み
  - csv # 標準ライブラリ
  - time # 標準ライブラリ
  - json # 標準ライブラリ

hardware_interfaces:

- name: “PWM 出力”  
  gpio_pin: 18  
  desc: “サーボアンプへの制御信号（50Hz PWM）”
- name: “非常停止ボタン入力”  
  gpio_pin: 23  
  desc: “GPIO23 に接続、GND プルダウン方式”

logging:  
 enabled: true  
 file: “rotation_log.csv”  
 fields:

- timestamp # Unix 時間秒
- angle_deg # 指令角度 (°)
- speed_pct # 指令速度 (%)
- estimated_nm # 推定トルク (Nm)

estimated_torque:  
 method: “speed_pct ÷ 100 × 最大トルク”  
 max_torque_nm: 55

emergency_stop:  
 button_gpio: 23  
 logic:

- ボタン押下 (GPIO.HIGH) で即時 pwm.stop() およびログファイルクローズ
- プログラム全体終了

command_schema:

- field: “mode”  
  type: “string”  
  description: “rotate または stop”
- field: “angle”  
  type: “integer”  
  unit: “degrees”
- field: “speed”  
  type: “integer”  
  unit: “%”

example_command:  
 format: JSON  
 content: |  
 {  
 "mode": "rotate",  
 "angle": 30,  
 "speed": 80  
 }

safety:

- “非常停止ボタン押下で全動作を即時停止”
- “ログ記録中もボタン入力を常時監視”
- “例外発生時にも GPIO.cleanup() とログファイルクローズを保証”

---

# ディレクトリ構成（更新版）

今いる dir
├── controller.py # 制御＋ CSV ログ＋非常停止機能  
├── rotation_log.csv # ログ出力ファイル（空ファイルで用意）  
└── README.md # 実行手順・回路接続図記載 ```
