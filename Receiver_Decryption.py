import tkinter as tk
from Cryptodome.Cipher import AES
from email.mime.multipart import MIMEMultipart
from Encrypt_and_Decrypt import decrypt_file

"""
18P5141@eng.asu.edu.eg: C\xa9\x8foQw/\xac\xeb\xfc\x9c\xdf%$n\xcc,
18P5722@eng.asu.edu.eg: x\xeb(\x02vV\xa6\xef\xb9\x00\x08\xa1G\x8f\xe8\x82,
ai.reda.mohsen@gmail.com: \x0e\x13O\x9b\xack\x89\x13s\x02\xaeS\x8f\xf0\x91\x81
"""


class ReceiverApp:
    def __init__(self):
        self.Session_Key = ""
        self.Receiver_Secret_Key = "\x0e\x13O\x9b\xack\x89\x13s\x02\xaeS\x8f\xf0\x91\x81"
        self.window = tk.Tk()
        self.window.title("Received Message Decryption")

        self.attachments = []
        self.Do_GUI()

        self.message = MIMEMultipart()

    def Do_GUI(self):
        read_button = tk.Button(self.window, text="Read Message", command=self.read_message)
        read_button.pack(pady=11)

        self.output_text = tk.Text(self.window, height=10, width=38, state=tk.DISABLED)
        self.output_text.pack()

        scrollbar = tk.Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)

    def read_message(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        with open("wrappedkey.txt", 'rb') as file:
            Encrypted_Session_Key = file.read()
            decryptor = AES.new(self.Receiver_Secret_Key.encode('utf-8'), AES.MODE_ECB)
            self.Session_Key = decryptor.decrypt(Encrypted_Session_Key)
            print(self.Session_Key)

        decrypt_file(self.Session_Key, "EncryptedBodyMessage.txt", "DecryptedMessage.txt")

        with open("DecryptedMessage.txt", "rb") as f:
            decryptedMessage = f.read()
            self.output_text.insert(tk.END, decryptedMessage)
            self.output_text.insert(tk.END, "\n\n")
        self.output_text.config(state=tk.DISABLED)

    def run(self):
        self.window.mainloop()


app = ReceiverApp()
app.run()
