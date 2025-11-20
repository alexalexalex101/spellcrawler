@echo off
cd /d "%~dp0"
echo.
echo === Starting SpellCrawler ===

REM --- Start allow server if not already running ---
echo Checking if allow_server is running...

tasklist /FI "WINDOWTITLE eq Allow Server" /FI "STATUS eq RUNNING" | find /I "cmd.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Starting allow_server.py...
    start "Allow Server" cmd /k "python allow_server.py"
) else (
    echo allow_server.py already running.
)

echo.
echo === Building Docker image ===
docker build --no-cache -t spellcrawler .

echo.
echo === Running crawler ===
docker run ^
  -v "%cd%\output:/app/output" ^
  -v "%cd%\custom_words.txt:/app/custom_words.txt" ^
  -v "%cd%\templates:/app/templates" ^
  spellcrawler

echo.
echo === Opening updated spell report ===
start "" "%cd%\output\spell_report.html"

echo.
echo === DONE ===
pause
