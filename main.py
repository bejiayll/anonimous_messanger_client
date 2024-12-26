import connection

import customtkinter as tk
from tkinter.messagebox import showerror
import socket
import threading
import pickle
import os
import rsa


class App:
    def __init__(self):

        self.server_ip = ""
        self.server_port = 0

        self.friend_key_path = "./config/freinds/public.txt"
        self.public_key_path = "./config/public.txt"
        self.private_key_path = "./config/private.txt"
        self.connection_path = "./config/connect.json"

        self.my_private_key = ""
        self.freind_public_key = ""

        self.app = tk.CTk()
        self.app.geometry("800x600")
        self.app.resizable(width=False, height=False)
        self.app.title("Forq's anonimous chat")

        try: 
            with open(self.private_key_path, "rb") as file:
                unpickler = pickle.Unpickler(file)
                self.my_private_key = unpickler.load()

            with open(self.friend_key_path, "rb") as file:
                unpickler = pickle.Unpickler(file)
                self.freind_public_key = unpickler.load()
        except:
            pass

        self.update_interface()

        self.app.protocol("WM_DELETE_WINDOW", lambda: self.exit())

    def exit(self):
            try:
                self.send_protocol("EXIT") 
                self.client.close()
            except:
                pass
            self.app.destroy()
            quit()

    def update_interface(self):

        self.tabview = tk.CTkTabview(self.app)
        self.tab_msg = self.tabview.add("Messages")
        self.tab_settings = self.tabview.add("Settings")
        
        self.tabview.pack(anchor="center")

        ## Message Tab ##
        self.chat_messages = tk.CTkScrollableFrame(self.tab_msg, bg_color="transparent", width=720, height=460)
        self.chat_messages.pack(padx= 10, pady= 10, anchor= "nw")

        self.message_input = tk.CTkEntry(self.tab_msg, width=550, height=30)
        self.message_input.pack(side="left", fill="both")

        self.message_button = tk.CTkButton(self.tab_msg, text="Send", width=40, height=30, command=self.send_msg_button)
        self.message_button.pack(side="right", fill="both")

        ## Settings tab ##
        self.ip_label = tk.CTkLabel(self.tab_settings, text="ip")
        self.port_label = tk.CTkLabel(self.tab_settings, text="port")

        self.ip_label.grid(row=0, column=0, padx=10)
        self.port_label.grid(row=0, column=3, padx=10)

        self.ip_input = tk.CTkEntry(self.tab_settings, width=300, height= 20)
        self.port_input = tk.CTkEntry(self.tab_settings, width=60, height= 20)

        self.ip_input.grid(row=0, column=1, padx=10)
        self.port_input.grid(row=0, column=2, padx=10)

        self.settings_connect_button = tk.CTkButton(self.tab_settings, text="Connect", fg_color="#017003", corner_radius=20, command=self.update_connection)
        self.settings_connect_button.grid(row=1, column=1, pady=10)
        self.settings_connect_button = tk.CTkButton(self.tab_settings, text="Generate\nencryption keys", fg_color="#017003", corner_radius=20, command=self.generate_encryption_keys)
        self.settings_connect_button.grid(row=2, column=1, pady=20)

        self.checker_keys()

    def update_connection(self):
        server_ip = self.ip_input.get() if self.ip_input.get() != None else ""
        server_port = self.port_input.get() if self.port_input.get() != None else ""
        if server_ip != "" and server_port != "":
            self.server_ip = server_ip
            self.server_port = (int)(server_port)
            self.connect_to_socket()
        else: 
            showerror(title="Connection error", message="The ip or port is incorrect")
        

    def show_error_msg(self, text):
        msg_frame = tk.CTkFrame(self.chat_messages, fg_color="transparent")
        msg = tk.CTkLabel(msg_frame, text=text, fg_color="#c21010", corner_radius=10)
        msg_frame.pack(anchor='center')        
        msg.pack(padx=10, pady=10, anchor="center")

    def show_getted_msg(self, text):
        msg_frame = tk.CTkFrame(self.chat_messages, fg_color="transparent")
        msg = tk.CTkLabel(msg_frame, text=text, fg_color="#1c1c1c", corner_radius=10)
        msg_frame.pack(anchor='nw')        
        msg.pack(padx=10, pady=10, anchor="nw")

    def show_sended_msg(self, text):
        msg_frame = tk.CTkFrame(self.chat_messages, fg_color="transparent")
        msg = tk.CTkLabel(msg_frame, text=text, fg_color="#13629e", corner_radius=10)
        msg_frame.pack(anchor='nw')        
        msg.pack(padx=10, pady=10, anchor="nw")
        
    def generate_encryption_keys(self):
        public, private = rsa.newkeys(512)

        with open("config\\public.txt", "wb") as file:
            pickle.dump(public, file)
        with open("config\\private.txt", "wb") as file:
            pickle.dump(private, file)

        self.my_private_key = private

    def checker_keys(self):
        if (os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path)):
            self.check_connection()
        else: 
            self.show_error_msg("Please generate your encryption keys")
    
    def check_connection(self):
        if os.path.exists(self.connection_path):
            self.connect_to_socket()
        else: 
            self.show_error_msg("Check connection")
            
    def connect_to_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.server_ip, self.server_port))
            threading.Thread(target=self.message_handler).start()
            return
        except socket.error:
            self.show_error_msg("Failed connect to server")
            return

    def message_handler(self):
        while True:
            message = self.client.recv(1024)
            message_decode = (str)(message.decode("utf-8"))
            if len(message_decode) > 0:
                try:
                    message_decrypt = rsa.decrypt(message_decode, self.my_private_key)
                    self.show_getted_msg(message_decrypt)
                except rsa.DecryptionError:
                    continue
    
    def send_msg_button(self):
        text = self.message_input.get()
        self.show_sended_msg(text)
        self.send_message(text)
        self.message_input.delete("0", tk.END)

    def send_message(self, text):
        #try:
            message = rsa.encrypt(text, self.freind_public_key)
            self.client.send(bytes(message, encoding="utf-8"))
        # except:
            # self.show_error_msg("An error occurred while sending a message")

    def send_protocol(self, text):
        self.client.send(bytes(text, encoding="utf-8"))

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
    