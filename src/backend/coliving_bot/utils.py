import os


def cleanup_empty_folders_media(path):
    for dir in os.listdir(path):
        a = os.path.join(path, dir)
        if os.path.isdir(a):
            if not os.listdir(a):
                os.rmdir(a)
            else:
                cleanup_empty_folders_media(a)
