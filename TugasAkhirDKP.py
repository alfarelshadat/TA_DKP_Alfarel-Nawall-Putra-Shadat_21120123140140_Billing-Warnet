from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from collections import deque
import qrcode
from PIL import Image, ImageTk

class AppBase:
    def __init__(self, root):
        self.root = root
        self.root.geometry("320x420")
        self.root.title("Billing Warnet")
        self.root.resizable(width=0, height=0)
        self.root.configure(bg='lightblue')
        
        self.prices = {
            '1 Jam': 6000,
            '2 Jam': 12000,
            '3 Jam': 16000,
            '4 Jam': 20000,
            '5 Jam': 24000,
            '6 Jam': 28000
        }
        
        self.history = []
        self.queue = deque()
        self.user_credentials = {}
        
        self.create_widgets()

    def create_widgets(self):
        self.welcome_label = Label(self.root, text="Selamat Datang!", font=("Helvetica", 20), bg='lightblue')
        self.welcome_label.pack(pady=20)
        self.welcome_label2 = Label(self.root, text="Gamers!!!", font=("Helvetica", 18), bg='lightblue')
        self.welcome_label2.pack(pady=20)
        self.welcome_label3 = Label(self.root, text="Di R9 WARNET", font=("Helvetica", 16), bg='lightblue')
        self.welcome_label3.pack(pady=20)
        
        self.next_button = Button(self.root, text="Next", command=self.show_billing_form, bg='lightgreen')
        self.next_button.pack(pady=10)

        self.exit_button = Button(self.root, text="Exit", command=self.exit_application, bg='lightcoral')
        self.exit_button.pack(pady=10)

        self.frame = Frame(self.root, bg='lightblue')

        self.label_nama = Label(self.frame, text="Name:", font=("times new roman", 10), bg='lightblue', anchor="w")
        self.label_nama.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.strnama = StringVar()
        self.entrynama = Entry(self.frame, textvariable=self.strnama, font=("times new roman", 10))
        self.entrynama.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = Label(self.frame, text="Password:", font=("times new roman", 10), bg='lightblue', anchor="w")
        self.label_password.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.strpassword = StringVar()
        self.entrypassword = Entry(self.frame, textvariable=self.strpassword, font=("times new roman", 10), show="*")
        self.entrypassword.grid(row=1, column=1, padx=5, pady=5)

        self.label_paket = Label(self.frame, text="Paket:", font=("times new roman", 10), bg='lightblue', anchor="w")
        self.label_paket.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.strpaket = StringVar(value='Pilih di sini')
        self.combobox1 = ttk.Combobox(self.frame, width=17, font=("times new roman", 10), textvariable=self.strpaket, state="readonly")
        self.combobox1.grid(row=2, column=1, padx=5, pady=5)
        self.combobox1['values'] = list(self.prices.keys())

        self.label_payment = Label(self.frame, text="Metode Pembayaran:", font=("times new roman", 10), bg='lightblue', anchor="w")
        self.label_payment.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.payment_var = StringVar(value='Cash')
        self.payment_options = ['Cash', 'Bank', 'Dana', 'OVO']
        self.payment_menu = OptionMenu(self.frame, self.payment_var, *self.payment_options)
        self.payment_menu.grid(row=3, column=1, padx=5, pady=5)

        self.billing_button = Button(self.root, text="Isi Billing", command=self.calculate_billing, bg='lightgreen')

    def show_billing_form(self):
        self.welcome_label.pack_forget()
        self.welcome_label2.pack_forget()
        self.welcome_label3.pack_forget()
        self.next_button.pack_forget()
        self.exit_button.pack_forget()
        self.frame.pack(pady=10)
        self.billing_button.pack(pady=10)
        self.exit_button.pack(pady=10)

    def calculate_billing(self):
        nama = self.strnama.get()
        password = self.strpassword.get()
        paket = self.strpaket.get()

        if not nama or not password:
            messagebox.showwarning("Peringatan", "Nama dan password harus diisi")
            return
        if nama in self.user_credentials and self.user_credentials[nama] != password:
            messagebox.showwarning("Peringatan", "Password salah untuk nama pengguna ini")
            return
        
        self.user_credentials[nama] = password  

        if paket in self.prices:
            harga = self.prices[paket]
            self.history.append((nama, paket))
            self.queue.append((nama, paket))
            payment_method = self.payment_var.get()
            message = f"Harga untuk {paket} adalah Rp{harga}\nMetode Pembayaran: {payment_method}"
            if payment_method == 'Cash':
                message += "\nSilahkan pergi ke kasir untuk membayar."
                messagebox.showinfo("Harga Billing", message)
            else:
                self.generate_qr_code(message)
        else:
            messagebox.showwarning("Peringatan", "Pilih paket yang valid")

    def generate_qr_code(self, data):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        self.qr_img = ImageTk.PhotoImage(img)

        self.show_qr_code_popup(data)

    def show_qr_code_popup(self, message):
        popup = Toplevel(self.root)
        popup.title("QR Code Pembayaran")
        popup.geometry("300x400")
        popup.configure(bg='lightblue')

        label_message = Label(popup, text=message, font=("Helvetica", 10), bg='lightblue')
        label_message.pack(pady=10)

        qr_label = Label(popup, image=self.qr_img, bg='lightblue')
        qr_label.pack(pady=10)

        button_ok = Button(popup, text="OK", command=popup.destroy, bg='lightgreen')
        button_ok.pack(pady=10)

    def exit_application(self):
        self.root.quit()

class BillingApp(AppBase):
    def __init__(self, root):
        super().__init__(root)
        
    def show_history(self):
        if self.history:
            history_message = "\n".join([f"{nama} - {paket}" for nama, paket in self.history])
            messagebox.showinfo("History", f"Riwayat paket yang dipilih:\n{history_message}")
        else:
            messagebox.showinfo("History", "Belum ada paket yang dipilih.")

    def show_queue(self):
        if self.queue:
            queue_message = "\n".join([f"{nama} - {paket}" for nama, paket in self.queue])
            messagebox.showinfo("Queue", f"Pengguna dalam antrian:\n{queue_message}")
        else:
            messagebox.showinfo("Queue", "Tidak ada pengguna dalam antrian.")

    def clear_queue(self):
        self.queue.clear()
        messagebox.showinfo("Queue", "Antrian telah dikosongkan.")

    def create_widgets(self):
        super().create_widgets()
        self.history_button = Button(self.root, text="Show History", command=self.show_history, bg='lightblue')
        self.history_button.pack(pady=10)
        self.queue_button = Button(self.root, text="Show Queue", command=self.show_queue, bg='lightblue')
        self.queue_button.pack(pady=10)
        self.clear_queue_button = Button(self.root, text="Clear Queue", command=self.clear_queue, bg='lightblue')
        self.clear_queue_button.pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    app = BillingApp(root)
    root.mainloop()
