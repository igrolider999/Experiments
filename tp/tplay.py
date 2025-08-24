import socket,time,threading,os,sys
from tkinter import *
from PIL import Image, ImageTk


def start(side):
    start_time = time.time()
    def server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(10)
        server.bind(('127.0.0.1', 9999))
        server.listen(1)
        print("Server started, waiting for connections...")
        try:
            client, addr = server.accept()
            print("Connected to:", addr)
            state.config(text="Connected to: " + str(addr))
            threading.Thread(target=ping_server, args=(client,), daemon=True).start()
            return client
        except socket.timeout:
            print("Server: Connection timed out.")
            state.config(text="Server: Connection timed out.")
            return None
    def client():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        try:
            client.connect(('127.0.0.1', 9999))
            print("Connected to the server.")
            state.config(text="Connected to the server.")
            threading.Thread(target=ping_server, args=(client,), daemon=True).start()
            return client
        except socket.timeout:
            print("Client: Connection timed out.")
            state.config(text="Client: Connection timed out.")
            return None
    if side == 0:
        start_server =threading.Thread(target=server, daemon=True)
        start_server.start()
    elif side == 1:
        start_client = threading.Thread(target=client, daemon=True)
        start_client.start()
    if time.time() - start_time > 10:
        print("Connection timed out")
        start_server.join()
        start_client.join()
        return


def res(file, height, og_height, og_width):
    return ImageTk.PhotoImage(Image.open(f"{file}").resize((height, int(og_height/og_width * height)), Image.LANCZOS))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def click():
    print("Clicked")

def host_server():
    threading.Thread(target=start, args=(0,), daemon=True).start()

def join_server():
    threading.Thread(target=start, args=(1,), daemon=True).start()

def ping_server(sock):
    while True:
        try:
            sock.send(b'ping')
            time.sleep(10)
        except Exception as e:
            print("Connection lost:", e)
            state.config(text=f"Connection lost: {e}")
            break


#Tk
menu = Tk()
menu.title("2Play")
menu.geometry("700x500")
menu.resizable(False, False)
menu.configure(bg="#2F3031")

logo_image = res(resource_path("logo.png"), 256, 92, 256)
logo = Label(menu, image=logo_image, bg="#2F3031", fg="white", font=("Arial", 40))
logo.pack(pady=50)

b_host = Button(menu, text="Host a server", bg="#4DFF8E", font=("Fixedsys", 20), width=15, height=2, command=host_server, relief="solid",borderwidth=5)
b_host.pack()

b_join = Button(menu, text="Join a server", bg="#5042E9", font=("Fixedsys", 20), width=15, height=2, command=join_server, relief="solid",borderwidth=5)
b_join.pack(pady=20)

state = Label(menu, text="Waiting for connection...", bg="#2F3031", fg="white", font=("Courier New", 12))
state.pack(pady=20)


#

class button:
    def __init__(self):
        self.button = Button(menu, text="", bg="#645494", font=("Fixedsys", 20), width=5, height=2, command=self.on_click)
        self.button.pack(pady=20)

    def on_click(self):
        print("Button clicked")
        self.button.config(text="X")


if __name__ == "__main__":
    menu.mainloop()