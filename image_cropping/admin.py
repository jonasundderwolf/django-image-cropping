from .utils import get_backend


class ImageCroppingMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        crop_fields = getattr(self.model, "crop_fields", {})
        if db_field.name in crop_fields:
            target = crop_fields[db_field.name]
            kwargs["widget"] = get_backend().get_widget(
                db_field, target, self.admin_site
            )

        return super().formfield_for_dbfield(db_field, request, **kwargs)
