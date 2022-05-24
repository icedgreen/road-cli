# road-cli
### This program scrapes <a url="royalroad.com">royalroad.com</a> for fictions and displays them in <a url="https://github.com/marktext/marktext">marktext</a>.
You can select one or a range of chapters to read or download, and they will be combined into one mardown file. All fictions that are read with the program will have their last selected chapter saved, and can be continued if history mode is selected.

# Usage
```
python3 road-cli.py [-h] [-a] [-d] [-D DIRECTORY] [-s SEARCH] [-H]
  -h --help           show help message
  -a --all            specify all chapters
  -d --download       set download mode
  -D --directory      set download mode and download directory
  -s --search         specify search query
  -H --history        set history mode
```

# Dependencies
- python 3.10 or newer
- marktext (in PATH)
