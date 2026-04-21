import random

class MockBody:
    """스페이스클레임의 'Body' 객체를 흉내냅니다."""
    def __init__(self, name):
        self.name = name
        self.id = random.randint(1000, 9999)
        self.is_alive = True

    def __repr__(self):
        return f"[{self.name} (ID:{self.id})]"

class MockSCDM:
    """스페이스클레임의 API 환경을 흉내냅니다."""
    def __init__(self):
        self.all_bodies = [MockBody("Solid1")] # 초기 솔리드

    def split_body(self, target, plane_name):
        """자르기 명령을 수행하면 기존 바디는 죽고, 새 조각들이 생겨납니다."""
        if target not in self.all_bodies:
            print(f"  [Error] {target} 을 찾을 수 없습니다! (이미 삭제되었거나 잘못된 참조)")
            return []

        print(f"  >> {target.name} 을 {plane_name} 으로 자르는 중...")
        self.all_bodies.remove(target)
        target.is_alive = False
        
        # 실제 스페이스클레임처럼 이름이 무작위로 바뀜 (Solid1-1, Solid1-2 등)
        child1 = MockBody(f"{target.name}_part1")
        child2 = MockBody(f"{target.name}_part2")
        
        self.all_bodies.append(child1)
        self.all_bodies.append(child2)
        
        return [child1, child2] # 새로 생성된 조각들을 반환

def run_simulation():
    scdm = MockSCDM()
    print("--- [시작] 초기 상태 ---")
    print(f"현재 바디들: {scdm.all_bodies}\n")

    # [문제 상황 재현] 나쁜 예: 기존 참조를 계속 쓰려고 할 때
    print("--- [Case A] 기존 참조를 재사용하는 잘못된 방식 ---")
    initial_target = scdm.all_bodies[0]
    
    # 1차 세로 자르기
    pieces_step1 = scdm.split_body(initial_target, "XZ_Plane")
    
    # 2차 가로 자르기 (실수! initial_target을 또 자르려고 함)
    print("\n  (2차 자르기 시도...)")
    scdm.split_body(initial_target, "YZ_Plane") 
    print(f"최종 결과: {scdm.all_bodies} (조각이 2개뿐!)\n")

    # [해결 방법] 좋은 예: 계보(Ancestry)를 추적하며 자식들을 모두 수집할 때
    scdm = MockSCDM() # 리셋
    print("--- [Case B] 계보(Ancestry)를 추적하는 안전한 방식 ---")
    target_group = [scdm.all_bodies[0]] # 자를 대상 그룹
    
    # 1차 세로 자르기
    print("  (1차 자르기 시작)")
    next_group = []
    for target in target_group:
        new_pieces = scdm.split_body(target, "XZ_Plane")
        next_group.extend(new_pieces)
    
    # 2차 가로 자르기 (1차에서 나온 '모든 자식들'을 대상으로 자름)
    print("\n  (2차 자르기 시작)")
    final_group = []
    for target in next_group:
        new_pieces = scdm.split_body(target, "YZ_Plane")
        final_group.extend(new_pieces)
    
    print(f"\n최종 결과: {scdm.all_bodies} (완벽하게 4조각 성공!)")

if __name__ == "__main__":
    run_full_simulation = run_simulation
    run_full_simulation()
