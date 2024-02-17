"""
This is the neck of execution.

Here you will find the plug-in launcher itself,
this autonomously reads the directories within the "plug-ins" directory
found in the generated user directory.

Each plug-in is initialized based off of the "plug_in.bootloader"
file found at the root of the plug-in directory

---

If you are looking to create your own plug-in
it is recommended to import the GlobalAPI from the root of the package

If you are looking to use api's logging features it is contained within GlobalAPI.Logger
"""

'''

from pkg import GlobalAPI, Tests
print("Finished initialization!\nRunning main call...")
active_logger=GlobalAPI.Logger()# used to save the state of the logger


@active_logger.decorator
def headless_mode(*__args,**__kwargs):
    """Runs the package without establishing any new functionality"""
    active_logger.write_to_output(active_logger.format_output("info",0,"this is a test"))
    active_logger.write_to_output(active_logger.format_output(
        "info",0,"this is a test to ensure file sync'ed correctly")
        )
    Tests()
headless_mode(call_reason="to execute the the main body of the package")

print("Saving progress, please do not close yet...")

print("Main call finished, closing script")
'''
