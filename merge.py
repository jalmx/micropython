#!/bin/env python

import sys
import re
import os
from collections import deque
from bs4 import BeautifulSoup, Tag
from jsmin import jsmin
from csscompressor import compress

# html param
html = sys.argv[1]
# target param
target = sys.argv[2]
# path from html param
path = re.sub(r"[^\/]*$", "", html)
# open html file
soup = BeautifulSoup(open(html), "html.parser")
# find last script as anchorpoint
lastScript = soup.findAll("script", attrs={"src": True})[-1]
# get all scripts containing src attribute (= external scripts)
scripts = soup.findAll("script", attrs={"src": True})
# find last style link as anchorpoint
lastStylesheet = soup.findAll("link", attrs={"rel": "stylesheet"})[-1]
# get all links to css stylesheets
stylesheets = soup.findAll("link", attrs={"rel": "stylesheet"})

# create list of script srcs
print("\nRead Scripts:")
scriptsSrc = deque()
for script in scripts:
    scriptsSrc.append(path + script.attrs["src"])
    print("\t" + path + script.attrs["src"])

# create list of stylesheets srcs
print("\nRead Stylesheets:")
stylesheetsSrc = deque()
for stylesheet in stylesheets:
    stylesheetsSrc.append(path + stylesheet.attrs["href"])
    print("\t" + path + stylesheet.attrs["href"])

# merge scripts to temp.js
print("\nMerge Scripts:")
print("\t", end="")
with open("temp.js", "w") as outfileScript:
    for fname in scriptsSrc:
        # add space every script
        outfileScript.write("\n")
        print("~", end="")
        with open(fname) as infile:
            for line in infile:
                outfileScript.write(line)
print("\n")

# merge stylsheets to temp.css
print("Merge Stylesheets:")
print("\t", end="")
with open("temp.css", "w") as outfileCSS:
    for fname in stylesheetsSrc:
        # add space every script
        outfileCSS.write("\n")
        print("~", end="")
        with open(fname) as infile:
            for line in infile:
                outfileCSS.write(line)
print("\n")

# minify javascript
print("Minify temp.js\n\t~")
with open("temp.js") as js:
    minified_js = jsmin(js.read())

# minify css
print("Minify temp.css")
with open("temp.css") as css:
    minified_css = compress(css.read())

# replace scripts with merged and min embed script / css
print("Replacing and deleting")
tag = soup.new_tag("script")
tag["type"] = "text/javascript"
tag.append(minified_js)
lastScript.replace_with(tag)

tag = soup.new_tag("style")
tag["type"] = "text/css"
tag.append(minified_css)
lastStylesheet.replace_with(tag)

# remove script and style tags
for script in scripts:
    script.decompose()
for stylesheet in stylesheets:
    stylesheet.decompose()

# remove temp
os.remove("temp.js")
os.remove("temp.css")

# save html as target
file = open(target, "w")
file.write(str(soup))
file.close()

print("Done")

# python build.py ../source.html target.html
# source: https://stackoverflow.com/questions/28258579/modify-html-file-to-embed-all-external-scripts-and-css-into-script-and-style
