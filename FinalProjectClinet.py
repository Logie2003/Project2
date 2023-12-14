import socket
import json
import PySimpleGUI as sg
import threading

def update_gui(json_data, window):
    try:
        formatted_data = [
            f"Core Temperature: {json_data['temp-core']}",
            f"Voltage: {json_data['volts']}",
            f"Iteration Count: {json_data['iteration_count']}",
            f"GPU Temperature: {json_data['gpu_temp']}",
            f"CPU Temperature: {json_data['cpu_temp']}",
            f"GPU Core Speed: {json_data['gpu_core_speed']}",
            f"HDMI Clock: {json_data['hdmi_clock']}",
        ]
    except KeyError as e:
        formatted_data = [f"Error: Key {e} not found in JSON data"]

    window['-DATA-'].update('\n'.join(formatted_data))

def receive_data(client, window):
    while True:
        chunk = client.recv(4096).decode('utf-8')
        if not chunk:
            break
        json_data = json.loads(chunk)

        update_gui(json_data, window)

# Set up the socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.50.75'  # Use localhost or the actual IP of the Raspberry Pi
port = 5020

# Bind the server to the address and port
server.bind((host, port))

# Listen for incoming connections
server.listen(1)

# Accept a connection
client, addr = server.accept()

# Define the PySimpleGUI layout
layout = [
    [sg.Text("Received Data:", font=('Helvetica', 14))],
    [sg.Multiline("", key='-DATA-', size=(40, 10), font=('Helvetica', 12), background_color='lightblue')],
]

# Create the PySimpleGUI window
window = sg.Window("Server GUI", layout, finalize=True)

try:
    # Start a thread to receive data and update the GUI
    thread = threading.Thread(target=receive_data, args=(client, window), daemon=True)
    thread.start()

    # Event loop for the PySimpleGUI window
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    client.close()

    # Close the PySimpleGUI window
    window.close()

    # Close the server socket
    server.close()
