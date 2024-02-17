# Things to note about launching the package

The package uses python as the core code language used

Python interpreter must be passed either ```-O``` or ```-OO```
> ```-O``` : Disables assertions from the runtime
>
> ```-OO``` : Disables assertions & docstrings from the runtime
>
> **NOTE:** These flags aid in the speed of the runtime as the used flag nulls the information before compiled to memory.
>
> Using either of these flags also disabled internal debug dunder variable. This is done as to not confuse the debug setting being parsed as they are not related in usage

The package must be initialized with the -m command from the root directory of the project to initialize package as a "module"

> The root directory of the project is the parent directory containing the package directory
>
> The package directory is the directory containing the core files for the application to work

The package must also be parse the following arguments:

- --MODE="Console"|"Hybrid"|"GUI"
- --USERDIR="\*ROOT DIR\*/usr"
- --LOG-OUTPUT="\*USR DIR\*/logs"
- --LOG-LEVEL="\*DEFAULT\*"

These flags dictate the following to the application:

- What mode of features to enable for use (i.e. command line interface(CLI) or graphical user interface (GUI))
- Where to find the default path to the user directory
  - Can potentially contain a redirect.config to point to a new location from the default location. This new location is expected to be the correct path and will ignore further redirect.config files
- Where to store the log files (default is within the user directory)
- Define the minimum level of concern for the logging output

## Enable debug mode

The following must be met:

- Debug flag passed to the package at runtime
- Mode must be in hybrid (console & gui)
- Log level must be set for debug
