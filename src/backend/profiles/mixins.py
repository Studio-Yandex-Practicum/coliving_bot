import os
import shutil

from coliving_bot.settings.base import MEDIA_ROOT


class DestroyWithMediaColivingRemovalMixin:
    def perform_destroy(self, instance):
        instance_pk = str(instance.id)
        instance_dir = f"{instance.__class__.__name__}s"
        path = os.path.join(MEDIA_ROOT, instance_dir, instance_pk)
        instance.delete()
        shutil.rmtree(path)
