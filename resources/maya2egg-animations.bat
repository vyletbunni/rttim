@echo off
:a
set /p f="Enter MB name (not extension): "
set /p e="Enter EGG name (not extension): "
C:\Panda3D-1.10.0-x64\bin\maya2egg2016 -a model -o %e%.egg %f%.mb
echo Done with egg.
echo -----
goto:a