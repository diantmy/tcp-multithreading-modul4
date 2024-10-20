import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Fungsi untuk menerima pesan dari server
def receive_messages(client_socket, text_area, status_label, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Jika pesan dari klien sendiri, tampilkan di sebelah kanan
                if message.startswith(client_name):
                    display_message(text_area, message, "right")
                else:
                    display_message(text_area, message, "left")
        except:
            status_label.config(text="Disconnected from the server", fg="red")
            print("Connection closed by the server.")
            break

# Fungsi untuk mengirim pesan ke server
def send_message(client_socket, entry, client_name, text_area):
    message = entry.get()
    if message:
        try:
            # Kirim pesan ke server
            client_socket.send(message.encode('utf-8'))
            # Tampilkan pesan klien sendiri di GUI (sebelah kanan)
            display_message(text_area, f"{client_name}: {message}", "right")
            entry.delete(0, tk.END)  # Kosongkan input setelah pesan dikirim
        except:
            display_message(text_area, "Failed to send message. You are disconnected.", "center")

# Fungsi untuk menampilkan pesan di GUI dengan posisi berbeda
def display_message(text_area, message, alignment):
    text_area.config(state=tk.NORMAL)
    
    # Tampilkan pesan dengan perataan sesuai: 'left' atau 'right'
    if alignment == "left":
        text_area.insert(tk.END, message + '\n', 'left')
    elif alignment == "right":
        text_area.insert(tk.END, message + '\n', 'right')
    else:
        text_area.insert(tk.END, message + '\n')

    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

# Fungsi untuk memutus koneksi dengan server
def disconnect_client(client_socket, status_label):
    try:
        client_socket.close()
        status_label.config(text="Disconnected", fg="red")
        messagebox.showinfo("Disconnected", "You have been disconnected from the server.")
    except:
        messagebox.showwarning("Error", "Failed to disconnect.")

# Fungsi untuk menginisialisasi GUI klien
def start_client_gui(client_name, server_ip='127.0.0.1', server_port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        client_socket.send(client_name.encode('utf-8'))

        # Inisialisasi GUI
        window = tk.Tk()
        window.title(f"Client - {client_name}")

        # Label Status Koneksi
        status_label = tk.Label(window, text="Connected", fg="green")
        status_label.pack(padx=10, pady=5)

        # Area untuk menampilkan pesan
        text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
        text_area.config(state=tk.DISABLED)
        text_area.pack(padx=20, pady=5)

        # Tambahkan tag untuk perataan kiri dan kanan
        text_area.tag_config('left', justify='left')
        text_area.tag_config('right', justify='right')

        # Field input untuk menulis pesan
        message_entry = tk.Entry(window, width=50)
        message_entry.pack(padx=20, pady=5)
        message_entry.focus_set()

        # Tombol untuk mengirim pesan
        send_button = tk.Button(window, text="Send", command=lambda: send_message(client_socket, message_entry, client_name, text_area))
        send_button.pack(padx=20, pady=5)

        # Tombol untuk memutus koneksi
        disconnect_button = tk.Button(window, text="Disconnect", command=lambda: disconnect_client(client_socket, status_label))
        disconnect_button.pack(padx=20, pady=5)

        # Mengirim pesan dengan tombol Enter
        window.bind('<Return>', lambda event: send_message(client_socket, message_entry, client_name, text_area))

        # Thread untuk menerima pesan dari server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, text_area, status_label, client_name))
        receive_thread.start()

        # Jalankan GUI
        window.mainloop()

    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        messagebox.showerror("Connection Error", f"Failed to connect to the server: {e}")

if __name__ == "__main__":
    # Ambil nama klien dari input pengguna
    client_name = input("Enter your name: ")
    start_client_gui(client_name)
