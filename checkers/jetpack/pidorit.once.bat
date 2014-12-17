@echo off

:PIDORIT
jetpack.checker.py %1 %2 %3 %4
echo %errorlevel%
GOTO PIDORIT