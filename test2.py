from Delta_robot import DeltaRobotKinematics
robot =DeltaRobotKinematics(133,
                         60,
                         251,
                         300)
a,b,c,d=robot.gate_curve()
print(len(a))
for i in range(len(a)-1):
    print(a[i],b[i],c[i],d[i])
    i+=1