"""
Controls the loading of all the plug-ins listed by the boot.loader

---

Available Calls: == WIP == broken until user directory search is stable
- path "Current expected directory to find launcher plug-ins"
- boot_loader "Current expected directory to find launcher "boot.loader""
- entry_file "Name of expected file to initiate the plug-in"
- boot_order "Reads the plug-in directory and "boot.loader" to confirm load order"
"""

from .__plugins import Plugins
