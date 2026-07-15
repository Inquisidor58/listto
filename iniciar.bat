@echo off
cd /d "C:\Users\dichaves\Documents\ShoppingList"

echo ====================================
echo  ListTo App
echo ====================================
echo.

echo [1/3] Iniciando backend...
start "ListTo Backend" cmd /c "cd /d backend && .\venv\Scripts\uvicorn app.main:app --reload"

echo [2/3] Iniciando frontend...
start "ListTo Frontend" cmd /c "cd /d frontend && npx vite --host"

echo.
echo Abriendo la aplicacion...
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo  ListTo corriendo en:
echo    Local:  http://localhost:5173
echo    Red:    http://%COMPUTERNAME%:5173  (desde tu iPhone en misma WiFi)
echo.
echo Para cerrar, solo cierra las ventanas de terminal.
pause
