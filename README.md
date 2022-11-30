# road-cli

**This program scrapes [royalroad.com](https://royalroad.com) for fictions and displays them in [marktext](https://github.com/marktext/marktext).**
You can select one or a range of chapters to read or download, and they will be combined into one mardown file. All fictions that are read with the program will have their last selected chapter saved, and can be continued if history mode is selected.

### Usage

In your terminal emulator (cmd or powershell on windows)

```
> python3 road-cli.py -h
usage: road-cli.py [-h] [-a] [-d] [-D DIRECTORY] [-s SEARCH] [-S] [-H] [-c] [-i] [-l LINK] [-t] [-I]

options:
  -h, --help                            show this help message and exit
  -a, --all                             select all chapters
  -d, --download                        download chapter
  -D DIRECTORY, --directory DIRECTORY   download chapter to specified directory
  -s SEARCH, --search SEARCH            search for fiction
  -S, --split                           split range of chapters into seperate files
  -H, --history                         open history file
  -c, --convert                         convert to epub (requires pandoc)
  -i, --ignore                          ignores file (does not open in marktext)
  -l LINK, --link LINK                  link to next chapter at end of chapter (1 or 2 brackets)
  -t, --no-title                        do not include chapter titles
  -I, --index                           prefix chapter titles with index
```

### Setup

1. Download and install [marktext](https://github.com/marktext/marktext/releases)
2. Download road-cli.py from the releases
3. Add marktext to PATH (on windows, find the folder where MarkText.exe is stored and [add it to path](https://www.computerhope.com/issues/ch000549.htm))
4. Now you can run road-cli.py as described in [usage](#Usage)

### Dependencies

- python 3.10 or newer
- python requests module (should be default on linux; will try to install if it does not detect the module)
- marktext (in PATH)
- pandoc (optional)

**Note:** pandoc does not always convert every chapter to epub correctly and so can cause errors with rendering in certain applications. 
