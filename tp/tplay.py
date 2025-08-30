import socket,time,threading,os,sys
from tkinter import *
from tkinter import scrolledtext
from PIL import Image, ImageTk
from playsound import playsound

am_server = None
my_name = None
other_name = None
chat_history = []

def start(side):
    start_time = time.time()
    def server():
        global connected, player1, player2, client, am_server, my_name, other_name
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(10)
        server.bind(('0.0.0.0', 9999))
        server.listen(1)
        print("Server started, waiting for connections...")
        state.config(fg="white", text="Server started, waiting for connections...")
        try:
            client, addr = server.accept()
            print("Connected to:", addr)
            player1 = nick.get()
            player2 = client.recv(1024).decode()
            state.config(text=f"Connected to: {player2}" + str(addr), fg="#4DFF8E")
            time.sleep(0.5)
            client.send(nick.get().encode())
            threading.Thread(target=ping_server, args=(client,), daemon=True).start()
            connected = True
            am_server = True
            if am_server:
                my_name = player1
                other_name = player2
            return client
        except socket.timeout:
            print("Server: Connection timed out.")
            state.config(text="Server: Connection timed out.", fg="#AC4343")
            time.sleep(2)
            state.config(text="")
            connected = False
            return None
    def client():
        global connected, player1, player2, client, am_server, my_name, other_name
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        try:
            client.connect((ip.get(), 9999))
            print("Connected to the server.")
            client.send(nick.get().encode())
            time.sleep(0.5)
            player1 = client.recv(1024).decode()
            player2 = nick.get()
            state.config(text=f"Connected to the server: {player1}", fg="#4DFF8E")
            threading.Thread(target=ping_server, args=(client,), daemon=True).start()
            connected = True
            am_server = False
            if not am_server:
                my_name = player2
                other_name = player1
            return client
        except socket.timeout:
            print("Client: Connection timed out.")
            state.config(text="Client: Connection timed out.", fg="#AC4343")
            time.sleep(2)
            state.config(text="")
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
    global connected
    while True:
        try:
            sock.send(b'ping')
            time.sleep(10)
        except Exception as e:
            print("Connection lost:", e)
            state.config(fg="#AC4343", text=f"Connection lost: {e}")
            connected = False
            break


class button:
    def __init__(self, master, text, bg, hvbg, font, wd, hg, cmd, pady):
        self.hvbg = hvbg
        self.bg = bg
        self.pady = pady
        self.button = Button(master, text=text, bg=bg, font=font, width=wd, height=hg, command=cmd, relief="solid", overrelief="solid", borderwidth=5, activebackground=bg, activeforeground="black")
        self.button.pack(pady=pady)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.button.config(bg=self.hvbg)
    def on_leave(self, event):
        self.button.config(bg=self.bg)


#Menu
menu = Tk()
menu.title("2Play")
menu.geometry("700x500")
menu.resizable(False, False)
menu.configure(bg="#2F3031")

logo_image = res(resource_path("logo.png"), 256, 92, 256)
logo = Label(menu, image=logo_image, bg="#2F3031", fg="white", font=("Arial", 40))
logo.pack(pady=10)

b_host = button(menu, "Host a server", "#4FDD83", "#77FFA9", ("Fixedsys", 20), 15, 2, host_server, pady=5)

b_join = button(menu, "Join a server", "#5042E9", "#6256E5", ("Fixedsys", 20), 15, 2, join_server, pady=5)

state = Label(menu, text="", bg="#2F3031", fg="white", font=("Courier New", 12))
state.pack(pady=5)

Label(menu, text="----------------------------", bg="#2F3031", fg="white", font=("Courier New", 12)).pack(pady=5)
nick = Entry(menu, text="Enter your nickname", bg="#FFFFFF", fg="black", font=("Courier New", 12), width=30)
nick.insert(0, "Your nickname")
nick.pack(pady=2)

ip = Entry(menu, text="Enter IP address", bg="#FFFFFF", fg="black", font=("Courier New", 12), width=30)
ip.insert(0, "IP to connect to")
ip.pack(pady=2)

#
connected = False


#Actions


def Chat(me, other, client):
    chat_open = True
    chat = Toplevel(menu)
    chat.title("Chat")
    chat.geometry("400x600")
    chat.resizable(False, False)
    chat.configure(bg="#2F3031")
    menu.withdraw()

    Label(chat, text=f"Chat with {other}", bg="#2F3031", fg="white", font=("Fixedsys", 10)).pack(pady=1)
    Label(chat, text="-"*35, bg="#2F3031", fg="#494949", font=("Fixedsys", 15)).pack()
    

    def send_message():
        global chat_history
        message = textbox.get("1.0", "end").strip()
        if message == "ping":
            ping_alert()
        else:
            client.send(message.encode())
            textbox.delete("1.0", "end")
            messages.configure(state="normal")
            messages.insert("end", f"{me}: {message}\n\n")
            messages.configure(state="disabled")
            chat_history.append((me, message))

    send = button(chat, "Send", "#4FDD83", "#77FFA9", ("Fixedsys", 12), 35, 1, send_message, pady=2)
    send.button.pack(side="bottom", pady=5)

    textbox = Text(chat, bg="#535556", fg="#C9C9C9", font=("Fixedsys", 16), width=35, height=5, relief="solid", borderwidth=5)
    textbox.pack(side="bottom")

    messages = scrolledtext.ScrolledText(chat, wrap=WORD,bg="#535556", fg="#C9C9C9", font=("Fixedsys", 16), width=40, height=30, relief="solid", borderwidth=5, state="disabled")
    messages.pack(padx=10, pady=5)


    def get_messages():
        global chat_history
        while True:
            message = client.recv(1024).decode()
            if not message:
                break
            if message != 'ping':
                messages.after(0, lambda msg=message: update_messages(msg))
                chat_history.append((other, message))
            time.sleep(0.2)
            print(chat_history)
    def update_messages(msg):
        messages.configure(state="normal")
        messages.insert("end", f"{other}: {msg}" + "\n\n")
        messages.configure(state="disabled")
        messages.see("end")
    threading.Thread(target=get_messages, daemon=True).start()

    def check_enter():
        while chat_open:
            text = textbox.get("1.0", "end-1c")
            if text.endswith("\n"):
                textbox.delete("1.0", "end")
                message = text.strip()
                if message:
                    if message == "ping":
                        ping_alert()
                    else:
                        client.send(message.encode())
                        textbox.after(0, lambda: textbox.delete("1.0", "end"))
                        messages.configure(state="normal")
                        messages.insert("end", f"{me}: {message}\n\n")
                        messages.configure(state="disabled")
                        chat_history.append((me, message))
            time.sleep(0.1)

    threading.Thread(target=check_enter, daemon=True).start()

    def ping_alert():
        error = Toplevel(chat)
        error.title("Error")
        error.geometry("300x200")
        error.configure(bg="#2F3031")
        threading.Thread(target=lambda: playsound(os.path.join(os.path.dirname(__file__), "ping_alert.wav")), daemon=True).start()
        Label(error, text="U fucking idiot", bg="#2F3031", fg="#AC4343", font=("Fixedsys", 12)).pack(pady=2)
        time.sleep(0.2)
        Label(error, text="u cant ping someone", bg="#2F3031", fg="#AC4343", font=("Fixedsys", 12)).pack(pady=2)
        time.sleep(0.2)
        Label(error, text="it is illegal", bg="#2F3031", fg="#AC4343", font=("Fixedsys", 12)).pack(pady=2)
        chat.after(3000, error.destroy)

    def on_close():
        global chat_open
        chat_open = False
        chat.destroy()
        menu.deiconify()

    chat.protocol("WM_DELETE_WINDOW", on_close)


def actions():
    global chat
    w_actions = Toplevel(menu)
    w_actions.title("2Play")
    w_actions.geometry("700x500")
    w_actions.resizable(False, False)
    w_actions.configure(bg="#2F3031")
    menu.withdraw()

    chat = button(w_actions, text="Chat", bg="#E2B450", hvbg="#F9D586", font=("Fixedsys", 20), wd=10, hg=1, cmd=lambda: Chat(me=my_name, other=other_name, client=client), pady=5)

    def on_close():
        global chat_open
        chat_open = False
        w_actions.destroy()
        menu.deiconify()

    w_actions.protocol("WM_DELETE_WINDOW", on_close)


def strt(): global actions; actions() if connected is True else None
b_start = button(menu, text="Start", bg="#FF5733", hvbg="#F4785D", font=("Fixedsys", 20), wd=10, hg=1, cmd=strt, pady=5)


if __name__ == "__main__":
    menu.mainloop()