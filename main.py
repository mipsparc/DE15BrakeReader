#coding:utf-8

import serial

class BrakeStatus:
    ERROR_SENSOR = 'センサー読み込み失敗'
    ERROR = 'センサー異常'
    EMER = '非常'
    FIX = '固定'
    MAX_BRAKE = '全ブレーキ'
    BRAKE = 'ブレーキ帯'
    RUN = '運転'
    LOWER_BRAKE = 'ユルメ'

class BrakeReader:
    def __init__(self, device):
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.3, write_timeout=0.3, inter_byte_timeout=0.3, baudrate=9600)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            exit()
        
        self.fix_value = self.read()
        self.value = self.fix_value # 初期値は固定位置のデータにしておく
        self.status = BrakeStatus.FIX

    # intで出力する
    def read(self):
        try:
            raw_value = self.ser.readline()
            self.ser.reset_input_buffer()
            raw_value = raw_value.decode('ascii')
            raw_value = raw_value.replace('\r\n', '')
            return int(float(raw_value))
        except KeyboardInterrupt:
            exit()
        except:
            return False

    def valueToStatus(self, brake_value):
        if brake_value == False:
            return BrakeStatus.ERROR_SENSOR
        elif brake_value < 7980:
            return BrakeStatus.EMER
        elif brake_value < 8100:
            return BrakeStatus.FIX
        elif brake_value < 8260:
            return BrakeStatus.MAX_BRAKE
        elif brake_value < 9181:
            return BrakeStatus.BRAKE
        elif brake_value < 9360:
            return BrakeStatus.RUN
        elif brake_value < 9700:
            return BrakeStatus.LOWER_BRAKE
        else:
            return BrakeStatus.ERROR
        
    def main(self):
        while True:
            value = brake.read()
            self.status = brake.valueToStatus(value)
            print(value)

            print(self.status)
            if self.status == BrakeStatus.BRAKE:
                brake_level = 1 - (float(value) - 8260) / (9181 - 8260)
                print(brake_level)

brake = BrakeReader('/dev/ttyACM0')
brake.main()
