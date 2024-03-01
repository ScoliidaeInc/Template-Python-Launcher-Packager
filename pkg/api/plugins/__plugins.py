"""Used to obfuscate variables from the namespace"""

from types import NoneType
from os import walk as view_current_directory
from importlib import import_module
from pkg.api import path

_plug_in_path:str=path.join_plugins()
def _determine_boot_order(loader_path:str,entry_file:str,settings_extension:str)-> dict|NoneType:
    """
    Reads the boot.loader file for boot order and type

    ---

    If file is empty, or non-existent and plug-ins exist within directory,
    boot.loader will be created and/or populated with an autogenerated
    boot order
    """
    def _create_bootloader()-> NoneType:
        """
        Creates a boot.loader file in the plug-ins directory

        ---

        if expected_plugin_order is passed,
        the enumerated values will be what populates the document in the represented order
        """
        bootloader_path:str=path.normalize(_plug_in_path+"boot.loader")
        try:# File does NOT exist, create it
            with open(bootloader_path,"x",encoding="utf-8"):
                return
        except FileExistsError:# File already exists
            return
        except MemoryError as exc:# Not enough RAM
            raise MemoryError("Ran out of usable RAM") from exc
        except OSError as exc:# Unexpected error occured
            raise OSError("An unexpected system error has occured") from exc

    loader_path:str=path.validate(# ensure provided path is valid
        path.normalize(f"{loader_path}")# sterilize path input
        )["path"]
    plugin_entry_file:str= entry_file.strip().lower()
    plugin_settings_ext:str= f".{settings_extension.strip().lower()}"
    found_plugins:dict={}
    asynchronous_mode_enabled:bool=False
    bootloader_contents:list|NoneType=[]
    # select path and break it at the last seperator
    expected_bootloader_path,bootloader_file= loader_path.rsplit(path.seperator,1)
    tree_view:list=list(view_current_directory(expected_bootloader_path))

    if not bootloader_file in tree_view[0][-1]:# Ensure boot.loader exists
        _create_bootloader()
        bootloader_already_read=True
    # Verify all potential plugins and settings have been detected before reading file
    for potential_plugin in tree_view[1:]:
        plugin_path,subdirs,subfiles=potential_plugin
        del subdirs# subdirs is unused, was only created for unpacking the sibling variables
        current_plugin_root,current_plugin= plugin_path.rsplit(path.seperator,1)
        if current_plugin_root!=expected_bootloader_path:
            continue
        elif not current_plugin in tree_view[0][1]:# skip current plug-in if not in expected list
            continue
        elif plugin_entry_file not in subfiles:
            tree_view[0][1].remove(current_plugin)
            continue
        settings_found:list=[file for file in subfiles if file.endswith(plugin_settings_ext)]
        found_plugins[current_plugin]={# store information about the found plug-in
            "async":False,
            "entry":plugin_entry_file,
            "order":"DISABLED",
            "path":plugin_path,
            "settings":None if len(settings_found)==0 else settings_found[0],
        }

    # Read the boot order
    with open(loader_path,"r",encoding="utf-8") as opened_bootloader:
        bootloader_contents:list=[# sterilize each line
            line.strip() for line in opened_bootloader.readlines() if line.strip()!=""
            ]
    if not bootloader_contents:# generate contents if empty
        asynchronous_mode_enabled=False
        with open(loader_path,"w",encoding="utf-8") as opened_bootloader:
            bootloader_contents=[
                "[Boot Order]",
                "asynchronous_mode= False"
                ]
            opened_bootloader.writelines([f"{line}\n" for line in bootloader_contents+[""]])
            for order,key in enumerate(found_plugins):
                current_line:str=f"{order}= {key}".strip()
                bootloader_contents.append(current_line)
                opened_bootloader.write(current_line+"\n")
            del current_line

        print(bootloader_contents)
    if bootloader_contents[0]!="[Boot Order]":
        bootloader_contents.insert(0,"[Boot Order]")
    if bootloader_contents[1].split("=",1)[0].strip()!="asynchronous_mode":
        asynchronous_mode_enabled=False
        bootloader_contents.insert(1,"asynchronous_mode= False")
    match bootloader_contents[1].split("=",1)[1].strip().lower():
        case "false":
            asynchronous_mode_enabled=False
        case "true":
            asynchronous_mode_enabled=True
        case _:
            asynchronous_mode_enabled=False
            bootloader_contents[1]= "asynchronous_mode= False"
    for line in bootloader_contents[2:]:
        key,value= line.split("=",1)
        value= value.strip()
        # ensure value is a valid target
        if not value in found_plugins:
            continue
        # ensure order is a valid entry
        try:# try to convert to integer
            key=int(key.strip(),base=10)
        except ValueError:# default to "DISABLED"
            key="DISABLED"
        finally:# update async & order for target value
            found_plugins[value]["async"]=asynchronous_mode_enabled
            found_plugins[value]["order"]=key

    with open(loader_path,"w",encoding="utf-8") as opened_bootloader:
        #region sort plug-ins order in file
        new_contents=[
            "[Boot Order]",
            f"asynchronous_mode= {asynchronous_mode_enabled}",
            ""
            ]
        plug_ord:list=[]
        confirmed_plugins:dict=found_plugins
        for plug in confirmed_plugins:
            current_target=ordr \
                if (ordr:=f"{found_plugins[plug]['order']}").lower().strip()!="disabled" \
                else -1
            plug_ord.append(f"{current_target}= {plug}")
        plug_ord.sort(key=lambda x: (int(x.split("=",1)[0]), x))
        #endregion sort plug-ins order in file
        opened_bootloader.writelines([f"{line}\n" for line in new_contents+plug_ord])
    return confirmed_plugins

class Plugins:
    """
    Controls the loading of all the plug-ins listed by the boot.loader

    ---

    Available Calls:
    - path "Current expected directory to find launcher plug-ins"
    - boot_loader "Current expected directory to find launcher "boot.loader""
    - entry_file "Name of expected file to initiate the plug-in"
    - boot_order "Reads the plug-in directory and "boot.loader" to confirm load order"
    """
    path:str=_plug_in_path
    boot_loader:str=path+"boot.loader"
    entry_file:str="load.plug_in"
    settings_extension:str="plug_in.settings"
    boot_order:dict|NoneType=_determine_boot_order(boot_loader,entry_file,settings_extension)
