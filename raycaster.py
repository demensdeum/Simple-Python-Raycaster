# Basic Python Raycaster
# Based on lodev tutorial
# http://lodev.org/cgtutor/raycasting.html

import pygame
from math import sqrt

nearZeroConst = 0.000000000000000000000000000000000001

class GameMap:

	worldMap = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Cursor:

	x = 0
	y = 0

class Vector:

	x = 0.0
	y = 0.0
	z = 0.0
	
class Screen:

	width = 800.0
	height = 600.0

class Camera:

	position = Vector()
	direction = Vector()
	plane = Vector()
	
class RaycasterRenderer:

	gameMap = GameMap()

	screen = Screen()
	
	camera = Camera()

	camera.position.x = 22
	camera.position.y = 12

	camera.direction.x = -1.0
	camera.direction.y = nearZeroConst
	
	camera.plane.x = nearZeroConst
	camera.plane.y = 0.66
	
	side = 0

	pygame.init()
	
	canvas = pygame.display.set_mode([int(screen.width), int(screen.height)])

	while True:
	
		canvas.fill((255, 255, 255)) 
	
		for x in range(0, int(screen.width)):
			
			wallDistance = 0.0
			renderX = 2 * x / screen.width - 1 # from -1 to 1
		
			rayStartPointVector = Vector()
			rayStartPointVector.x = camera.position.x
			rayStartPointVector.y = camera.position.y
		
			rayDirectionVector = Vector()
			rayDirectionVector.x = camera.direction.x + camera.plane.x * renderX
			rayDirectionVector.y = camera.direction.y + camera.plane.y * renderX
			
			tileX = int(rayStartPointVector.x)
			tileY = int(rayStartPointVector.y)
			
			sideDistanceVector = Vector()
			
			cursor = Cursor()
			cursor.x = int(camera.position.x)
			cursor.y = int(camera.position.y)
			
			#print "---"
			#print "renderX: " + str(renderX)
			
			#DDA
		
			ddaDeltaDistanceVector = Vector()
			ddaDeltaDistanceVector.x = sqrt(1 + (rayDirectionVector.y * rayDirectionVector.y) / (rayDirectionVector.x * rayDirectionVector.x))
			ddaDeltaDistanceVector.y = sqrt(1 + (rayDirectionVector.x * rayDirectionVector.x) / (rayDirectionVector.y * rayDirectionVector.y))
		
			#calculate step and initial sideDist
		
			stepDiffX = 0
			stepDiffY = 0
		
			if rayDirectionVector.x < 0:
		
				stepDiffX = -1
				sideDistanceVector.x = (camera.position.x - float(cursor.x)) * ddaDeltaDistanceVector.x
			else:
				stepDiffX = 1
				sideDistanceVector.x = (float(cursor.x) + 1.0 - camera.position.x) * ddaDeltaDistanceVector.x

			if rayDirectionVector.y < 0:
		
				stepDiffY = -1
				sideDistanceVector.y = (camera.position.y - float(cursor.y)) * ddaDeltaDistanceVector.y
			else:
				stepDiffY = 1
				sideDistanceVector.y = (float(cursor.y) + 1.0 - camera.position.y) * ddaDeltaDistanceVector.y
		
			#print sideDistanceVector.x
			#print sideDistanceVector.y
			
			# walk through map by x or y
			
			while True:
			
        
				if sideDistanceVector.x < sideDistanceVector.y:
				
					sideDistanceVector.x += ddaDeltaDistanceVector.x
					cursor.x += stepDiffX
					side = 0
				else:
        
					sideDistanceVector.y += ddaDeltaDistanceVector.y
					cursor.y += stepDiffY
					side = 1
        
				if gameMap.worldMap[cursor.x][cursor.y] > 0:
							
					break

			if side == 0:
				wallDistance = (float(cursor.x) - camera.position.x + (1 - stepDiffX) / 2) / rayDirectionVector.x;
			else:
				wallDistance = (float(cursor.y) - camera.position.y + (1 - stepDiffY) / 2) / rayDirectionVector.y;					

			lineHeight = int(screen.height / wallDistance)
			
			pygame.draw.rect(canvas, [255,0,0], (x, screen.height / 2 - lineHeight / 2, 1, lineHeight))
	
		pygame.display.update()
		
		camera.position.x -= 0.1
		
	pygame.quit()
	
class GameEngine:
	
	screen = Screen()
	
	gameMap = GameMap()
	
	camera = Camera()
	
	renderer = RaycasterRenderer()
	
	
	