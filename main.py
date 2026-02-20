import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys

# ======================================================
# 🔥 企业品牌配置区域（后期只需修改这里）
# ======================================================

ACTIVE_COMPANY = "default"

COMPANY_PROFILE = {
    "default": {
        "designer": "AGRAYSON",
        "company_cn": "知枢科技",
        "company_en": "WisdomHub Intelligent Technology Co., Ltd",
        "email": "wishubinttech@gmail.com",
        "license_key": "GC-WIT-FREESHARE"
    },
}

PROFILE = COMPANY_PROFILE[ACTIVE_COMPANY]

APP_NAME = "Icon Generator Pro"
VERSION = "v4.2 Enterprise"
LICENSE_FILE = "license.dat"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# ======================================================
# 🔐 授权窗口
# ======================================================

class LicenseWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("软件授权验证")
        self.geometry("520x380")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.create_ui()

    def create_ui(self):

        title = ctk.CTkLabel(self, text="软件授权验证", font=("Segoe UI", 22, "bold"))
        title.pack(pady=25)

        info = ctk.CTkLabel(
            self,
            text=f"{PROFILE['company_cn']}\n{PROFILE['company_en']}\nDesigner: {PROFILE['designer']}\nEmail: {PROFILE['email']}",
            justify="center"
        )
        info.pack(pady=10)

        self.entry = ctk.CTkEntry(self, width=340, placeholder_text="请输入授权码")
        self.entry.pack(pady=25)

        self.result = ctk.CTkLabel(self, text="")
        self.result.pack()

        btn = ctk.CTkButton(self, text="验证授权", command=self.verify)
        btn.pack(pady=15)

    def verify(self):
        key = self.entry.get().strip()
        if key == PROFILE["license_key"]:
            with open(LICENSE_FILE, "w") as f:
                f.write("activated")
            self.after(600, self.success)
        else:
            self.result.configure(text="授权码错误 ❌", text_color="red")

    def success(self):
        self.destroy()
        self.parent.deiconify()

    def close_app(self):
        self.parent.destroy()
        sys.exit()


# ======================================================
# 主程序
# ======================================================

class IconGeneratorApp(ctk.CTk):

    WIN_SIZES = [16, 24, 32, 48, 64, 128, 256]

    def __init__(self):
        super().__init__()

        self.title(f"{APP_NAME} {VERSION}")

        self.geometry("900x950")
        self.minsize(850, 900)

        self.withdraw()

        self.logo_path = ""
        self.output_dir = ""
        self.lang = "CN"

        self.size_vars = {}

        self.create_ui()
        self.after(200, self.check_license)

    # ======================================================

    def check_license(self):
        if os.path.exists(LICENSE_FILE):
            self.deiconify()
        else:
            LicenseWindow(self)

    # ======================================================

    def create_ui(self):

        title = ctk.CTkLabel(self, text=f"{APP_NAME} {VERSION}", font=("Segoe UI", 24, "bold"))
        title.pack(pady=12)

        company = ctk.CTkLabel(
            self,
            text=f"{PROFILE['designer']}\n"
                 f"{PROFILE['company_cn']}\n"
                 f"{PROFILE['company_en']}\n"
                 f"{PROFILE['email']}",
            justify="center"
        )
        company.pack(pady=8)

        self.card = ctk.CTkFrame(self, corner_radius=20)
        self.card.pack(padx=18, pady=10, fill="both", expand=True)

        self.lang_btn = ctk.CTkButton(self.card, text="English", width=90, command=self.switch_language)
        self.lang_btn.pack(anchor="ne", padx=10, pady=8)

        self.logo_btn = ctk.CTkButton(self.card, text="选择高清LOGO", command=self.select_logo)
        self.logo_btn.pack(pady=8)

        self.preview = ctk.CTkLabel(self.card, text="图标预览", width=200, height=200)
        self.preview.pack(pady=8)

        self.output_btn = ctk.CTkButton(self.card, text="选择输出目录", command=self.select_output)
        self.output_btn.pack(pady=8)

        # 尺寸区域
        size_frame = ctk.CTkFrame(self.card, corner_radius=15)
        size_frame.pack(pady=12)

        size_title = ctk.CTkLabel(size_frame, text="Win11 常用尺寸")
        size_title.pack(pady=4)

        grid_frame = ctk.CTkFrame(size_frame)
        grid_frame.pack(pady=6)

        for i, size in enumerate(self.WIN_SIZES):
            var = ctk.BooleanVar()
            self.size_vars[size] = var

            cb = ctk.CTkCheckBox(
                grid_frame,
                text=f"{size}x{size}",
                variable=var
            )
            cb.grid(row=i // 4, column=i % 4, padx=12, pady=6)

        # 自定义尺寸
        custom_frame = ctk.CTkFrame(self.card, corner_radius=15)
        custom_frame.pack(pady=12)

        custom_label = ctk.CTkLabel(custom_frame, text="自定义尺寸")
        custom_label.pack(pady=4)

        self.width_entry = ctk.CTkEntry(custom_frame, width=90, placeholder_text="宽度")
        self.width_entry.pack(side="left", padx=5, pady=6)

        self.height_entry = ctk.CTkEntry(custom_frame, width=90, placeholder_text="高度")
        self.height_entry.pack(side="left", padx=5, pady=6)

        self.keep_ratio = ctk.BooleanVar(value=True)
        self.keep_ratio_check = ctk.CTkCheckBox(
            custom_frame,
            text="保持比例（透明填充）",
            variable=self.keep_ratio
        )
        self.keep_ratio_check.pack(side="left", padx=10)

        self.progress = ctk.CTkProgressBar(self.card)
        self.progress.pack(pady=12)
        self.progress.set(0)

        # 批量生成 PNG
        self.generate_btn = ctk.CTkButton(
            self.card,
            text="🔥 批量生成图标",
            height=50,
            command=self.generate_icons
        )
        self.generate_btn.pack(pady=16)

        # 自动化生成 ICO（不弹窗）
        self.ico_btn = ctk.CTkButton(
            self.card,
            text="💎 自动生成多尺寸 ICO",
            height=40,
            command=self.generate_ico_auto
        )
        self.ico_btn.pack(pady=8)

        # 状态栏
        self.status = ctk.CTkLabel(self, text="状态：等待操作", anchor="w")
        self.status.pack(side="bottom", fill="x", padx=10, pady=5)

    # ======================================================

    def switch_language(self):
        if self.lang == "CN":
            self.lang = "EN"
            self.logo_btn.configure(text="Select Logo")
            self.output_btn.configure(text="Select Output Folder")
            self.keep_ratio_check.configure(text="Keep Aspect Ratio (Transparent Fill)")
            self.generate_btn.configure(text="🔥 Generate Icons")
            self.ico_btn.configure(text="💎 Auto Generate Multi-size ICO")
            self.lang_btn.configure(text="中文")
        else:
            self.lang = "CN"
            self.logo_btn.configure(text="选择高清LOGO")
            self.output_btn.configure(text="选择输出目录")
            self.keep_ratio_check.configure(text="保持比例（透明填充）")
            self.generate_btn.configure(text="🔥 批量生成图标")
            self.ico_btn.configure(text="💎 自动生成多尺寸 ICO")
            self.lang_btn.configure(text="English")

    # ======================================================

    def select_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.logo_path = path
            img = Image.open(path)
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.preview.configure(image=photo, text="")
            self.preview.image = photo

    def select_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir = path

    # ======================================================
    # 批量生成 PNG
    # ======================================================
    def generate_icons(self):

        if not self.logo_path or not self.output_dir:
            messagebox.showerror("错误", "请选择LOGO和输出目录")
            return

        img = Image.open(self.logo_path).convert("RGBA")

        selected_sizes = [size for size, var in self.size_vars.items() if var.get()]

        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            selected_sizes.append((w, h))
        except:
            pass

        if not selected_sizes:
            messagebox.showerror("错误", "请至少选择一个尺寸")
            return

        total = len(selected_sizes)
        step = 1 / total
        self.progress.set(0)

        for item in selected_sizes:

            if isinstance(item, tuple):
                width, height = item
            else:
                width = height = item

            if self.keep_ratio.get():
                temp = img.copy()
                temp.thumbnail((width, height))
                background = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                x = (width - temp.width) // 2
                y = (height - temp.height) // 2
                background.paste(temp, (x, y))
                result = background
            else:
                result = img.resize((width, height))

            save_path = os.path.join(self.output_dir, f"icon_{width}x{height}.png")
            result.save(save_path)

            self.progress.set(self.progress.get() + step)
            self.update()

        self.status.configure(text="状态：全部生成完成")
        messagebox.showinfo("成功", "所有尺寸生成完成")

    # ======================================================
    # 自动化生成 ICO（无需弹窗）
    # ======================================================
    def generate_ico_auto(self):
        if not self.logo_path or not self.output_dir:
            messagebox.showerror("错误", "请先选择图片和输出目录")
            return
        try:
            img = Image.open(self.logo_path).convert("RGBA")
            save_path = os.path.join(self.output_dir, "icon.ico")
            sizes = [(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]
            img.save(save_path, format="ICO", sizes=sizes)
            self.status.configure(text=f"状态：ICO 文件已生成 → icon.ico")
            messagebox.showinfo("成功", f"ICO 文件已生成：\n{save_path}")
        except Exception as e:
            messagebox.showerror("错误", f"生成 ICO 失败:\n{e}")
            print("生成 ICO 异常：", e)


# ======================================================
# 启动程序
# ======================================================
if __name__ == "__main__":
    app = IconGeneratorApp()
    app.mainloop()
