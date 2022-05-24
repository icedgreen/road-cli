# /bin/python3 road-cli

# create history file if does not exist
from os.path import expanduser

history_dir = expanduser("~") + "/.road-cli_history"
history_file = open(history_dir, "a")
history_file.close()

# parse command line arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all", help="select all chapters", action="store_true")
parser.add_argument("-d", "--download", help="download chapter", action="store_true")
parser.add_argument("-D", "--directory", help="download chapter to specified directory")
parser.add_argument("-s", "--search", help="search for fiction")
parser.add_argument("-H", "--history", help="open history file", action="store_true")
args = parser.parse_args()

is_download = args.download
download_dir = args.directory
if download_dir != None:
    is_download = True
spec_all = args.all
query = args.search
is_history = args.history

# do history file stuff
import re

base_url = "https://royalroad.com"

class Fiction:
    def __init__(self, title, href, chapters, h_name=None, h_index=None):
        self.title = title
        self.href = href
        self.chapters = chapters
        self.history_name = h_name
        self.history_index = h_index

fictions = []

if is_history:
    history_file = open(history_dir, "r")

    while line := history_file.readline():
        title, href, h_name, h_index = line.split("§§§") # NOTE seperator
        h_index = re.sub("\\n", "", h_index)
        fictions.append(Fiction(title, href, None, h_name, h_index))

    history_file.close()

# search and get fictions list from response else update history chapter information
import requests

if is_history:
    print("\nHistory:")
    for i in range(len(fictions)):
        resp = requests.get(base_url + fictions[i].href)
        fictions[i].chapters = re.findall(r'<div class="actions"><span class="label label-default pull-right">(.*?) Chapters</span></div>', resp.text)[0]
else:
    while len(fictions) == 0:
        if query == None:
            print("Enter search query (leave empty to quit):", end = "")
            query = input(" ")
            if query == "":
                exit()

        resp = requests.get(base_url + "/fictions/search?title=" + query.replace(" ", "+"))

        if resp.status_code in range(200, 299):
            hrefs = re.findall(r'<a href="(.*?)" class="font-red-sunglo bold">', resp.text)
            chapters = re.findall(r'>(.*?) Chapters</span>', resp.text)
            titles = []
            for href in hrefs:
                titles.append((href.rsplit('/',1)[-1]).replace("-", " "))

            for i in range(len(titles)):
                fictions.append(Fiction(titles[i], hrefs[i], chapters[i]))

            if len(fictions) == 0:
                print("No novels found for search query '" + query + "'")
                query = None
        else:
            print("ERROR: Website returned status code", resp.status_code)
            exit()

# select fiction from list (search or history)
selection = Fiction

for i in range(len(fictions)):
    print("[" + str(i) + "] " + fictions[i].title + " (" + fictions[i].chapters + " Chapters)")
    if is_history:
        print("    ", fictions[i].history_name)

while True:
    selected_index = input("Enter selection (leave empty to quit): ")

    if selected_index == "":
        exit()
    elif not (0 <= int(selected_index) < len(fictions)):
        print("ERROR: Selection out of range 0 -", len(fictions) - 1)
    else:
        selection = fictions[int(selected_index)]
        break

# scrape fiction page for chapters
class Chapter:
    def __init__(self, title, date, url):
        self.title = title
        self.date = date
        self.url = url

chapters = []

resp = requests.get(base_url + selection.href)

if resp.status_code in range(200, 299):
    chapter_list = [line for line in resp.text.split('\n') if "window.chapters" in line][0]

    chapter_titles = re.findall(r'"title":"(.*?)"', chapter_list)
    for i in range(len(chapter_titles)):
        chapter_titles[i] = re.sub(r'\\u0027|\\u2018|\\u2019', "'", chapter_titles[i])
        chapter_titles[i] = re.sub(r'\\u0026', "&", chapter_titles[i])
        chapter_titles[i] = re.sub(r'\\u200B', "", chapter_titles[i])
    chapter_dates = re.findall(r'"date":"(.*?)"', chapter_list) # NOTE maybe fix date display?
    chapter_urls = re.findall(r'"url":"(.*?)"', chapter_list)

    for i in range(len(chapter_titles)):
        chapters.append(Chapter(chapter_titles[i], chapter_dates[i], chapter_urls[i]))
else:
    print("ERROR: Website returned stauts code", resp.status_code)
    exit()

# loop with chapter list
import subprocess

if len(chapters) == 0:
    print("ERROR: Fiction has no chapters")
    exit()

chapter_selection_start = selection.history_index
chapter_selection_end = -1
chapter_input = ""
is_output = True

while True:
    print("\n" + selection.title)
    if chapter_selection_start != None:
        print(chapters[int(chapter_selection_start)].title, "\n")

    if is_output:
        print("\nChapter commands")
        print("f - goto first chapter")
        print("l - goto last chapter")
        print("n - goto next chapter")
        print("p - goto previous chapter")
        print("s - search for specific chapter")
        print("r - search for range of chapters")
        print("a - select all chapters")
        print("d - delete fiction from history")

        is_output = True

    if is_history:
        is_history = False
    else:
        while True:
            chapter_input = input("Enter selection (leave empty to quit): ")
            if len(chapter_input) == 1 and chapter_input in "flnpsrad":
                break
            elif chapter_input == "":
                exit()
            else:
                print("ERROR: Invalid input '" + chapter_input + "'")

    num_select = 1
    match(chapter_input):
        case "f":
            chapter_selection_start = 0
        case "l":
            chapter_selection_start = len(chapters) - 1
        case "n":
            if 0 <= int(chapter_selection_start) + 1 < len(chapters):
                chapter_selection_start += 1
            else:
                print("ERROR: The currently selected chapter is the latest/last chapter")
                is_output = False
        case "p":
            if 0 <= int(chapter_selection_start) - 1 < len(chapters):
                chapter_selection_start -= 1
            else:
                print("ERROR: The currently selected chapter is the first one")
                is_output = False
        case "s" | "r":
            if chapter_input == "r":
                num_select += 1

            start_chapter = Chapter
            end_chapter = Chapter

            while num_select:
                chapter_search = input("Enter chapter search query (leave empty to quit): ")
                search_results = []

                if chapter_search == "":
                    exit()
                else:
                    for i in range(len(chapters)):
                        if chapter_search in chapters[i].title:
                            search_results.append(chapters[i])

                for i in range(len(search_results)):
                    print("[" + str(i) + "] " + search_results[i].title + " (Released " + search_results[i].date + ")")

                if len(search_results) == 0:
                    print("ERROR: No results found for query '" + chapter_search + "'")
                else:
                    chapter_selection = input("Enter chapter to select (leave empty to quit): ")

                    if chapter_selection == "":
                        exit()
                    elif not (0 <= int(chapter_selection) < len(search_results)):
                        print("ERROR: Selection is out of range")
                    else:
                        if num_select == 2:
                            start_chapter = search_results[int(chapter_selection)]
                            num_select -= 1
                        else:
                            if chapter_input == "r":
                                end_chapter = search_results[int(chapter_selection)]
                            else:
                                start_chapter = search_results[int(chapter_selection)]

                            num_select -= 1

            for i in range(len(chapters)):
                if chapters[i] == start_chapter:
                    chapter_selection_start = i
                if chapters[i] == end_chapter:
                    chapter_selection_end = i
        case "a":
            chapter_selection_start = 0
            chapter_selection_end = len(chapters) - 1
        case "d":
            delete_selection = input("Are you sure you want to delete this fiction from history? (y/n): ")

            if delete_selection == "y":
                history_file = open(history_dir, "r")

                history_file_contents = []

                while line := history_file.readline():
                    history_title = line.split("§§§")[0] # NOTE seperator

                    if history_title != selection.title:
                       history_file_contents.append(line)

                history_file.close()

                history_file = open(history_dir, "w")
                history_file.writelines(history_file_contents)
                history_file.close()

                print("Fiction has been deleted. Exiting...")

            elif delete_selection == "n":
                print("Fiction has not been deleted. Exiting...")

            else:
                print("Invalid choice. Exiting...")

            exit()

   # get chapter from url and open or download
    chapter = chapter_selection_start

    temp_dir = selection.title + ".md"
    if is_download:
        if download_dir != None:
            temp_dir = download_dir + "/" + temp_dir
        else:
            temp_dir = "./" + temp_dir
    else:
        temp_dir = expanduser("/tmp/") + selection.title + ".md"

    while True:
        resp = requests.get(base_url + chapters[int(chapter)].url)

        chapter_inner = re.search(r'<div class="chapter-inner chapter-content">(.*?)</div>\n                <h6', resp.text, re.MULTILINE | re.DOTALL).group()
        chapter_content = ''.join(chapter_inner)
        chapter_content = re.sub('> +<', '><', chapter_content)
        chapter_content = re.sub(' +<', '<', chapter_content)

        temp_file = open(temp_dir, "a")
        temp_file.write("# " + chapters[int(chapter)].title + "\n")
        temp_file.write(chapter_content)
        temp_file.write("\n\n---\n\n")
        temp_file.close()

        if chapter == chapter_selection_end or chapter_selection_end == -1:
            subprocess.call(["marktext", temp_dir])
            if not is_download:
                subprocess.call(["rm", temp_dir])
            break

        chapter += 1

    chapter_selection_start = chapter
    chapter_selection_end = -1

    # add fiction w/ chapter to history file
    history_file = open(history_dir, "r")
    history_file_contents = []
    contains_title = False

    while line := history_file.readline():
        history_title = line.split("§§§")[0] # NOTE seperator

        if history_title == selection.title:
            contains_title = True
            history_file_contents.append(selection.title + "§§§" + selection.href + "§§§" + chapters[int(chapter)].title + "§§§" + str(chapter) + "\n")
        else:
            history_file_contents.append(line)

    history_file.close()

    if not contains_title:
        history_file = open(history_dir, "a")
        history_file.write(selection.title + "§§§" + selection.href + "§§§" + chapters[chapter].title + "§§§" + str(chapter) + "\n")
        history_file.close()
    else:
        history_file = open(history_dir, "w")
        history_file.writelines(history_file_contents)
        history_file.close()
