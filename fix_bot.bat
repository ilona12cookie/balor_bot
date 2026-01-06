@echo off
cd /d "C:\Users\User\balor_bot"
call venv\Scripts\activate.bat
pip uninstall python-telegram-bot -y
pip install python-telegram-bot==20.7
python main.py
pause