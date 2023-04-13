from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Encryption")
        self.geometry("500x400")

        self.key = None
        self.file_label = tk.Label(self, text="No File Selected")
        self.key_label = tk.Label(self, text= "No Key Selected")
        self.file_button = tk.Button(self, text = "Select file", command=self.select_file)
        self.key_button = tk.Button(self, text="Select Key File", command = self.select_key_file)
        self.encrypt_button = tk.Button(self, text = "Encrypt file", command = self.encrypt_file)
        self.decrypt_button = tk.Button(self, text = "Decrypt File", command = self.decrypt_file)
        self.quit_button = tk.Button(self, text="Quit", command = self.quit)

        self.file_label.pack(pady=10)
        self.key_label.pack(pady=10)
        self.file_button.pack(pady=10)
        self.key_button.pack(pady=10)
        self.encrypt_button.pack(pady=10)
        self.decrypt_button.pack(pady=10)
        self.quit_button.pack(pady=10)


    def generate_key(self):
        key = Fernet.generate_key()
        key_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key.key")
        with open(key_file_path, "wb") as f:
            f.write(key)

    def select_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.filename = filename
            self.file_label.config(text=filename)

    def select_key_file(self):
        keyfilename = filedialog.askopenfilename()
        if keyfilename:
            self.keyfilename = keyfilename
            self.key_label.config(text=keyfilename)

    def encrypt_file(self):
        # If key file is not selected, generate a new key
        if not hasattr(self, 'keyfilename'):
            self.generate_key()
            self.keyfilename = "key.key"

        with open(self.keyfilename, "rb") as f:
            self.key = f.read()

        fernet = Fernet(self.key)

        with open(self.filename, "rb") as f:
            file_data = f.read()

        encrypted_data = fernet.encrypt(file_data)

        with open(self.filename, "wb") as f:
            f.write(encrypted_data)
        self.file_label.config(text="File Encrypted")

    def decrypt_file(self):
        if self.key is None:
            tk.messagebox.showerror("Error", "No key selected")
            return

        with open(self.filename, "rb") as f:
            encrypted_data = f.read()

        try:
            fernet = Fernet(self.key)
            decrypted_data = fernet.decrypt(encrypted_data)
        except:
            tk.messagebox.showerror("Error", "Invalid key")
        else:
            with open(self.filename, "wb") as f:
                f.write(decrypted_data)
            self.file_label.config(text="File decrypted")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()