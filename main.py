import connection

import customtkinter as tk
import threading
import pickle
import socket
import os
import rsa
class App:
    def __init__(self):

        self.server_ip = "localhost"
        self.server_port = 12345

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

        self.update_interface()

    def update_interface(self):

        self.tabview = tk.CTkTabview(self.app)
        self.tab_msg = self.tabview.add("Messages")
        self.tab_settings = self.tabview.add("Settings")
        
        self.tabview.pack(anchor="center")

        ## Message Tab
        self.chat_messages = tk.CTkScrollableFrame(self.tab_msg, bg_color="transparent", width=720, height=460)
        self.chat_messages.pack(padx= 10, pady= 10, anchor= "nw")

        self.message_input = tk.CTkEntry(self.tab_msg, width=550, height=30)
        self.message_input.pack(side="left", fill="both")

        self.message_button = tk.CTkButton(self.tab_msg, text="Send", width=40, height=30, command=self.send_msg_button)
        self.message_button.pack(side="right", fill="both")

        ## Settings tab

        self.settings_frame = tk.CTkFrame(self.tab_settings, bg_color="transparent", width=780, height=550) 
        self.settings_frame.pack(anchor = "center")

        self.checker_keys()

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
        except:
            self.show_error_msg("Failed to connect server")
            return

    def message_handler(self):
        while True:
            message = self.client.recv(1024)
            message_decode = (str)(message.decode("utf-8"))
            if len(message_decode) > 0:
                try:
                    #message_decrypt = rsa.decrypt(message_decode, self.my_private_key)
                    self.show_getted_msg(message_decode)
                except rsa.DecryptionError:
                    continue
    
    def send_msg_button(self):
        text = self.message_input.get()
        self.show_sended_msg(text)
        self.send_message(text)
        self.message_input.delete("0", tk.END)

    def send_message(self, text):
        #try:
            #message = rsa.encrypt(self.freind_public_key)
        self.client.send(bytes(text, encoding="utf-8"))
        #except:
            #self.show_error_msg("An error occurred while sending a message")

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
    