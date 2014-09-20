import random
from tronclient.Client import *
import time

class Powers():
	def __init__(self, x, y):
		self.pos_x = x
		self.pos_y = y;
		return
	
	def find_shortest(self):
		return
	
	def find_longest(self):
		return

class PlayerAI():

	def __init__(self):
		self.op_has_power = False
		self.map = 0
		self.powerups = 0
		self.op_power = 0
		return

	def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
		start = time.time()
		map_file = open('map.csv','w')
		map_length = len(game_map)
		self.map = [[0 for j in range(map_length)] for i in range(map_length)]
		self.powerups = []
		for i in range(map_length):
			for j in range(map_length):
				self.map[i][j] = game_map[j][i]
				if self.map[i][j] == 'powerup':
					x = Powers(j,i)
					self.powerups.append(x)
				map_file.write('%s,'%(self.map[i][j]))
			map_file.write('\n')
		for i in range(len(self.powerups)):
			print '%d %d, '%(self.powerups[i].pos_x,self.powerups[i].pos_y)
		end = time.time()
		print end - start
		return

	def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):

		my_position = player_lightcycle['position']
		my_x = my_position[0]
		my_y = my_position[1]
		my_direction = player_lightcycle['direction']
		
		op_position = opponent_lightcycle['position']
		op_x = op_position[0]
		op_y = op_position[1]
		op_direction = opponent_lightcycle['direction']
		
		if op_direction == Direction.UP :
			self.map[op_x][op_y+1] = TRAIL
		elif op_direction == Direction.DOWN :
			self.map[op_x][op_y-1] = TRAIL
		elif op_direction == Direction.LEFT :
			self.map[op_x+1][op_y] = TRAIL
		else :
			self.map[op_x-1][op_y] = TRAIL
		
		if my_direction == Direction.UP :
			self.map[op_x][op_y+1] = TRAIL
		elif my_direction == Direction.DOWN :
			self.map[op_x][op_y-1] = TRAIL
		elif my_direction == Direction.LEFT :
			self.map[op_x+1][op_y] = TRAIL
		else :
			self.map[op_x-1][op_y] = TRAIL
		
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
				self.powerups.pop(i)
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
				self.powerups.pop(i)
		
		if opponent_lightcycle['hasPowerup'] != self.op_has_power :
			self.op_has_power = opponent_lightcycle['hasPowerup']
			if self.op_has_power == False:
				#Used
				print 'Used'
		
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
		randMove = random.randint(0, 3)
		if randMove == 0:
			print "LEFT"
			return PlayerActions.MOVE_LEFT
		elif randMove == 1:
			print "RIGHT"
			return PlayerActions.MOVE_RIGHT
		elif randMove == 2:
			print "DOWN"
			return PlayerActions.MOVE_DOWN
		else:
			print "UP"
			return PlayerActions.MOVE_UP
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
