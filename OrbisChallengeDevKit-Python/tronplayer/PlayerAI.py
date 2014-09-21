import random
from tronclient.Client import *
import time

class Powers():
	def __init__(self, x, y):
		self.pos_x = x
		self.pos_y = y
		return

class PlayerAI():

	def __init__(self):
		self.op_has_power = False
		self.map = 0
		self.powerups = 0
		self.op_power = 0
		self.my_off_map = 0
		self.op_off_map = 0
		self.op_ded_x = 0
		self.op_ded_y = 0
		self.op_dead = False
		return

	def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
		#map_file = open('map.csv','w')
		map_length = len(game_map)
		self.map = [[0 for j in range(map_length)] for i in range(map_length)]
		self.powerups = []
		for i in range(map_length):
			for j in range(map_length):
				self.map[i][j] = game_map[i][j]
				if self.map[i][j] == 'powerup':
					x = Powers(i,j)
					self.powerups.append(x)
				#map_file.write('%s,'%(self.map[i][j]))
			#map_file.write('\n')
		return

	def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):
		start = time.time()
		my_position = player_lightcycle['position']
		my_x = my_position[0]
		my_y = my_position[1]
		my_direction = player_lightcycle['direction']
		
		op_position = opponent_lightcycle['position']
		op_x = op_position[0]
		op_y = op_position[1]
		op_direction = opponent_lightcycle['direction']
		
		if (op_x == self.op_ded_x) and (op_y == self.op_ded_y) and (self.op_dead == False):
			self.op_dead = True
		self.map[my_x][my_y] = LIGHTCYCLE
		self.map[op_x][op_y] = LIGHTCYCLE
		
		if op_direction == Direction.UP :
			self.map[op_x][op_y+1] = TRAIL
		elif op_direction == Direction.DOWN :
			self.map[op_x][op_y-1] = TRAIL
		elif op_direction == Direction.LEFT :
			self.map[op_x+1][op_y] = TRAIL
		else :
			self.map[op_x-1][op_y] = TRAIL
		
		if my_direction == Direction.UP :
			self.map[my_x][my_y+1] = TRAIL
		elif my_direction == Direction.DOWN :
			self.map[my_x][my_y-1] = TRAIL
		elif my_direction == Direction.LEFT :
			self.map[my_x+1][my_y] = TRAIL
		else :
			self.map[my_x-1][my_y] = TRAIL
		
		thingstopop = []
		
		for i in range(len(self.powerups)) :
			if (op_x == self.powerups[i].pos_x) and (op_y == self.powerups[i].pos_y) :
				if opponent_lightcycle['hasPowerup'] != self.op_has_power :
					#Obtained power
					self.op_has_power = opponent_lightcycle['hasPowerup']
					self.op_power = opponent_lightcycle['powerupType']
				else :
					for j in range(5) :
						for k in range(-2,2) :
							if op_direction == Direction.UP :
								if (op_x+k < len(game_map)) and (op_x+k >= 0) and (op_y-j < len(game_map)) and (op_y-j >= 0) :
									self.map[op_x+k][op_y-j]=game_map[op_x+k][op_y-j]
							elif op_direction == Direction.DOWN :
								if (op_x+k < len(game_map)) and (op_x+k >= 0) and (op_y+j < len(game_map)) and (op_y+j >= 0) :
									self.map[op_x+k][op_y+j]=game_map[op_x+k][op_y+j]
							elif op_direction == Direction.LEFT :
								if (op_x-j < len(game_map)) and (op_x-j >= 0) and (op_y+k < len(game_map)) and (op_y+k >= 0) :
									self.map[op_x-j][op_y+k]=game_map[op_x-j][op_y+k]
							else :
								if (op_x+j < len(game_map)) and (op_x+j >= 0) and (op_y+k < len(game_map)) and (op_y+k >= 0) :
									self.map[op_x+j][op_y+k]=game_map[op_x+j][op_y+k]
				thingstopop.append(i)
			if (my_x == self.powerups[i].pos_x) and (my_y == self.powerups[i].pos_y) :
				for j in range(5) :
						for k in range(-2,2) :
							if my_direction == Direction.UP :
								if (my_x+k < len(game_map)) and (my_x+k >= 0) and (my_y-j < len(game_map)) and (my_y-j >= 0) :
									self.map[my_x+k][my_y-j]=game_map[my_x+k][my_y-j]
							elif my_direction == Direction.DOWN :
								if (my_x+k < len(game_map)) and (my_x+k >= 0) and (my_y+j < len(game_map)) and (my_y+j >= 0) :
									self.map[my_x+k][my_y+j]=game_map[my_x+k][my_y+j]
							elif my_direction == Direction.LEFT :
								if (my_x-j < len(game_map)) and (my_x-j >= 0) and (my_y+k < len(game_map)) and (my_y+k >= 0) :
									self.map[my_x-j][my_y+k]=game_map[my_x-j][my_y+k]
							else :
								if (my_x+j < len(game_map)) and (my_x+j >= 0) and (my_y+k < len(game_map)) and (my_y+k >= 0) :
									self.map[my_x+j][my_y+k]=game_map[my_x+j][my_y+k]
				thingstopop.append(i)
		
		for i in range(len(thingstopop)):
			self.powerups.pop(thingstopop[i])
		
		if opponent_lightcycle['hasPowerup'] != self.op_has_power :
			self.op_has_power = opponent_lightcycle['hasPowerup']
		'''
		Algo:
		If path exists bwt players (Note if mine: go to cut off)
			Yes => Offensive
			No => Powerup check
			
		Offensive:
			Maximize our area
			
		Powerup check:
			If invincibility and we have less area,
				cut into opponent area
			If bomb,
				Cut more into opponent area
			Else
				Circle
		'''	
		value = [0,0,0,0]
		valuecheck = [0,0,0,0]
		#print moveNumber
		#print my_x
		#print my_y
		
		#map_file = open('map.csv','w')
		#for i in range(len(self.map)):
		#	for j in range(len(self.map)):
		#		map_file.write('%s,'%(self.map[j][i]))
		#	map_file.write('\n')
			
		if (self.map[my_x][my_y-1] == EMPTY) or (self.map[my_x][my_y-1] == POWERUP):
			value[0] = self.find_value(my_x,my_y,op_x,op_y,0)
			valuecheck[0] = 1
		if (self.map[my_x][my_y+1] == EMPTY) or (self.map[my_x][my_y+1] == POWERUP):
			value[1] = self.find_value(my_x,my_y,op_x,op_y,1)
			valuecheck[1] = 1
		if (self.map[my_x-1][my_y] == EMPTY) or (self.map[my_x-1][my_y] == POWERUP):
			value[2] = self.find_value(my_x,my_y,op_x,op_y,2)
			valuecheck[2] = 1
		if (self.map[my_x+1][my_y] == EMPTY) or (self.map[my_x+1][my_y] == POWERUP):
			value[3] = self.find_value(my_x,my_y,op_x,op_y,3)
			valuecheck[3] = 1
		highestvalue = -10000000
		for i in range(4):
			if valuecheck[i] == 1:
				valuecheck[i] = 0
				if value[i] > highestvalue:
					valuecheck[i] = 1
					highestvalue = value[i]
		#print valuecheck[0]
		#print valuecheck[1]
		#print valuecheck[2]
		#print valuecheck[3]
		#print '\n'
		self.op_ded_x = op_x
		self.op_ded_y = op_y
		#end = time.time()
		#print end-start
		if valuecheck[3] == 1:
			return PlayerActions.MOVE_RIGHT
		elif valuecheck[2] == 1:
			return PlayerActions.MOVE_LEFT
		elif valuecheck[1] == 1:
			return PlayerActions.MOVE_DOWN
		elif valuecheck[0] == 1:
			return PlayerActions.MOVE_UP
		else:
			if player_lightcycle['hasPowerup']:
				if (self.map[my_x][my_y-1] != WALL) and my_direction != Direction.DOWN:
					return PlayerActions.ACTIVATE_POWERUP_MOVE_UP
				if (self.map[my_x][my_y+1] != WALL) and my_direction != Direction.UP:
					return PlayerActions.ACTIVATE_POWERUP_MOVE_DOWN
				if (self.map[my_x-1][my_y] != WALL) and my_direction != Direction.RIGHT:
					return PlayerActions.ACTIVATE_POWERUP_MOVE_LEFT
				if (self.map[my_x+1][my_y] != WALL) and my_direction != Direction.LEFT:
					return PlayerActions.ACTIVATE_POWERUP_MOVE_RIGHT
	#Scoring:
	#Wall in our territory = 0
	#Regular Space in our = 1
	#Powerup in our = 1
	#Regular is we can't get to it or tehy get their fisrt = negative
	def find_value(self, my_x, my_y, op_x, op_y, Direction):
		value = 0
		valueup = 0
		valuedown = 0
		valueleft = 0
		valueright = 0
		valuecheck = [0,0,0,0]
		valuelength = 0
		my_new_x = my_x
		my_new_y = my_y
		temp_my_new = 0
		temp_op_new = 0
		valuedead = 0
		if Direction == 0: #up
			my_new_y -= 1
		elif Direction == 1: #down
			my_new_y += 1
		elif Direction == 2: #left
			my_new_x -= 1
		elif Direction == 3: #right
			my_new_x += 1
			
		#Temporary TRAIL for fill_map
		self.map[my_x][my_y] = TRAIL
		temp_my_new = self.map[my_new_x][my_new_y]
		self.map[my_new_x][my_new_y] = LIGHTCYCLE
		self.map[op_x][op_y] = TRAIL

		if self.op_dead == False:
			#If opponent moves up
			if op_y > 0:
				op_new_x = op_x
				op_new_y = op_y - 1
				if(self.map[op_new_x][op_new_y] == EMPTY) or (self.map[op_new_x][op_new_y] == POWERUP):
					temp_op_new = self.map[op_new_x][op_new_y]
					self.map[op_new_x][op_new_y] = LIGHTCYCLE
					self.my_off_map = self.fill_map(my_new_x, my_new_y)
					self.op_off_map = self.fill_map(op_new_x, op_new_y)
					valuecheck[0] = 1
					for i in range(len(self.map)):
						for j in range(len(self.map)):
							if (self.my_off_map[i][j] == -1) and (self.op_off_map[i][j] == -1):
								continue
							elif (self.my_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valueup -= 1
								if self.map[i][j] == POWERUP:
									valueup -= 1
							elif (self.op_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valueup += 1
								if self.map[i][j] == POWERUP:
									valueup += 1
							elif (self.my_off_map[i][j] == self.op_off_map[i][j]):
								continue
							elif (self.my_off_map[i][j] < self.op_off_map[i][j]):
								if self.map[i][j] == EMPTY:
									valueup += 1
								if self.map[i][j] == POWERUP:
									valueup += 1
							else:
								if self.map[i][j] == EMPTY:
									valueup -= 1
								if self.map[i][j] == POWERUP:
									valueup -= 1
					self.map[op_new_x][op_new_y] = temp_op_new
			#If opponent moves down
			if op_y < (len(self.map)-1):
				op_new_x = op_x
				op_new_y = op_y + 1
				if(self.map[op_new_x][op_new_y] == EMPTY) or (self.map[op_new_x][op_new_y] == POWERUP):
					temp_op_new = self.map[op_new_x][op_new_y]
					self.map[op_new_x][op_new_y] = LIGHTCYCLE
					self.my_off_map = self.fill_map(my_new_x, my_new_y)
					self.op_off_map = self.fill_map(op_new_x, op_new_y)
					valuecheck[1] = 1
					for i in range(len(self.map)):
						for j in range(len(self.map)):
							if (self.my_off_map[i][j] == -1) and (self.op_off_map[i][j] == -1):
								continue
							elif (self.my_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valuedown -= 1
								if self.map[i][j] == POWERUP:
									valuedown -= 1
							elif (self.op_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valuedown += 1
								if self.map[i][j] == POWERUP:
									valuedown += 1
							elif (self.my_off_map[i][j] == self.op_off_map[i][j]):
								continue
							elif (self.my_off_map[i][j] < self.op_off_map[i][j]):
								if self.map[i][j] == EMPTY:
									valuedown += 1
								if self.map[i][j] == POWERUP:
									valuedown += 1
							else:
								if self.map[i][j] == EMPTY:
									valuedown -= 1
								if self.map[i][j] == POWERUP:
									valuedown -= 1
					self.map[op_new_x][op_new_y] = temp_op_new				
			#If opponent moves left
			if op_x > 0:
				op_new_x = op_x - 1
				op_new_y = op_y
				if(self.map[op_new_x][op_new_y] == EMPTY) or (self.map[op_new_x][op_new_y] == POWERUP):
					temp_op_new = self.map[op_new_x][op_new_y]
					self.map[op_new_x][op_new_y] = LIGHTCYCLE
					self.my_off_map = self.fill_map(my_new_x, my_new_y)
					self.op_off_map = self.fill_map(op_new_x, op_new_y)
					valuecheck[2] = 1
					for i in range(len(self.map)):
						for j in range(len(self.map)):
							if (self.my_off_map[i][j] == -1) and (self.op_off_map[i][j] == -1):
								continue
							elif (self.my_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valueleft -= 1
								if self.map[i][j] == POWERUP:
									valueleft -= 1
							elif (self.op_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valueleft += 1
								if self.map[i][j] == POWERUP:
									valueleft += 1
							elif (self.my_off_map[i][j] == self.op_off_map[i][j]):
								continue
							elif (self.my_off_map[i][j] < self.op_off_map[i][j]):
								if self.map[i][j] == EMPTY:
									valueleft += 1
								if self.map[i][j] == POWERUP:
									valueleft += 1
							else:
								if self.map[i][j] == EMPTY:
									valueleft -= 1
								if self.map[i][j] == POWERUP:
									valueleft -= 1
					self.map[op_new_x][op_new_y] = temp_op_new				
			#If opponent moves right
			if op_x < (len(self.map)-1):
				op_new_x = op_x + 1
				op_new_y = op_y
				if(self.map[op_new_x][op_new_y] == EMPTY) or (self.map[op_new_x][op_new_y] == POWERUP):
					temp_op_new = self.map[op_new_x][op_new_y]
					self.map[op_new_x][op_new_y] = LIGHTCYCLE
					self.my_off_map = self.fill_map(my_new_x, my_new_y)
					self.op_off_map = self.fill_map(op_new_x, op_new_y)
					valuecheck[2] = 1
					for i in range(len(self.map)):
						for j in range(len(self.map)):
							if (self.my_off_map[i][j] == -1) and (self.op_off_map[i][j] == -1):
								continue
							elif (self.my_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valueright -= 1
								if self.map[i][j] == POWERUP:
									valueright -= 1
							elif (self.op_off_map[i][j] == -1):
								if self.map[i][j] == EMPTY:
									valueright += 1
								if self.map[i][j] == POWERUP:
									valueright += 1
							elif (self.my_off_map[i][j] == self.op_off_map[i][j]):
								continue
							elif (self.my_off_map[i][j] < self.op_off_map[i][j]):
								if self.map[i][j] == EMPTY:
									valueright += 1
								if self.map[i][j] == POWERUP:
									valueright += 1
							else:
								if self.map[i][j] == EMPTY:
									valueright -= 1
								if self.map[i][j] == POWERUP:
									valueright -= 1
					self.map[op_new_x][op_new_y] = temp_op_new
		else:
			self.my_off_map = self.fill_map(my_new_x, my_new_y)
			for i in range(len(self.map)):
				for j in range(len(self.map)):
					if (self.my_off_map[i][j] == -1):
						if self.map[i][j] == EMPTY:
							valuedead -= 1
						if self.map[i][j] == POWERUP:
							valuedead -= 1
					else:
						if self.map[i][j] == EMPTY:
							valuedead += 1
						if self.map[i][j] == POWERUP:
							valuedead += 1
			self.map[my_x][my_y] = LIGHTCYCLE
			self.map[my_new_x][my_new_y] = temp_my_new
			self.map[op_x][op_y] = WALL
			return valuedead

		self.map[my_x][my_y] = LIGHTCYCLE
		self.map[my_new_x][my_new_y] = temp_my_new
		self.map[op_x][op_y] = LIGHTCYCLE
		
		if valuecheck[0] == 1:
			valuelength += 1
			value += valueup
		if valuecheck[1] == 1:
			valuelength += 1
			value += valuedown
		if valuecheck[2] == 1:
			valuelength += 1
			value += valueleft
		if valuecheck[3] == 1:
			valuelength += 1
			value += valueright
		if valuelength == 0:
			return 0
		value = value/valuelength
		return value
	
	def fill_map(self, pos_x, pos_y):
		map = [[-1 for j in range(len(self.map))] for i in range(len(self.map))]
		map[pos_x][pos_y] = 0
		q = []
		point = [pos_x,pos_y]
		q.append(point)
		dist = 0
		while (len(q) != 0):
			dist += 1
			mpoint = q.pop(0)
			if ((self.map[mpoint[0]+1][mpoint[1]] == EMPTY) or (self.map[mpoint[0]+1][mpoint[1]] == POWERUP)) and (map[mpoint[0]+1][mpoint[1]] == -1):
				map[mpoint[0]+1][mpoint[1]] = dist
				point = [mpoint[0]+1,mpoint[1]]
				q.append(point)
			if ((self.map[mpoint[0]-1][mpoint[1]] == EMPTY) or (self.map[mpoint[0]-1][mpoint[1]] == POWERUP)) and (map[mpoint[0]-1][mpoint[1]] == -1):
				map[mpoint[0]-1][mpoint[1]] = dist
				point = [mpoint[0]-1,mpoint[1]]
				q.append(point)
			if ((self.map[mpoint[0]][mpoint[1]+1] == EMPTY) or (self.map[mpoint[0]][mpoint[1]+1] == POWERUP)) and (map[mpoint[0]][mpoint[1]+1] == -1):
				map[mpoint[0]][mpoint[1]+1] = dist
				point = [mpoint[0],mpoint[1]+1]
				q.append(point)
			if ((self.map[mpoint[0]][mpoint[1]-1] == EMPTY) or (self.map[mpoint[0]][mpoint[1]-1] == POWERUP)) and (map[mpoint[0]][mpoint[1]-1] == -1):
				map[mpoint[0]][mpoint[1]-1] = dist
				point = [mpoint[0],mpoint[1]-1]
				q.append(point)
		return map
'''

8888888 8888888888 8 888888888o.      ,o888888o.     b.             8 
      8 8888       8 8888    `88.  . 8888     `88.   888o.          8 
      8 8888       8 8888     `88 ,8 8888       `8b  Y88888o.       8 
      8 8888       8 8888     ,88 88 8888        `8b .`Y888888o.    8 
      8 8888       8 8888.   ,88' 88 8888         88 8o. `Y888888o. 8 
      8 8888       8 888888888P'  88 8888         88 8`Y8o. `Y88888o8 
      8 8888       8 8888`8b      88 8888        ,8P 8   `Y8o. `Y8888 
      8 8888       8 8888 `8b.    `8 8888       ,8P  8      `Y8o. `Y8 
      8 8888       8 8888   `8b.   ` 8888     ,88'   8         `Y8o.` 
      8 8888       8 8888     `88.    `8888888P'     8            `Yo
      
                                Quick Guide
                --------------------------------------------
                      Feel free to delete this comment.

        1. THIS IS THE ONLY .PY OR .BAT FILE YOU SHOULD EDIT THAT CAME FROM THE ZIPPED STARTER KIT

        2. Any external files should be accessible from this directory

        3. new_game is called once at the start of the game if you wish to initialize any values

        4. get_move is called for each turn the game goes on

        5. game_map is a 2-d array that contains values for every board position.
                example call: game_map[2][3] == POWERUP would evaluate to True if there was a powerup at (2, 3)

        6. player_lightcycle is your lightcycle and is what the turn you respond with will be applied to.
                It is a dictionary with corresponding keys: "position", "direction", "hasPowerup", "isInvincible", "powerupType"
                position is a 2-element int array representing the x, y value
                direction is the direction you are travelling in. can be compared with Direction.DIR where DIR is one of UP, RIGHT, DOWN, or LEFT
                hasPowerup is a boolean representing whether or not you have a powerup
                isInvincible is a boolean representing whether or not you are invincible
                powerupType is what, if any, powerup you have

        7. opponent_lightcycle is your opponent's lightcycle. Same keys and values as player_lightcycle

        8. You ultimately are required to return one of the following:
                                                PlayerAction.SAME_DIRECTION
                                                PlayerAction.MOVE_UP
                                                PlayerAction.MOVE_DOWN
                                                PlayerAction.MOVE_LEFT
                                                PlayerAction.MOVE_RIGHT
                                                PlayerAction.ACTIVATE_POWERUP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_UP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_DOWN
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_LEFT
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_RIGHT
                
        9. If you have any questions, contact challenge@orbis.com

        10. Good luck! Submissions are due Sunday, September 21 at noon. You can submit multiple times and your most recent submission will be the one graded.
 
'''
