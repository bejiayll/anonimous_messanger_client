import customtkinter as tk

app = tk.CTk()
app.geometry("800x600")
app.resizable(width=False, height=False)
app.title("Forq's anonimous chat")

chat_messages = tk.CTkScrollableFrame(app, bg_color="transparent", width=780, height=500)
chat_messages.pack(padx= 10, pady= 10, anchor= "nw")

frame = tk.CTkFrame(chat_messages, bg_color="transparent", corner_radius=90)
frame.pack(padx = 5, pady = 5,anchor='nw')

enter = tk.CTkEntry(app, width=500)
enter.place(x=10, y=550)

def handel_send_message():
    ...

def send_message():
    text = enter.get()
    newframe = tk.CTkFrame(chat_messages, fg_color="transparent")
    newframe.pack(padx = 5, pady = 5, anchor='ne')
    newmessage = tk.CTkLabel(newframe, text=text, fg_color="#1e78a6", corner_radius=10)
    newmessage.pack(padx=10, pady=10, anchor="nw")

send_button = tk.CTkButton(app, text="Send", width= 40, command=send_message)
send_button.place(x=540, y=550)

message = tk.CTkLabel(frame, text="Message, but very-very long", corner_radius=10, fg_color="#1c1c1c")
message.pack(padx=10, pady=10, anchor="nw")




app.mainloop()
