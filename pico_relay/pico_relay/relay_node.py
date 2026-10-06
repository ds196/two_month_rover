import rclpy
from rclpy.node import Node

import serial
import serial.tools.list_ports
import sys
import threading
import glob

from std_msgs.msg import String

KNOWN_USBS = [
    (0x2E8A, 0x00C0),  # Raspberry Pi Pico
    (0x1A86, 0x55D4),  # Adafruit Feather ESP32 V2
    (0x10C4, 0xEA60),  # DOIT ESP32 Devkit V1
    (0x1A86, 0x55D3),  # ESP32 S3 Development Board
]


class SerialRelay(Node):
    def __init__(self):
        # Initalize node with name
        super().__init__("serial_relay")

        ######################################################
        # Setup Serial device

        # Find the Serial port for the Pico
        ports = self._find_ports()
        
        if len(ports) == 0:
            self.get_logger().fatal("Unable to find Pico... is it plugged in?")
            sys.exit(1)
        elif len(ports) > 1:
            self.get_logger().fatal("Found more than one Pico... aborting.")
            sys.exit(1)

        self.port = ports[0]

        self.ser = serial.Serial(self.port, 115200, timeout=0.1)

        ######################################################
        # Setup topics

        # Create a publisher to publish any output the pico sends
        self._rx_pub = self.create_publisher(String, '/serial/rx', 10) 

        # Create a subscriber to listen to any commands sent for the pico
        self._tx_sub = self.create_subscription(String, '/serial/tx', self.send, 10)

    def read_pico(self):
        output = self.ser.read_until(b"\n")
        if not output:
            return

        try:
            mcu_string = output.decode("utf8").strip()
        except UnicodeDecodeError as e:
            self.get_logger().warn(f"Ignoring invalid unicode from MCU: {e}")
            return

        self.get_logger.info(f"[Pico] [RX] {output}")

        self._rx_pub.publish(String(data=mcu_string))
   
    def send(self, msg):
        output = msg.data.strip() + "\n"
        self.get_logger().info(f"[Pico] [TX] {output}")

        # Send to Pico
        self.ser.write(output.encode("utf8"))

    def _find_ports(self) -> list[str]:
        """
        Finds all valid ports but does not test them

        returns: all valid ports
        """
        comports = serial.tools.list_ports.comports()
        valid_ports = list(
            map(  # get just device strings
                lambda p: p.device,
                filter(  # make sure we have a known device
                    lambda p: (p.vid, p.pid) in KNOWN_USBS and p.device is not None,
                    comports,
                ),
            )
        )
        self.get_logger().info(f"found valid MCU ports: [ {', '.join(valid_ports)} ]")
        return valid_ports
        

def main(args=None):
    rclpy.init(args=args)

    serial_pub = SerialRelay()
    try:
        while rclpy.ok():
            serial_pub.read_pico()
    except KeyboardInterrupt:
        sys.exit(0)

    serial_pub.run()


if __name__ == '__main__':
    main()
