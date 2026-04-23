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
# [사용자 설정] 아래 경로들을 본인의 Windows 환경에 맞게 수정하세요.
# (맥(Mac)의 공유 폴더를 윈도우에서 접근하는 경우, 윈도우에서 보이는 드라이브 경로(예: Z:\...)를 입력해야 합니다)
# ------------------------------------------------------------------------------
PROJECT_ROOT = r"C:\path\to\your\solid_decomposer" 

# 외부 CPython 실행 파일 경로 (가상환경이 있다면 가상환경의 python.exe 경로)
# 예: r"C:\path\to\your\solid_decomposer\.venv\Scripts\python.exe"
PYTHON_EXE = r"python" 

# ------------------------------------------------------------------------------
# 내부 경로 자동 설정
EXTRACTOR_PATH = os.path.join(PROJECT_ROOT, "01_extractor", "scdm_extractor.py")
MAIN_RUN_PATH = os.path.join(PROJECT_ROOT, "main_run.py")
GENERATED_SCRIPT_PATH = os.path.join(PROJECT_ROOT, "04_scripts", "scdm_decomposition_script.py")

def run_master_pipeline():
    print("=" * 50)
    print("🚀 AntiGravity One-Click Pipeline Started")
    print("=" * 50)

    # 1단계: 형상 데이터 추출
    print("\n[Step 1] Extracting Geometry Data...")
    if not os.path.exists(EXTRACTOR_PATH):
        print("Error: Extractor script not found at " + EXTRACTOR_PATH)
        return
    try:
        # 데이터 저장 경로 강제 지정
        DATA_PATH = os.path.join(PROJECT_ROOT, "data", "geometry_data.json")
        
        # Extractor 스크립트를 읽어서 실행하되, OUTPUT_PATH를 현재 컨텍스트에서 오버라이드
        with open(EXTRACTOR_PATH, 'r') as f:
            # globals()를 넘겨서 SpaceClaim API 함수들에 접근 가능하게 함
            # 로컬 변수로 OUTPUT_PATH를 주입
            exec(f.read(), globals(), {'OUTPUT_PATH': DATA_PATH})
        print(" -> Extraction Completed: " + DATA_PATH)
    except Exception as e:
        print(" -> Extraction Failed: " + str(e))
        return

    # 2단계: 외부 파이썬(CPython) 플래너 호출
    print("\n[Step 2] Calling External AI Planner...")
    try:
        # CPython 실행을 위한 프로세스 설정
        start_info = ProcessStartInfo()
        start_info.FileName = PYTHON_EXE
        # 인자 전달: [main_run.py 경로] [기기이름] [JSON파일명]
        # JSON 경로는 파일명만 전달 (ExtractManager가 data/ 폴더에서 찾음)
        input_json_name = os.path.basename(DATA_PATH)
        start_info.Arguments = '"{0}" DEVICE {1}'.format(MAIN_RUN_PATH, input_json_name)
        start_info.WorkingDirectory = PROJECT_ROOT
        start_info.UseShellExecute = False
        start_info.CreateNoWindow = True # 검은색 CMD 창 숨기기
        
        process = Process.Start(start_info)
        process.WaitForExit() # 외부 파이썬 작업이 끝날 때까지 스페이스클레임 대기
        
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
            exec(f.read())
        print(" -> Decomposition Execution Completed Successfully!")
    except Exception as e:
        print(" -> Execution Failed: " + str(e))

    print("\n" + "=" * 50)
    print("🏁 All Tasks Finished!")
    print("=" * 50)

# 파이프라인 실행
run_master_pipeline()
