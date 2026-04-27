@echo off
setlocal enabledelayedexpansion

REM Usage:
REM   run_search.bat "D:\index\docs_index.sqlite" "PRXY poisson"
REM Defaults:
REM   db = D:\index\docs_index.sqlite

set "DB=%~1"
if "%DB%"=="" set "DB=D:\index\docs_index.sqlite"

set "Q=%~2"
if "%Q%"=="" (
  echo [err] provide query string as 2nd argument
  echo example: run_search.bat "D:\index\docs_index.sqlite" "PRXY poisson"
  exit /b 2
)

py -3.10 "%~dp0index\search.py" --db "%DB%" --q "%Q%"
exit /b %errorlevel%

