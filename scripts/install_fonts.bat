@echo off

REM You will may need to run the terminal as administrator to install fonts.

REM Change the path to brain-games folder "C:\Users\%USERNAME%\YourFolder\brain-games\fonts"
set "fontFolder=C:\Users\%USERNAME%\Downloads\brain-games\fonts"

for %%F in ("%fontFolder%\*.otf") do (
    echo Installing font: %%~nxF
    copy "%%F" "%windir%\Fonts" > nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo Font %%~nxF is already installed.
    ) else (
        if %ERRORLEVEL% equ 1 (
            echo Failed to install font %%~nxF.
        )
    )
)
