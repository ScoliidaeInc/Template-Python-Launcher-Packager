# Template Launcher and Packager for Python-based application
This is a launcher and packager pair that is designed for aiding in more rapid development and deployment of Python applications for multiple platforms.

The launcher consists of api files and logic for booting plug-ins from the user directory which will be auto generated if it does not yet exist.
This default path can be changed by moving the contents of the generated directory to a new path and place a text file in the default directory named ```redirect.config```.
The contents of the file must contain the following:
```
[Usr_Dir]
path= "/path/to/new/directory"
```
> NOTE: You are expected to replace ```/path/to/new/directory``` with your new directory path

---

To take advantage of the api as well as add functionality to build out the application, please insert your Python project within the user directory in a subdirectory named ```plugins```.
