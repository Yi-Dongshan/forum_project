import os


def print_tree(directory, prefix=""):
    """递归打印目录结构"""
    # 获取目录下的所有文件和文件夹，并按照名称排序
    entries = sorted(os.listdir(directory))

    # 过滤掉不需要的文件或文件夹
    ignore_dirs = {'.git', '__pycache__', '.DS_Store', 'venv', 'node_modules'}
    entries = [e for e in entries if e not in ignore_dirs]

    # 遍历所有条目
    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = (index == len(entries) - 1)  # 是否为当前层的最后一个元素

        # 选择合适的前缀符号
        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)

        # 如果是目录，则递归打印
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(path, new_prefix)


if __name__ == "__main__":
    root_dir = "D:\\My Workspace\\forum_project"  # 可以修改为其他路径
    print(root_dir)  # 打印起始目录
    print_tree(root_dir)