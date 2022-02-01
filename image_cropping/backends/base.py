import abc

from django.utils.translation import gettext as _

from .. import widgets


class ImageBackend(metaclass=abc.ABCMeta):
    """
    Abstract class to expose the expected methods and properties that a custom
    backend should provide.
    """

    exceptions_to_catch = (IOError,)

    WIDGETS = {
        "foreign_key": widgets.CropForeignKeyWidget,
        "hidden": widgets.HiddenImageCropWidget,
        "ImageField": widgets.ImageCropWidget,
        "ImageCropField": widgets.ImageCropWidget,
    }

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abc.abstractmethod
    def get_thumbnail_url(self, image_path, thumbnail_options):
        pass

    @abc.abstractmethod
    def get_size(self, image):
        pass

    def get_widget(self, db_field, target, admin_site):
        "Get the widget from a db_field"
        if target["fk_field"]:
            # it's a ForeignKey
            return self.WIDGETS["foreign_key"](
                db_field.remote_field,
                field_name=target["fk_field"],
                admin_site=admin_site,
            )
        elif target["hidden"]:
            # it's a hidden ImageField
            return self.WIDGETS["hidden"]
        else:
            # it's a regular image field, get from its class name
            class_name = type(db_field).__name__
            if class_name not in self.WIDGETS:
                msg = _(
                    "There's no widget registered to the class {class_name}"
                ).format(class_name=class_name)
                raise ValueError(msg)
            return self.WIDGETS[class_name]
