# Introduction
This is a project to create a motion-capture plugin for Blender using the OpenNI library and a Microsoft Kienct.

# Why?
There are a couple of other similar things out there.  I don't like them because either:
* They are not free software
* They are not maintained and won't compile with currently-available versions of other libraries

# Status
Currently there is a plugin for Blender that loads OpenNI and starts the skeleton tracker, but that's as far as
I've got.  The next step is to figure out a good way of mapping the OpenNI joints to the bones of an armature
and then the co-ordinate transform from the OpenNI co-ordinate system to the Belnder system.

# How to Build PyOpenNI
As of writing, the PyOpenNI repository on github only builds against Python 2.7.  Here's an outline of how to
build it for Python 3.2:
* Get the github version
* In the Python sources, fix all references to 'print' so that they are function-form (ie. parens around arguments)
* That includes compilerFlags.py
* In the C++ sources, change references to PyInt_Type to by PyLong_Type instead (or add an appropriate macro - typedefs don't work)
* Run CMake as per the instructions
* Edit CMakeCache.txt and change all references to python -> python3.2, python2.7 -> python3.2 and py27 -> py32
* Run make
* Copy lib/openni.so to /usr/lib/python3.2/lib-dynload
