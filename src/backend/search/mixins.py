from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response

from search.constants import ONE_MONTH, MatchStatuses


class OldLikesDestroyMixin:
    model = None

    def get_queryset(self):
        if self.model is None:
            raise NotImplementedError(
                "Необходимо определить атрибут model в наследнике"
            )

        one_month_ago = datetime.now() - timedelta(days=ONE_MONTH)
        return self.model.objects.filter(
            created_date__lte=one_month_ago,
            status__in=(MatchStatuses.is_pending, MatchStatuses.is_rejected),
        )

    def delete(self, request, *args, **kwargs):
        dislikes = self.get_queryset()
        deleted_dislikes, _ = dislikes.delete()
        return Response(
            {"deleted_dislikes": deleted_dislikes}, status=status.HTTP_204_NO_CONTENT
        )
