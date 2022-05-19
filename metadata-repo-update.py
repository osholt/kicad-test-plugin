import base64
import hashlib
import io
import json
import os
import requests
import logging
from datetime import datetime
import zipfile


READ_SIZE = 65536

VERSION = os.environ["VERSION"]
STATUS = os.environ["STATUS"]
KICAD_VERSION = os.environ["KICAD_VERSION"]
RELEASE_URL_BASE = os.environ["RELEASE_URL_BASE"]
RELEASE_ARCHIVE_NAME = os.environ["RELEASE_ARCHIVE_NAME"]
UNIQUE_IDENTIFIER = os.environ["UNIQUE_IDENTIFIER"]

RELEASE_URL = RELEASE_URL_BASE +  VERSION + "/" + RELEASE_ARCHIVE_NAME


def getsha256(filename: str) -> str:
    hash = hashlib.sha256()
    with io.open(filename, "rb") as f:
        data = f.read(READ_SIZE)
        while data:
            hash.update(data)
            data = f.read(READ_SIZE)
    return hash.hexdigest()

def load_json_file(file_name: str) -> dict:
    with io.open(file_name, encoding="utf-8") as f:
        return json.load(f)

def write_json_file(jd: dict, file_name: str) -> bool:
    with open(file_name, 'w') as fp:
        json.dump(jd, fp)

def get_file_base64(file_name: str) -> str:
    with io.open(file_name, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_package_stats(filename: str) -> tuple:
    instsize = 0
    z = zipfile.ZipFile(filename, "r")
    for entry in z.infolist():
        if not entry.is_dir():
            instsize += entry.file_size
    return getsha256(filename), os.path.getsize(filename), instsize

def update(jd: dict, file: str) -> bool:
    sha, size, instsize = get_package_stats(file)
    #if sha == jd["download_sha256"]:
    #    return False
    jd["version"] = VERSION
    jd["status"] = STATUS
    jd["kicad_version"] = KICAD_VERSION
    jd["download_sha256"] = sha
    jd["download_size"] = size
    jd["download_url"] = RELEASE_URL
    jd["install_size"] = instsize
    return True


metadata = load_json_file("metadata/packages/"+UNIQUE_IDENTIFIER+"/metadata.json")

numberOfVersions = len(metadata["versions"])
entryToUpdate = 0
#number of versions in json already
print(numberOfVersions)

#uncomment if extra entries are allowed
for x in metadata["versions"]:
    #print(x["version"])
    #print(VERSION)
    if x["version"] == VERSION:
        break
    else:
        entryToUpdate = entryToUpdate+1

#index to update
print(entryToUpdate) 

#print(metadata["versions"])
#add a new version entry if needed
if entryToUpdate >= numberOfVersions:
    metadata["versions"].append({"version":"test5"})

#print the new number of versions in the json
numberOfVersions = len(metadata["versions"])
print(numberOfVersions)

#update the json if needed
y = metadata["versions"][entryToUpdate]

update_metadata = update(y,RELEASE_ARCHIVE_NAME)

if update_metadata or (entryToUpdate >= numberOfVersions):
    write_json_file(metadata, "metadata/packages/"+UNIQUE_IDENTIFIER+"/metadata.json")
else:
    print("No change detected")
