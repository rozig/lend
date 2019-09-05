from rest_framework.viewsets import ModelViewSet

from app.core.mixins import CreateMixin, ListMixin, RetrieveMixin, UpdateMixin


class ViewSet(ModelViewSet, CreateMixin, ListMixin, RetrieveMixin, UpdateMixin):
    """
    A viewset that overrides default get_serializer_class() method depending on actions.
    """
    pass
