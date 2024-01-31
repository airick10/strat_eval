import csv
import re

def gatherPlayer(row):
	# Assigning Arm rating
	matches = re.findall(r'\(([-+]?\d+)\)', row['FIELDING'])
	arm = 0
	if matches:
		arm = int(matches[0])

    # Assigning bat side
	if "*" in row['HITTERS']:
		bat = "L"
	elif "+" in row['HITTERS']:
		bat = "S"
	else:
		bat = "R"

	# Breaking down the BallPark Diamonds
	if "w" in row['BP v lhp']:
		bpvl = 0
	elif "*" in row['BP v lhp']:
		strin = row['BP v lhp']
		bpvl = int(strin[0])
	else:
		bpvl = row['BP v lhp']

	if "w" in row['BP v rhp']:
		bpvr = 0
	elif "*" in row['BP v rhp']:
		strin = row['BP v rhp']
		bpvr = int(strin[0])
	else:
		bpvr = row['BP v rhp']


	# Appropriately assigning positions integers
	column_to_variable = {
    'CA': 'ca',
    '1B': 'fb',
    '2B': 'sb',
    '3B': 'tb',
    'SS': 'ss',
    'LF': 'lf',
    'CF': 'cf',
    'RF': 'rf',
	}

	positions = {}

	for column_name, variable_name in column_to_variable.items():
		value = row.get(column_name, '0')  # Use '0' as a default value if the column is missing
		if value is not None and value.strip():  # Check if it's not None and not empty after stripping whitespace
			positions[variable_name] = int(value)
		else:
			positions[variable_name] = 0

	
	player = {
            'name': row['HITTERS'],
            'bat': bat,
            'ab': int(row['AB']),
            'sovl': float(row['SO v lhp']),
            'bbvl': float(row['BB v lhp']),
            'hvl': float(row['HIT v lhp']),
            'obvl': float(row['OB v lhp']),
            'tbvl': float(row['TB v lhp']),
            'hrvl': float(row['HR v lhp']),
            'bpvl': int(bpvl),
            'dpvl': float(row['DP v lhp']),
            'sovr': float(row['SO v rhp']),
            'bbvr': float(row['BB v rhp']),
            'hvr': float(row['HIT v rhp']),
            'obvr': float(row['OB v rhp']),
            'tbvr': float(row['TB v rhp']),
            'hrvr': float(row['HR v rhp']),
            'bpvr': int(bpvr),
            'dpvr': float(row['DP v rhp']),
            'stealing': row['STEALING'],
            'spd': int(row['SPD']),
            'inj': int(row['INJ']),
            'ca': positions['ca'],
            '1b': positions['fb'],
            '2b': positions['sb'],
            '3b': positions['tb'],
            'ss': positions['ss'],
            'lf': positions['lf'],
            'cf': positions['cf'],
            'rf': positions['rf'],
            'arm': int(arm)
        }
	return player

def getERating(rating):
	if rating >= 500:
		return rating - 500
	elif rating >= 400:
		return rating - 400
	elif rating >= 300:
		return rating - 300
	elif rating >= 200:
		return rating - 200
	else:
		return rating - 100

	return rating

def getRange(rating):
	if rating >= 500:
		return 5
	elif rating >= 400:
		return 4
	elif rating >= 300:
		return 3
	elif rating >= 200:
		return 2
	else:
		return 1

	return rating

def evalFielding(pos, frange, erating):
	if pos == "c":
		if frange == 1 and erating <= 4:
			return 100
		elif (frange == 1 and erating > 4) or (frange == 2 and erating <= 4):
			return 50
		elif (frange == 2 and erating > 4) or (frange == 3 and erating <= 4):
			return 25
		elif frange < 5:
			return 10

	if pos == "ss" or pos == "sb":
		if frange == 1 and erating <= 20:
			return 120
		elif (frange == 1 and erating > 20) or (frange == 2 and erating <= 20):
			return 60
		elif (frange == 2 and erating > 20) or (frange == 3 and erating <= 20):
			return 35

	if pos == "3b":
		if frange == 1 and erating <= 10:
			return 100
		elif (frange == 1 and erating > 10) or (frange == 2 and erating <= 10):
			return 75
		elif (frange == 2 and erating > 10) or (frange == 3 and erating <= 10):
			return 50
		elif frange < 5:
			return 10

	if pos == "1b":
		if frange == 1 and erating <= 7:
			return 75
		elif (frange == 1 and erating > 7) or (frange == 2 and erating <= 7):
			return 50
		elif (frange == 2 and erating > 7) or (frange == 3 and erating <= 7):
			return 25
		elif frange < 5:
			return 10

	if pos == "lf" or pos == "rf":
		if frange == 1 and erating <= 8:
			return 75
		elif (frange == 1 and erating > 8) or (frange == 2 and erating <= 8):
			return 50
		elif (frange == 2 and erating > 8) or (frange == 3 and erating <= 8):
			return 25
		elif frange < 5:
			return 10

	if pos == "cf":
		if frange == 1 and erating <= 8:
			return 100
		elif (frange == 1 and erating > 8) or (frange == 2 and erating <= 8):
			return 50
		elif (frange == 2 and erating > 8) or (frange == 3 and erating <= 8):
			return 25

	return 0

def getAB(player):
	if player['ab'] > 420:
		ab_score = 100
	elif player['ab'] < 200:
		ab_score = 25

	return ab_score

def getArm(player):
	#Arm
	if player['ca'] > 0 or player['cf'] > 0:
		arm = (player['arm'] * 10)
	elif player['lf'] > 0 or player['rf'] > 0:
		arm = (player['arm'] * 5)
	else:
		arm = 0

	if arm > 0:
		arm_score = -arm
	else:
		arm_score = abs(arm)

	return arm_score

def getFielding(player):
	pos_array = ['ss','2b','cf','3b','ca','1b','lf','rf']

	field_score = 0
	keep_going = True
	for key in pos_array:
		if player[key] > 0 and keep_going:
			frange = getRange(player[key])
			erating = getERating(player[key])
			pos_score = evalFielding(key, frange, erating)
			if frange < 4:
				keep_going = False
		else:
			pos_score = 0
		field_score += pos_score

	return field_score


def getSpeed(player):
	speed_score = 0
	if "*" in player['stealing']:
		speed_score = 50
	speed_score = speed_score + (player['spd'] * 2)

	return speed_score	
	
def getLeftHitting(player):
	# Hitting Evaluation
	left_hitting = ((player['sovl'] - player['bbvl']) * CONST_SOBB) + (player['hvl'] - player['dpvl']) + ((player['obvl'] + player['tbvl']) * CONST_OBTB) + (player['hrvl'] * CONST_HR) + (player['bpvl'] * CONST_BP) 
	if player['bat'] == "L":
		left_hitting = left_hitting * CONST_SAMESIDE
	elif player['bat'] == "R":
		left_hitting = left_hitting * CONST_OPPOSIDE

	if player['ab'] <= 200:
		left_hitting = left_hitting * 0.65
	elif player['ab'] <= 300 and player['ab'] > 200:
		left_hitting = left_hitting * 0.8
	elif player['ab'] < 420 and player['ab'] > 300:
		left_hitting = left_hitting * 0.9


	return round(left_hitting, 2)

def getRightHitting(player):
	# Hitting Evaluation
	right_hitting = ((player['sovr'] - player['bbvr']) * CONST_SOBB) + (player['hvr'] - player['dpvr']) + ((player['obvr'] + player['tbvr']) * CONST_OBTB) + (player['hrvr'] * CONST_HR) + (player['bpvr'] * CONST_BP) 
	if player['bat'] == "L":
		right_hitting = right_hitting * CONST_OPPOSIDE
	elif player['bat'] == "R":
		right_hitting = right_hitting * CONST_SAMESIDE

	if player['ab'] <= 200:
		right_hitting = right_hitting * 0.65
	elif player['ab'] <= 300 and player['ab'] > 200:
		right_hitting = right_hitting * 0.8
	elif player['ab'] < 420 and player['ab'] > 300:
		right_hitting = right_hitting * 0.9
	return round(right_hitting, 2)	

def userInput(dialog, default):
	value = input(f"{dialog} {default}):  ")
	if value == "":
		return default
	else:
		return int(value)

if __name__ == "__main__":
	score_sheet = {}

	filename = userInput("What is the CSV rile you want to use?  Needs to be in the same directory (Default", "strat_hitters.csv")

	CONST_SOBB = userInput("What is your K - BB weight? (Default  ", 0.8)
	CONST_OBTB = userInput("What is your OB + TB weight? (Default  ", 1.6)
	CONST_HR = userInput("What is your HR weight? (Default  ", 1.4)
	CONST_BP = userInput("What is your Diamonds weight? (Default  ", 1.4)
	CONST_OPPOSIDE = userInput("What is your weight as hitter/pitcher opposite side? (Default  ", .095)
	CONST_SAMESIDE = userInput("What is your weight as hitter/pitcher same side? (Default  ", 1.05)

	with open(filename, 'r') as filevar:
	    reader = csv.DictReader(filevar, delimiter=',', quotechar='"')
	    for row in reader:
	    	player = gatherPlayer(row)
	    	arm_score = getArm(player)
	    	field_score = getFielding(player)
	    	speed_score = getSpeed(player)
	    	left_hitting = getLeftHitting(player)
	    	right_hitting = getRightHitting(player)

	    	score = arm_score + field_score + left_hitting + (right_hitting * 1.2) + speed_score
	    	score = round(score, 2)

	    	#string_score = (f"Score: {score}  vsL: {left_hitting}  vsR: {right_hitting}  Field: {field_score}  Arm: {arm_score}  Speed: {speed_score}")
	    	#score_sheet[player['name']] = string_score
	    	score_sheet[player['name']] = score

	writevar = open('hitters_output.csv', 'w', newline='')
	writer = csv.writer(writevar)
	#score_sheet = dict(sorted(score_sheet.items(), key=lambda item: item[1], reverse=True))
	for key, value in score_sheet.items():
	    print(f'{key}: {value}')
	    row = [key, value]
	    writer.writerow(row)


