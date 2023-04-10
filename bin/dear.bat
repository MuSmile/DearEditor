@echo off
set idedir=C:/DearEditor
set  pybin=python

rem show hello and help info
IF "%1" == "init" (
	rem echo "setting up python venv..."
	rem %pybin% -m venv py

	echo "installing dependencies..."
	set pip=%idedir%/py/Scripts/pip3
	set req=%idedir%/py/requirements.txt
	%pip% install -r %req%

	EXIT /b
)

set py=%idedir%/py/Scripts/python
%py% -u %idedir%/main.py %1 %2 %3 %4 %5 %6 %7 %8

IF /I %0 EQU "%~dpnx0" PAUSE