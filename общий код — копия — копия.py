from robodk import*
from robolink import*
RDK = Robolink()
robot = RDK.Item("KUKA KR 3 R540")
target = RDK.Item("Target 1")
i = 1
for i in range(1):
	while 1:
		program = RDK.AddProgram('program 1')
		print("pick")
		i = int(input("Первая координата: "))
		b = int(input("Вторая координата: "))
		c = int(input("Третья координата: "))
		i *= -1
		c *= -1
		approach = target.Pose()*transl(i, b, c)
		robot.MoveJ(approach)
		program.setDO(2, 1)
		pause(1000)
		program.setDO(1, 0)
		pause(1000)
		RDK.RunProgram("program 1")
		break
i = 1
for i in range(1):
	program = RDK.AddProgram('program 2')
	print("place")
	i = int(input("Первая координата: "))
	b = int(input("Вторая координата: "))
	c = int(input("Третья координата: "))
	i *= -1
	c *= -1
	approach = target.Pose()*transl(i, b, c)
	robot.MoveJ(approach)
	program.setDO(2, 0)
	pause(1000)
	program.setDO(1, 1)
	pause(1000)
	RDK.RunProgram("program 2")
	break
quit()