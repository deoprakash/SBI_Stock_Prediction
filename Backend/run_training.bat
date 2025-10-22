@echo off
REM Daily Model Training Script for Windows
REM This batch file activates the virtual environment and runs training

cd /d "%~dp0"
call myenv\Scripts\activate.bat
python train_model.py

if %ERRORLEVEL% EQU 0 (
    echo Training completed successfully at %date% %time%
) else (
    echo Training failed at %date% %time%
)

pause
