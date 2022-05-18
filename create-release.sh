#!/bin/bash

#create temporary envirronemtnal variables for 

export VERSION = "0.0.4"
export STATUS = "stable"
export KICAD_VERSION = "6.0",
export RELEASE_URL_BASE = "https://github.com/osholt/kicad-test-plugin/releases/download/v"
export RELEASE_ARCHIVE_NAME = "Archive.zip"

prerelease = 1

#Create archive of 
cd plugins
zip -r ../Archive.zip . -x ".*" -x "__MACOSX"
cd ..
python metadata-update.py

git commit -a -m "Automated commit before release"
git push

if [[ $prerelease -eq 1 ]]
then
    gh release create v$VERSION "$RELEASE_ARCHIVE_NAME" -p
else
    gh release create v$VERSION "$RELEASE_ARCHIVE_NAME"
fi

