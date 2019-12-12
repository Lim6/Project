from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
#Handles the socket connection
BUFSIZ = 1024
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("localhost", 1234))

def receive(): # Handles receiving the messages
    
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  
            break


def send(event=None):  # Handles sending the messages.
    
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "/quit":
        client_socket.close()
        top.quit()
    elif msg == "/shrug":
        msg = "ʅ（◞‿◟）ʃ"
        client_socket.send(bytes(msg, "utf8"))

    elif msg == "/weirdo":
        msg = "( ͡° ͜ʖ ͡°)"
        client_socket.send(bytes(msg, "utf8"))
     
    elif msg == "/smile" :
        msg = "•ᴗ•"
        client_socket.send(bytes(msg, "utf8"))
    elif msg == "/nani" :
        msg = "ლ(ಠ_ಠლ)"
        client_socket.send(bytes(msg, "utf8"))

def on_closing(event=None): # This is called when the window is closed.
   
    my_msg.set("/quit")
    send()
# This creates the GUI
top = tkinter.Tk()
top.title("WebChat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  
# This sets the size of the GUI
msg_list = tkinter.Listbox(messages_frame, height=40, width=130, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
# This creates the message bar and also the send and quit button
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
quit_button = tkinter.Button(top, text = "Quit", command = on_closing)
quit_button.pack()


top.protocol("WM_DELETE_WINDOW", on_closing)





# Handles receiving the server and also starts the GUI
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  
