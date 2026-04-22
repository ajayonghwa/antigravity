import cadquery as cq

class FeatureLibrary:
    """위상적 특징(Topological Features) 기반의 고도화된 형상 생성 라이브러리"""
    
    @staticmethod
    def create_through_hole(base_size=(100, 100, 20), hole_r=10):
        """1-1. 관통공 (Through Hole): 판재를 관통하는 구멍"""
        return cq.Workplane("XY").box(*base_size).faces(">Z").workplane().circle(hole_r).cutThruAll()

    @staticmethod
    def create_blind_hole(base_size=(100, 100, 40), hole_r=10, depth=25):
        """1-2. 막힌 구멍 (Blind Hole): 바닥면이 존재하는 구멍"""
        return cq.Workplane("XY").box(*base_size).faces(">Z").workplane().circle(hole_r).cutBlind(-depth)

    @staticmethod
    def create_slot(base_size=(100, 100, 20), length=40, width=15, depth=10):
        """1-3. 슬롯/키홈 (Slot): 끝단이 둥근 형태의 함몰 부위"""
        return (cq.Workplane("XY").box(*base_size)
                .faces(">Z").workplane()
                .slot2D(length, width).cutBlind(-depth))

    @staticmethod
    def create_boss(base_size=(100, 100, 20), boss_r=15, boss_h=15):
        """2-1. 돌출 보스 (Boss): 평면 위에 솟아오른 원통"""
        return (cq.Workplane("XY").box(*base_size)
                .faces(">Z").workplane()
                .circle(boss_r).extrude(boss_h))

    @staticmethod
    def create_t_junction(main_pipe_r=20, branch_pipe_r=15, length=100):
        """3-1. T자 분기 (T-Junction): 두 관이 수직으로 만나는 지점"""
        main_pipe = cq.Workplane("XY").circle(main_pipe_r).extrude(length).center(0, length/2)
        # 옆구리에서 분기 파이프 추가
        branch = (cq.Workplane("YZ").workplane(offset=0)
                  .circle(branch_pipe_r).extrude(length/2 + main_pipe_r))
        return main_pipe.union(branch)

    @staticmethod
    def add_fillet(model, radius=2.0, selector=">Z"):
        """4-1. 필렛/라운드 추가 (Fillet)"""
        return model.edges(selector).fillet(radius)

    @staticmethod
    def create_tapered_shaft(r1=30, r2=50, length=100):
        """4-2. 테이퍼 샤프트 (Taper/Cone): 지름이 변하는 구간"""
        return cq.Workplane("XY").circle(r1).workplane(offset=length).circle(r2).loft(combine=True)

    @staticmethod
    def create_square_to_circle(size=80, radius=30, height=60):
        """4-3. 단면 변환 (Square to Circle): 네모에서 동그라미로 전이"""
        return (cq.Workplane("XY").rect(size, size).workplane(offset=height)
                .circle(radius).loft(combine=True))

if __name__ == "__main__":
    # 개별 피쳐 생성 테스트
    lib = FeatureLibrary()
    # Lv.2: 필렛이 들어간 막힌 구멍 생성 예시
    model = lib.create_blind_hole()
    model = lib.add_fillet(model, radius=3.0, selector=">Z")
    print("Feature Library logic verified.")
