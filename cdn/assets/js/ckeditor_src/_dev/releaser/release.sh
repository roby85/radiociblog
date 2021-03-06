#!/usr/bin/env bash

# Copyright (c) 2003-2012, CKSource - Frederico Knabben. All rights reserved.
# For licensing, see LICENSE.html or http://ckeditor.com/license

if [ -L $0 ] ; then
    DIR=$(dirname $(readlink -f $0)) ;
else
    DIR=$(dirname $0) ;
fi ;

LANGTOOL="$(cd $(dirname "$0"); pwd)/langtool.sh"

pushd $DIR
rm -rf release
rm -rf ../../../ckeditor
java -jar ckreleaser/ckreleaser.jar ckreleaser.release ../.. release "3.6.3 (SVN)" ckeditor_3.6.3_svn --run-before-release=$LANGTOOL
mv release/release ../../../ckeditor
rm -rf ../../../ckeditor/_source
popd
