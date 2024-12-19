import customtkinter as tk

app = tk.CTk()
app.geometry("800x600")
app.resizable(width=False, height=False)
app.title("Forq's anonimous chat")

frame = tk.CTkFrame(app, bg_color="transparent")
frame.pack(padx = 5, pady = 10,anchor='nw')

enter = tk.CTkEntry(app, width=500)
enter.place(x=10, y=550)

def handel_send_message():
    ...

def send_message():
    text = enter.get()
    newframe = tk.CTkFrame(app, fg_color="#1e78a6")
    newframe.pack(padx = 5, pady = 5, anchor='nw')
    newmessage = tk.CTkLabel(newframe, text=text, fg_color="#1e78a6", bg_color="#1e78a6")
    newmessage.pack(padx=9, pady=5, anchor="nw")

send_button = tk.CTkButton(app, text="Send", width= 40, command=send_message)
send_button.place(x=540, y=550)

message = tk.CTkLabel(frame, text="Message, but very-very long", corner_radius=3)
message.pack(padx=5, pady=5, anchor="nw")




app.mainloop()
