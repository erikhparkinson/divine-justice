@echo off
setlocal enabledelayedexpansion
chcp 65001>nul
 
echo ⏱️  Initializing
 
set "last_was_origin=no"
set "origin=https://www.zilch.dev"
for %%x in (%*) do (
    if "%%~x"=="--origin" (
        set "last_was_origin=yes"
    ) else if "!last_was_origin!"=="yes" (
        set "origin=%%~x"
        goto :originDone
    )
)
:originDone
 
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set "arch=x64"
    goto :archDone
)

if "%PROCESSOR_ARCHITECTURE%"=="ARM64" (
    set "arch=arm64"
    goto :archDone
)

set "arch=x64"
for /f "tokens=1-3" %%i in ('systeminfo') do (
    if "%%i %%j"=="System Type:" (
        if "%%k"=="ARM-based" (
            set "arch=arm64"
        )
 
        goto :archDone
    )
)

:archDone

set "version_check_url=!origin!/zilch-connect/win-!arch!"
 
for /f "tokens=1-2" %%i in ('curl --silent --show-error --fail !version_check_url!') do (
    set /a "chunks_minus_1=%%i - 1"
    set "latest_version=%%j"
)
 
set "zilch_connect_dir=!homedrive!!homepath!\.zilch\zilch-connect"
set "zilch_connect=!zilch_connect_dir!\!latest_version!"
set "zilch_connect_exe=!zilch_connect!.exe"
 
if not exist !zilch_connect_exe! (
    echo 🌐 Updating
 
    if exist !zilch_connect_dir! (
        rmdir /s /q !zilch_connect_dir!
    )
 
    mkdir !zilch_connect_dir!
 
    set "download_url=!origin!/zilch-connect/!latest_version!"
 
    for /l %%i in (0,1,!chunks_minus_1!) do (
        curl --silent --show-error --fail "!download_url!.%%i" -o "!zilch_connect!.%%i"   
    )
 
    copy /b "!zilch_connect_dir!\*"; !zilch_connect_exe! >nul
 
    for /l %%i in (0,1,!chunks_minus_1!) do (
        del !zilch_connect!.%%i
    )
 
    echo ✅ Update complete
)
 
!zilch_connect_exe! %*
