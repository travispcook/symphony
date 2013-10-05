#!/bin/sh
#
# http://pastebin.com/wKLWgatq
#
# This script will download NodeJS, NPM and lessc, and bower, and install them into your Python
# virtualenv.
#
# Based on a post by Natim:
# http://stackoverflow.com/questions/8986709/how-to-install-lessc-and-nodejs-in-a-python-virtualenv

NODEJS="https://github.com/joyent/node.git"

# Check dependencies
for dep in gcc wget curl tar make git; do
        which $dep > /dev/null || (echo "ERROR: $dep not found"; exit 10)
done

# Must be run from virtual env
if [ "$VIRTUAL_ENV" = "" ]; then
        echo "ERROR: you must activate the virtualenv first!"
        exit 1
fi

echo "1) Installing nodejs in current virtual env"
echo

cd "$VIRTUAL_ENV"

# Create temp dir
if [ ! -d "src" ]; then
        mkdir src
fi
cd src || (echo "ERROR: entering src directory failed"; exit 4)

echo -n "- Entered temp dir: "
pwd

# Download
fname=`basename "$NODEJS" .git`
if [ -f "$fname" ]; then
        echo "- $fname already exists, not downloading"
else
        echo "- Downloading $NODEJS"
        git clone "$NODEJS" || (echo "ERROR: download failed"; exit 2)
fi

cd $fname || (echo "ERROR: entering source directory failed"; exit 4)

git checkout v0.10.20 || (echo "ERROR: checking out tag v0.10.20 failed."; exit 4)

echo "- Configure"
./configure --prefix="$VIRTUAL_ENV" || (echo "ERROR: configure failed"; exit 5)

echo "- Make"
make -j 4 || (echo "ERROR: build failed"; exit 6)

echo "- Install "
make install || (echo "ERROR: install failed"; exit 7)


echo
echo "2) Installing npm"
echo
curl https://npmjs.org/install.sh | sh || (echo "ERROR: install failed"; exit 7)

echo
echo "3) Installing bower"
echo
npm install bower -g || (echo "ERROR: bower install failed"; exit 8)

echo "Congratulations! Bower is now installed in your virtualenv"
