import os
import csv
import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path")
args = parser.parse_args()

if args.path is None:
    file_path = input("csv file path: ")
else:
    file_path = args.path

mydict = dict()
if not os.path.exists(file_path):
    print("create {}".format(file_path))
    f = open(file_path, "w")
    f.close()
else:
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            mydict[row[0]] = row[1]
    pprint.pprint(mydict)
    while(True):
        inputs = input("Are you sure you want to overwrite {} ([y]/n)? ".format(file_path))
        if inputs == "y":
            break
        elif inputs == "n":
            exit()

while(True):
    inputs = input("Continue ([y]/n)? ")
    if inputs == "n":
        break
    elif inputs != "y":
        continue

    word = input("word: ")
    hint = input("hint: ")

    if word in mydict:
        mydict[word] += ", " + hint
    else:
        mydict[word] = hint
    
with open(file_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "hint"])
    for k, v in mydict.items():
        writer.writerow([k, v])

print("goodbye...")