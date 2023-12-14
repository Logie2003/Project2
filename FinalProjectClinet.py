import socket
import json
import PySimpleGUI as sg
import threading

CIRCLE = '●'  # Unicode symbol 9899 for ON
CIRCLE_OUTLINE = '○'  # Unicode symbol 9898 for OFF

def update_gui(window, json_data):
    try:
        formatted_data = [
            f"Core Temperature: {json_data['Core Temperature']}",
            f"GPU Temperature: {json_data['GPU Temperature']}",
            f"CPU Temperature: {json_data['CPU Temperature']}",
            f"Voltage: {json_data['Voltage']}",
            f"GPU Core Speed: {json_data['GPU Core Speed']}",
            f"HDMI Clock: {json_data['HDMI Clock']}",
            f"Pixel Values: {json_data['Pixel Values']}",
            f"H264 block: {json_data['H264 block']}",
            f"Iteration Count: {json_data['iteration_count']}",
        ]
        window['-DATA-'].update('\n'.join(formatted_data))
        window['-LED-'].update(CIRCLE if json_data['LED_status'] else CIRCLE_OUTLINE, text_color='green')
    except KeyError as e:
        formatted_data = [f"Error: Key {e} not found in JSON data"]
        window['-DATA-'].update('\n'.join(formatted_data))

# Set up the socket client
client = socket.socket()
host = '192.168.50.75'  # Use the actual IP of the Raspberry Pi
port = 5022

# Define the PySimpleGUI layout
layout = [
    [sg.Text("Received Data:", font=('Helvetica', 14))],
    [sg.Multiline("", key='-DATA-', size=(40, 10), font=('Helvetica', 12), background_color='lightblue')],
    [sg.Text("LED STATE", font=('Helvetica', 14), text_color='white'), sg.Text("", key='-LED-', font=('Helvetica', 14))],
    [sg.Button('Exit')],
]

# Create the PySimpleGUI window
window = sg.Window("Client GUI", layout, finalize=True) 

iteration_count = 0

try:
    # Connect to the Raspberry Pi's socket server
    client.connect((host, port))

    # Event loop for the PySimpleGUI window
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or iteration_count >= 50 or event == 'Exit':
            break

        # Receive and process data from the server
        chunk = client.recv(4096).decode('utf-8')
        if not chunk:
            break

        json_data = json.loads(chunk)
        update_gui(window, json_data)
        iteration_count += 1

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    client.close()

    # Close the PySimpleGUI window
    window.close()
