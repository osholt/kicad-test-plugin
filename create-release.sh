#!/bin/bash

#create temporary envirronemtnal variables for 

VERSION = "0.0.4"
STATUS = "stable"
KICAD_VERSION = "6.0",
RELEASE_URL_BASE = "https://github.com/osholt/kicad-test-plugin/releases/download/v"
RELEASE_ARCHIVE_NAME = "Archive.zip"
prerelease = 1

echo $VERSION

export VERSION
export STATUS
export KICAD_VERSION
export RELEASE_URL_BASE
export RELEASE_ARCHIVE_NAME


#Create archive of 
cd plugins
zip -r ../Archive.zip . -x ".*" -x "__MACOSX"
cd ..
python metadata-update.py

git commit -a -m "Automated commit before release"
git push

echo $VERSION

if [[ $prerelease -eq 1 ]]
then
    gh release create "v$VERSION" $RELEASE_ARCHIVE_NAME -t "Release $VERSION" -n "This was auto-generated." -p 
else
    gh release create "v$VERSION" $RELEASE_ARCHIVE_NAME -t "Release $VERSION" -n "This was auto-generated."
fi

