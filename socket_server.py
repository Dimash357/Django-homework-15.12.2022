import os
import socket
import tkinter
import threading
import _thread
import json


def new_connection(connection):
    print("connection start...")
    send_json_files(connection)
    while True:
        data = connection.recv(1024)

        res = f"[request]: {data} {type(data)}"

        global _set_text
        _set_text(res)
        print(res)

        if not data:
            connection.send(b"[response]: MOT_ANY_DATA 400")
            break
        else:
            connection.send(b"[response]: OK 200")

    connection.close()


def send_json_files(connection):
    for filename in os.listdir("."):
        if filename.endswith(".json"):
            with open(filename, "r") as f:
                data = json.loads(f.read())
                connection.send(json.dumps(data).encode())


def backend_server() -> None:

    global _set_text
    _set_text("server started")

    with open("config.json", 'rb') as f:
        config = json.load(f)

    host = config["host"]
    port = config["port"]
    print(host, port)

    print_lock = threading.Lock()
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((host, port))
    my_socket.listen(5)

    while True:
        connection, address = my_socket.accept()
        print_lock.acquire()

        _thread.start_new_thread(new_connection, (connection,))
    my_socket.close()


def start_server():
    threading.Thread(target=backend_server).start()


def frontend_server() -> None:
    tk_windows = tkinter.Tk()
    tk_windows.title("our server")
    tk_windows.geometry("300x100")

    tk_label = tkinter.Label(tk_windows, text="server ready to start")
    tk_label.grid(row=0, column=0)

    def __set_text(__text: str) -> None:
        tk_label.config(text=__text)

    global _set_text
    _set_text = __set_text

    tk_button = tkinter.Button(tk_windows, text="start server", command=start_server)
    tk_button.grid(row=1, column=0)

    tk_windows.mainloop()


if __name__ == '__main__':
    def _set_text_ph(__text: str) -> None:
        pass

    _set_text = _set_text_ph

    frontend_server()
