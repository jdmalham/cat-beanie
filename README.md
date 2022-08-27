# cat-beanie

PyQt based IDE. VERY basic. Currently supports changing font type and size, saving and opening text based files, and running python files. Features file system navigation tree, wherein folders can be opened and saved. I have yet to add the ability to delete files from nav directory from inside IDE. Future updates to include syntax highlighting, multi-programming language support, compiler integration, and shell terminals.

Known bugs:
  Editor freezes when python file is being run. Editor cannot be accessed while script is running, and attempting to access it causes the entire thing to     freeze.

To Use:

Save .py file to desired location and create folder to be used as a directory. Copy this folder's path into the .py script under the self.dir_path        variable (line 12). This will host all symlink folders to be displayed in navigation tree.
