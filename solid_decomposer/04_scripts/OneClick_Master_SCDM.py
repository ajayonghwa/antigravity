# -*- coding: utf-8 -*-
import os
import sys
import clr
import System
from System.Diagnostics import Process, ProcessStartInfo

# [v4.55] 외부 파이썬의 출력을 실시간으로 가져와서 표시하는 기능 추가
PROJECT_ROOT = r"D:\yhheo\py_programs_by_yh\solid_decomposer" 
PYTHON_EXE = r"python" 

EXTRACTOR_PATH = os.path.join(PROJECT_ROOT, "01_extractor", "scdm_extractor.py")
MAIN_RUN_PATH = os.path.join(PROJECT_ROOT, "main_run.py")
GENERATED_SCRIPT_PATH = os.path.join(PROJECT_ROOT, "04_scripts", "scdm_decomposition_script.py")
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "geometry_data.json")

def run_master_pipeline():
    print("=" * 50)
    print("🚀 AntiGravity One-Click Pipeline (v4.55)")
    print("=" * 50)

    # 1단계: 형상 데이터 추출
    print("\n[Step 1] Extracting Geometry Data...")
    try:
        global_vars = globals().copy()
        global_vars['OUTPUT_PATH'] = DATA_PATH
        with open(EXTRACTOR_PATH, 'r') as f:
            exec(f.read(), global_vars)
        print(" -> Extraction Completed.")
    except Exception as e:
        print(" -> Extraction Failed: " + str(e))
        return

    # 2단계: 외부 파이썬(CPython) 플래너 호출
    print("\n[Step 2] Calling External AI Planner...")
    try:
        start_info = ProcessStartInfo()
        start_info.FileName = PYTHON_EXE
        start_info.Arguments = '"{0}" DEVICE geometry_data.json'.format(MAIN_RUN_PATH)
        start_info.WorkingDirectory = PROJECT_ROOT
        
        # [v4.55] 출력 리다이렉션 설정
        start_info.UseShellExecute = False
        start_info.RedirectStandardOutput = True
        start_info.RedirectStandardError = True
        start_info.CreateNoWindow = True
        
        process = Process.Start(start_info)
        
        # 실시간 출력 읽기
        output = process.StandardOutput.ReadToEnd()
        error = process.StandardError.ReadToEnd()
        
        process.WaitForExit()
        
        if output: print(output)
        if error: 
            print("-" * 30)
            print("Python Error Output:")
            print(error)
            print("-" * 30)
        
        if process.ExitCode == 0:
            print(" -> Planning Completed Successfully.")
        else:
            print(" -> External Planner failed with Exit Code: " + str(process.ExitCode))
            return
    except Exception as e:
        print(" -> Error calling external Python: " + str(e))
        return

    # 3단계: 생성된 분할 스크립트 실행
    print("\n[Step 3] Executing Decomposition...")
    if not os.path.exists(GENERATED_SCRIPT_PATH):
        print("Error: Generated script not found.")
        return
    try:
        with open(GENERATED_SCRIPT_PATH, 'r') as f:
            exec(f.read(), globals())
        print(" -> Decomposition Execution Completed Successfully!")
    except Exception as e:
        print(" -> Execution Failed: " + str(e))

    print("\n" + "=" * 50)
    print("🏁 All Tasks Finished!")
    print("=" * 50)

run_master_pipeline()
