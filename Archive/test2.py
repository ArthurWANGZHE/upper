from Delta_robot import DeltaRobotKinematics
robot =DeltaRobotKinematics(133,
                         60,
                         251,
                         300)
a,b,c,d=robot.point2point(10,10,10,20,10,10,)
print(len(a))
for i in range(len(a)-1):
    print(a[i],b[i],c[i],d[i])
    i+=1