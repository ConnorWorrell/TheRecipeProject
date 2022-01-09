#!/bin/python
# Updates tags across repo

# Get a list of every recipe

import os
import re
import pathlib

AbsPath = str(pathlib.PurePosixPath(__file__).parent.parent.parent)

Recipes = os.listdir(AbsPath + "/Recipes") 

# For each recipe record extract the tags

RecipeDB = {}


def Recipe2Link(Recipe):
    return "[" + Recipe + "](/Recipes/" + Recipe + ".md)"

def Tag2Link(Tag):
    return "[" + Tag + "](/Tags/" + Tag + ".md)"

NotStrs = ["\n", ",", "[", "]"]
NotTags = ["Tags:","\n",""]

for Recipe in Recipes:
    RecipeName = Recipe.split(".md")[0]
    # Open file
    file = open(AbsPath + '/Recipes/' + Recipe,'r')
    Lines = file.readlines()
    RecipeTags = []
    RecipeFile = []
    for line in Lines:
        if "Tags:" in line:
            # Remove Links
            line = re.sub(r'\([^)]*\)','',line)

            for NotAStrs in NotStrs:
                while NotAStrs in line:
                    line = line.replace(NotAStrs,"")
            tags=line.split(" ")
            for NotATag in NotTags:
                if NotATag in tags:
                    tags.remove(NotATag)
            RecipeTags = RecipeTags + tags

            # Replace tags with links
            FileLine = "Tags: "
            for tag in RecipeTags:
                FileLine = FileLine + Tag2Link(tag) + " "
            RecipeFile.append(FileLine + "\n")
        else:
            RecipeFile.append(line)

    RecipeDB[RecipeName] = RecipeTags
    file.close()
    
    # Write updated recipe file
    file = open(AbsPath + '/Recipes/' + Recipe, 'w')
    file.writelines(RecipeFile)

#Invert the RecipeDB
TagDB = {}
for Recipe in RecipeDB.keys():
    tags = RecipeDB[Recipe]
    for tag in tags:
        if tag not in TagDB.keys():
            TagDB[tag] = [Recipe]
        else:
            TagDB[tag].append(Recipe)

##print(TagDB)
TagsSorted = [key for key in TagDB.keys()]
TagsSorted.sort()


# Write the files in Tags folder
for Tag in TagDB.keys():
    file = open(AbsPath + '/Tags/' + Tag + ".md", 'w')
    file.writelines(["# " + Tag + "\n\n"] + [str(number + 1) + ". " + Recipe2Link(recipe) + "\n" for number, recipe in enumerate(TagDB[Tag])])

# Find unused tag files
UnusedTagFiles = os.listdir(AbsPath + "/Tags")
for i in TagDB.keys():  
    if i + ".md" in UnusedTagFiles:
        UnusedTagFiles.remove(i + ".md")

##print("Unused TagFiles: " + str(UnusedTagFiles))
for File in UnusedTagFiles:
    os.remove(AbsPath + "/Tags/" + File)

# Copy read me file
readMe = open(AbsPath + "/ReadMe.md", "r")
readMeFile = []
for line in readMe.readlines():
    readMeFile.append(line)
readMe.close()

# Make changes
TagSectionStartIndex = -1
TagSectionEndIndex = 0
##print("\n\n\n")
for linenumber, line in enumerate(readMeFile):
    ##print(str(linenumber) + line.replace("\n",""))

    # Remove old tags section
    if TagSectionStartIndex != -1:
        if "#"  == line[0]:
            TagSectionEndIndex = linenumber
            break
    
    # Start of tags section
    if "# Tags" in line:
        # Tags seciton found
        ##print("Found tags at " + str(linenumber))
        TagSectionStartIndex = linenumber + 1

# if EOF occurs before next heading
if TagSectionEndIndex == 0:
    TagSectionEndIndex = len(readMeFile)
    

# Remove old tags
for i in range(TagSectionEndIndex - TagSectionStartIndex):
    readMeFile.pop(TagSectionStartIndex)

# Insert new tags
##print(readMeFile)
for number, tag in enumerate(TagsSorted):
    readMeFile.insert(TagSectionStartIndex + number, str(number + 1) + ". " + Tag2Link(tag) + "\n")
readMeFile.insert(TagSectionStartIndex,"\n")
readMeFile.insert(TagSectionStartIndex + number + 2, "\n")


# Push changes
readMe = open(AbsPath + "/ReadMe.md", "w")
for line in readMeFile:
    readMe.write(line)
readMe.close()
