"""
Provides immutable information about the system as used by the package

---

Available Calls:

- Info "Stores basic information about the application"
    - name "Referencable name of the application"
    - version "Current version of the application"
    - args "Arguments parsed to the application at runtime"
    - kwargs "Key-Word Arguments parsed to the application at runtime"
    - device "Minimal information about the device the application is running on for logging"

- settings ==WIP== "This is the finalized set of settings to be used while the app is running"
"""

from .__application import Info
from .settings.__init__ import Finalized as settings
