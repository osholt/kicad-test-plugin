#!/bin/bash

#create temporary envirronemtnal variables for 

export VERSION="0.0.2"
export STATUS="stable"
export KICAD_VERSION="6.0",
export RELEASE_URL_BASE="https://github.com/osholt/kicad-test-plugin/releases/download/v"
export RELEASE_ARCHIVE_NAME="Archive.zip"
export UNIQUE_IDENTIFIER="com.github.osholt.test"
prerelease=1



#Create archive of 
cd plugins
zip -r ../Archive.zip . -x ".*" -x "__MACOSX" > /dev/null
cd ..
python3 metadata-update.py

git commit -a -m "Automated commit before release" --quiet
git push --quiet

#echo $VERSION

if [[ $prerelease -eq 1 ]]
then
    gh release create "v$VERSION" $RELEASE_ARCHIVE_NAME -t "Release $VERSION" -n "This was auto-generated." -p 
else
    gh release create "v$VERSION" $RELEASE_ARCHIVE_NAME -t "Release $VERSION" -n "This was auto-generated."
fi

#pull metadata repo and update that

git clone https://github.com/osholt/kicad-plugin-repo-metadata metadata --quiet
python3 metadata-repo-update.py
cd metadata
git commit -a -m "Automated update" --quiet
git push --quiet
cd ..
rm -rvf metadata > /dev/null

#update main repo
git clone https://github.com/osholt/kicad-plugin-repo plugin_repo --quiet
cd plugin_repo
./ci/build.sh
rm -rv plugin_repo
