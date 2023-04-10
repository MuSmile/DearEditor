@echo off

IF exist %~dp0 (rmdir /s/q %~dp0..\build)
mkdir %~dp0..\build

IF /I %0 EQU "%~dpnx0" PAUSE
