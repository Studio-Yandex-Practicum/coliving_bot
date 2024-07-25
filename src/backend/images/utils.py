from coliving_bot.utils import slugify


def images_directory_path(instance, filename):
    """
    Определяет структуру хранения фотографий объектов 'Coliving' и 'Profile'.
    """
    name, extension = filename.rsplit(".", 1)
    name = slugify(name)
    return "{0}/{1}".format(instance, f"{name}.{extension}")
