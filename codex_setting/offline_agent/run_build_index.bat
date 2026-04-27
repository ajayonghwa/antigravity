@echo off
setlocal enabledelayedexpansion

REM Usage:
REM   run_build_index.bat "D:\docs" "D:\index\docs_index.sqlite"
REM Defaults:
REM   docs_root = D:\docs
REM   out_db    = D:\index\docs_index.sqlite

set "DOCS_ROOT=%~1"
if "%DOCS_ROOT%"=="" set "DOCS_ROOT=D:\docs"

set "OUT_DB=%~2"
if "%OUT_DB%"=="" set "OUT_DB=D:\index\docs_index.sqlite"

echo [info] DOCS_ROOT=%DOCS_ROOT%
echo [info] OUT_DB=%OUT_DB%

REM If you're using a venv, activate it before running this script.
py -3.10 "%~dp0index\build_index.py" --docs-root "%DOCS_ROOT%" --out "%OUT_DB%" --reset
if errorlevel 1 (
  echo [err] build_index failed
  exit /b 1
)
echo [ok] index built: %OUT_DB%
exit /b 0

