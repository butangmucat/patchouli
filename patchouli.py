#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# patchouli: a tool to update the EXIF information of scans from a film lab
# with data recorded using camera's logging function.
# Requires logged data to be transferred into a CSV file
# with the following fields:
# <DateTimeOriginal>,<ShutterSpeedValue>,<ApertureValue>,<FocalLength>,<MaxApertureValue>,<ISOSpeed>
#
# Known issues: the records in the CSV file must match the number and order of the image files supplied
#               otherwise undefined behaviors will occur
#
# Copyright (c) 2018, Sijie Bu
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from subprocess import call
import glob
import shutil
import sys

# name of the author
ARTIST = "Sijie Bu"
# vendor of the camera
MAKE = "Minolta"
# model of the camera
MODEL = "a-7"
# text encoding of the csv file
CSV_ENCODING = "utf-8"

# bail out if no enough arguments are provided
if len(sys.argv) < 3:
   print("Error: too few arguments")
   print("Usage: patchouli.py <path to csv file> <path to images>")
   exit(-1)

# bail out if ExifTool executable is not in PATH
cmdExists = lambda cmd: shutil.which(cmd) is not None
if cmdExists("exiftool") is False:
   print("Error: cannot find ExifTool executable")
   print("Please ensure you have ExifTool executable in PATH")
   exit(-2)

# extract information from given parameters
csvFileName = sys.argv[1]
imageFileNames = list()
# for you Windows guys, if the system does not expand wildcard then we have to do it ourselves
for i in sys.argv[2:]:
   imageFileNames += glob.glob(i)

# update the files one by one
with open(csvFileName, "r", encoding=CSV_ENCODING) as paramsDb:
   for i in imageFileNames:
      line = paramsDb.readline()
      params = line.split(",")
      call(["exiftool", "-overwrite_original", "-artist=" + ARTIST,
            "-Make=" + MAKE, "-Model=" + MODEL, "-DateTimeOriginal=" + params[0],
            "-ShutterSpeedValue=" + params[1], "-ApertureValue=" + params[2],
            "-FocalLength=" + params[3], "-FocalLengthIn35mmFormat="+ params[3],
            "-MaxApertureValue=" + params[4], "-ISO=" + params[5], "-ISOSpeed=" + params[5],
            i])