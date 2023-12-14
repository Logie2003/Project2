import socket
import json
import time
import os

# Set up the socket client
client = socket.socket()
host = '192.168.50.75'  # Use localhost or the actual IP of the Raspberry Pi
port = 5020

try:
    # Connect to the Raspberry Pi's socket server
    client.connect((host, port))

    # Infinite loop for continuous updates
    iteration_count = 0
    while True:
        v = os.popen('vcgencmd measure_volts ain1').readline()
        core = os.popen('vcgencmd measure_temp').readline()
        gpu_temp = os.popen('vcgencmd measure_temp').readline()
        cpu_temp = os.popen('vcgencmd measure_temp').readline()
        gpu_core_speed = os.popen('vcgencmd measure_clock core').readline()
        hdmi_clock = os.popen('vcgencmd measure_clock hdmi').readline()

        JsonResult = {
            "thing": [{"temp": "You're"}],
            "volts": v,
            "temp-core": core,
            "iteration_count": iteration_count,
            "gpu_temp": gpu_temp,
            "cpu_temp": cpu_temp,
            "gpu_core_speed": gpu_core_speed,
            "hdmi_clock": hdmi_clock,
        }

        JsonResult = json.dumps(JsonResult)
        jsonbyte = bytearray(JsonResult, "UTF-8")
        client.send(jsonbyte)

        iteration_count += 1
        time.sleep(0.5)  # Adjust the sleep time to control update frequency

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    client.close()
