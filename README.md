# Rover Two Month 2026 Example Software Stack

This repository provides an example ROS2 node (for the Orange Pi) and embedded code (for the Pico) for Rover TM.

The ROS2 node serves as a serial driver, exposing the serial connection to the connected Pico as ROS2 topics. The Pico code will blink the LED and respond to a few basic serial commands.

Feel free to ask me any questions (`ddavdd` on Discord) if you have any problems.

## ROS2 Serial Node

### Requirements

- **pyserial** - can be installed via `pip` or system packages
- **ROS2** - will only work during competition if you use ROS2 Jazzy Jalisco, but this package should support Humble thru Lyrical.

### Setup

1. Create a ROS2 workspace (see this [tutorial](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)):
  ```bash
  mkdir -p ros2_ws/src
  cd ros2_ws/src
  git clone https://github.com/ds196/two_month_rover
  ```
2. Build the workspace:
  ```bash
  cd ..
  colcon build --symlink-install
  ```
  - You should get the following output:
    ```txt
    Starting >>> pico_relay
    Finished <<< pico_relay [2.85s]          

    Summary: 1 package finished [3.18s]
    ```

### Usage

1. Source the workspace:
  ```bash
  source install/setup.bash
  ```
2. Run the node:
  ```bash
  ros2 run pico_relay relay
  ```
  - Please note that the node will fail to start if a different application is already using the serial port.

## Pico Code

### Requirements

- **Arduino IDE v2** - can be installed from [here](https://www.arduino.cc/en/software/).
  - **Pico board** - these steps allow you to upload code to your Pico:
    - Add the following line to your "additional boards manager URLs":
      ```txt
      https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
      ```
    - In the Boards Manager, download the following board: "Raspberry Pi Pico/RP2040/RP2350" by Earle J. Philhower, III

### Setup

1. Open the provided `.ino` file in Arduino IDE
2. Flash this code to your Pico

### Usage

1. Use the Serial Monitor to test sending commands:
  - Sending `ping`, the Pico should respond with `pong`.

## Contributors

- David Sharpe
- Tristan McGinnis
- Areeb Mohammed
