"""
This file is setup to obfuscate variables from the namespace while running the package

---

Available Calls:

- SystemInfo "Handles information generated for use during the runtime process"
    - args "Arguments parsed to the application at runtime"
    - kwargs "Key-Word Arguments parsed to the application at runtime"
    - device "Minimal information about the device the application is running on for logging"
- Info(SystemInfo) "Stores basic information about the application"
    - name "Referencable name of the application"
    - version "Current version of the application"
"""
from sys import argv as _argv
from os import (
    mkdir as _mkdir,
    remove as _rmvdir
    )
from os.path import (
    sep as _os_path_sep,
    realpath as _real_path,
    exists as _path_exists,
    isdir as _path_isdir,
    isfile as _path_isfile,
    )
from platform import \
    machine as _machine, \
    system as _system, \
    release as _system_release, \
    version as _system_version, \
    platform as _platform

def _sort_argkwarg()-> dict:
    """Sorts through the parsed args and kwargs from runtime for preapproved inputs"""
    def validate_found_usr_dir(path:str)-> str:
        """
        Checks a given path to determine if path is a valid usr directory,
        or if path has been properly setup for a redirect to a new path
        """
        if not isinstance(path,str):
            raise TypeError("Invalid type for path, please ensure it is of data type string.")
        else:
            path=_os_path_sep.join(
                [
                    dir.strip().rstrip(".") \
                        for dir in path.strip().split(_os_path_sep)
                    ]
                )
            root_dir:str=__file__.split(__package__.replace(".",_os_path_sep),1)[0]
        if f"*PKG DIR*{_os_path_sep}" in path:
            _subpath:str= path.rsplit(f"*PKG DIR*{_os_path_sep}",1)[1]
            path=f"*ROOT DIR*{_os_path_sep}pkg{_os_path_sep}{_subpath}"
        if f"*ROOT DIR*{_os_path_sep}" in path:
            _subpath:str= path.rsplit(f"*ROOT DIR*{_os_path_sep}",1)[1]
            path=root_dir+ _subpath
        path:str=_real_path(path)
        if _path_exists(path) is False:
            try:
                _mkdir(path)
            except OSError as exc:
                default_path=root_dir+"usr"
                if path!= root_dir+"usr":
                    if _path_exists(default_path) is False:
                        try:# creating default path
                            _mkdir(default_path)
                        except OSError:# failed to create default path
                            raise OSError(exc) from exc
                        except MemoryError as err:# ran out of memory
                            raise MemoryError(err) from err
                        else:# no errors
                            path=default_path
                    path=default_path
            except MemoryError as exc:
                raise MemoryError(
                    "Ran out of memory while attempting to create the user directory..."
                    ) from exc

        redirect_config_path:str=f"{path}{_os_path_sep}redirect.config"
        if _path_exists(redirect_config_path) is True \
            and _path_isfile(redirect_config_path) is True:
            orus_contents:list=[]
            with open(redirect_config_path,"r",encoding="utf-8") as opened_redirected_user_settings:
                orus_contents+=[# read all contents split by line and append to outer list
                    line.strip() \
                        for line in opened_redirected_user_settings.readlines() \
                            if not line.startswith("//") \
                            and not line.strip()==""
                    ]
            if orus_contents[0]!="[Usr_Dir]" and len(orus_contents)==1:
                orus_contents.insert(0,"[Usr_Dir]")
            elif orus_contents[0]=="[Usr_Dir]":
                pass
            else:
                _rmvdir(redirect_config_path)
            if orus_contents[0] \
                and orus_contents[1].split("=",1)[0].strip()=="path" \
                and len(orus_contents)==2:
                new_path:str= orus_contents[1]\
                    .split("=",1)[1]\
                    .strip() \
                    .strip('"') \
                    .strip("'")
                if new_path.replace("'","").replace('"',"")=="":
                    _rmvdir(redirect_config_path)
                    path=root_dir+"usr"
                else:
                    path=new_path
        return path

    cwd:str=_argv[0]
    argumentative_kwargs= frozenset(_argv[1:])
    _args:list=[]
    _kwargs:dict={}
    #region Sift potential args and kwargs into seperate variables
    for arg_or_kwarg in argumentative_kwargs:
        arg_or_kwarg=arg_or_kwarg.strip()
        if "=" in arg_or_kwarg:
            kw,arg=arg_or_kwarg.split("=",1)
            kw=kw.strip()
            arg=arg.strip()
            _kwargs[kw]=arg
            continue
        match arg_or_kwarg:
            case ""|"-m":# empty string or package flag
                continue
            case _:# All remaining answers append as arg
                _args.append(arg_or_kwarg)
    #endregion Sift potential args and kwargs into seperate variables
    #region Check paired flags are not present in both searches
    for kwarg in _kwargs.copy():
        match kwarg.lower():
            case "--debug":
                if "-d" in _args:
                    _kwargs.pop(kwarg)
            case "--test-suite":
                if "-ts" in _args:
                    _kwargs.pop(kwarg)
    #endregion Check paired flags are not present in both searches
    #region ensure root directory and package directory are correctly added
    _kwargs["ROOT DIR"], _kwargs_pkg_dir= cwd.rsplit(_os_path_sep,2)[:-1]
    _kwargs["PKG DIR"]= f"*ROOT DIR*{_os_path_sep}{_kwargs_pkg_dir}"
    #endregion ensure root directory and package directory are correctly added
    _args=frozenset(_args)# Lock args as frozen set (order might not always be consistent)

    final_sort:dict={"args":_args,"kwargs":_kwargs}
    if final_sort["kwargs"].get("--USRDIR",None) is None:# ensure a default path exists to be used
        final_sort["kwargs"]["--USRDIR"]="*ROOT DIR*/usr"
    # ensure user directory is properly setup
    final_sort["kwargs"]["--USRDIR"]= validate_found_usr_dir(final_sort["kwargs"]["--USRDIR"])
    return final_sort
def _device_info_gather()-> dict:
    """Gathers information about the current device"""
    platform= "mobile" if "aarch" in _platform() else "computer"
    match _system().lower():
        case "linux":
            os="Linux"
        case "darwin":
            os="MacOs"
        case "windows":
            os="Windows"
        case _:
            os=f"Unrecognized ({_system()})"
    os_version,os_distro,cpu= _temp_call.split("-",2) \
        if (_temp_call:=f"{_system_release()}").lower()!="nt" \
        else _system_version()
    os_distro, cpu= os_distro.capitalize(), cpu.upper()
    del _temp_call

    cpu_architecture= _machine()
    device:dict={
        "platform":platform,
        "os":os,
        "os version":os_version,
        "os distro":os_distro,
        "processor":cpu,
        "architecture":cpu_architecture
    }
    return device
class SystemInfo:
    """
    Handles information generated for use during the runtime process

    ---

    Available Calls:
    - args "Arguments parsed to the application at runtime"
    - kwargs "Key-Word Arguments parsed to the application at runtime"
    - device "Minimal information about the device the application is running on for logging"
    """
    args,kwargs= _sort_argkwarg().values()
    device:dict= _device_info_gather()

class Info(SystemInfo):
    """
    Stores basic information about the application

    ---

    Available Calls:
    - name "Referencable name of the application"
    - version "Current version of the application"
    - args "Arguments parsed to the application at runtime"
    - kwargs "Key-Word Arguments parsed to the application at runtime"
    - device "Minimal information about the device the application is running on for logging"
    """
    name:str=__package__.strip().split(".",1)[0]
    version:str=f"DevKit.Sandbox.{name}.0.0.0.0.0.00000001"
