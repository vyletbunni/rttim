@echo off
:a
set /p f="Enter File Name (not extension): "
C:\Panda3D-1.10.0-x64\bin\bam2egg %f%.bam %f%.egg
echo Done.
echo -----
goto:a