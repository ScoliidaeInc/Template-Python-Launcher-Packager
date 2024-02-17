"""
Handles all formats involving time used by the application


If it ticks, it can be counted here

---

Available Calls:
- () "Initializes the class, if printed returns the used format"
- timestamp "Returns a float representation of a given date and time"
- read_timestamp "Returns a date time string based on a given float"
- utc_offset "Returns the number of hours offset from Universal Time Coordinated"
- now "Returns the current time"
"""

from .__time import Time as time
