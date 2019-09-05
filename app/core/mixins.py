from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)


class CreateMixin(CreateModelMixin):
    """
    Create a model instance.
    """

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class


class ListMixin(ListModelMixin):
    """
    List model instances.
    """

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        assert self.list_serializer_class is not None, (
            "'%s' should either include a `list_serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.list_serializer_class


class RetrieveMixin(RetrieveModelMixin):
    """
    Retrieve a model instance.
    """

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        assert self.retrieve_serializer_class is not None, (
            "'%s' should either include a `retrieve_serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.retrieve_serializer_class


class UpdateMixin(UpdateModelMixin):
    """
    Update a model instance.
    """

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        assert self.retrieve_serializer_class is not None, (
            "'%s' should either include a `retrieve_serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.retrieve_serializer_class
