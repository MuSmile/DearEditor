@echo off

call %~dp0..\..\..\py\Scripts\activate.bat

pushd %~dp0..\build
cmake -DCMAKE_BUILD_TYPE=Release .. -DADS_VERSION=4.0.2
popd

IF /I %0 EQU "%~dpnx0" PAUSE
