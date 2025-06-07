@echo off
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo Execution du script de resolution d'IP...
python resolve_ips.py %*

echo.
echo Script termine. Appuyez sur une touche pour continuer...
pause >nul