import os


def cleanup_empty_folders_media(path):
    if os.path.isdir(path):
        for dir in os.listdir(path):
            id_dir = os.path.join(path, dir)
            if os.path.isdir(id_dir):
                if not os.listdir(id_dir):
                    os.rmdir(id_dir)
                else:
                    cleanup_empty_folders_media(id_dir)
