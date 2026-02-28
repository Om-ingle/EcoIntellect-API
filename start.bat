@echo off
echo.
echo  ==========================================
echo   EcoIntellect API - Starting Servers...
echo  ==========================================
echo.

REM Start Backend in a new terminal window
echo [1/2] Starting FastAPI Backend on http://localhost:8000 ...
start "EcoIntellect Backend" cmd /k "cd /d "%~dp0backend" && pip install -r requirements.txt -q && uvicorn app.main:app --reload --port 8000"

REM Wait 3 seconds for backend to boot
timeout /t 3 /nobreak > nul

REM Start Frontend in a new terminal window
echo [2/2] Starting React Frontend on http://localhost:5173 ...
start "EcoIntellect Frontend" cmd /k "cd /d "%~dp0frontend" && npm install --silent && npm run dev"

echo.
echo  ==========================================
echo   Both servers starting in separate windows
echo.
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo   Frontend:  http://localhost:5173
echo   API Docs:  http://localhost:5173/api-documentation.html
echo  ==========================================
echo.
pause
