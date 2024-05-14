from Delta_robot import DeltaRobotKinematics

a = DeltaRobotKinematics(390,
                         120,
                         241,
                         300)
b = a.inverse_kinematics(300, 300, 300)
print(b)
# (0.0, -1.4210854715202004e-14, -440.7124727947029)
kinematics_params = {
    "static_dia": 390,
    "moving_dia": 120,
    "link_length": 241,
    "travel_range": 300
}
ws=a.calculate_workspace(1)
print(ws)
