# -*- coding: utf-8 -*-
# 이 코드는 스페이스클레임(IronPython) 환경에서 실행될 때 안전한 API 호출을 보장합니다.

class SafeSCDM:
    """Ansys 버전(2021, 2024 등)에 관계없이 안전하게 명령을 실행하는 래퍼"""
    
    @staticmethod
    def get_all_bodies(part):
        """GetAllBodies()가 없으면 Bodies 속성에서 직접 가져옵니다."""
        if hasattr(part, 'GetAllBodies'):
            return list(part.GetAllBodies())
        elif hasattr(part, 'Bodies'):
            return list(part.Bodies)
        return []

    @staticmethod
    def split_body_safe(body, plane):
        """자르기 후 생성된 바디들을 확실하게 반환받습니다."""
        try:
            # 최신 버전 방식
            result = Body.Split(body, plane)
            if hasattr(result, 'CreatedBodies'):
                return list(result.CreatedBodies)
            return []
        except:
            # 구버전이나 예외 상황 시, 다시 전체 바디를 수집하는 로직으로 대체 가능
            return None

def main_logic():
    # 실제 스페이스클레임에서의 사용 예시 (슈도 코드)
    # root = GetRootPart()
    # bodies = SafeSCDM.get_all_bodies(root)
    # ...
    pass
