"""Test-Suite for the application"""

from typing import Literal

from pkg import api

active_logger:api.logger= api.logger()
example_format_output:str= active_logger.format_output(20,0.01,'''Hi, I'm paul''')
@active_logger.decorator
def example_call(*args,**kwargs)-> Literal["Proof of concept only :)"]:
    """This is only to show the decorator from the active logger"""
    del args, kwargs
    return "Proof of concept only :)"

class Tests:
    """
    This is where every call within the API
    may be manually set for testing and determining runtime order
    """

    print(
        "Starting testing on: [ api.application.Info ]",
        f"{api.application.Info.name= }",
        f"{api.application.Info.version= }",
        f"{api.application.Info.device= }",
        f"{api.application.Info.args= }",
        f"{api.application.Info.kwargs= }",
        "Finished testing on: [ api.application.Info ]",
        "",
        "Starting testing on: [ api.path ]",
        f"{api.path.normalize('/foo/*ROOT DIR*/help')= }",
        f"{api.path.validate('*PLUG-IN DIR*/help')= }",
        f"{api.path.join_root('*ROOT DIR*/*PLUG-IN DIR*/../pkg')= }",
        f"{api.path.join_pkg('*PKG DIR*/help')= }",
        f"{api.path.join_user('*USR DIR*/help')= }",
        f"{api.path.join_logs('*LOG DIR*/help')= }",
        f"{api.path.join_plugins('*PLUG-IN DIR*/help')= }",
        "Finished testing on: [ api.path ]",
        "",
        "Starting testing on: [ api.calendar.time ]",
        f"{api.calendar.time= }",
        f"{api.calendar.time()= }",
        f"{api.calendar.time.timestamp()= }",
        f"{api.calendar.time.timestamp('2/14/2024 23:59:59.999999')= }",
        f"{api.calendar.time.timestamp('2/14/2024 11:59:59.999999PM')= }",
        f"{api.calendar.time.read_timestamp('1707955199.999999')= }",
        f"{api.calendar.time.utc_offset()= }",
        f"{api.calendar.time.now()= }",
        "Finished testing on: [ api.calendar.time ]",
        "",
        "Starting testing on: [ api.logger.Default ]",
        f"{api.logger.Default.allowed_levels= }",
        f"{api.logger.Default.level= }",
        f"{api.logger.Default.encoding= }",
        f"{api.logger.Default.handler= }",
        f"{api.logger.Default.dir= }",
        "Finished testing on: [ api.logger.Default ]",
        "",
        "Starting testing on: [ api.logger ]",
        f"{api.logger.normalize_level(10)= }",
        f"{active_logger.level= }",
        f"{active_logger.encoding= }",
        f"{active_logger.handler= }",
        f"{active_logger.dir= }",
        f"{example_format_output= }",
        f"{example_call(log_lvl='Info',return_value=True)= }",
        f"{active_logger.current_file= }",
        f"{active_logger.write_to_output('''[INFO]0.01|Hi, I'm paul''')= }",
        "Finished testing on: [ api.logger ]",
        "",
        "Starting testing on: [ api.plugins ]",
        #f"{api.plugins.path= }",
        #f"{api.plugins.boot_loader= }",
        #f"{api.plugins.entry_file= }",
        #f"{api.plugins.boot_order= }",
        "Finished testing on: [ api.plugins ]",
        sep="\n"
    )
