import numpy as np

class MeshEvaluator:
    """
    고도화된 심판 모듈: 피쳐별 로컬 좌표계 대응 (Feature-Aware Scoring)
    """
    def calculate_score(self, body_data, plan):
        strategy = plan.get("strategy", "UNKNOWN")
        scores = []
        
        if "split_plane" not in plan:
            return 0

        plane_origin = np.array(plan["split_plane"]["origin"])
        plane_normal = np.array(plan["split_plane"]["normal"])
        plane_normal = plane_normal / np.linalg.norm(plane_normal)

        # 1. 가장 가까운 피쳐(실린더) 찾기
        cylinders = body_data.get("cylinders", [])
        target_cyl = None
        min_dist = float('inf')
        
        for cyl in cylinders:
            dist = np.linalg.norm(plane_origin - np.array(cyl["origin"]))
            if dist < min_dist:
                min_dist = dist
                target_cyl = cyl
        
        if not target_cyl:
            return 50 # 피쳐가 없으면 기본점수

        # 2. 타겟 피쳐의 로컬 축 기준으로 평가
        feat_axis = np.array(target_cyl["axis"])
        feat_axis = feat_axis / np.linalg.norm(feat_axis)
        feat_origin = np.array(target_cyl["origin"])
        
        # 2-1. 직교성 (Feature-Local Orthogonality)
        dot = np.abs(np.dot(plane_normal, feat_axis))
        
        if strategy in ["TRANSVERSE", "AXIAL"]:
            # 단면/단차 분할은 피쳐 축과 평행해야 함 (법선이 축과 일치)
            ortho_score = 100 * (1.0 - abs(dot - 1.0))
        elif strategy == "SECTOR":
            # 십자 분할은 피쳐 축과 수직해야 함 (법선이 축과 직교)
            ortho_score = 100 * (1.0 - abs(dot - 0.0))
        else:
            ortho_score = 100 * (1.0 - min(abs(dot - 0), abs(dot - 1)))
        
        scores.append(ortho_score)

        # 2-2. 위치 정합성 (Feature-Local Centricity)
        # 평면이 피쳐의 원점을 지나는지 확인 (축 방향 거리는 무시하고 수평 거리만)
        vec_to_plane = plane_origin - feat_origin
        # 축 방향 성분 제거
        dist_vec = vec_to_plane - np.dot(vec_to_plane, feat_axis) * feat_axis
        dist_val = np.linalg.norm(dist_vec)
        
        pos_score = max(0, 100 - dist_val * 50)
        scores.append(pos_score)

        return np.mean(scores)

    def visualize_plan(self, body_data, plans): pass
