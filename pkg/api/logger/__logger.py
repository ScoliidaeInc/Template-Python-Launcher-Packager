"""Used to obfuscate variables from the namespace"""

from typing import Literal, Any
from types import NoneType
from codecs import lookup as _lookup

from pkg.api import path, calendar

class Logger:
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
    class Default:
        """
        Stores default values used by the logger

        ---

        Available Calls:
        - allowed_levels
        - level
        - encoding
        - handler
        - user_dir
        - output_dir
        """
        allowed_levels:list[# Debug,Info,Warning,Error,Critical
            Literal[
                "Debug",
                "Info","Information",
                "Warn","Warning",
                "Err","Error",
                "Crit","Critical"
                ]
            ]=["Debug","Info","Information","Warn","Warning","Err","Error","Crit","Critical"]
        level:dict={"value":20,"alias":"Info"}
        encoding:str="UTF-8"
        handler:Literal["File","Console"]="File"
        dir:str|NoneType= path.join_logs("") if handler.strip().lower()=="file" else None
    @classmethod
    def normalize_level(cls,
        new_level:Literal[
            "Debug",
            1,10,
            "Info",
            2,20,
            "Warning",
            3,30,
            "Error",
            4,40,
            "Critical",
            5,50
            ]
        )-> dict:
        """

        Parse a given level to recieve a normalized output

        ---

        Use this as a default for sterilizing new level inputs from elsewhere in the program
        """
        approved_levels:list=[
            {"value":10,"alias":"Debug"},
            {"value":20,"alias":"Info"},
            {"value":30,"alias":"Warning"},
            {"value":40,"alias":"Error"},
            {"value":50,"alias":"Critical"},
        ]
        #region Sterilize input
        match new_level:# to expected data-type to associate into a str repr
            case float():
                new_level=str(new_level).split(".",1)[0]
            case int():
                new_level=str(new_level)
            case str():
                new_level=new_level.strip().lower().replace(" ","")
            case dict():
                if new_level in approved_levels:
                    return new_level
                err:str="new_level must be of type string,"+\
                    f" integer or floating-point, not {type(new_level)}"
                raise TypeError(err)
            case _:# all unexpected inputs
                err:str="new_level must be of type string,"+\
                    f" integer or floating-point, not {type(new_level)}"
                raise TypeError(err)
        if new_level=="":
            err:str="new_level must not be an empty string! Please double check your inputs..."
            raise ValueError(err)
        #endregion Sterilize input
        match new_level:# to assign a value if expected value is found
            case "1"|"10"|"debug":
                return {"value":10,"alias":"Debug"}
            case "2"|"20"|"info"|"information":
                return {"value":20,"alias":"Info"}
            case "3"|"30"|"warn"|"warning":
                return {"value":30,"alias":"Warning"}
            case "4"|"40"|"err"|"error":
                return {"value":40,"alias":"Error"}
            case "5"|"50"|"crit"|"critical":
                return {"value":20,"alias":"Critical"}
            case _:# No valid match found
                try:# to convert to integer and find range value fits wihin FIRST and assign value
                    new_level=int(new_level)
                    if new_level<20:
                        return {"value":10,"alias":"Debug"}
                    elif new_level<30:
                        return {"value":20,"alias":"Info"}
                    elif new_level<40:
                        return {"value":30,"alias":"Warning"}
                    elif new_level<50:
                        return {"value":40,"alias":"Error"}
                    elif new_level>=50:
                        return {"value":50,"alias":"Info"}
                # due to not being able to convert to int, so default value instead
                except ValueError:
                    return cls.Default.level

    def __init__(self,
        output_path:str=Default.dir,
        encoding:str="utf-8",
        handler:Literal["file","console"]="file",
        level:Literal[10,"Debug",20,"Info",30,"Warning",40,"Error",50,"Critical"]=Default.level
        ) -> NoneType:
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
        self.__level:dict=self.normalize_level(new_level=level)
        self.__handler:str= self.__pick_handler(handler)
        self.__encoding:str= self.__check_encoding(encoding)
        self.__output_path:str= path.validate(output_path,False,False)["path"]
        self.__current_session_log_file:str=None
    #region level
    @property
    def level(self)-> dict:
        """This is the current minimum level used by the logger"""
        return self.__level
    @level.setter
    def level(self,
        new_level:Literal[10,"Debug",20,"Info",30,"Warning",40,"Error",50,"Critical"]
        )-> NoneType:
        self.__level= self.normalize_level(new_level)
    #endregion level
    #region output_path
    @property
    def dir(self)-> dict:
        """This is the currently selected directory to store logs within"""
        return self.__output_path
    @dir.setter
    def dir(self, new_path)-> NoneType:
        self.__output_path= __chosen_path["path"] \
            if not (__chosen_path:=path.validate(new_path)) is None \
            else self.Default.dir
    #endregion output_path
    #region current session file
    @property
    def current_file(self)-> str|NoneType:
        """
        This is the current file logs are being stored within

        ---

        Only assigns a value upon first writes to the provided directory
        """
        return self.__current_session_log_file
    @current_file.setter
    def current_file(self, new_path)-> NoneType:
        self.__current_session_log_file= path.validate(
            path.normalize(new_path),
            create_path_as_file=True
            )["path"]
    #endregion current session file
    #region handler
    def __pick_handler(self, output_handler:Literal["console","file"])-> str:
        """Normalizes inputs for use with assigning a handler"""
        output_handler=fr"{output_handler}".strip().lower().replace(" ","")
        return "console" \
            if output_handler=="console" \
                and self.__level["alias"].lower()=="debug" \
            else "file"
    @property
    def handler(self)-> dict:
        """Determines if the recorded events should be logged to a file or console"""
        return self.__handler
    @handler.setter
    def handler(self, alt_handler:str)-> NoneType:
        self.__handler= self.__pick_handler(alt_handler)
    #endregion handler
    #region encoding
    def __check_encoding(self, value:str, /)-> str:
        value_found:str=None
        try:
            value_found=str(_lookup(value)).split("encoding ",1)[1].split(" ",1)[0]
        except LookupError:
            value_found=self.Default.encoding
        return value_found
    @property
    def encoding(self)-> dict:
        """Ensures a standardized encoding for the logger to use"""
        return self.__encoding
    @encoding.setter
    def encoding(self, new_encoding:str)-> NoneType:
        self.__encoding= self.__check_encoding(new_encoding)
    #endregion encoding
    def format_output(self, log_lvl:int|str, time:float, msg:str)-> str:
        """Takes a few inputs to format a standardaized output for logging events"""
        if not isinstance(log_lvl,(int,str)):
            raise TypeError("Inappropriate argument type for log_lvl.")
        elif not isinstance(time,(float,int)):
            raise TypeError("Inappropriate argument type for time.")
        elif isinstance(msg,NoneType):
            msg:str="to do unknown..."
        elif not isinstance(msg,str):
            raise TypeError("Inappropriate argument type for msg.")
        if msg.strip()=="":
            msg:str="to do unknown..."
        else:
            msg=msg.strip()
        if isinstance(time,int):
            time=float(time)
        if time<=0.0:
            time=calendar.time.timestamp()
        log_lvl=self.normalize_level(log_lvl)
        return f"[{log_lvl['alias'].upper()}]{time}|{msg[:1].capitalize()+msg[1:]}"
    def write_to_output(self, *content:str)-> NoneType:
        """Writes contents to a file, please ensure the content parsed is already formatted"""
        def detect_format(msg:str)->bool:
            """
            Returns True if message is a valid format else corrects it,
            this may cause unwanted messages,
            please ensure messages are already formatted
            """
            msg=msg.strip()
            if not all({"[" in msg,"]" in msg,"|" in msg,}):
                return False
            allowed_level_aliases:tuple=(
                "debug",
                "info" , "information",
                "warn" , "warning",
                "err"  , "error",
                "crit" , "critical"
            )
            detected_level,detected_time=None,None
            if msg.startswith("[") \
                and "]" in msg \
                and msg[1:].lower().split("]",1)[0] in allowed_level_aliases \
                and "|" in msg \
                and msg.find("]")<msg.find("|") \
                and msg[1:].lower().split("]",1)[0] in allowed_level_aliases:
                detected_level=msg[1:].lower().split("]",1)[0].strip()
                #region verify time format slot
                try:
                    detected_time=float(msg.split("]",1)[1].split("|",1)[0].strip())
                except ValueError:
                    pass
                finally:
                    if detected_time is None:
                        raise ValueError("Invalid time input, must be a timestamp(float)")
                #endregion verify time format slot
            return True if detected_level is not None and detected_time is not None else False
        match self.handler.lower():
            case "console":
                for line in content:
                    output_enabled:bool= True \
                        if self.level["value"]<=self.normalize_level(#..)["value"]
                            line[1:].split("]",1)[0])["value"] \
                        else False
                    if detect_format(line) is False:
                        output_enabled=False
                    if output_enabled is True:
                        print(line)
                return
            case "file":
                self.__current_session_log_file=f"{path.normalize(self.dir)}{path.seperator}"+\
                f"{content[0][content[0].find(']')+1:content[0].find('|')].replace('.','_',1)}.log"\
                    if self.__current_session_log_file is None \
                    else self.__current_session_log_file
                path.validate(self.__current_session_log_file,create_path_as_file=True)
                with open(file=self.__current_session_log_file,
                    mode="a",
                    encoding=self.encoding
                ) as active_output_log_file:
                    for line in content:
                        output_enabled:bool= True \
                            if self.level["value"]<=self.normalize_level(#...)["value"]
                                line[1:].split("]",1)[0])["value"] \
                            else False
                        if detect_format(line) is False:
                            output_enabled=False
                        if output_enabled is True:
                            active_output_log_file.write(f"{line.strip()}\n")
    def decorator(self, func)-> Any|NoneType:
        """
        This is a wrapper-decorator to automatically log function calls

        NOTE:
        If the log level is not a valid value found, it will use the logger default log level value

        ---

        :log_lvl: Sets the level of the reported logging from the active function

        :return_value: Determines whether or not the function's return value is given

        :call_reason: Message the logger uses to record that an action has been taken
        """
        def log_action(*args,**kwargs)-> Any|NoneType:
            """
            Logs the function's call and end.
            You will need to manually call the logger from within the function
            to gain further logging details
            """
            log_lvl=self.normalize_level(kwargs.get("log_lvl","Info"))
            return_value=kwargs.get("return_value",False)
            call_reason=reason \
                if (reason:=f'{kwargs.get("call_reason","to do unknown...")}'.strip())!="" \
                else "to do unknown..."
            if not isinstance(return_value,bool):
                err:str="Inappropriate argument type for "+\
                    f"return_value of type({type(return_value)})."
                raise TypeError(err)
            output_enabled:bool=False
            if self.level["value"]<=log_lvl["value"]:
                output_enabled=True
                origin_time=calendar.time.timestamp()
                custom_output_msg=f"[{log_lvl['alias'].upper()}]{origin_time}|"+\
                    f"Calling {func.__qualname__} {call_reason}"
                self.write_to_output(custom_output_msg)
            func_return_value= func(args,kwargs)
            if output_enabled is True:
                end_time=calendar.time.timestamp()
                custom_output_msg=f"[{log_lvl['alias'].upper()}]{end_time}|"+\
                    f"Finished calling {func.__qualname__}. "+\
                    f"The call took aproximately {end_time-origin_time:.6f} seconds"
                self.write_to_output(custom_output_msg)
            return None if return_value is False or output_enabled is False else func_return_value
        return log_action
