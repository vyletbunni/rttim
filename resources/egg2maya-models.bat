@echo off
:a
set /p f="Enter File Name (not extension): "
C:\Panda3D-1.10.0-x64\bin\egg2maya2016 %f%.egg %f%.mb
echo Done.
echo -----
goto:a