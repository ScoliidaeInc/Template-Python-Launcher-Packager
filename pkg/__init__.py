"""
This Package is only a headless launcher,
please write the heads as plug-ins and place them in the user directory
"""
#Handles all pre-loading actions for the script
# Used to ensure package was initialized correctly,
# as well as ensuring functions are added to the namespace correctly
from . import (
    api,# used to add to global namespace for application
    testing# Used to actively find the limitations of each call in the api
)

if __package__ is None or __name__=="__main__":# Package wasn't initialized correctly
    raise SystemError(
        "The package was not properly initialized, please try using the included launch script."
        )
elif __package__==__name__:# Only triggers when the package has been properly initialized
    testing.Tests()
elif __name__=="__init__":# Only Triggers when the file has been called after package
    pass
