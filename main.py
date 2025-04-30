import os

def collect_files_code(root_dir, extensions, output_file):
    """
    遍历指定目录及其子目录，提取指定扩展名文件的内容，写入txt文件
    参数：
    root_dir: 要遍历的根目录路径
    extensions: 包含多个文件扩展名的列表，例如 ['.py', '.cpp']
    output_file: 输出txt文件的路径
    """
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for foldername, subfolders, filenames in os.walk(root_dir):
            for filename in filenames:
                # 将扩展名转换为小写后比较，确保大小写无关
                ext = os.path.splitext(filename)[1].lower()
                if ext in extensions:
                    file_path = os.path.join(foldername, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        # 获取相对路径，更简洁
                        relative_path = os.path.relpath(file_path, root_dir)
                        # 写入标题，带书名号和空行
                        out_f.write(f"《{relative_path}》\n\n")
                        out_f.write(content)
                        out_f.write("\n\n" + "-"*80 + "\n\n")
                    except Exception as e:
                        print(f"读取文件出错: {file_path}, 错误信息: {e}")

if __name__ == '__main__':
    # 输入目录路径
    user_input = input("请输入要遍历的目录路径:\n")
    directory = user_input.strip().strip('"').strip("'")

    # 输入扩展名列表
    ext_input = input("请输入要包含的文件扩展名（例如 .py .cpp .txt），多个用空格分隔:\n")
    # 处理输入：去空格、补点、统一小写
    extensions = []
    for e in ext_input.strip().split():
        e = e.strip().lower()
        if not e.startswith('.'):
            e = '.' + e
        extensions.append(e)

    # 验证目录是否存在
    if not os.path.isdir(directory):
        print(f"目录不存在，请检查路径是否正确：{directory}")
    elif not extensions:
        print("未指定任何有效扩展名，请重新运行。")
    else:
        output_txt_path = 'All_Code.txt'
        collect_files_code(directory, extensions, output_txt_path)
        print(f"文件内容已成功写入：{output_txt_path}")