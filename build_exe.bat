@echo off
echo ============================================
echo   AniGap - EXE Builder
echo ============================================
echo.

REM Install required packages
echo [1/2] Installing dependencies...
py -m pip install pyinstaller customtkinter requests pyperclip pillow --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies. Make sure Python is installed.
    pause
    exit /b 1
)

REM Get customtkinter path
echo [2/2] Building EXE (this may take a minute)...
for /f "delims=" %%i in ('py -c "import customtkinter; print(customtkinter.__path__[0])"') do set CTK_PATH=%%i

py -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "AniGap v7" ^
    --icon "icon.ico" ^
    --add-data "icon.ico;." ^
    --add-data "%CTK_PATH%;customtkinter/" ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=pyperclip ^
    anigap.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   SUCCESS! Your EXE is in the dist\ folder
echo   dist\AniGap v7.exe
echo ============================================
pause
