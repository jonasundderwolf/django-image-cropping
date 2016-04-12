import abc
import six


class ImageBackend(six.with_metaclass(abc.ABCMeta)):
    """
    Abstract class to expose the expected methods and properties that a custom
    backend should provide.
    """

    exceptions_to_catch = (IOError, )

    @abc.abstractmethod
    def get_thumbnail_url(self, image_path, thumbnail_options):
        pass

    @abc.abstractmethod
    def get_size(self, image):
        pass
