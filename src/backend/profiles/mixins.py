import os
import shutil

from django.shortcuts import get_object_or_404

from coliving_bot.settings.base import MEDIA_ROOT
from profiles.models import Profile


def delete_profile_folder(self):
    images_dir = "profiles"
    profile = get_object_or_404(
        Profile, user__telegram_id=self.kwargs.get("telegram_id")
    )
    profile_id = str(profile.id)
    path = os.path.join(MEDIA_ROOT, images_dir, profile_id)
    shutil.rmtree(path)


class DestroyWithMediaColivingRemovalMixin:
    def perform_destroy(self, instance):
        instance_pk = str(instance.id)
        instance_dir = f"{instance.__class__.__name__}s"
        path = os.path.join(MEDIA_ROOT, instance_dir, instance_pk)
        instance.delete()
        shutil.rmtree(path)
