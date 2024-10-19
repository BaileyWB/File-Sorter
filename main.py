import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def browse_directory():
    global source_directory
    source_directory = filedialog.askdirectory()
    list_files()

def list_files():
    file_list.delete(0, tk.END)
    for filename in os.listdir(source_directory):
        file_list.insert(tk.END, filename)

def sort_selected_files():
    selected_files = file_list.curselection()
    for index in selected_files:
        filename = file_list.get(index)
        file_extension = filename.split('.')[-1].lower()
        if file_extension in categories['Documents']:
            destination_category = "Documents"
        elif file_extension in categories['Images']:
            destination_category = "Images"
        elif file_extension in categories['Music']:
            destination_category = "Music"
        elif file_extension in categories['Videos']:
            destination_category = "Videos"
        elif "clip" in filename.lower() or "medal" in filename.lower():
            destination_category = "Clips"
        else:
            continue
        
        destination_dir = os.path.join(source_directory, destination_category)
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)
        
        source_file_path = os.path.join(source_directory, filename)
        destination_file_path = os.path.join(destination_dir, filename)
        if not os.path.exists(destination_file_path):
            shutil.move(source_file_path, destination_file_path)
    
    list_files()

def delete_folder_or_file():
    selected_item = file_list.get(tk.ACTIVE)
    selected_item_path = os.path.join(source_directory, selected_item)
    
    if os.path.isfile(selected_item_path):
        os.remove(selected_item_path)
    elif os.path.isdir(selected_item_path):
        shutil.rmtree(selected_item_path)
    
    list_files()

def create_folder():
    new_folder_name = simpledialog.askstring("Create Folder", "Enter the name for the new folder:")
    if new_folder_name:
        new_folder_path = os.path.join(source_directory, new_folder_name)
        os.mkdir(new_folder_path)
        list_files()

def move_folder():
    source_folder = filedialog.askdirectory(title="Select Folder to Move")
    if source_folder:
        destination_folder = filedialog.askdirectory(title="Select Destination Folder")
        if destination_folder:
            shutil.move(source_folder, destination_folder)
            list_files()

def get_storage_info():
    ssd_usage = shutil.disk_usage(os.path.splitdrive(source_directory)[0])
    hard_drive_usage = shutil.disk_usage(os.path.splitdrive(source_directory)[1])

    ssd_total = ssd_usage.total / (1024 ** 3)
    ssd_used = ssd_usage.used / (1024 ** 3)
    ssd_free = ssd_usage.free / (1024 ** 3)

    hard_drive_total = hard_drive_usage.total / (1024 ** 3)
    hard_drive_used = hard_drive_usage.used / (1024 ** 3)
    hard_drive_free = hard_drive_usage.free / (1024 ** 3)

    storage_info = f"SSD:\nTotal: {ssd_total:.2f} GB\nUsed: {ssd_used:.2f} GB\nFree: {ssd_free:.2f} GB\n\n" \
                   f"Hard Drive:\nTotal: {hard_drive_total:.2f} GB\nUsed: {hard_drive_used:.2f} GB\nFree: {hard_drive_free:.2f} GB"

    messagebox.showinfo("Storage Information", storage_info)

# Initialize the main window
root = tk.Tk()
root.title("Automated File Sorter")

# Create buttons
browse_button = tk.Button(root, text="Browse Directory", command=browse_directory)
sort_button = tk.Button(root, text="Sort Selected Files", command=sort_selected_files)
delete_button = tk.Button(root, text="Delete Folder/File", command=delete_folder_or_file)
create_folder_button = tk.Button(root, text="Create Folder", command=create_folder)
move_folder_button = tk.Button(root, text="Move Folder", command=move_folder)
storage_info_button = tk.Button(root, text="Storage Info", command=get_storage_info)  # New button for storage info

# Create file list
file_list = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=15)

# Arrange widgets using grid layout
browse_button.grid(row=0, column=0, padx=10, pady=10)
sort_button.grid(row=1, column=0, padx=10, pady=5)
delete_button.grid(row=2, column=0, padx=10, pady=5)
create_folder_button.grid(row=3, column=0, padx=10, pady=5)
move_folder_button.grid(row=4, column=0, padx=10, pady=5)
storage_info_button.grid(row=5, column=0, padx=10, pady=5)  # Position the storage info button
file_list.grid(row=0, column=1, rowspan=6, padx=10, pady=5)  # Adjust rowspan for the file list

# Define file categories
categories = {
    "Documents": ["pdf", "doc", "txt"],
    "Images": ["jpg", "png", "gif"],
    "Music": ["mp3", "wav"],
    "Videos": ["mp4", "avi", "mkv"]
}

source_directory = ""

root.mainloop()
