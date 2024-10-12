import os
import requests
from os.path import join, dirname
import pathlib
from ParamsBase import tactParametters

drive = pathlib.Path.home().drive
root_dir = os.getcwd()


# Đường dẫn thực của Folder2Iso.exe
folder2iso_path = join(drive, "RunProgram", "Folder2Iso", "Folder2Iso.exe")
mParams = tactParametters(
    logdir=dirname(folder2iso_path),
)

os.makedirs(dirname(folder2iso_path), exist_ok=True)


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


def downloadexe():
    if not os.path.exists(folder2iso_path):
        url_exe = "https://github.com/ntanhfai/Make_Iso_folders/blob/main/Folder2Iso.exe?raw=true"  # URL có thêm "?raw=true" để tải file trực tiếp
        print(f"Đang tải {url_exe} về {folder2iso_path}...")
        try:
            # Tải file từ URL
            response = requests.get(url_exe)
            response.raise_for_status()  # Kiểm tra nếu có lỗi khi tải file
            # Lưu file vào folder2iso_path
            with open(folder2iso_path, "wb") as file:
                file.write(response.content)
            print(f"Tải thành công {folder2iso_path}")
        except Exception as e:
            print(f"Lỗi khi tải file: {e}")
    else:
        print(f"File đã tồn tại: {folder2iso_path}")


if __name__ == "__main__":
    mParams.ta_print_log(
        "Chương trình tạo toàn bộ các folder của thư mục này thành file ISO tự động"
    )
    mParams.ta_print_log(
        "Chương trình sẽ tự download các file cần thiết về rồi sẽ tạo file create_iso.bat, chạy file bat đó để tạo file iso"
    )
    # Gọi hàm để tải file nếu chưa tồn tại
    downloadexe()
    mParams.ta_print_log(folder2iso_path)
    # Đường dẫn tới Folder2Iso và thư mục gốc

    output_file = "create_iso.bat"

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
                mParams.ta_print_log(batch_line)

    mParams.ta_print_log(f"File batch đã được tạo tại: {output_file}")
    os.startfile(output_file)
