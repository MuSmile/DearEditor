@echo off

call %~dp0..\..\..\py\Scripts\activate.bat

pushd %~dp0..\build
cmake --build . --target install --config Release -j6
popd

IF /I %0 EQU "%~dpnx0" PAUSE
