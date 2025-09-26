import os
import shutil
import customtkinter as ctk
from customtkinter import filedialog
from folder_names import folder_names

def get_history_path():
    history_folder = "MP_history"
    history_file = "history.txt"
    file_path = os.path.join(os.path.expanduser("~"), history_folder, history_file)
    return file_path

def update_history(path, add=True):
    history_file = get_history_path()
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    
    if add:
        with open(history_file, 'a') as file:
            file.write(f"{path}\n")
    else:
        with open(history_file, 'r') as file:
            lines = file.readlines()
        with open(history_file, 'w') as file:
            file.writelines(line for line in lines if line.strip() != path)
    update_label()

def reorganize_folder(path):
    if not os.path.exists(path): return

    folders = [os.path.join(path, folder) for folder in folder_names if os.path.exists(os.path.join(path, folder))]
    
    for folder in folders:
        for root, _, files in os.walk(folder):
            for file in files:
                dest = os.path.join(path, file)
                counter = 1
                while os.path.exists(dest):
                    dest = os.path.join(path, f"{os.path.splitext(file)[0]}({counter}){os.path.splitext(file)[1]}")
                    counter += 1
                shutil.move(os.path.join(root, file), dest)

        for folder in folders:
            try: os.rmdir(folder)
            except OSError: pass

    update_history(path, add=False)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No history found"

def update_label():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    file_path = get_history_path()
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
        
        if lines:
            for path in lines:
                frame = ctk.CTkFrame(master=scrollable_frame)
                frame.pack(pady=5, fill="x", padx=5)

                ctk.CTkLabel(frame, text=path, wraplength=250).pack(side="left", padx=10)
                ctk.CTkButton(frame, text="↻ Redo", fg_color="#e17055", width=30, command=lambda p=path: reorganize_folder(p)).pack(side="right", padx=(5, 2))
        else:
            ctk.CTkLabel(scrollable_frame, text="Your organized folders are going to be here", font=("Arial", 13), text_color="grey").pack(padx=10, pady=90)
    else:
        ctk.CTkLabel(scrollable_frame, text="Organized folders are going to be shown here",text_color="grey").pack(pady=85)

def get_folder():
    folder_path = entry.get().strip()
    if folder_path and os.path.isdir(folder_path := os.path.join(os.path.expanduser("~"), folder_path)):
        return folder_path
    print("Invalid folder path!")
    return None

def choose_file():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, "end")
        entry.insert(0, folder_path)

#"Organize" button action
def button_callback():
    path = get_folder()
    if path is None: return

    for folder, ext in folder_names.items():
        files_to_move = [file for file in os.listdir(path) if os.path.splitext(file)[1].lower() in ext]
        for file in files_to_move:
            folder_path = os.path.join(path, folder)
            os.makedirs(folder_path, exist_ok=True)
            dest = os.path.join(folder_path, file)
            if not os.path.exists(dest):
                shutil.move(os.path.join(path, file), dest)
    
    update_history(path)
    update_label()

app = ctk.CTk()
app.geometry("400x425")
app.title("Organizer+")
app.resizable(False, False)
app.iconbitmap("Icon_image\iconplus.ico")

scrollable_frame = ctk.CTkScrollableFrame(app, width=325, height=200)
scrollable_frame.pack(padx=20, pady=30)

frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=5)

entry = ctk.CTkEntry(frame, placeholder_text="Enter folder name", font=("Arial", 13), height=40, width=300)
entry.pack(side="left", padx=(0, 5))

ctk.CTkButton(app, text="Organize", font=("Arial", 13, "bold"), corner_radius=10, fg_color="#0984e3", command=button_callback, height=40).pack(padx=20, pady=30)
ctk.CTkButton(frame, text="📂", fg_color="#485460", text_color="#0984e3", command=choose_file, height=40, width=40, font=("Arial", 19)).pack(side="left")

update_label()
app.mainloop()