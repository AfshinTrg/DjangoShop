from django.http import Http404


class AdminRequiredMixin:
    """Verify that the current user is Admin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404('Only Admin can open this feature')
        return super().dispatch(request, *args, **kwargs)
