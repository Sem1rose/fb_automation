@echo off
echo Installing required tools...
pip install playwright
playwright install chromium
echo.
echo All tools are installed! You can now use run_bot.bat.
pause