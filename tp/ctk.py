import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.config(bg="#2F3031")
root.title("Вывод сообщений")

# Поле вывода только для чтения
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
chat_box.config(bg="#2F3031", fg="#d3dae0", font=("fixedsys", 20), relief="solid", borderwidth=5)
chat_box.pack(padx=10, pady=10)
state = False
# Заполняем тестовыми сообщениями
for i in range(1, 51):
    text = "Message"
    chat_box.insert(tk.END, f"Player2: {text} {i}\n" if state is False else f"{' '*(35-len(text))}{text} {i}\n")
    state = not state

# Делаем только для чтения (нельзя вводить руками)
chat_box.configure(state="disabled")

root.mainloop()
