"""
Standardized Application Programming Interface

---

Available Calls:

- application "Provides immutable information about the system as used by the package"
    - Info "Stores basic information about the application"
        - args "Arguments parsed to the application at runtime"
        - kwargs "Key-Word Arguments parsed to the application at runtime"
        - device "Minimal information about the device the application is running on for logging"
        - name "Referencable name of the application"
        - version "Current version of the application"
    - settings ==WIP== "This is the finalized set of settings to be used while the app is running"
- calendar "Handles all dates, times, and events"
    - date ==WIP== "Hours feeling long? Look only further."
    - events ==WIP== "I swear there was a reason I tied this string to my finger!"
    - time "If it ticks, it can be counted here"
        - () "Initializes the class, if printed returns the used format"
        - timestamp "Returns a float representation of a given date and time"
        - read_timestamp "Returns a date time string based on a given float"
        - utc_offset "Returns the number of hours offset from Universal Time Coordinated"
        - now "Returns the current time"
- logger "Documents function & event calls made by the application"
    - Default "Stores default values used by the logger functions"
        - allowed_levels "levels allowed to be used for indicating logging functions"
        - level "default level used to track minimum outputs"
        - encoding "character encoding for provided strings, default is UTF-8"
        - handler "Determines if output should be a file or the console"
        - dir "the path to be used to log files to"
    - normalize_level "Attempts to normalize the input for use of parsing to the logger"
    - () "Initializes the logger to start recording events called"
        - level "The active level determining the minimum output level"
        - encoding "Character set encoding used to dictate language outputs"
        - handler "Determines if the output is sent to a file or the console"
        - dir "If enabled is the path all events are logged and stored under"
        - current_file "The current open file used by the logger to record events"
        - format_output "Template for output message for use with logging to output"
        - write_to_output "Writes given lines to the active logging output"
        - decorator "Wrapper function for logging functions called
- path "Handles anything involving paths"
    - Default "Stores default path values"
        - root_dir "Root directory containing the application"
        - pkg_dir "Directory containing the application"
        - usr_dir "Directory containing the user settings"
        - log_dir "Logging directory containing the output logs"
        - plugin_dir "Directory containing the plug-ins for the application"
    - normalize "normalizes path across platforms"
    - validate "Validates the credentials of a path, and optionally creates"
    - join_root "Assumes path as a sub-directory of the root directory"
    - join_pkg "Assumes path as a sub-directory of the application"
    - join_user "Assumes path as a sub-directory of the user directory"
    - join_logs "Assumes path as a sub-directory of the logs directory"
    - join_plugins "Assumes path as a sub-directory of the plug-ins directory"
    - seperator "Operating System path seperator"
- plugins == WIP == "Broken until user directory search is fixed"
- plugins "Controls the loading of all the plug-ins listed by the boot.loader"
    - path "Current expected directory to find launcher plug-ins"
    - boot_loader "Current expected directory to find launcher "boot.loader""
    - entry_file "Name of expected file to initiate the plug-in"
    - boot_order "Reads the plug-in directory and "boot.loader" to confirm load order"
"""

# CAUTION WHEN USING PLUG-INS
# these are designed to be capable of using this package to create an application
# this being said, anything can be executed from the plug-ins once imported
# only add trusted plug-ins to the boot.loader file

#fix soon as user directory search is corrected
#####  WIP  ######## from .plugins import Plugins as plugins

#region mangle api namespace to bury exposed nodes not intended for use
from .path import Path as path# Handles anything involving paths
from .logger import Logger as logger# Application event logger
from . import (
    calendar,# Handles all dates, times, and events
    application,# Provides immutable information about the system as used by the package
    )
#endregion mangle api namespace to bury exposed nodes not intended for use

#from . import (# api branches that have not yet been created/worked on
#    updater,
#    mathapedia,
#    graphicaluserinterface,
#)
