"""Custom api module designed to be shipped with the launcher package for rapid application design"""
from sys import \
    argv as _argv# Used by Internal.SystemInfo.Runtime.__sort_argkwarg
from os import mkdir as _mkdir
from os.path import \
    exists as _exists, \
    isdir as _isdir, \
    isfile as _isfile, \
    realpath as _realpath, \
    sep as _os_path_sep
    # _realpath is used by Internal.SystemInfo.Path.normalize_path
    # The Following are used by Internal.SystemInfo.Path.validate:
    # - _exists
    # - _isdir
    # - _isfile
from types import \
    NoneType# Used to reveal the datatype for type None
from typing import \
    Any, \
    Literal# Used by Internal.Logger for denoting potential I/O
from platform import \
    machine as _machine, \
    system as _system, \
    release as _system_release, \
    version as _system_version, \
    platform as _platform
    # Used by the following:
    # - Internal.SystemInfo().platform
    # - Internal.SystemInfo().os
    # - Internal.SystemInfo().os_version
    # - Internal.SystemInfo().os_distro
    # - Internal.SystemInfo().cpu
    # - Internal.SystemInfo().cpu_architecture
from calendar import isleap as _isleap
from datetime import \
    timedelta as _timedelta, \
    datetime# Used by the following:
            # - Internal.Calendar.Time.timestamp
            # - Internal.Calendar.Time.read_timestamp
            # - Internal.Calendar.Time.utc_offset
from codecs import lookup as _lookup

class PlugIns:
    """Handles all plug-ins for the application"""
    class Settings:
        """Handles the settings for the plug-ins"""
class Internal:
    """Internally developed classes & functions (some build off of functionality of functions imported)"""

    class SystemInfo:
        """Provides immutable information about the system as used by the package"""

        class Settings(PlugIns.Settings):
            """Stores all settings values accessible by/for the package"""
            def __read_from_config_file(func)-> dict:
                def sieve_input_for_kwargs(*args, **kwargs)-> dict:
                    file_path,encoding,read_as_bytes,buffer_size=func(*args,**kwargs)
                    def read_file_line(file_path=file_path,encoding=encoding,read_as_bytes=read_as_bytes,buffer_size=buffer_size):
                        with open(
                            file_path,
                            "r" if read_as_bytes is False else "rb",
                            encoding=encoding.strip() if encoding.strip()!="" else "utf-8",
                            buffering=buffer_size if buffer_size is not None else -1
                            ) as temp_opened_file:
                            for line in temp_opened_file:
                                yield line.replace("\xFe","`pb`").replace("\n", "{<\xFe-- NEWLINE --\xFe>}")

                    _kwargs:dict={}
                    for current_line in read_file_line():
                        if "=" not in current_line:
                            continue
                        keyword, value= current_line.split("=",1)
                        _kwargs[keyword.strip().lower()]=value
                    return _kwargs
                return sieve_input_for_kwargs
            @__read_from_config_file
            def read(file_path:str, encoding:str="utf-8", read_as_bytes:bool=False, buffer_size:int=None)->dict:
                """
                Reads a provided file path and iterates by line to find all kwargs

                ---

                NOTE: **ALL** values in dict returned have **NOT** been stripped of excess whitespace.
                This choice is to allow anyone in the future using this to have the choice on how the values recieved are handled

                Further note, newlines have been replace with "þ",
                if "þ" is already in the string, it has been replaced with `pb`
                """
                return [file_path,encoding,read_as_bytes,buffer_size]

            class User:
                """Settings the defaults have allowed the user to edit through proxy"""
                def __init__(self) -> NoneType:
                    self.dir:str|NoneType=None

            class Factory:
                """Defines all default settings without user settings"""
                @property
                def path(self)-> str:
                    return self.__path
                @path.setter
                def path(self)-> NoneType:
                    return

                def __filter_results(func)-> dict:
                    def results(*args, **kwargs)-> dict:
                        file_path=Internal.SystemInfo.Settings.Factory.path
                        allowed_keywords=func(args,kwargs)
                        raw_results=Internal.SystemInfo.Settings.read(file_path)
                        results:dict={}
                        for keyword in allowed_keywords:
                            if keyword.lower().strip() not in raw_results:
                                continue
                            results[keyword.lower().strip()]=raw_results[keyword.lower().strip()]

                        return results
                    return results
                @__filter_results
                def read(self)-> dict:
                    expected_settings_keywords=[
                        # INPUT COMMANDS HERE
                        ## Do not include expected values here,
                        ## they belong in the settings file
                        ##
                        ## also ensure all inputs here are lowercase

                        # [USER Directory]
                        "usr dir",# default path for user directory
                        "usr dir movable",
                            # if path found as only input in file
                                # if found
                                    # assign new path
                                # else generate new usr dir and contents
                            # else treat as normal settings file
                                # save contents every time change is detected to remove invalid inputs

                        # [Logs]
                        "log output",# default output path as str
                        "usr log output type",# expected input type to change output path for logger
                        "usr change log output",# if user is allowed to change output path

                        "log handler",# method of output (console OR file)
                        "log handler checked from",# decided if handler is determined by file,runtime,usr

                        "log level",# default level for the logger
                        "usr log level type",# expected input type from user to change the log level
                        "usr change log level",# determines if the user is allowed to change the log level

                        # [Screen]
                        "screen width",# detected width of the screen
                        "screen height",# detected height of the screen
                        "screen ratio",# the current screen ratio

                        # [Application]
                        "window width",# determines the window size(width)
                        "window width locked",# if user is allowed to change the width size
                        "user window width",# user input for width if allowed
                        "user window width type",# expected input type from the user to change the window width
                        "window height",# determines the window size(height)
                        "window height locked",# if user is allowed to change the height size
                        "user window height",# user input for height if allowed
                        "user window height type",# expected input type from the user to change the window height
                        "window resizable",# determines if the application is allowed to be resized
                        "bezel offset top left",# determines the position of the top left corner from edge of the screen
                    ]
                    return expected_settings_keywords
                def __init__(self) -> NoneType:
                    self.__path= Internal.SystemInfo.Path.pkgdir_join("*PKG DIR*/Settings.Factory.config")
            class Finalized:
                @property
                def __app_dict__(self)-> dict:
                    merged_settings:dict=Internal.SystemInfo.Settings.Factory
                    return merged_settings
                def __init__(self, search_for_setting:str=None) -> NoneType:
                    pass
                def __repr__(self) -> str:
                    return ""
        class Runtime:
            """Handles information generated for use during the runtime process"""
            def __sort_argkwarg()-> dict:
                """Sorts through the parsed args and kwargs from runtime for preapproved inputs"""
                cwd:str=_argv[0]
                argumentative_kwargs= frozenset(_argv[1:])
                args:list=[]
                kwargs:dict={}

                #region Sift potential args and kwargs into seperate variables
                for arg_or_kwarg in argumentative_kwargs:
                    arg_or_kwarg=arg_or_kwarg.strip()
                    if "=" in arg_or_kwarg:
                        kw,arg=arg_or_kwarg.split("=",1)
                        kw=kw.strip(); arg=arg.strip()

                        kwargs[kw]=arg
                        continue
                    match arg_or_kwarg:
                        case ""|"-m":# empty string or package flag
                            continue
                        case _:# All remaining answers append as arg
                            args.append(arg_or_kwarg)
                #endregion Sift potential args and kwargs into seperate variables
                #region Check paired flags are not present in both searches
                for kwarg in kwargs.copy():
                    match kwarg.lower():
                        case "--debug":
                            if "-d" in args:
                                kwargs.pop(kwarg)
                        case "--test-suite":
                            if "-ts" in args:
                                kwargs.pop(kwarg)
                #endregion Check paired flags are not present in both searches
                #region ensure root directory and package directory are correctly added
                kwargs["ROOT DIR"], kwargs["PKG DIR"]= cwd.rsplit(_os_path_sep,2)[:-1]
                kwargs["PKG DIR"]= f"*ROOT DIR*{_os_path_sep}{kwargs['PKG DIR']}"
                #endregion ensure root directory and package directory are correctly added
                args=frozenset(args)# Lock args as frozen set (order might not always be consistent)
                return {"args":args,"kwargs":kwargs}
            args=__sort_argkwarg().get("args",None)
            kwargs=__sort_argkwarg().get("kwargs",None)


        class Path:
            """Handles anything involving paths"""
            seperator:str=_os_path_sep
            @classmethod
            def normalize_path(cls, potential_path:str)-> str:
                """Sterilizes and attempts to determine if path uses relative path and fills gaps if possible,
                this can also be used to normalize path symbol between operating systems"""
                if "/"!=cls.seperator and "/" in potential_path:# common path seperator found in given path but is unused
                    potential_path=potential_path.replace("/",cls.seperator)
                high_pot_path= _realpath(potential_path)

                new_pot_path=None
                if f"*ROOT DIR*{cls.seperator}" in high_pot_path:
                    new_pot_path= cls.rootdir_join(high_pot_path.rsplit(f"*ROOT DIR*{cls.seperator}",1)[1])
                if f"*PKG DIR*{cls.seperator}" in high_pot_path:
                    new_pot_path= cls.pkgdir_join(high_pot_path.rsplit(f"*PKG DIR*{cls.seperator}",1)[1])
                if f"*USR DIR*{cls.seperator}" in high_pot_path:
                    new_pot_path= cls.usrdir_join(high_pot_path.rsplit(f"*USR DIR*{cls.seperator}",1)[1])

                return high_pot_path if new_pot_path is None else new_pot_path
            @classmethod
            def validate(cls, potential_path:str, /, return_exists:bool=True,return_isfile:bool=True,return_isdir:bool=True,return_valid_path:bool=True):
                """
                Validates a path with the given parameters

                Note: This reads the path EXACTLY as typed and does not interpret where the path leads.
                Use normalize_path() to handle relative paths first
                """
                #region input sanitation
                potential_path=str(potential_path).strip() if not isinstance(potential_path,str) else potential_path.strip()
                return_exists= True if isinstance(return_exists,bool) and return_exists is True else False
                return_isfile= True if isinstance(return_isfile,bool) and return_isfile is True else False
                return_isdir= True if isinstance(return_isdir,bool) and return_isdir is True else False
                return_valid_path= True if isinstance(return_valid_path,bool) and return_valid_path is True else False
                #endregion input sanitation
                path_found:bool=False
                path_isfile:bool=False
                path_isdir:bool=False

                if all({# inputs are false
                    return_exists is False,
                    return_isfile is False,
                    return_isdir is False,
                    return_valid_path is False,
                }):
                    return {}

                if return_exists is True:
                    path_found=True if _exists(potential_path) is True else False
                    if return_valid_path is True and path_found is False:# generate new path if not exist but path needs returned
                        try:
                            with open(potential_path,"w",encoding=Internal.Logger.Default.encoding):
                                pass
                        except Exception:
                            path_found=False
                        finally:
                            path_found=True if _exists(potential_path) is True else False

                if return_isfile is True:
                    path_isfile=True if _isfile(potential_path) is True else False
                if return_isdir is True:
                    path_isdir=True if _isdir(potential_path) is True else False

                results= {"exists":path_found,"isfile":path_isfile,"isdir":path_isdir}
                if return_valid_path is True: results["path"]=potential_path
                return results

            def __path_lock(func):
                """All directories passed are assumed sub-directories of the functions passed to this call"""
                def inner_call(path_to_add):
                    match str(func)[1:].rsplit(" ",2)[0]:
                        case "function Internal.SystemInfo.Path.rootdir_join":
                            root_dir_join__raw=func(path_to_add)
                            estimated_path=Internal.SystemInfo.Path.normalize_path(root_dir_join__raw)
                            if Internal.SystemInfo.Runtime.kwargs["ROOT DIR"] not in estimated_path:
                                raise ValueError("Path attempted to navigate out of the established root directory")
                            return estimated_path
                        case "function Internal.SystemInfo.Path.pkgdir_join":
                            pkg_dir_join__raw=func(path_to_add)
                            estimated_path=Internal.SystemInfo.Path.normalize_path(pkg_dir_join__raw)
                            if Internal.SystemInfo.Runtime.kwargs["ROOT DIR"] not in estimated_path:
                                raise ValueError("Path attempted to navigate out of the package directory")
                            return estimated_path
                    results= func(path_to_add)
                    return results
                return inner_call
            @__path_lock
            def rootdir_join(path_to_add:str)-> str:
                """Appends input to the end of the root directory under assumption input is a sub-directory of the root"""
                root_dir= Internal.SystemInfo.Runtime.kwargs["ROOT DIR"].strip()
                results= f"{root_dir}{_os_path_sep}{path_to_add.rsplit('*ROOT DIR*',1)[1] if '*ROOT DIR*' in path_to_add else path_to_add}"
                if "*USR DIR*" in results:
                    results= Internal.SystemInfo.Path.usrdir_join(results)
                if "*PKG DIR*" in results:
                    results= Internal.SystemInfo.Path.pkgdir_join(results)
                return results
            @__path_lock
            def pkgdir_join(path_to_add:str)-> str:
                """Appends input to the end of the package directory under assumption input is a sub-directory of the package"""
                pkg_dir= Internal.SystemInfo.Path.rootdir_join(Internal.SystemInfo.Runtime.kwargs["PKG DIR"])
                results= f"{pkg_dir}{_os_path_sep}{path_to_add.rsplit('*PKG DIR*',1)[1] if '*PKG DIR*' in path_to_add else path_to_add}"
                if "*USR DIR*" in results:
                    results= Internal.SystemInfo.Path.usrdir_join(results)
                if "*PKG DIR*" in results:
                    results= Internal.SystemInfo.Path.pkgdir_join(results)
                return results

            @classmethod
            def usrdir_join(cls, path_to_add:str)-> str:
                user_directory= Internal.SystemInfo.Settings.User().dir if Internal.SystemInfo.Settings.User().dir is not None else Internal.Logger.Default.user_dir

                path_already_added=False
                if "*USR DIR*" in path_to_add:
                    user_directory= f"{user_directory}{_os_path_sep}{path_to_add.split('*USR DIR*')[1].strip()}"
                    path_already_added=True
                if "*ROOT DIR*" in user_directory:
                    user_directory= Internal.SystemInfo.Path.rootdir_join(user_directory)
                if "*PKG DIR*" in user_directory:
                    user_directory= Internal.SystemInfo.Path.rootdir_join(user_directory)
                return user_directory if path_already_added==True else f"{user_directory}{_os_path_sep}{path_to_add.strip()}"

        class Calendar:
            """"Handles all things involving dates and times"""
            class Time:
                """Handles all functions pertaining to calculating time"""

                @classmethod
                def now(cls, international:bool=True, written:bool=False)-> str:
                    """Returns the current time"""
                    return Internal.SystemInfo.Calendar.Time.read_timestamp(
                            Internal.SystemInfo.Calendar.Time.timestamp(),
                            international=international,written=written
                        ).split(" ",1)[1]

                @classmethod
                def timestamp(cls, date_time:str=None)-> float:
                    """Returns a float value from the datetime library using the current system time or an optionally passed ```date time``` in string format"""
                    if not isinstance(date_time, (str,NoneType)):
                        raise TypeError("Inappropriate argument type for argument date_time, please try a str type input.")
                    elif date_time is None:
                        return datetime.timestamp(datetime.now())
                    date_time=date_time.replace("/","-")
                    date_indicator:str= "-"
                    time_indicator:str= ":"
                    ms_indicator:str= "." if "." in date_time else None

                    if any({date_indicator not in date_time, time_indicator not in date_time}):
                        raise ValueError("Inappropriate argument value (of correct type), please make sure the string includes both the date and the time.")

                    #region date find
                    date= date_time.split(" ",1)[0].replace(" ","").strip().split(date_indicator) if date_time.find(date_indicator)<date_time.find(" ") else date_time.split(" ")[1].replace(" ","").strip().split(date_indicator)
                    if 1<=int(date[1])<=12 and 1<=int(date[2])<=31:# yr/m/dy
                        year=int(date[0])
                        month=int(date[1])
                        day=int(date[2])
                    elif 1<=int(date[1])<=31 and 1<=int(date[2])<=12:# yr/dy/m
                        year=int(date[0])
                        day=int(date[1])
                        month=int(date[2])
                    elif 1<=int(date[0])<=12 and 1<=int(date[1])<=31:# m/dy/yr
                        month=int(date[0])
                        day=int(date[1])
                        year=int(date[2])
                    elif 1<=int(date[0])<=12 and 1<=int(date[2])<=31:# m/yr/dy
                        month=int(date[0])
                        year=int(date[1])
                        day=int(date[2])
                    elif 1<=int(date[0])<=31 and 1<=int(date[1])<=12:# dy/m/yr
                        day=int(date[0])
                        month=int(date[1])
                        year=int(date[2])
                    elif 1<=int(date[0])<=31 and 1<=int(date[2])<=12:# dy/yr/m
                        day=int(date[0])
                        year=int(date[1])
                        month=int(date[2])
                    else:# No format expected matched
                        raise ValueError(f"Could not establish a normalized date format, please check your input(date={date})")
                    #region verify valid date
                    short_months:dict={4:"Apirl",6:"June",8:"August",10:"October",12:"December"}
                    exception_month:int=2
                    if month==exception_month:
                        leap_yr=29 if _isleap(year) else 28
                        if leap_yr<day:
                            recommended_date=f"{year}-{month+1}-{day-leap_yr}"
                            raise ValueError(f"Invalid day({day}) for February of {year}! Perhaps you meant to use, {recommended_date} instead?")
                    elif day==31 and month in short_months:
                        recommended_date=f"{year}-{short_months[month+1]}-{day-30}"
                        raise ValueError(f"Invalid day({day}) for {short_months[month]} of {year}! Perhaps you meant to use, {recommended_date} instead?")
                    #endregion verify valid date
                    #endregion date find

                    #region configure time output for regions
                    time= date_time.split(" ",1)[1].replace(" ","").strip().lower() if date_time.split(" ",1)[1]!=date else date_time.split(" ",1)[0].replace(" ","").strip().lower()

                    #region assign hr:min:sec:ms
                    hour,minute,remaining=time[:-2].split(":")
                    if ms_indicator is not None:
                        second,microsecond=remaining.split(ms_indicator,1)
                        microsecond=int(microsecond)
                    else:
                        second,microsecond=remaining,0
                    if second=="":
                        second=0
                    hour,minute,second= int(hour),int(minute),int(second)
                    #endregion assign hr:min:sec:ms
                    international_format:bool= True if not time.endswith(("am","pm")) else False
                    if international_format is False:
                        hour= hour+12 if not time.endswith("pm") and hour<12 else hour

                    #region verify all values fall within proper ranges
                    if hour<0 or 23<hour:
                        print(hour)
                        raise ValueError("Hour is outside of range accepted for time format")
                    elif minute<0 or 59<minute:
                        raise ValueError("Minute is outside of range accepted for time format")
                    elif second<0 or 59<second:
                        raise ValueError("Second is outside of range accepted for time format")
                    elif microsecond<0 or 999999<microsecond:
                        raise ValueError("Microsecond is outside of range accepted for time format")
                    #endregion verify all values fall within proper ranges
                    #endregion configure time output for regions

                    return datetime(
                        year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute=minute,
                        second=second,
                        microsecond=microsecond
                        ).timestamp()
                @classmethod
                def read_timestamp(cls, snowflake:float, /, international:bool=True, written:bool=False)-> str:
                    """
                    Returns a human-readable string representation of the passed float value (snowflake)

                    ---

                    By default human_readable AND international are set to False

                    Example: 01-01-2024 00:00:00.000000
                    Format: nMonth-nDay-nYear 12hr:min:sec:ms(AM/PM)
                    """
                    year,month,day,hour,minute,*remaining= str(
                        datetime.fromtimestamp(snowflake)
                        ).replace("-"," ").replace(":"," ").replace("."," ").split(" ",6)
                    second=remaining[0]
                    if len(remaining)!=1:
                        microsecond= remaining[1]
                    else:
                        microsecond="000000"
                    month,day,hour= int(month),int(day),int(hour)

                    if written is True:
                        #region value aliasing
                        month_alias={
                            1:"January",
                            2:"February",
                            3:"March",
                            4:"April",
                            5:"May",
                            6:"June",
                            7:"July",
                            8:"August",
                            9:"September",
                            10:"October",
                            11:"November",
                            12:"December"
                        }
                        ending_pronounciation= {
                            1:"first",
                            2:"second",
                            3:"third",
                            4:"fourth",
                            5:"fifth",
                            6:"sixth",
                            7:"seventh",
                            8:"eigth",
                            9:"nineth",
                            10:"tenth",
                            11:"eleventh",
                            12:"twelfth",
                            13:"thirteenth",
                            14:"fourteenth",
                            15:"fifteenth",
                            16:"sixteenth",
                            17:"seventeenth",
                            18:"eighteenth",
                            19:"nineteenth",
                            20:"twentieth",
                            30:"thirtieth"
                        }
                        #endregion value aliasing
                        #region associate numeric with written form
                        if day<=20 or day==30:
                            day= ending_pronounciation[day]
                        elif 20<day<30:
                            day= f"twenty {ending_pronounciation[day-20]}"
                        else:
                            day="thirty first"
                        #endregion associate numeric with written form
                        if international is True:
                            return f"{hour}:{minute}:{second}.{microsecond} on the {day} day of {month_alias[month]}, {year}"
                        return f"{hour-12 if 12<hour else hour}:{minute}:{second}.{microsecond} {'AM' if hour<12 else 'PM'} on the {day} day of {month_alias[month]}, {year}"
                    #region format month,day,hour,minute,second
                    month= f"0{month}" if len(f"{month}")<2 else month
                    day= f"0{day}" if len(f"{day}")<2 else day
                    hour= f"0{hour}" if len(f"{hour}")<2 else hour
                    minute= f"0{minute}" if len(f"{minute}")<2 else minute
                    second= f"0{second}" if len(f"{second}")<2 else second
                    #endregion format month,day,hour,minute,second

                    if international is True:
                        return f"{year}-{month}-{day} {hour}:{minute}:{second}.{microsecond}"
                    return f"{year}-{month}-{day} {f'0{int(hour)-12}' if 12<int(hour) else hour}:{minute}:{second}.{microsecond} {'AM' if int(hour)<12 else 'PM'}"

                @classmethod
                def datetime_format(cls, /,international:bool=False, written=False)-> str:
                    """Returns the available output formats for dates and times"""
                    if international is False and written is False:
                        return "Month-Day-Year 12Hour:Minute:Second.Microsecond (AM/PM) UTC(+/-)HoursOffset"
                    elif international is True and written is False:
                        return "Year-Month-Day 24Hour:Minute:Second.Microsecond UTC(+/-)HoursOffset"

                    elif international is False and written is True:
                        return "12Hour:Minute:Second.Microsecond (AM/PM) UTC(+/-)HoursOffset on the nDayth day of wMonth, Year"
                    elif international is True and written is True:
                        return "24Hour:Minute:Second.Microsecond UTC(+/-)HoursOffset on the nDayth day of wMonth, Year"
                @classmethod
                def timestamp_offset(cls, snowflake_a:float, snowflake_b:float)-> str:
                    """Calculates the time offsets between 2 dates, must use datetime objects for calculation"""
                    if not isinstance(snowflake_a,float):
                        raise TypeError("Inappropriate argument type for snowflake_a.")
                    elif not isinstance(snowflake_b,float):
                        raise TypeError("Inappropriate argument type for snowflake_b.")
                    snowflake_a= datetime.fromtimestamp(snowflake_a)
                    snowflake_b= datetime.fromtimestamp(snowflake_b)
                    offset= f"+{snowflake_a-snowflake_b}" if snowflake_b<snowflake_a else f"-{snowflake_b-snowflake_a}"
                    offset_direction= offset[:1]
                    hour,minute,second=offset[1:].split(":")
                    second, microsecond= second.split(".")
                    if microsecond.startswith(("5","6","7","8","9")):
                        second=int(second)+1
                        microsecond=0

                        if second==60:
                            second=0
                            minute=int(minute)+1
                        if minute==60:
                            minute=0
                            hour=int(hour)+1
                        if hour==24:
                            hour=0
                            offset_direction="+"
                        return f"UTC{offset_direction}{hour}"
                    return f"UTC{offset_direction}{hour}"
                @classmethod
                def utc_offset(cls, /)-> float:
                    """returns utc or international time offsets"""
                    utc_time:float= datetime.timestamp(datetime.utcnow())
                    lan_time:float= cls.timestamp()
                    return cls.timestamp_offset(lan_time,utc_time)
            class Date:
                """Handles all things directly involving only the date"""
                def years_offset(count:int,starting_date:float)-> str:
                    """Returns information on the date of n years prior"""
                    if not isinstance(count,int):
                        raise TypeError("Inappropriate argument type for count.")
                    elif not isinstance(starting_date,float):
                        raise TypeError("Inappropriate argument type for starting_date.")

                    date,time= Internal.SystemInfo.Calendar.Time.read_timestamp(starting_date).split(" ")
                    year,month,day=date.split("-")
                    hour,minute,second=time.split(":")
                    second,microsecond=second.split(".")
                    year,month,day,hour,minute,second,microsecond=int(year),int(month),int(day),int(hour),int(minute),int(second),int(microsecond)
                    return str(datetime(year+count,month,day,hour,minute,second,microsecond))
                def months_offset(count:int,starting_date:float)-> str:
                    """Returns information on the date of n months prior"""
                    if not isinstance(count,int):
                        raise TypeError("Inappropriate argument type for count.")
                    elif not isinstance(starting_date,float):
                        raise TypeError("Inappropriate argument type for starting_date.")

                    date,time= Internal.SystemInfo.Calendar.Time.read_timestamp(starting_date).split(" ")
                    year,month,day=date.split("-")
                    hour,minute,second=time.split(":")
                    second,microsecond=second.split(".")
                    year,month,day,hour,minute,second,microsecond=int(year),int(month),int(day),int(hour),int(minute),int(second),int(microsecond)
                    count_is_neg:bool= True if str(count).startswith("-") else False

                    if count==0:
                        return f"{date} {time}"
                    elif count_is_neg is False and count+month<=12:
                        return str(datetime(year,month+count,day,hour,minute,second,microsecond))
                    elif count_is_neg is True and 1<=count-month:
                        return str(datetime(year,month+count,day,hour,minute,second,microsecond))
                    elif count%12==0:
                        return str(datetime(year+int(count/12),month,day,hour,minute,second,microsecond))
                    result_divmod= divmod(count,12)
                    return str(datetime(year+result_divmod[0],month+result_divmod[1],day,hour,minute,second,microsecond))
                def days_offset(count:int,starting_date:float)-> str:
                    """Returns information on the date of n days prior"""
                    if not isinstance(count,int):
                        raise TypeError("Inappropriate argument type for count.")
                    elif not isinstance(starting_date,float):
                        raise TypeError("Inappropriate argument type for starting_date.")

                    year,month,day,hour,minute,second,wkday,yrday,is_dst= datetime.fromtimestamp(starting_date).timetuple()
                    microsecond= Internal.SystemInfo.Calendar.Time.read_timestamp(starting_date).split(" ")[1].split(":")[-1].split(".")[1]
                    del month,day,wkday,is_dst
                    return f"{datetime(year, 1, 1, hour=hour,minute=minute,second=second) + _timedelta((yrday+count)-1)}.{microsecond}"
                @classmethod
                def offset(cls, snowflake_a:str,snowflake_b:str=None)->str:
                    time_alias=Internal.SystemInfo.Calendar.Time
                    snowflake_a=time_alias.timestamp(snowflake_a)
                    snowflake_b=time_alias.timestamp(snowflake_b) if not snowflake_b is None else time_alias.timestamp()
                    offset_snowflakes= _timedelta(seconds=snowflake_a-snowflake_b)
                    offset_time= str(offset_snowflakes).split(" ",2)[-1]
                    offset_hours,offset_minutes,offset_seconds= int(offset_time.split(":",2)[0]),int(offset_time.split(":",2)[1]),float(offset_time.split(":",2)[2])
                    expected_date=cls.days_offset(offset_snowflakes.days,snowflake_b)
                    return

            class Events:
                """Stores any time,date event that needs to be remembered"""
        def __init__(self,/)-> None:
            """Provides immutable information about the system as used by the package"""
            self.pkg_name:str=__package__.strip().split(".")[0]
            self._вuৰéमैंאָн:str=f"Developer.Sandbox.{self.pkg_name}.0.0.0.0.0.00000001"

            #region Gather basic information about the device currently being ran on
            self.platform= "mobile" if "aarch" in _platform() else "computer"
            match _system().lower():
                case "linux":
                    self.os="Linux"
                case "darwin":
                    self.os="MacOs"
                case "windows":
                    self.os="Windows"
                case _:
                    self.os=f"Unrecognized ({_system()})"
            self.os_version, self.os_distro, self.cpu= _temp_call.split("-",2) if (_temp_call:=f"{_system_release()}").lower()!="nt" else _system_version(); self.os_distro, self.cpu= self.os_distro.capitalize(), self.cpu.upper(); del _temp_call
            self.cpu_architecture= _machine()
            self.device:dict={
                "platform":self.platform,
                "os":self.os,
                "os version":self.os_version,
                "os distro":self.os_distro,
                "processor":self.cpu,
                "architecture":self.cpu_architecture
            }
            #endregion Gather basic information about the device currently being ran on

        #region Control version assignment for runtime
        @property
        def version(self,/)-> str:
            """
            ### Returns the current version release of the application

            Attempting to set the value will point the script to search for an update file/package at the specified path.

            ---

            Will continue using current version if one of the requirements are met:
            - Path is invalid
            - The updater fails
            - Package already up to date
            """
            # Version variable name is broken char for char into the following languages
            ## Russian
            ## Samoan
            ## Assamese
            ## Portugese
            ## Hindi
            ## Yiddish
            ## Serbian
        @version.getter
        def version(self,/)-> str:
            """
            Version format is as follows:

            Branch.Sub-Branch.PackageName.Rewrite.MajorUpdate.SecurityUpdate.BugFix.Patch.Snapshot
            """
            return self._вuৰéमैंאָн
        @version.setter
        def version(self,/, manual_update_path:str=None)-> None:
            """Recieves new value by calling the updater, defaults to current value if updater fails or is already newest update"""

            # Trying to fail the checks forcefully
            # Ensuring input is of matching qualities
            ## type(str)
            ## non-empty string
            ## not searching for default value
            ## matches expected file extension
            #
            # These checks are for where a file for updating the current version may be found
            if any({
                not isinstance(manual_update_path,str),
                manual_update_path.strip()=="",
                manual_update_path.strip().lower()=="default",
                not manual_update_path.endswith((".updt.lnk", ".version.pkg")),
                not manual_update_path.startswith((
                    f"Public.Stable.{self.pkg_name}.",
                    f"Public.Experimental.{self.pkg_name}.",
                    f"Developer.Stable.{self.pkg_name}.",
                    f"Developer.Experimental.{self.pkg_name}.",
                    f"Developer.Sandbox.{self.pkg_name}.",
                    ))
                }):
                return
            Internal.UpdateChecker(update_file=manual_update_path)
        #endregion Assign version for runtime

    class Logger:
        """Records events from the current application to an output file to track what potentially caused the reported issue"""
        class Default:
            """Default values for the logger"""
            level:dict={"value":20,"alias":"Info"}
            encoding:Literal["utf-8"]="utf-8"
            handler:str="file"
            user_dir:str="*ROOT DIR*/usr"
            output_path:str= "*USR DIR*/logs" if handler.lower().strip()=="file" else None
            allowed_levels:list= ["Debug","Info","Warning","Error","Critical"]
        @classmethod
        def normalize_level(cls, new_level:str|int)-> dict:
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
                    raise TypeError(f"new_level must be of type string, integer or floating-point, not {type(new_level)}")
                case _:# all unexpected inputs
                    raise TypeError(f"new_level must be of type string, integer or floating-point, not {type(new_level)}")

            if new_level=="":
                raise ValueError("new_level must not be an empty string! Please double check your inputs...")
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
                    except ValueError:# due to not being able to convert to int, so default value instead
                        return Internal.Logger.Default.level

        def __init__(self, output_path:str=Default.output_path,
                     encoding:str="utf-8",
                     handler:Literal["file","console"]="file",
                     level:Literal[10,"Debug",20,"Info",30,"Warning",40,"Error",50,"Critical"]=Default.level
                     ) -> NoneType:
            self.__level:dict=self.normalize_level(new_level=level)
            #region WIP
            self.__output_path:str= Internal.SystemInfo.Path.validate(output_path,False,False,False,True)["path"]
            self.__handler:str= self.__pick_handler(handler)
            self.__encoding:str= self.__check_encoding(encoding)
            self.__current_session_log_file:str=None
            #endregion WIP
        def write_to_output(self, *content:str)-> NoneType:
            """Writes contents to a file, please ensure the content parsed is already formatted"""

            def detect_format(msg:str)->bool:
                """Returns True if message is a valid format else corrects it, this may cause unwanted messages, please ensure messages are already formatted"""
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
                        output_enabled:bool= True if self.level["value"]<=self.normalize_level(line[1:].split("]",1)[0])["value"] else False
                        if detect_format(line) is False:
                            output_enabled=False
                        print(line) if output_enabled is True else ""
                    return
                case "file":
                    self.__current_session_log_file=f"{Internal.SystemInfo.Path.normalize_path(self.output_path)}{Internal.SystemInfo.Path.seperator}{content[0][content[0].find(']')+1:content[0].find('|')].replace('.','_',1)}.log" if self.__current_session_log_file is None else self.__current_session_log_file

                    if Internal.SystemInfo.Path.validate(self.__current_session_log_file,True,True,False,True)["exists"] is False:
                        _mkdir(f"{Internal.SystemInfo.Path.normalize_path(self.output_path)}{Internal.SystemInfo.Path.seperator}")

                    with open(file=self.__current_session_log_file,
                        mode="a",
                        encoding=self.encoding
                    ) as active_output_log_file:
                        for line in content:
                            output_enabled:bool= True if self.level["value"]<=self.normalize_level(line[1:].split("]",1)[0])["value"] else False
                            if detect_format(line) is False:
                                output_enabled=False
                            active_output_log_file.write(f"{line.strip()}\n") if output_enabled is True else ""

        #region level
        @property
        def level(self)-> dict:
            return self.__level
        @level.getter
        def level(self)-> dict:
            return self.__level
        @level.setter
        def level(self, new_level:Literal[10,"Debug",20,"Info",30,"Warning",40,"Error",50,"Critical"])-> NoneType:
            self.__level= self.normalize_level(new_level)
        #endregion level
        #region output_path
        @property
        def output_path(self)-> dict:
            return self.__output_path
        @output_path.getter
        def output_path(self)-> dict:
            return self.__output_path
        @output_path.setter
        def output_path(self, new_path)-> NoneType:
            self.__output_path= Internal.SystemInfo.Path.validate(new_path) if not Internal.SystemInfo.Path.validate(new_path,
                                    return_exists=False,
                                    return_isfile=False,
                                    return_isdir=False,
                                    return_new_path=True
                                    )[0] is None else self.Default.output_path
        #endregion output_path
        #region current session file
        @property
        def current_file(self)-> str|NoneType:
            return self.__current_session_log_file
        @current_file.getter
        def current_file(self)-> str|NoneType:
            return self.__current_session_log_file
        @current_file.setter
        def current_file(self, new_path)-> NoneType:
            output_results= Internal.SystemInfo.Path.validate(Internal.SystemInfo.Path.normalize_path(f"{new_path}"))
            if output_results["exists"] is None:
                _mkdir(output_results)
            self.__current_session_log_file=output_results
        #endregion current session file
        #region handler
        def __pick_handler(self, output_handler:Literal["console","file"])-> str:
            output_handler=fr"{output_handler}".strip().lower().replace(" ","")
            #output_handler="file" if Internal.SystemInfo.Runtime.kwargs.get()
            return "console" \
                if output_handler=="console" \
                    and self.level["alias"].lower()=="debug" \
                else "file"
        @property
        def handler(self)-> dict:
            return self.__handler
        @handler.getter
        def handler(self)-> dict:
            return self.__handler
        @handler.setter
        def handler(self, alt_handler:str)-> NoneType:
            self.__handler= self.__pick_handler(alt_handler)
        #endregion handler
        #region encoding
        def __check_encoding(self, value:str, /)-> str:
            try:
                value_found=str(_lookup(value)).split("encoding ",1)[1].split(" ",1)[0]
            except LookupError:
                value_found=self.Default.encoding
            finally:
                return value_found
        @property
        def encoding(self)-> dict:
            return self.__encoding
        @encoding.getter
        def encoding(self)-> dict:
            return self.__encoding
        @encoding.setter
        def encoding(self, new_encoding:str)-> NoneType:
            self.__encoding= self.__check_encoding(new_encoding)
        #endregion encoding

    class GraphicalUserInterface:
        """Functions for a gui if enabled"""
        class PreBoot:
            """Visual for end-user that the program has launched"""
        class Window:
            """This is a tutorial & welcome to user's who have freshly installed this package"""

        def __init__(self, /)-> None:
            pass
    class Library:
        """Reused functions"""
        class Sanitation:
            """ """
        class Mathapedia:
            """ """
    class UpdateChecker:
        """Checks current version for update"""
        class InternetConnection:
            """Handles any outbout traffic which can be referenced elsewhere within the script"""

            def __init__(self,/):
                self.connection_available:bool=True if self.test_connection() is not None else False
            def test_connection(self,/)-> dict|None:
                """Tests the current connection to see if it is established"""
        def __init__(self, updater_path:str=None) -> None:
            self.auto_updates_enabled:bool=False if updater_path is not None and isinstance(updater_path,str) and updater_path.strip()!="" else True
            if self.auto_updates_enabled is True:
                Internal.UpdateChecker(updater_path)

class GlobalAPI:
    """
    Globally Accessible Program Interface

    ---

    This does not directly execute code but can be used as a means of standardizing information to be parsed throughout the package.

    If something is reusable in the package it can be found here.

    This api is to filter out unwanted variables from leaking through into unwanted spaces
    """
    def __init__(self, *args,**kwargs) -> None:
        pass# must accept global args and kwargs so it may be called

    class SystemInfo:
        """Returns information about the system and any direct access to the system that is a non-logger event"""
        class Settings:
            """WIP"""
            class Factory:
                """WIP"""
            class PlugIns:
                """WIP"""
            class User:
                """WIP"""
            class Finalized:
                """WIP"""
        class Runtime:
            """Returns the Args & Kwargs parsed at runtime with pkg call"""
            args=Internal.SystemInfo.Runtime.args
            kwargs=Internal.SystemInfo.Runtime.kwargs
        class Path(Internal.SystemInfo.Path):
            """ """
        class Calendar:
            """ """
            class Time(Internal.SystemInfo.Calendar.Time):
                """ """
            class Date(Internal.SystemInfo.Calendar.Date):
                """ """
            class Events(Internal.SystemInfo.Calendar.Events):
                """ """
        pkg_name,version,device=Internal.SystemInfo().pkg_name,\
            Internal.SystemInfo().version, \
            Internal.SystemInfo().device

    class Logger(Internal.Logger):
        """Standardized event logging script for the package"""

        def decorator(self, func)-> Any|NoneType:
            """
            This is a wrapper-decorator to automatically log function calls

            NOTE: If the log level is not a valid value found, it will use the logger default log level value

            ---

            :log_lvl: Sets the level of the reported logging from the active function

            :return_value: Determines whether or not the function's return value is given

            :call_reason: Message the logger uses to record that an action has been taken
            """

            def log_action(*args,**kwargs)-> Any|NoneType:
                """Logs the function's call and end. You will need to manually call the logger from within the function to gain further logging details"""

                log_lvl=self.normalize_level(kwargs.get("log_lvl","Info"))
                return_value=kwargs.get("return_value",False)
                call_reason=reason if (reason:=f'{kwargs.get("call_reason","to do unknown...")}'.strip())!="" else "to do unknown..."

                if not isinstance(return_value,bool):
                    raise TypeError(f"Inappropriate argument type for return_value of type({type(return_value)}).")

                output_enabled:bool=False
                if self.level["value"]<=log_lvl["value"]:
                    output_enabled=True
                    origin_time=Internal.SystemInfo.Calendar.Time.timestamp()
                    custom_output_msg=f"[{log_lvl['alias'].upper()}]{origin_time}|Calling {func.__qualname__} {call_reason}"
                    self.write_to_output(custom_output_msg)

                func_return_value= func(args,kwargs)

                if output_enabled is True:
                    end_time=Internal.SystemInfo.Calendar.Time.timestamp()
                    custom_output_msg=f"[{log_lvl['alias'].upper()}]{end_time}|Finished calling {func.__qualname__}. The call took aproximately {end_time-origin_time:.6f} seconds"
                    self.write_to_output(custom_output_msg)

                return None if return_value is False or output_enabled is False else func_return_value
            return log_action
        def format_output(self, log_lvl:int|str, time:float, msg:str)-> str:
            """Takes a few inputs to format a standardaized output for logging events"""
            if not isinstance(log_lvl,(int,str)):
                raise TypeError(f"Inappropriate argument type for log_lvl.")
            elif not isinstance(time,(float,int)):
                raise TypeError(f"Inappropriate argument type for time.")
            elif not isinstance(msg,str):
                raise TypeError(f"Inappropriate argument type for msg.")
            if msg.strip()=="":
                msg="to do unknown..."
            else:
                msg=msg.strip()
            if isinstance(time,int):
                time=float(time)
            if time<=0.0:
                time=Internal.SystemInfo.Calendar.Time.timestamp()
            log_lvl=self.normalize_level(log_lvl)

            return f"[{log_lvl['alias'].upper()}]{time}|{msg[:1].capitalize()+msg[1:]}"
    class GraphicalUserInterface(Internal.GraphicalUserInterface):
        """WIP: Handles visual interactive windows shown for end-user experience"""
    class Library:
        """WIP: Handles functions commonly used throughout the package not stored elsewhere"""
        class Sanitation:
            """WIP: Sterilizes various input types"""
        class Mathapedia(Internal.Library.Mathapedia):
            """WIP: Attempts to solve formulas to generate an answer for the equation"""
    class UpdateChecker(Internal.UpdateChecker):
        """WIP: Attempts and handles updating of core files for the package"""
    class PlugIns(PlugIns):
        """WIP: Handles everything involving plug-ins that're non-settings related"""


# Status of the api results: WIP
# Status will remain in WIP until:
#   the minimum of everything besides the library node
#   no longer has a WIP status
#
#   Library node is used to add new features to the package internally,
#   hence will always be in WIP unless no new recent features and,
#   existing features have been implemented
#
# =====================================================================
#
# Notes about the api:
# This api is designed to streamline the process of setting up and,
#   managing the launching of the package with the proper properties,
#   be usable with any package as well as serve as a package template.
#   The package is also designed to also provide some internal modules
#       for global access
#
#
# GlobalAPI (WIP)
#       region SystemInfo (WIP)
#           region Settings (WIP)
#               read (finished)
#               Factory (WIP)
#               PlugIns (WIP)
#               User (WIP)
#               Finalized (WIP)
            #endregion Settings
#           region Runtime (Finished)
#               args (Finished)
#               kwargs (Finished)
                #endregion Runtime
#           region Path (Finished)
#               normalize_path (Finished)
#               validate (Finished)
#               __path_lock (Finished)
#               rootdir_join (Finished)
#               pkgdir_join (Finished)
#               usrdir_join (Finished)
#               seperator (Finished)
                #endregion Path
#           region Calendar (WIP)
#               region Time (Finished)
#                   now (Finished)
#                   timestamp (Finished)
#                   read_timestamp (Finished)
#                   datetime_format (Finished)
#                   timestamp_offset (Finished) # currently requires datetime module inputs, replace with timestamps
#                   utc_offset (Finished)
                    #endregion Time
#               Date (WIP)
#               Events (WIP)
                #endregion Calendar
#           pkg_name (Finished)
#           version (Finished)
#           device (Finished)
            #endregion SystemInfo
#       region Logger (Finished)
#           region Default (Finished)
#               level (Finished)
#               encoding (Finished)
#               handler (Finished)
#               user_dir (WIP)
#               output_path (Finished)
#               allowed_levels (Finished)
                #endregion Default
#           decorator (Finished)
#           format_output (Finished)
#           normalize_level (Finished)
#           write_to_output (Finished)
#           level (Finished)
#           output_path (Finished)
#           current_file (Finished)
#           handler (Finished)
#           encoding (Finished)
            #endregion Logger
#       region GUI (WIP)
#           PreBoot (WIP)
#           Window (WIP)
            #endregion GUI
#       region Library (WIP)
#           Sanitation (WIP)
#           Mathapedia (WIP)
            #endregion Library
#       region UpdateChecker (WIP)
#           region InternetConnection (WIP)
#               connection_available (WIP)
#               test_connection (WIP)
                #endregion InternetConnection
#           auto_updates_enabled (WIP)
#           updater_path (WIP)
            #endregion UpdateChecker
#       region PlugIns (WIP)
            #endregion PlugIns
