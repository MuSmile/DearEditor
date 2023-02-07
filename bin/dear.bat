@echo off
set curdir=%cd%
set idedir=C:/DearEditor/
set  pybin=python
rem set  pybin=C:/Python39/python

rem show hello and help info
IF "%1" == "" (
	%pybin% -u %idedir%main.py
	EXIT /b
)

rem install all required py pkgs
IF "%1" == "install" (
	pip install -r %idedir%requirements.txt
	EXIT /b
)

rem report prj summary
IF "%1" == "report" (
	cd %idedir%
	%pybin% -u report.py
	cd %curdir%
	EXIT /b
)

rem raise ide window
cd %idedir%
%pybin% -u main.py %1 %2 %3 %4 %5 %6 %7 %8
cd %curdir%

IF /I %0 EQU "%~dpnx0" PAUSE