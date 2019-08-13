from robodk import*
from robolink import*
RDK = Robolink()
robot = RDK.Item("UR 10")
target = RDK.Item("Target 1")
x = 400
y = 0
z = 220
x *= -1
z *= -1
approach = target.Pose()*transl(x, y, z)
robot.MoveJ(approach)