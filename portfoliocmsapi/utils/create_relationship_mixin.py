from rest_framework.exceptions import ValidationError


class CreateRelationshipMixin:
    """
    Mixin for handling many-to-many relationship creation in ViewSets.
    Requires relationship_configs to be defined in the ViewSet.
    """

    def perform_create(self, serializer):
        instance = serializer.save()

        for field_name, config in self.relationship_configs.items():
            ids = self.request.data.get(field_name, [])
            if ids:
                model = config["model"]
                for item_id in ids:
                    if not model.objects.filter(id=item_id).exists():
                        raise ValidationError(
                            f"{model.__name__} with id {item_id} does not exist"
                        )
                getattr(instance, field_name).add(*ids)
