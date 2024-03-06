"""
Controls the loading of all the plug-ins listed by the boot.loader

---

Available Calls:
- path "Current expected directory to find launcher plug-ins"
- path_exists() "Checks if the given path exists"
- boot_loader "Current expected directory to find launcher "boot.loader""
- boot_loader_exists() "Checks if the given path exists"
- entry_file "Name of expected file to initiate the plug-in"
- settings_extension "Name of the file type expected for plug-in settings"
- boot_order "Reads the plug-in directory and "boot.loader" to confirm load order"
"""

from .__plugins import Plugins
