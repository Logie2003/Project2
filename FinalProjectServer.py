import socket
import json
import subprocess
import time
import threading

def get_sensor_data():
    try:
        # Use vcgencmd to get various sensor data
        core_temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8').strip().replace('temp=', '')
        gpu_temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8').strip().replace('temp=', '')
        cpu_temp = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp']).decode('utf-8').strip()
        voltage = subprocess.check_output(['vcgencmd', 'measure_volts']).decode('utf-8').strip()
        gpu_core_speed = subprocess.check_output(['vcgencmd', 'measure_clock', 'core']).decode('utf-8').strip()
        hdmi_clock = subprocess.check_output(['vcgencmd', 'measure_clock', 'hdmi']).decode('utf-8').strip()
        pixel_values = "123, 456, 789"  # Replace with actual pixel values retrieval logic
        h264_block = subprocess.check_output(['vcgencmd', 'measure_clock', 'h264']).decode('utf-8').strip()

        return {
            "Core Temperature": core_temp,
            "GPU Temperature": gpu_temp,
            "CPU Temperature": f"{float(cpu_temp) / 1000:.2f}",  # Convert to degrees Celsius
            "Voltage": voltage,
            "GPU Core Speed": gpu_core_speed,
            "HDMI Clock": hdmi_clock,
            "Pixel Values": pixel_values,
            "H264 block": h264_block,
        }
    except Exception as e:
        print(f"Error getting sensor data: {e}")
        return {}

def send_data(client):
    iteration_count = 0
    while True:
        try:
            sensor_data = get_sensor_data() 
            if not sensor_data:
                continue

            sensor_data['iteration_count'] = iteration_count
            sensor_data['LED_status'] = True if iteration_count % 2 == 0 else False

            json_data = json.dumps(sensor_data)
            client.sendall(json_data.encode('utf-8'))

            iteration_count += 1 
            time.sleep(0.5)  # Adjust the sleep time as needed
        except Exception as e:
            print(f"Error sending data: {e}")

# Set up the socket server
server = socket.socket()
host = '192.168.50.75'  # Use the actual IP of the Raspberry Pi
port = 5022

server.bind((host, port))
server.listen()

print(f"Server listening on {host}:{port}")

while True:
    client, addr = server.accept()
    print(f"Accepted connection from {addr}")

    # Start a thread to send data to the client
    threading.Thread(target=send_data, args=(client,), daemon=True).start()
