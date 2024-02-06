"""This Package is only a headless launcher, please write the heads as plug-ins and place them in the user directory"""
#Handles all pre-loading actions for the script
# Used to ensure package was initialized correctly,
# as well as ensuring functions are added to the namespace correctly
from .api import GlobalAPI

class Tests:
    """Tests the GlobalAPI class above and all sub-access"""
    def __init__(self) -> None:
        print("Starting Tests")
        # order of operations for boot
        logger=GlobalAPI.Logger()
        path= GlobalAPI.SystemInfo.Path
        time= GlobalAPI.SystemInfo.Calendar.Time
        date= GlobalAPI.SystemInfo.Calendar.Date
        print(
            # Obtain all Args, Kwargs and Settings
            f"{GlobalAPI.SystemInfo.Runtime.args= }",
            f"{GlobalAPI.SystemInfo.Runtime.kwargs= }",
            f"{GlobalAPI.SystemInfo.Settings.Finalized()= }",
            f"{GlobalAPI.SystemInfo().version= }",
            f"{GlobalAPI.SystemInfo().pkg_name= }",
            f"{GlobalAPI.SystemInfo().device= }",
            "",
            f"{time.datetime_format(international=False, written=False)= }",
            f"{time.datetime_format(international=True, written=False)= }",
            f"{time.datetime_format(international=False, written=True)= }",
            f"{time.datetime_format(international=True, written=True)= }",
            "",
            f"{time.timestamp()= }",
            f"{time.timestamp('30/2023/12 13:06: 14.5 864a M')= }",
            f"{time.read_timestamp(time.timestamp('30/2023/12 13:06: 14.5 864a M'))= }",
            f"{time.now()= }",
            f"{time.now(international=False)= }",
            f"{time.utc_offset()= }",
            "",
            f"{__file__= }",
            f"{path.normalize_path(f'{__file__}/.')= }",
            f"{path.validate(__file__, return_exists=True,return_valid_path=True,return_isfile=True,return_isdir=True)= }",
            f"{path.validate(__file__, return_exists=True,return_valid_path=True,return_isfile=True,return_isdir=False)= }",
            f"{path.validate(__file__, return_exists=True,return_valid_path=True,return_isfile=False,return_isdir=True)= }",
            f"{path.validate(__file__, return_exists=True,return_valid_path=False,return_isfile=False,return_isdir=False)= }",
            f"{path.validate(__file__, return_exists=False,return_valid_path=False,return_isfile=False,return_isdir=False)= }",
            "",
            f"{path.rootdir_join('')= }",
            f"{path.pkgdir_join('')= }",
            "",
            f"{logger.level= }",
            f"{logger.handler= }",
            f"{logger.output_path= }",
            f"{path.usrdir_join(logger.output_path)= }",
            f"{logger.encoding= }",
            "",
            f"{date.days_offset(count=-1_000, starting_date=time.timestamp())= }",
            f"{date.months_offset(count=-25, starting_date=time.timestamp())= }",
            f"{date.years_offset(count=-25, starting_date=time.timestamp())= }",
            f"{date.offset('7/5/1996 20:30:00.000000')= }",
            sep="\n"
        )
        print("Finished Tests!")

if __package__ is None or __name__=="__main__":# Package wasn't initialized correctly
    raise SystemError("The package was not properly initialized, please try using the included launch script.")
if __package__==__name__:# Only triggers when the package has been properly initialized
    # These notes are for quicker reference when writing new tests
    # These notes are also for use of knowledge on what is exposed for calls by other scripts
    #
    # Be cautious of what can wind up visible here, consider these end-points and Classes/Functions to be global access
    # These notes denote the current program structure, please ensure these are updated as new functions are added or removed
    # Anything imported is also considered global access
    #
    # Only use "lazy loading" of imports if you are aware that, that import will not be in use anywhere else within the application
    # Lazy loading can help in use-cases for speed-up, however it also makes the code harder to read
    # If an import is to be used elsewhere, use the standard "import" and "from PKG.PATH import" methods
    # import for anything that is standard shipped with Python
    # from PKG.PATH for anything that is path found within the packaged application
    #
    #
    # If it becomes desired to adjust what keywords are allowed from settings,
    # please go to GlobalAPI.SystemInfo.Settings.Factory.read()
    # and change the expected inputs' values
    # keep in mind these are keywords only! not values
    #
    # GlobalAPI.SystemInfo.Settings.Factory also controls what settings are available within GlobalAPI.SystemInfo.Settings.User
    # GlobalAPI.SystemInfo.Settings.Factory controls it via flags from the settings
    #
    # GlobalAPI.SystemInfo.Settings.User is generated from GlobalAPI.SystemInfo.Settings.Factory and heavily restricted
    # The settings here take higher priority than the factory settings when given proper access
    # GlobalAPI.SystemInfo.Settings.Factory must grant GlobalAPI.SystemInfo.Settings.User access to each command INDIVIDUALLY
    #
    # Once the GlobalAPI.SystemInfo.Settings.Factory and GlobalAPI.SystemInfo.Settings.User settings have been loaded
    # GlobalAPI.SystemInfo.Settings.Finalized is the locked in settings, will only update user settings during runtime
    # new settings can neither be added nor removed from this point
    #
    #
    # Program Structure
    # -----------------
    # PKG
    # |-> __init__
    # |     |->
    # |-> __main__
    #print(f"{__package__} has been started!")
    #print("Starting initialization...")
    pass
elif __name__=="__init__":
    #print("Script was imported directly")# Can only be triggered after the package has properly initialized
# Custom script written out for this package to standardize values used within the package
    # Global API also contains functions to aid in the following:
    # - Logging
    # - Read Settings
    # - Do basic math
    # - Sanitize inputs of various datatypes and string format
    # - Use plugins with the script to alter the "end-user experience"
    #       - I.e. Create a gui application to host/monitor a discord bot using this package as a launcher
    #           - plug-in must be initialized through a "run.plug_in" file found in the directory named as the plug-in name
    #           - I.e. a "Discord Bot" directory would contain a "run.plug_in" file
    #           > Under the hood "run.plug_in" is a python file
    #   > Please note this package is headless and only runs via plug-ins
    #   > You can control which plug-ins are enabled via the "plug_in.bootloader" text file auto-generated in the targetted user directory
    pass
