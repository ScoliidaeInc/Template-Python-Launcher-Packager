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
from os.path import sep as _os_path_sep
from platform import \
    machine as _machine, \
    system as _system, \
    release as _system_release, \
    version as _system_version, \
    platform as _platform

def _sort_argkwarg()-> dict:
    """Sorts through the parsed args and kwargs from runtime for preapproved inputs"""
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
    _kwargs["ROOT DIR"], _kwargs["PKG DIR"]= cwd.rsplit(_os_path_sep,2)[:-1]
    _kwargs["PKG DIR"]= f"*ROOT DIR*{_os_path_sep}{_kwargs['PKG DIR']}"
    #endregion ensure root directory and package directory are correctly added
    _args=frozenset(_args)# Lock args as frozen set (order might not always be consistent)
    return {"args":_args,"kwargs":_kwargs}
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
