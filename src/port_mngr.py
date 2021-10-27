import src.alerter as alr
import serial.tools.list_ports

# Const
IS_RUNNING = False
DECODING = False


def get_ports():
    return [[port, desc, hwid] for port, desc, hwid in sorted(serial.tools.list_ports.comports())]


def read_port(port_name, widget):
    try:
        session = serial.Serial(port_name)
        alr.messagebox.showinfo("Connected", f'Successfully connected to: "{port_name}"')
    except Exception as e:
        alr.messagebox.showerror("Error", e)
        return

    while IS_RUNNING:
        data = session.readline()

        if DECODING:
            data = data.decode()

        if IS_RUNNING:
            widget.insert("end", str(data))

    del session
    alr.messagebox.showinfo("Disconnected", f'Successfully disconnected from: "{port_name}"')

