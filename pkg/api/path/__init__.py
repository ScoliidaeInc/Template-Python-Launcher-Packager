"""
Handles anything involving paths

---

Available Calls:
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
"""

from .__path import Path
