
import time
import json
import csv
import sys
import os

# fake_rpi を RPi.GPIO としてインポート
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    from fake_rpi.RPi import GPIO

# --- 設定 ---
SERVO_PIN = 18
ESTOP_PIN = 23
LOG_FILE = 'rotation_log.csv'
MAX_TORQUE_NM = 55

# --- GPIO 初期化 ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# --- PWM 初期化 ---
# 50HzでPWMを初期化
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

# --- ログファイル初期化 ---
log_file_exists = os.path.exists(LOG_FILE)
log_file_obj = open(LOG_FILE, 'a', newline='') # 'a' (追記) モードで開く
csv_writer = csv.writer(log_file_obj)

if not log_file_exists:
    # ファイルが新規作成された場合のみヘッダーを書き込む
    csv_writer.writerow(['timestamp', 'angle_deg', 'speed_pct', 'estimated_nm'])

# --- 関数定義 ---

def angle_to_duty(angle):
    """角度をPWMデューティサイクルに変換する"""
    # 2.5 (0度) から 12.5 (180度) の範囲でマッピング
    return 2.5 + (angle / 180.0) * 10.0

def estimate_torque(speed_pct):
    """速度パーセンテージからトルクを推定する"""
    return (speed_pct / 100.0) * MAX_TORQUE_NM

def log_rotation(angle, speed):
    """回転ログをCSVに記録する"""
    timestamp = time.time()
    torque = estimate_torque(speed)
    csv_writer.writerow([timestamp, angle, speed, torque])
    log_file_obj.flush() # ファイルに即時書き込み

def emergency_stop_callback(channel):
    """非常停止ボタンのコールバック関数"""
    print("非常停止ボタンが押されました！")
    cleanup()
    sys.exit("非常停止")

def cleanup():
    """クリーンアップ処理"""
    print("クリーンアップ処理を実行します。")
    pwm.stop()
    GPIO.cleanup()
    if log_file_obj and not log_file_obj.closed:
        log_file_obj.close()

# --- 非常停止の割り込み設定 ---
GPIO.add_event_detect(ESTOP_PIN, GPIO.RISING, callback=emergency_stop_callback, bouncetime=200)


# --- メインループ ---
def main():
    try:
        print("サーボ制御プログラムを開始します。commands.jsonからコマンドを読み込みます...")
        with open('commands.json', 'r') as f:
            commands = json.load(f)

        for command in commands:
            try:
                mode = command.get('mode')
                if mode == 'rotate':
                    angle = command.get('angle', 0)
                    speed = command.get('speed', 50)

                    # 指令をログに記録
                    log_rotation(angle, speed)

                    # サーボを制御
                    duty = angle_to_duty(angle)
                    pwm.ChangeDutyCycle(duty)
                    print(f"サーボを角度 {angle} 度、速度 {speed} %で回転させます。")
                    time.sleep(2) # 次のコマンドの前に2秒待機

                elif mode == 'stop':
                    print("サーボを停止します。")
                    pwm.ChangeDutyCycle(0)
                    time.sleep(1)
                else:
                    print(f"未定義のモードです: {mode}")

            except (KeyboardInterrupt, SystemExit):
                raise # クリーンアップのために例外を再送出
            except Exception as e:
                print(f"コマンド '{command}' の実行中にエラーが発生しました: {e}")
        
        print("全てのコマンドが完了しました。")

    finally:
        cleanup()

if __name__ == '__main__':
    main()
