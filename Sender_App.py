import tkinter as tk
import tkinter.font as tkFont
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import socket
import time
from Cryptodome.Cipher import AES
import os
from Encrypt_and_Decrypt import encrypt_file


class App:
    sender = "18P5141@eng.asu.edu.eg"
    password = "XXXXXXXX"   # Enter password before run
    tovar = ""
    Sender_Encrypted_Session_Key = ""
    Receiver_Encrypted_Session_Key = ""
    Session_Key = ""

    def __init__(self, root):
        # setting title
        self.to_var = tk.StringVar()
        root.title("Secure Mail Composer")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times', size=12)

        # Creating and placing GUI widgets
        label_To = tk.Label(root)
        label_To["font"] = ft
        label_To["fg"] = "#333333"
        label_To["justify"] = "right"
        label_To["text"] = "To:"
        label_To.place(x=40, y=40, width=70, height=25)

        label_Subject = tk.Label(root)
        label_Subject["font"] = ft
        label_Subject["fg"] = "#333333"
        label_Subject["justify"] = "right"
        label_Subject["text"] = "Subject:"
        label_Subject.place(x=40, y=90, width=70, height=25)

        self.email_To = tk.Entry(root, textvariable=self.to_var)
        self.email_To["borderwidth"] = "1px"
        self.email_To["font"] = ft
        self.email_To["fg"] = "#333333"
        self.email_To["justify"] = "left"
        self.email_To["text"] = "To"
        self.email_To.place(x=120, y=40, width=420, height=30)

        self.email_Subject = tk.Entry(root)
        self.email_Subject["borderwidth"] = "1px"
        self.email_Subject["font"] = ft
        self.email_Subject["fg"] = "#333333"
        self.email_Subject["justify"] = "left"
        self.email_Subject["text"] = "Subject"
        self.email_Subject.place(x=120, y=90, width=417, height=30)

        self.email_Body = tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=50, y=140, width=500, height=302)

        button_Send = tk.Button(root)
        button_Send["bg"] = "#f0f0f0"
        button_Send["font"] = ft
        button_Send["fg"] = "#000000"
        button_Send["justify"] = "center"
        button_Send["text"] = "Send"
        button_Send.place(x=470, y=460, width=70, height=25)
        button_Send["command"] = self.button_Send_command

    def send_email(self, subject, body, attach, receiver):
        """
        Sends the email with encrypted body and attachment to the recipient.
        """

        # Establish connection with the KDS
        # to get the encrypted session keys
        self.Connect_and_Get_Session_Key_From_KDS(10000, self.sender, receiver)     # localhost:10000
        decryptor = AES.new(attach.encode('utf-8'), AES.MODE_ECB)
        # Decrypt the encrypted session key using the secret key of the sender
        self.Session_Key = decryptor.decrypt(self.Sender_Encrypted_Session_Key)
        print("Session Key:")
        print(self.Session_Key)

        # Write the receiver's secret key to a file
        with open("wrappedkey.txt", "wb") as f:
            f.write(self.Receiver_Encrypted_Session_Key)

        # Read the receiver's session key from a file
        with open("wrappedkey.txt", "rb") as f:
            key = f.read()

        # Write the email body to a file
        # Encrypt it with the received session key obtained from the KDS
        with open("body.txt", "wb") as f:
            f.write(body.encode("utf-8"))
        encrypt_file(self.Session_Key, "body.txt", "EncryptedBodyMessage.txt")
        with open("EncryptedBodyMessage.txt", "rb") as f:
            file_contents = f.read()
        os.remove("body.txt")

        # Create and attach the email message
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = receiver
        msg.attach(MIMEText(
            "The message content is in the [EncryptedBodyMessage.txt]."
            "You can use [wrappedkey.txt] to Decrypt and read the real message body!",
            'plain'))
        part = MIMEApplication(file_contents)
        part['Content-Disposition'] = f'attachment; filename={os.path.basename("EncryptedBodyMessage.txt")}'
        msg.attach(part)
        part = MIMEApplication(key)
        part['Content-Disposition'] = f'attachment; filename={os.path.basename("wrappedkey.txt")}'
        part['Content-Disposition'] = 'attachment; filename=wrappedkey.txt'
        msg.attach(part)

        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        print("Connected")
        smtp_server.starttls()
        print("TLS OK")
        smtp_server.login(self.sender, self.password)
        print("login OK")
        smtp_server.sendmail(self.sender, receiver, msg.as_string())
        print("mail sent")
        smtp_server.quit()

    def button_Send_command(self):
        """
        Callback function for the "Send" button.
        Retrieves email details and calls send_email method.
        """

        tovar = self.email_To.get()
        print(tovar)
        subject = self.email_Subject.get()
        body = self.email_Body.get("1.0", "end")
        Sender_Secret_Key = 'C\xa9\x8foQw/\xac\xeb\xfc\x9c\xdf%$n\xcc'
        self.send_email(subject, body, Sender_Secret_Key, tovar)

    def Connect_and_Get_Session_Key_From_KDS(self, PORT, Sender_ID, Receiver_ID):
        """
        Establishes a connection with the Key Distribution Server (KDS)
        and retrieves encrypted session keys for sender and receiver.
        """

        # Create a socket object
        Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address
        Server_Address = ('localhost', PORT)

        Key_Received_Status = False

        try:
            # Start Connection With Server
            Client_Socket.connect(Server_Address)
            print("Connected to PORT", PORT)
            data = Client_Socket.recv(2048)

            # Send the Emails to the KDS
            Client_Socket.send(Sender_ID.encode('utf-8'))   # Send sender id to KDS
            time.sleep(1)
            Client_Socket.send(Receiver_ID.encode('utf-8'))   # Send receiver id to KDS

            counter = 0
            # Receive the encrypted session keys from the KDS
            while not Key_Received_Status:
                data = Client_Socket.recv(2048)
                if counter == 0:
                    print(data)
                    self.Sender_Encrypted_Session_Key = data    # Receive sender session key
                    counter += 1
                elif counter == 1:
                    print(data)
                    self.Receiver_Encrypted_Session_Key = data  # Receive receiver session key
                    Key_Received_Status = True

            # Close the Connection
            Client_Socket.close()
            print("Connection Closed")
        except ConnectionRefusedError:
            print("Connection Error!")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
