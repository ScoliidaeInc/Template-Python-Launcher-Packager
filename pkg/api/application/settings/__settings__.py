"""Used to obfuscate variables from the namespace"""

from .factory import Factory as __factory # default settings loaded
from .plugins import PlugIn as __plug_in # plug-in settings loaded
from .user import Usr as __usr # user settings loaded
# Merges all loaded settings to a single accessible dictionary
class Finalized:
    """This is the finalized set of settings to be used while the app is running"""
