import os

from coliving_bot.settings.base import MEDIA_ROOT

from .utils import cleanup_empty_folders_media

profile_dir = os.path.join(MEDIA_ROOT, "profiles")
coliving_dir = os.path.join(MEDIA_ROOT, "colivings")

cleanup_empty_folders_media(profile_dir)
cleanup_empty_folders_media(coliving_dir)
