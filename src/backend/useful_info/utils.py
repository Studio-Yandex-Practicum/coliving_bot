from coliving_bot.utils import slugify


def files_directory_path(_instance, filename):
    """
    Определяет структуру хранения file объектов 'UsefulMaterial'.
    """
    name, extension = filename.rsplit(".", 1)
    name = slugify(name)
    return f"materials/{name}.{extension}"
