"""
Used to obfuscate variables from namespace

rename class Path to "path" upon import
"""

#required by everything involving paths
from os.path import sep as _os_path_sep
#required by _validate_path_credentials()
from os import mkdir as _mkdir
from os.path import \
    exists as _exists, \
    isdir as _isdir, \
    isfile as _isfile
# required by _normalize_path_string()
from os.path import expanduser as _user_home_dir
from re import match as _regular_expression_match
# required by lock_path()
from typing import Literal
from types import NoneType

from pkg.api.application import Info as _Info

def _normalize_path_string(potential_path:str)-> str|None:
    """
    Takes a given string and attempts to ensure it follows path patterns
    of the local operating system

    Only accepts paths containing a-z,A-Z,0-9,.,",",;,',[,],{,},(,&,^,%,$,#,@,!,`,~,-,_,=,+,)

    Only use "~" followed by a path seperator
    in the path to signify a route to the home directory

    ---

    If on Windows and wish to find a directory within the AppData directory,
    use "%" on both sides of the appdata route alias followed by a path seperator

    ---

    If you wish to use relative paths use the path function for the corresponding path you
    are wishing to extend off of

    ---

    If you need to change the targets for the following:
    - *ROOT DIR*
    - *PKG DIR*
    - *USR DIR*
    - *LOG DIR*
    - *PLUG-IN DIR*

    please change these values in the "Default" sibling class
    """
    #region Clean user input
    sterilized_potential_path:str= f"{potential_path !r}"\
        .replace("\\","/")\
        .replace("/",_os_path_sep)\
        .replace("\"","")\
        .replace("?","")\
        .replace("<","")\
        .replace(">","")\
        .replace("|","")
    if sterilized_potential_path.startswith("'") and sterilized_potential_path.endswith("'"):
        sterilized_potential_path=sterilized_potential_path[1:-1]
    while f"{_os_path_sep}{_os_path_sep}" in sterilized_potential_path:
        sterilized_potential_path= sterilized_potential_path\
            .replace(f"{_os_path_sep}{_os_path_sep}",_os_path_sep)
    #region Excuse "*" from results temporarily
    if "*ROOT DIR*" in sterilized_potential_path:
        alias:str="*ROOT DIR*"
        root_dir:str=Path.Default.root_dir
        new_path:str=_p\
            if (_p:=sterilized_potential_path.rsplit(alias,1)[1]).startswith(_os_path_sep) \
            else sterilized_potential_path.rsplit(alias,1)[1]+_os_path_sep
        sterilized_potential_path=root_dir+new_path
    if "*PKG DIR*" in sterilized_potential_path:
        alias:str="*PKG DIR*"
        pkg_dir:str=Path.Default.pkg_dir
        new_path:str=_p\
            if (_p:=sterilized_potential_path.rsplit(alias,1)[1]).startswith(_os_path_sep) \
            else sterilized_potential_path.rsplit(alias,1)[1]+_os_path_sep
        sterilized_potential_path=pkg_dir+new_path
    if "*USR DIR*" in sterilized_potential_path:
        alias:str="*USR DIR*"
        usr_dir:str=Path.Default.usr_dir
        new_path:str=_p\
            if (_p:=sterilized_potential_path.rsplit(alias,1)[1]).startswith(_os_path_sep) \
            else sterilized_potential_path.rsplit(alias,1)[1]+_os_path_sep
        sterilized_potential_path=usr_dir+new_path
    if "*LOG DIR*" in sterilized_potential_path:
        alias:str="*LOG DIR*"
        log_dir:str=Path.Default.log_dir
        new_path:str=_p\
            if (_p:=sterilized_potential_path.rsplit(alias,1)[1]).startswith(_os_path_sep) \
            else sterilized_potential_path.rsplit(alias,1)[1]+_os_path_sep
        sterilized_potential_path=log_dir+new_path
    if "*PLUG-IN DIR*" in sterilized_potential_path:
        alias:str="*PLUG-IN DIR*"
        plugin_dir:str=Path.Default.plugin_dir
        new_path:str=_p\
            if (_p:=sterilized_potential_path.rsplit(alias,1)[1]).startswith(_os_path_sep) \
            else sterilized_potential_path.rsplit(alias,1)[1]+_os_path_sep
        sterilized_potential_path=plugin_dir+new_path
    if any((# purge remaining iterations of an * in path
        "*ROOT DIR*" in sterilized_potential_path,
        "*PKG DIR*" in sterilized_potential_path,
        "*USR DIR*" in sterilized_potential_path,
        "*LOG DIR*" in sterilized_potential_path,
        "*PLUG-IN DIR*" in sterilized_potential_path
    )) is True:
        sterilized_potential_path:str=_normalize_path_string(sterilized_potential_path)
        sterilized_potential_path=f"{sterilized_potential_path}".replace("*","")
    #endregion Excuse "*" from results temporarily
    #endregion Clean user input
    #region Bleach aliased paths
    if any((# alias to home directory present
        f"~{_os_path_sep}" in sterilized_potential_path \
            and sterilized_potential_path[0]=="~",
        f"{_os_path_sep}~{_os_path_sep}" in sterilized_potential_path
        )):
        sterilized_potential_path:str=f"{_user_home_dir('~')}"+\
            f"{_os_path_sep}{sterilized_potential_path.rsplit(f'~{_os_path_sep}',1)[1]}"
        # change path to start from home dir starting from the alias indicator
    match _Info.device["os"].lower():
        case "windows":
            #region aliases to the AppData directory
            if sterilized_potential_path.lower().startswith((
                f"{_os_path_sep}%appdata%{_os_path_sep}",
                f"%appdata%{_os_path_sep}",
                )
            ) or f"%appdata%{_os_path_sep}" in sterilized_potential_path.lower():
                _lowered:str=sterilized_potential_path.lower()\
                    .rsplit(f'%appdata%{_os_path_sep}',1)[0]+\
                    f"%appdata%{_os_path_sep}"
                sterilized_potential_path:str=f"{_user_home_dir('~')}"+\
                    f"{_os_path_sep}AppData{_os_path_sep}Roaming"+\
                    f"{_os_path_sep}{sterilized_potential_path[len(_lowered):]}"
            if sterilized_potential_path.lower().startswith((
                f"{_os_path_sep}%localappdata%{_os_path_sep}",
                f"%localappdata%{_os_path_sep}",
                )
            ) or f"%localappdata%{_os_path_sep}" in sterilized_potential_path.lower():
                _lowered:str=sterilized_potential_path.lower()\
                    .rsplit(f'%localappdata%{_os_path_sep}',1)[0]+\
                    f"%localappdata%{_os_path_sep}"
                sterilized_potential_path:str=f"{_user_home_dir('~')}"+\
                    f"{_os_path_sep}AppData{_os_path_sep}Local"+\
                    f"{_os_path_sep}{sterilized_potential_path[len(_lowered):]}"
            if sterilized_potential_path.lower().startswith((
                f"{_os_path_sep}%locallowappdata%{_os_path_sep}",
                f"%locallowappdata%{_os_path_sep}",
                )
            ) or f"%locallowappdata%{_os_path_sep}" in sterilized_potential_path.lower():
                _lowered:str=sterilized_potential_path.lower()\
                    .rsplit(f'%locallowappdata%{_os_path_sep}',1)[0]+\
                    f"%locallowappdata%{_os_path_sep}"
                sterilized_potential_path:str=f"{_user_home_dir('~')}"+\
                    f"{_os_path_sep}AppData{_os_path_sep}LocalLow"+\
                    f"{_os_path_sep}{sterilized_potential_path[len(_lowered):]}"
            #endregion aliases to the AppData directory
    #endregion Bleach aliased paths
    #region check for invalid path names
    drive:str=""
    if 0<sterilized_potential_path.find(":"):# set drive location
        drive=sterilized_potential_path.split(":",1)[0].strip()+":"
    if sterilized_potential_path.startswith(_os_path_sep):# ensure path is common structure
        sterilized_potential_path=sterilized_potential_path[len(_os_path_sep):]
    _broken_path:list=sterilized_potential_path.split(_os_path_sep)
    _fixed_path:list=[]
    for directory in _broken_path:
        dr:str=directory.strip()
        while dr.endswith("."):
            dr=dr[:-1].strip()
        _fixed_path.append(dr)
    sterilized_potential_path=_os_path_sep+_os_path_sep.join(_fixed_path)
    #endregion check for invalid path names
    #region Validate user input
    pattern_format:str=r"^[/][a-zA-Z0-9\,\.\'\{\}\[\]\;\-\_\+\=\`\~\!\@\#\$\%\^\&\(\)]?"+\
        r"[a-zA-Z0-9\'\{\}\[\]\;\-\_\=\`\~\!\@\#\$\%\^\&\(\)\s/]*"
    #endregion Validate user input
    results:str=f"{drive}{sterilized_potential_path}"
    while f"{_os_path_sep}{_os_path_sep}" in results:
        results=results.replace(f"{_os_path_sep}{_os_path_sep}",_os_path_sep)
    return results if _regular_expression_match(
            pattern_format,
            sterilized_potential_path
            ) is not None else None
def _validate_path_credentials(potential_path:str,
    create_path_as_file:bool=False,
    create_path_as_dir:bool=False)-> dict:
    """
    Recieves a potential path as an input with optional flags

    ---

    Expected output documentation:

    :exists: Returns if the given path exists
    :isfile: Returns if the given path is an existing file
    :create_path_as_file: Attempts to create the provided as a file
    :isdir:  Returns if the given path is an existing directory
    :create_path_as_dir: Attempts to create the provided as a directory

    NOTE: Cannot have both create file and dir active simultaneously,
    this behaviour is the already the default when creating a file into directories
    that also do not yet exist.
    """
    #region Sterilize inputs
    if not isinstance(potential_path,str):
        raise TypeError("Invalid type for potential path, please ensure it is of type string.")
    elif not isinstance(create_path_as_file,bool):
        boolean_error:str="Invalid type for create_path_as_file,"+\
            " please ensure it is of type boolean."
        raise TypeError(boolean_error)
    elif not isinstance(create_path_as_dir,bool):
        boolean_error:str="Invalid type for create_path_as_dir,"+\
            " please ensure it is of type boolean."
        raise TypeError(boolean_error)
    elif create_path_as_file is True and create_path_as_dir is True:
        input_error:str="Please only choose 1 option"+\
            " when choosing between create_path_as_file and create_path_as_dir"
        raise ValueError(input_error)
    else:
        sterile_path:str|None=_normalize_path_string(potential_path)\
            .replace(_os_path_sep+_os_path_sep,_os_path_sep)
        if sterile_path is None:# Result failed
            raise ValueError("Failed to normalize path, please ensure inputs are correct.")
        del potential_path
    #endregion Sterilize inputs
    #region Validate
    path_exists:bool=_exists(sterile_path)
    path_isfile:bool=_isfile(sterile_path)
    path_isdir :bool=_isdir (sterile_path)
    #region Generate path and update validations
    if path_exists is False and create_path_as_file is True:
        parent_dir:str=sterile_path.rsplit(_os_path_sep,1)[0]
        _placeholder_path:str=parent_dir \
            if parent_dir[1]!=":" \
            else parent_dir.split(_os_path_sep,1)[0]
        drive:str|NoneType=parent_dir.split(_os_path_sep,1)[0] \
            if parent_dir[1]==":" \
            else None
        confirmed_paths:list=[drive,] if drive is not None else []
        for _dir in _placeholder_path.split(_os_path_sep):
            if _dir.strip()=="":
                confirmed_paths.append(_os_path_sep)
                continue
            elif _exists(_os_path_sep.join(confirmed_paths)+_dir) is True:
                confirmed_paths.append(_dir+_os_path_sep)
                continue
            try:
                _mkdir((confirmed_paths:="".join(confirmed_paths)+_dir+_os_path_sep))
            except MemoryError as exc:
                err:str="Sorry, looks like the application ran out of usable RAM"
                raise MemoryError(err) from exc
            except OSError as exc:
                err="Sorry, it looks like the path could not be created due to an unknown error"
                raise OSError(err) from exc

        try:
            with open(sterile_path,"x", encoding="utf-8") as newly_made_path:
                newly_made_path.close()
            path_exists:bool=_exists(sterile_path)
            path_isfile:bool=_isfile(sterile_path)
            path_isdir :bool=_isdir (sterile_path)
        except MemoryError as exc:
            raise MemoryError("Sorry, looks like the application ran out of usable RAM") from exc
        except OSError as exc:
            raise OSError("Sorry, it looks like the path could not be created") from exc
    elif path_exists is False and create_path_as_dir is True:
        try:
            _mkdir(sterile_path)
            path_exists:bool=_exists(sterile_path)
            path_isfile:bool=_isfile(sterile_path)
            path_isdir :bool=_isdir (sterile_path)
        except MemoryError as exc:
            raise MemoryError("Sorry, looks like the application ran out of usable RAM") from exc
        except OSError as exc:
            raise OSError("Sorry, looks like the application ran out of usable RAM") from exc
    #endregion Generate path and update validations
    output_dict:dict={
        "path":sterile_path,
        "exists": path_exists,
        "isfile": path_isfile,
        "isdir" : path_isdir
    }
    #endregion Validate
    return output_dict
def _lock_path(potential_path:str,root_dir:Literal["root","pkg","usr","log","plug-in"])-> str:
    """
    Attempts to handle relative paths and keeps them within range of the given root directory

    ---

    Does NOT account for relative paths,
    only the first detected relative path if matched with the root_dir is recognized
    """
    if not isinstance(potential_path,str):
        raise TypeError("Please ensure the provided path is a string")
    elif not isinstance(root_dir,str):
        raise TypeError("Please ensure the provided root_dir is a string")
    else:
        potential_path=potential_path.strip().removeprefix(_os_path_sep)
        root_dir:str=f"{root_dir.strip().lower()} dir" \
            if not root_dir.strip().lower().endswith(" dir") \
            else root_dir.strip().lower()

    if potential_path.split(_os_path_sep,1)[0].strip().lower().strip("*")==root_dir:
        potential_path=potential_path.split(_os_path_sep,1)[1].strip().removeprefix(_os_path_sep)
    match root_dir:
        case "root"|"root dir":
            confirmed_root:str=Path.Default.root_dir+_os_path_sep
        case "pkg"|"pkg dir":
            confirmed_root:str=Path.Default.pkg_dir+_os_path_sep
        case "usr"|"usr dir"|"user dir":
            confirmed_root:str=Path.Default.usr_dir+_os_path_sep
        case "log"|"logs"|"logs dir"|"log dir":
            confirmed_root:str=Path.Default.log_dir+_os_path_sep
        case "plugin"|"plug-in"|"plug_in"|"plugins"|"plug-ins"|"plug_ins":
            confirmed_root:str=Path.Default.plugin_dir+_os_path_sep
        case "plugin dir"|"plug-in dir"|"plug_in dir"|"plugins dir"|"plug-ins dir"|"plug_ins dir":
            confirmed_root:str=Path.Default.plugin_dir+_os_path_sep
        case _:# reject any unknown path roots
            raise ValueError("Invalid root_dir entry, please ensure it is valid")
    #region sift for relative pathing
    broken_path:list=[]
    for _dir in potential_path.split(_os_path_sep):
        _dir=_dir.strip()
        # ignores empty and standard string directories
        if _dir.endswith("."):# Checks if string is ONLY "."*len()
            if len(_dir)!=_dir.count("."):# string is valid format but ends with "."
                while _dir.endswith("."):
                    _dir=_dir.removesuffix(".").strip()
                broken_path.append(_dir)
                continue
            # full string is guaranteed to be relative path
            go:int=__counter \
                if 0<=(__counter:=_dir.count(".")-1) \
                    and 0<len(broken_path) \
                else 0
            # ensure distance is within range of the broken path length
            go= go if go<=len(broken_path) else len(broken_path)
            # go is guaraunteed to be range(0,len(_dir))
                # ensures broken path has an entry,
                #and go is greater than 0
            if 0<go:# go up is allowed and restricted to length of the broken path
                for i in range(go):# dynamically purge broken path as navigating up
                    del i
                    broken_path.pop(-1)
                    continue
            continue
        broken_path.append(_dir)
    #endregion sift for relative pathing
    return confirmed_root+_os_path_sep.join(broken_path)


class Path:
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
    - normalize "Normalizes path across platforms"
    - validate "Validates the credentials of a path, and optionally creates"
    - join_root "Assumes path as a sub-directory of the root directory"
    - join_pkg "Assumes path as a sub-directory of the application"
    - join_user "Assumes path as a sub-directory of the user directory"
    - join_logs "Assumes path as a sub-directory of the logs directory"
    - join_plugins "Assumes path as a sub-directory of the plug-ins directory"
    - seperator "Operating System path seperator"
    """
    class Default:
        """
        Stores default path values

        ---

        Available Calls:
        - root_dir "Root directory containing the application"
        - pkg_dir "Directory containing the application"
        - usr_dir "Directory containing the user settings"
        - log_dir "Logging directory containing the output logs"
        - plugin_dir "Directory containing the plug-ins for the application"
        """
        root_dir:str=_Info.kwargs["ROOT DIR"]
        pkg_dir:str=root_dir+_os_path_sep+_Info.name
        usr_dir:str=_Info.kwargs.get("--USRDIR",f"*ROOT DIR*{_os_path_sep}user")
        log_dir:str=_Info.kwargs.get("--LOG_OUTPUT",f"*USR DIR*{_os_path_sep}logs")
        plugin_dir:str=f"*USR DIR*{_os_path_sep}plug_ins"
    @staticmethod
    def normalize(potential_path:str)-> str|None:
        """
        Takes a given string and attempts to ensure it follows path patterns
        of the local operating system

        Only accepts paths containing a-z,A-Z,0-9,.,",",;,',[,],{,},(,&,^,%,$,#,@,!,`,~,-,_,=,+,)

        Only use "~" followed by a path seperator
        in the path to signify a route to the home directory

        ---

        If on Windows and wish to find a directory within the AppData directory,
        use "%" on both sides of the appdata route alias followed by a path seperator

        ---

        If you wish to use relative paths use the path function for the corresponding path you
        are wishing to extend off of
        - join_root()
        - join_pkg()
        - join_user()
        - join_log()
        - join_plugin()

        ---

        If you need to change the targets for the following:
        - *ROOT DIR*
        - *PKG DIR*
        - *USR DIR*
        - *LOG DIR*
        - *PLUG-IN DIR*

        please change these values in the "Default" sibling class
        """
        return _normalize_path_string(potential_path=potential_path)
    @staticmethod
    def validate(potential_path:str,
        create_path_as_file:bool=False,
        create_path_as_dir:bool=False)-> dict:
        """
        Recieves a potential path as an input with optional flags

        ---

        Expected output documentation:

        :path: Returns the normalized path
        :exists: Returns if the given path exists
        :isfile: Returns if the given path is an existing file
        :isdir:  Returns if the given path is an existing directory

        ---

        Force validation via inputs (only select 1 of the 2)

        :create_path_as_file: Attempts to create the provided as a file
        :create_path_as_dir: Attempts to create the provided as a directory
        """
        return _validate_path_credentials(potential_path,
            create_path_as_file,
            create_path_as_dir)

    @classmethod
    def join_root(cls, path_to_add:str="")-> str:
        """
        Returns a path as a subdirectory of the root directory of the application

        > Does not accept aliased paths
        """
        return _lock_path(path_to_add,"root")
    @staticmethod
    def join_pkg(path_to_add:str="")-> str:
        """
        Returns a path as a subdirectory of the application

        > Does not accept aliased paths
        """
        return _lock_path(path_to_add,"pkg")
    @staticmethod
    def join_user(path_to_add:str="")-> str:
        """
        Returns a path as a subdirectory of the user directory of the application

        > Does not accept aliased paths
        """
        return _lock_path(path_to_add,"usr")
    @staticmethod
    def join_logs(path_to_add:str="")-> str:
        """
        Returns a path as a subdirectory of the logs directory of the application

        > Does not accept aliased paths
        """
        return _lock_path(path_to_add,"logs")
    @staticmethod
    def join_plugins(path_to_add:str="")-> str:
        """
        Returns a path as a subdirectory of the plug-in directory of the application

        > Does not accept aliased paths
        """
        return _lock_path(path_to_add,"plug-ins")
    seperator:str=_os_path_sep
