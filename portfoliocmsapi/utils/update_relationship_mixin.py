from rest_framework.exceptions import ValidationError


class UpdateRelationshipMixin:
    """
    Mixin for handling many-to-many relationship updates in ViewSets.
    Requires relationship_configs to be defined in the ViewSet.
    """

    def perform_update(self, serializer):
        instance = serializer.save()

        for field_name, config in self.relationship_configs.items():
            if field_name in self.request.data:
                ids = self.request.data.get(field_name, [])
                relationship_field = getattr(instance, field_name)

                if not ids:  # Empty array = clear all
                    relationship_field.clear()
                else:
                    model = config["model"]
                    for item_id in ids:
                        if not model.objects.filter(id=item_id).exists():
                            raise ValidationError(
                                f"{model.__name__} with id {item_id} does not exist"
                            )

                        if relationship_field.filter(id=item_id).exists():
                            relationship_field.remove(item_id)
                        else:
                            relationship_field.add(item_id)
