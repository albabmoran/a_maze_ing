def crear_cuadradito(width = 3, height = 3):
	x = 0
	y = 0

	for y in range(height):
		for x in range(width):
			if (x == 0 and y == 0) or (x == width - 1 and y == 0) or (x == 0 and y == height - 1) or (x == width - 1 and y == height - 1):
				print(" ", end="")
			elif x == 0 or x == width - 1:
				print("|", end="")
			elif y == 0 or y == height - 1:
				print("-", end="")
			else:
				print(" ", end="")
		print()

crear_cuadradito()