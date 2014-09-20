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
		opponent_has_power = false;
		return

	def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
		start = time.time()
		map_file = open('map.csv','w')
		map_length = len(game_map)
		map = [[0 for j in range(map_length)] for i in range(map_length)]
		powerups = []
		for i in range(map_length):
			for j in range(map_length):
				map[i][j] = game_map[j][i]
				if map[i][j] == 'powerup':
					x = Powers(j,i)
					powerups.append(x)
				map_file.write('%s,'%(map[i][j]))
			map_file.write('\n')
		for i in range(len(powerups)):
			print '%d %d, '%(powerups[i].pos_x,powerups[i].pos_y)
		end = time.time()
		print end - start
		return

	def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):

		my_position = player_lightcycle['position']
		my_x = my_position[0]
		my_y = my_position[1]
		my_direction = player_lightcycle['direction']
		
		opponent_position = opponent_lightcycle['position']
		opponent_x = opponent_position[0]
		opponent_y = opponent_position[1]
		opponent_direction = opponent_lightcycle['direction']
		
		if opponent_lightcycle['hasPowerUp'] != opponent_has_power :
			opponent_has_power = opponent_lightcycle['hasPowerUp']
			if opponent_has_power == true:
				#Obtained power
				print 
			else
				#used
		#Update map
		
		'''
		Algo:
		If path exists bwt players (Note if mine: go to cut off)
			Yes => Offensive
			No => Powerup check
			
		Offensive:
			Maximize our area
			
		Powerup check:
			If invincibility && we have less area,
				cut into opponent area
			If bomb,
				Cut more into opponent area
			Else
				Circle
		'''	
		randMove = random.randint(0, 3)
		if randMove == 0:
			#print "LEFT"
			return PlayerActions.MOVE_LEFT
		elif randMove == 1:
			#print "RIGHT"
			return PlayerActions.MOVE_RIGHT
		elif randMove == 2:
			#print "DOWN"
			return PlayerActions.MOVE_DOWN
		else:
			#print "UP"
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
