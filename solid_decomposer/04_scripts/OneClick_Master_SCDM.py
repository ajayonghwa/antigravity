# -*- coding: utf-8 -*-
# ==============================================================================
# AntiGravity Solid Decomposer - One-Click Master Script (for SpaceClaim)
# 
# 이 스크립트를 스페이스클레임에서 실행하면 다음 작업이 자동으로 순차 진행됩니다:
# 1. 형상 데이터 추출 (Extractor)
# 2. 외부 Python 플래너 호출 (Planner & Generator)
# 3. 분할 스크립트 즉시 실행 (Execution)
# ==============================================================================
import os
import sys
import clr
import System
from System.Diagnostics import Process, ProcessStartInfo

# ------------------------------------------------------------------------------
# [사용자 설정] 경로 설정 (윈도우 환경에 맞춤)
# ------------------------------------------------------------------------------
PROJECT_ROOT = r"D:\yhheo\py_programs_by_yh\solid_decomposer" 

# 외부 CPython 실행 파일 경로
PYTHON_EXE = r"python" # 가상환경 사용 시 해당 경로로 변경 권장

# ------------------------------------------------------------------------------
# 내부 경로 자동 설정
EXTRACTOR_PATH = os.path.join(PROJECT_ROOT, "01_extractor", "scdm_extractor.py")
MAIN_RUN_PATH = os.path.join(PROJECT_ROOT, "main_run.py")
GENERATED_SCRIPT_PATH = os.path.join(PROJECT_ROOT, "04_scripts", "scdm_decomposition_script.py")
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "geometry_data.json")

def run_master_pipeline():
    print("=" * 50)
    print("🚀 AntiGravity One-Click Pipeline Started (v3.2)")
    print("=" * 50)

    # 1단계: 형상 데이터 추출
    print("\n[Step 1] Extracting Geometry Data...")
    if not os.path.exists(EXTRACTOR_PATH):
        print("Error: Extractor script not found at " + EXTRACTOR_PATH)
        return
    try:
        # Extractor 실행 시 OUTPUT_PATH를 전역으로 주입
        with open(EXTRACTOR_PATH, 'r') as f:
            extractor_code = f.read()
            # globals()를 넘기고 locals에 OUTPUT_PATH를 넣어 정의 충돌 방지
            exec(extractor_code, globals(), {'OUTPUT_PATH': DATA_PATH})
        print(" -> Extraction Completed: " + DATA_PATH)
    except Exception as e:
        print(" -> Extraction Failed: " + str(e))
        return

    # 2단계: 외부 파이썬(CPython) 플래너 호출
    print("\n[Step 2] Calling External AI Planner...")
    try:
        start_info = ProcessStartInfo()
        start_info.FileName = PYTHON_EXE
        # 인자 전달: [main_run.py] [기기이름] [JSON파일명]
        start_info.Arguments = '"{0}" DEVICE geometry_data.json'.format(MAIN_RUN_PATH)
        start_info.WorkingDirectory = PROJECT_ROOT
        start_info.UseShellExecute = False
        start_info.CreateNoWindow = True
        
        process = Process.Start(start_info)
        process.WaitForExit()
        
        if process.ExitCode == 0:
            print(" -> Planning & Script Generation Completed.")
        else:
            print(" -> External Planner failed with Exit Code: " + str(process.ExitCode))
            return
    except Exception as e:
        print(" -> Error calling external Python: " + str(e))
        return

    # 3단계: 생성된 분할 스크립트 실행
    print("\n[Step 3] Executing Decomposition...")
    if not os.path.exists(GENERATED_SCRIPT_PATH):
        print("Error: Generated script not found at " + GENERATED_SCRIPT_PATH)
        return
    try:
        with open(GENERATED_SCRIPT_PATH, 'r') as f:
            # Step 3 실행 시에도 globals()를 넘겨서 API와 ALL_CUTTERS 등에 접근 가능하게 함
            exec(f.read(), globals())
        print(" -> Decomposition Execution Completed Successfully!")
    except Exception as e:
        print(" -> Execution Failed: " + str(e))

    print("\n" + "=" * 50)
    print("🏁 All Tasks Finished!")
    print("=" * 50)

# 파이프라인 실행
run_master_pipeline()
