def images_directory_path(instance, filename):
    """
    Определяет структуру хранения фотографий объектов 'Coliving' и 'Profile'.
    """
    return "{0}/{1}".format(instance, filename)
