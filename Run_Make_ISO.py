import os

try:
    import gdown
except:
    os.system("pip install gdown")
    import gdown


def get_folder_files_bytes(dir_path):
    folder_count = 0
    file_count = 0
    total_size = 0
    for root, dirs, files in os.walk(dir_path):
        folder_count += len(dirs)
        file_count += len(files)
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return folder_count, file_count, total_size


folder2iso_pathraw = r"D:/Folder2Iso.exe"
folder2iso_path = r"D:/Folder2Iso/Folder2Iso.exe"


def downloadexe():
    if not os.path.exists(folder2iso_path):
        url_exe = "https://drive.google.com/uc?id=0B7nKMWPhyfl-SlVoWXprWkhHR2c&export=download"
        output_dir = os.path.dirname(folder2iso_pathraw)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Tải file về đường dẫn folder2iso_path
        gdown.download(url_exe, folder2iso_pathraw, quiet=False)
        os.startfile(folder2iso_path)


if __name__ == "__main__":
    # Gọi hàm để tải file nếu chưa tồn tại
    downloadexe()

    # Đường dẫn tới Folder2Iso và thư mục gốc
    root_dir = os.getcwd()
    output_file = f"{root_dir}/create_iso.bat"

    # Tạo file batch
    with open(output_file, "w", encoding="utf-8") as batch_file:
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            # Kiểm tra nếu folder_path là một thư mục
            if os.path.isdir(folder_path):
                folder_count, file_count, total_size = get_folder_files_bytes(
                    folder_path
                )
                iso_path = f"{folder_path}.iso"
                batch_line = (
                    f'"{folder2iso_path}" "{folder_path}" "{iso_path}" "{folder_name}" '
                    f'{folder_count} {file_count} {total_size} "UTF-8"\n'
                )
                batch_file.write(batch_line)

    print(f"File batch đã được tạo tại: {output_file}")
