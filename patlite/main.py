import rclpy
from rclpy.node import Node
import serial

from std_msgs.msg import Int8
import time

PWM = 0
AUTO = 1
MANUAL = 2

class PatLight(Node):

    def __init__(self):
        super().__init__('patlight')
        self.ser = serial.Serial('/dev/serial/by-id/usb-Numato_Systems_Pvt._Ltd._Numato_Lab_4_Channel_USB_Relay_Module_NLRL211027A0357-if00', 9600, timeout=None)
        self.subscription = self.create_subscription(Int8, 'mm_status', self.listener_callback, 10)
        self.status = 0
        self.flash = 0

        self.ser.write("relay off 1\n\r")
        self.ser.write("relay off 2\n\r")
        self.ser.write("relay on 0\n\r")
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def listener_callback(self, msg):
        if self.status != PWM and msg == PWM:
            self.status = PWM
            self.ser.write("relay off 1\n\r")
            self.ser.write("relay off 2\n\r")
            self.ser.write("relay on 0\n\r")
        elif self.status != AUTO and msg == AUTO:
            self.status = AUTO
            self.ser.write("relay off 0\n\r")
            self.ser.write("relay off 2\n\r")
            self.ser.write("relay on 1\n\r")
        elif self.status != MANUAL and msg == MANUAL:
            self.status = MANUAL
            self.ser.write("relay off 1\n\r")
            self.ser.write("relay off 0\n\r")
            self.ser.write("relay on 2\n\r")

    def timer_callback(self):
        if self.flash == 1:
            if self.status == PWM:
                self.ser.write("relay off 0\n\r")
                time.sleep(0.5)
                self.ser.write("relay on 0\n\r")
            elif self.status == AUTO:
                self.ser.write("relay off 1\n\r")
                time.sleep(0.5)
                self.ser.write("relay on 1\n\r")
            elif self.status == MANUAL:
                self.ser.write("relay off 2\n\r")
                time.sleep(0.5)
                self.ser.write("relay on 2\n\r")
        

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = PatLight()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
