from robodk import*
from robolink import*
RDK = Robolink()
program = RDK.AddProgram('program 1')
robot = RDK.Item("KUKA KR 3 R540")
target = RDK.Item("Target 1")

while 1:
	try:
		i = int(input("Первая координата: "))
		b = int(input("Вторая координата: "))
		c = int(input("Третья координата: "))
		i *= -1
		c *= -1
		approach = target.Pose()*transl(i, b, c)
		robot.MoveJ(approach)
		program.setDO(2, 1)
		program.setDO(1, 0)
	except Exception:
		i = int(input("Первая координата: "))
		b = int(input("Вторая координата: "))
		c = int(input("Третья координата: "))
		i *= -1
		c *= -1
		approach = target.Pose()*transl(i, b, c)
		robot.MoveJ(approach)
		program.setDO(2, 1)
		program.setDO(1, 0)