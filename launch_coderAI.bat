@echo off
echo Starting CoderAI with Helpmate-AI integration...
cd /d "%~dp0"
call .venv\Scripts\activate
python launch.py
pause
