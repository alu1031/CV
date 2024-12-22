import os
import shutil

# 原始文件夹路径
source_folder = "ORL"
# 目标文件夹路径
target_folder = "111"

# 遍历原始文件夹中的所有文件夹
for folder_name in os.listdir(source_folder):
    folder_path = os.path.join(source_folder, folder_name)
    # 检查是否是文件夹
    if os.path.isdir(folder_path):
        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # 构建新的文件名，加上文件夹名作为前缀
            new_filename = f"{folder_name}_{filename}"
            # 拷贝文件到目标文件夹
            shutil.copy(file_path, os.path.join(target_folder, new_filename))
