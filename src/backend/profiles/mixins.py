import os
import shutil

from coliving_bot.settings.base import MEDIA_ROOT


class DestroyWithMediaRemovalMixin:
    def perform_destroy(self, instance):
        """Удаляет анкету, затем удаляет директорию с фотографиями анкеты."""
        instance_pk = str(instance.id)
        instance_dir = f"{instance.__class__.__name__}s".lower()
        path = os.path.join(MEDIA_ROOT, instance_dir, instance_pk)
        instance.delete()
        shutil.rmtree(path, ignore_errors=True)
