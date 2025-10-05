#!/usr/bin/env python3
import time
import json
from fake_rpi.RPi import GPIO

# --- 設定 ---
PWM_PIN    = 18      # BCM番号（物理ピン12）
FREQ       = 50      # サーボ制御用 50Hz
NEUTRAL    = 7.5     # 中立位置デューティ（%）
DC_PER_DEG = 5.0/180 # ±90°→±5%デューティを想定

# --- 初期化 ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(PWM_PIN, FREQ)
pwm.start(NEUTRAL)

def rotate(angle, speed):
    """
    angle: -90〜+90 (°)
    speed: 0〜100 (%)
    """
    duty = NEUTRAL + (angle * DC_PER_DEG) * (speed / 100.0)
    pwm.ChangeDutyCycle(duty)

def main():
    # テストコマンドを JSON 文字列で記述
    cmd_json = '{"mode":"rotate","angle":45,"speed":75}'
    cmd = json.loads(cmd_json)

    if cmd.get("mode") == "rotate":
        rotate(cmd["angle"], cmd["speed"])
        print(f"Rotate → angle={cmd['angle']}°, speed={cmd['speed']}%")
    time.sleep(3)

    # 中立に戻す
    rotate(0, 0)
    print("Stop")
    time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    finally:
        pwm.stop()
        GPIO.cleanup()