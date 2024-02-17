"""
Records events from the current application to an output file
to track what potentially caused the reported issue

---

Available Calls:
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
"""

from .__logger import Logger
