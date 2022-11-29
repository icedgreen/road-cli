# road-cli

**This program scrapes [royalroad.com](https://royalroad.com) for fictions and displays them in [marktext](https://github.com/marktext/marktext).**
You can select one or a range of chapters to read or download, and they will be combined into one mardown file. All fictions that are read with the program will have their last selected chapter saved, and can be continued if history mode is selected.

### Usage

In your terminal emulator (cmd or powershell on windows)

```
python3 road-cli.py [-h] [-a] [-d] [-D DIRECTORY] [-s SEARCH] [-H]
  -h --help           show help message
  -a --all            specify all chapters
  -d --download       set download mode
  -D --directory      set download mode and download directory
  -s --search         specify search query
  -H --history        set history mode
  -c --convert        convert to epub (requires pandoc)
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
