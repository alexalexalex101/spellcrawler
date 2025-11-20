@echo off
echo.
echo === Starting SpellCrawler ===

REM --- Step 1: Start allow server if not already running ---
echo Checking if allow_server is running...

tasklist /FI "WINDOWTITLE eq Allow Server" /FI "STATUS eq RUNNING" | find /I "cmd.exe" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Starting allow_server.py...
    start "Allow Server" cmd /k "python allow_server.py"
) else (
    echo allow_server.py already running.
)

REM --- Step 2: Build Docker Image (FORCE REBUILD) ---
echo.
echo === Building Docker image ===
cd spellcrawler
docker build --no-cache -t spellcrawler .

REM --- Step 3: Run Container With Correct Volume Mounts ---
echo.
echo === Running crawler ===

docker run ^
  -v "%cd%\..\output:/app/output" ^
  -v "%cd%\..\custom_words.txt:/app/custom_words.txt" ^
  -v "%cd%\..\templates:/app/templates" ^
  spellcrawler

REM --- Step 4: Open Updated Report ---
echo.
echo === Opening updated spell report ===
start "" "%cd%\..\output\spell_report.html"

echo.
echo === DONE ===
pause