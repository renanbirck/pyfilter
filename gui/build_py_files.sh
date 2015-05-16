#!/usr/bin/env bash

for file in *.ui;
do pyuic4 $file > ${file/\.ui/\.py};
done
