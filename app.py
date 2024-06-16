import streamlit as st
import serial.tools.list_ports
import subprocess

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout if result.returncode == 0 else result.stderr

# Streamlit UI Components
st.title('UPDI Device Programmer')
device_name = "attiny412"  # Can be adjusted or made dynamic

# COM Port Selection
com_ports = list_serial_ports()
selected_port = st.selectbox('Select COM Port:', com_ports)

# File Uploader
uploaded_file = st.file_uploader("Upload HEX file", type=['hex'])
hex_file_path = None
if uploaded_file is not None:
    hex_file_path = "uploaded.hex"
    with open(hex_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

# Erase and Program Buttons
if st.button('Erase Device'):
    if selected_port:
        erase_command = f"pymcuprog erase -t uart -u {selected_port} -d {device_name}"
        erase_result = run_command(erase_command)
        st.success(f'Device erased successfully: {erase_result}')
    else:
        st.error('Please select a COM port.')

if st.button('Program Device'):
    if uploaded_file is not None and selected_port:
        program_command = f"pymcuprog write -t uart -u {selected_port} -d {device_name} -f {hex_file_path}"
        program_result = run_command(program_command)
        st.success(f'Device programmed successfully: {program_result}')
    else:
        st.error('Please select a COM port and upload a HEX file.')
