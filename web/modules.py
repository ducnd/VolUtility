# https://github.com/viper-framework/viper/blob/master/viper/core/plugins.py
import pkgutil
import inspect
from web.common import Extension
import logging

logger = logging.getLogger(__name__)

def load_extensions():
    # Import modules package.
    import extensions

    extension_list = dict()

    # Walk recursively through all modules and packages.
    for loader, extension_name, ispkg in pkgutil.walk_packages(extensions.__path__, extensions.__name__ + '.'):
        # If current item is a package, skip.
        if ispkg:
            continue

        # Try to import the module, otherwise skip.
        try:
            ext = __import__(extension_name, globals(), locals(), ['dummy'], -1)
        except ImportError as e:
            logger.error("Something wrong happened while importing the extension {0}: {1}".format(extension_name, e))
            continue


        # Walk through all members of currently imported modules.
        for member_name, member_object in inspect.getmembers(ext):
            # Check if current member is a class.
            if inspect.isclass(member_object):
                # Yield the class if it's a subclass of Module.
                if issubclass(member_object, Extension) and member_object is not Extension:
                    logger.info("Loaded Extension: {0}".format(member_object.extension_name))
                    extension_list[member_object.extension_name] = dict(obj=member_object, description=member_object.extension_name)


    return extension_list

__extensions__ = load_extensions()
