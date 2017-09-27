@echo off
title RTTIM Client
set TTS_GAMESERVER=127.0.0.1
set TTS_PLAYCOOKIE=kooldood

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:

title RTTIM Client (%TTS_PLAYCOOKIE%)

set is_ai=0
set is_ud=0

rem Export the environment variables:
set TTI_PLAYCOOKIE=%TTS_PLAYCOOKIE%

echo ===============================
echo Starting Toontown...
echo ppython: %PPYTHON_PATH%
echo Username: %TTS_PLAYCOOKIE%
echo Gameserver: %TTS_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m Start
pause
