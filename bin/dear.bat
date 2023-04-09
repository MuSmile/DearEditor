rem @echo off
set idedir=C:/DearEditor/
set  pybin=python3

rem install all required py pkgs
IF "%1" == "init" (
  	echo "setting up python venv..."
	pushd %idedir%
  	%pybin% -m venv py
    echo "installing dependencies..."
	py/bin/pip3 install -r py/requirements.txt
	popd

) else (
	set py=%idedir%/py/bin/python3
	%py% -u %idedir%/main.py %1 %2 %3 %4 %5 %6 %7 %8
）

IF /I %0 EQU "%~dpnx0" PAUSE