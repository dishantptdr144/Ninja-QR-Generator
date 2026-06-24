
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from urllib.parse import quote
import qrcode
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NinjaQR:
    def __init__(self, root):
        self.root = root
        self.root.title("NINJA QR GENERATOR")
        self.root.geometry("1000x600")

        self.qr_image = None
        self.qr_color = "#000000"
        self.bg_color = "#FFFFFF"

        title = ctk.CTkLabel(root, text="⚡ NINJA QR GENERATOR", font=("Segoe UI", 28, "bold"))
        title.pack(pady=15)

        self.mode = ctk.StringVar(value="Custom QR")

        top = ctk.CTkFrame(root)
        top.pack(fill="x", padx=15)

        ctk.CTkOptionMenu(
            top,
            values=["Custom QR", "UPI QR"],
            variable=self.mode,
            command=lambda x: self.switch_mode()
        ).pack(side="left", padx=10, pady=10)

        body = ctk.CTkFrame(root)
        body.pack(fill="both", expand=True, padx=15, pady=15)

        self.left = ctk.CTkFrame(body)
        self.left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right = ctk.CTkFrame(body)
        self.right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.custom_frame = ctk.CTkFrame(self.left)
        self.upi_frame = ctk.CTkFrame(self.left)

        ctk.CTkLabel(self.custom_frame, text="URL / Text").pack(anchor="w", padx=15, pady=(15,5))
        self.custom_text = ctk.CTkEntry(self.custom_frame, width=400)
        self.custom_text.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(self.upi_frame, text="UPI ID *").pack(anchor="w", padx=15, pady=(15,5))
        self.upi_id = ctk.CTkEntry(self.upi_frame)
        self.upi_id.pack(fill="x", padx=15)

        ctk.CTkLabel(self.upi_frame, text="Name (Optional)").pack(anchor="w", padx=15, pady=(10,5))
        self.upi_name = ctk.CTkEntry(self.upi_frame)
        self.upi_name.pack(fill="x", padx=15)

        ctk.CTkLabel(self.upi_frame, text="Amount (Optional)").pack(anchor="w", padx=15, pady=(10,5))
        self.upi_amount = ctk.CTkEntry(self.upi_frame)
        self.upi_amount.pack(fill="x", padx=15)

        ctk.CTkLabel(self.upi_frame, text="Note (Optional)").pack(anchor="w", padx=15, pady=(10,5))
        self.upi_note = ctk.CTkEntry(self.upi_frame)
        self.upi_note.pack(fill="x", padx=15)

        btn_frame = ctk.CTkFrame(self.left)
        btn_frame.pack(fill="x", padx=10, pady=15)

        ctk.CTkButton(btn_frame, text="🎨 QR Color", command=self.pick_qr).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🖼 Background", command=self.pick_bg).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="⚡ Generate", command=self.generate).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="💾 Save", command=self.save).pack(side="left", padx=5)

        self.preview = ctk.CTkLabel(self.right, text="QR Preview")
        self.preview.pack(expand=True)

        self.switch_mode()

    def switch_mode(self):
        self.custom_frame.pack_forget()
        self.upi_frame.pack_forget()

        if self.mode.get() == "Custom QR":
            self.custom_frame.pack(fill="x", padx=10, pady=10)
        else:
            self.upi_frame.pack(fill="x", padx=10, pady=10)

    def pick_qr(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.qr_color = c

    def pick_bg(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.bg_color = c

    def get_data(self):
        if self.mode.get() == "Custom QR":
            return self.custom_text.get().strip()

        upi = self.upi_id.get().strip()
        if not upi:
            raise ValueError("UPI ID required")

        data = f"upi://pay?pa={quote(upi)}"

        if self.upi_name.get().strip():
            data += f"&pn={quote(self.upi_name.get().strip())}"

        if self.upi_amount.get().strip():
            data += f"&am={self.upi_amount.get().strip()}"

        if self.upi_note.get().strip():
            data += f"&tn={quote(self.upi_note.get().strip())}"

        return data

    def generate(self):
        try:
            data = self.get_data()
            if not data:
                raise ValueError("Enter data first")

            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=12,
                border=4
            )
            qr.add_data(data)
            qr.make(fit=True)

            self.qr_image = qr.make_image(
                fill_color=self.qr_color,
                back_color=self.bg_color
            ).convert("RGB")

            img = self.qr_image.resize((320, 320))

            self.ctk_image = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(320, 320)
            )
            
            self.preview.configure(
                image=self.ctk_image,
                text=""
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save(self):
        if self.qr_image is None:
            messagebox.showerror("Error", "Generate QR first")
            return

        path = filedialog.asksaveasfilename(
            initialfile="QR GENERATED BY NINJA TOOL.png",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")]
        )

        if path:
            self.qr_image.save(path)
            messagebox.showinfo("Success", "QR saved successfully")

root = ctk.CTk()
app = NinjaQR(root)
root.mainloop()
