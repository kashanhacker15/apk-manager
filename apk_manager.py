import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import os
import shutil
from PIL import Image, ImageTk

# folders
if not os.path.exists("apk_store"):
    os.makedirs("apk_store")

if not os.path.exists("icons"):
    os.makedirs("icons")

# database
conn = sqlite3.connect("apk_manager.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS apps(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
apk TEXT,
icon TEXT,
downloads INTEGER DEFAULT 0
)
""")

conn.commit()

# login system
def login():
    user = username.get()
    pw = password.get()

    if user == "admin" and pw == "admin123":
        login_frame.pack_forget()
        dashboard.pack()
        load_apps()
    else:
        messagebox.showerror("Login Failed","Wrong credentials")

# upload APK
def upload_apk():
    name = app_name.get()

    apk_path = filedialog.askopenfilename(filetypes=[("APK Files","*.apk")])
    icon_path = filedialog.askopenfilename(filetypes=[("Image Files","*.png *.jpg")])

    if apk_path == "":
        return

    apk_name = os.path.basename(apk_path)
    icon_name = os.path.basename(icon_path)

    shutil.copy(apk_path,"apk_store/"+apk_name)
    shutil.copy(icon_path,"icons/"+icon_name)

    cursor.execute("INSERT INTO apps(name,apk,icon) VALUES(?,?,?)",(name,apk_name,icon_name))
    conn.commit()

    load_apps()

# load apps
def load_apps():

    for widget in app_list.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM apps")

    for row in cursor.fetchall():

        frame = tk.Frame(app_list,bg="#1e293b")
        frame.pack(fill="x",pady=5)

        icon_path = "icons/"+row[3]

        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            img = img.resize((40,40))
            photo = ImageTk.PhotoImage(img)

            label_img = tk.Label(frame,image=photo)
            label_img.image = photo
            label_img.pack(side="left",padx=5)

        tk.Label(frame,text=row[1],bg="#1e293b",fg="white").pack(side="left",padx=10)

        tk.Label(frame,text="Downloads: "+str(row[4]),bg="#1e293b",fg="white").pack(side="left",padx=10)

        tk.Button(frame,text="Download",command=lambda r=row:download_app(r)).pack(side="right")

# download function
def download_app(row):

    cursor.execute("UPDATE apps SET downloads = downloads + 1 WHERE id=?",(row[0],))
    conn.commit()

    messagebox.showinfo("Download","APK saved in apk_store folder")

    load_apps()

# search
def search_app():

    key = search_box.get()

    for widget in app_list.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM apps WHERE name LIKE ?",('%'+key+'%',))

    for row in cursor.fetchall():

        frame = tk.Frame(app_list,bg="#1e293b")
        frame.pack(fill="x",pady=5)

        tk.Label(frame,text=row[1],bg="#1e293b",fg="white").pack(side="left",padx=10)

        tk.Button(frame,text="Download",command=lambda r=row:download_app(r)).pack(side="right")

# main window
root = tk.Tk()
root.title("Professional APK Manager")
root.geometry("800x600")
root.configure(bg="#0f172a")

# login frame
login_frame = tk.Frame(root,bg="#0f172a")
login_frame.pack()

tk.Label(login_frame,text="Admin Login",font=("Arial",20),bg="#0f172a",fg="white").pack(pady=20)

username = tk.Entry(login_frame)
username.pack(pady=5)
username.insert(0,"admin")

password = tk.Entry(login_frame,show="*")
password.pack(pady=5)

tk.Button(login_frame,text="Login",command=login).pack(pady=10)

# dashboard
dashboard = tk.Frame(root,bg="#0f172a")

top = tk.Frame(dashboard,bg="#0f172a")
top.pack()

app_name = tk.Entry(top,width=30)
app_name.pack(side="left",padx=5)
app_name.insert(0,"App Name")

tk.Button(top,text="Upload APK",command=upload_apk).pack(side="left")

search_box = tk.Entry(top,width=20)
search_box.pack(side="left",padx=10)

tk.Button(top,text="Search",command=search_app).pack(side="left")

# app list
app_list = tk.Frame(dashboard,bg="#0f172a")
app_list.pack(fill="both",expand=True,pady=20)

root.mainloop()