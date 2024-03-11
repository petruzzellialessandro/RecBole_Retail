import os
import shutil

def copy_directory_contents(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dst_path)

if __name__ == '__main__':
    ROOT_DIR = os.getcwd()
    BACKEND_DIR = os.path.join(ROOT_DIR, "src", "app", "backend")

    print(f"Starting project setup...")
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    DATA_DIR_BACKEND = os.path.join(BACKEND_DIR, "data")
    print(f"Copying files from {DATA_DIR} to {DATA_DIR_BACKEND} directory")
    copy_directory_contents(DATA_DIR, DATA_DIR_BACKEND)

    print(f"Task completed!")
        