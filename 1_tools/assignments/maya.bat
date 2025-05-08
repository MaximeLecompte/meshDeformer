:: comment

:: echo = print
:: echo "This is Text"
:: @echo off


:: close command prompt
:: exit

:: set variable
set "MAYA_VERSION=2023"

:: PATH
set "SCRIPT_PATH=C:\Users\Maxime\Documents\Mlecompte\"
set "PYTHONPATH=%SCRIPT_PATH%;%PYTHONPATH%"


:: set variable + other varianble
set "MAYA_PATH=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"

:: add to variable
set "MAYA_PLUG_IN_PATH=C:\Program Files\Autodesk\Maya2023\plugins;%MAYA_PLUG_IN_PATH%"

:: start
start "" "C:\Program Files\Autodesk\Maya%MAYA_VERSION%\bin\maya.exe"