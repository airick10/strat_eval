import csv
import re

def gatherPlayer(row):
	# Assigning Arm rating
	if "S" in row['ENDURANCE'] and "R" in row['ENDURANCE']:
		pattern = r'(\w+)\((\d+)\) (\w+)\((\d+)\)'
		match = re.match(pattern, row['ENDURANCE'])
		role = "SR"
		if match:
			endurance = int(match.group(2))
		else:
			endurance = 0
	elif "S" in row['ENDURANCE']:
		if "*" in row['ENDURANCE']:
			pattern = r'(\w+)\((\d+)[^)]*\)'
			match = re.match(pattern, row['ENDURANCE'])
			role = "SP"
		else:
			pattern = r'(\w+)\((\d+)\)'
			match = re.match(pattern, row['ENDURANCE'])
			role = "S"
		if match:
			endurance = int(match.group(2))
		else:
			endurance = 0
	elif "R" in row['ENDURANCE'] or "C" in row['ENDURANCE']:
		role = "R"
		endurance = 0



    # Assigning bat side
	if "*" in row['PITCHERS']:
		throw = "L"
	else:
		throw = "R"

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
	values = row['FIELD'].split("-")
	frange = int(values[0])
	erating = int(values[1])

	if int(row['SPD']) > 10:
		speed = True
	else:
		speed = False
	
	player = {
            'name': row['PITCHERS'],
            'throw': throw,
            'ip': int(row['IP']),
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
            'hold': int(row['HO']),
            'endurance': endurance,
            'role': str(role),
            'range': frange,
            'erating': erating,
            'speed': speed
        }
	return player

def getFielding(player):
	frange = player['range']
	erating = player['erating']

	field_score = 35
	if frange == 1:
		field_score = 0
	elif frange == 2:
		field_score = 15
	elif frange == 3:
		field_score = 35

	if erating == 0:
		field_score = field_score - 50
	elif erating > 0 and erating < 12:
		field_score = field_score - 25

	return field_score

def getIP(player):
	if player['ip'] >= 120:
		return 0
	elif player['ip'] < 120 and player['ip'] > 50:
		return 25
	else:
		return 100

def getHold(player):
	return player['hold'] * 10		

def getEndurance(player):
	endurance_score = 100
	if "P" in player['role']:
		endurance_score = 0
	elif "S" in player['role']:
		endurance_score = (endurance_score / player['endurance']) * 2
	else:
		endurance_score = 35
	return endurance_score

def getSpeed(player):
	if player['speed']:
		return 0
	else:
		return 15	
	
def getLeftPitching(player):
	# Hitting Evaluation
	left_pitching = ((player['sovl'] - player['bbvl']) * CONST_SOBB) + (player['hvl'] - player['dpvl']) + ((player['obvl'] + player['tbvl']) * CONST_OBTB) + (player['hrvl'] * CONST_HR) + (player['bpvl'] * CONST_BP) 
	if player['throw'] == "L":
		left_pitching = left_pitching * CONST_SAMESIDE
	elif player['throw'] == "R":
		left_pitching = left_pitching * CONST_OPPOSIDE

	if player['ip'] <= 50:
		left_pitching = left_pitching * 0.65
	elif player['ip'] > 50 and player['ip'] <= 100:
		left_pitching = left_pitching * 0.75
	elif player['ip'] > 100 and player['ip'] <= 150:
		left_pitching = left_pitching * 0.85
	else:
		left_pitching = left_pitching * 0.9


	return round(left_pitching, 2)

def getRightPitching(player):
	# Hitting Evaluation
	right_pitching = ((player['sovr'] - player['bbvr']) * CONST_SOBB) + (player['hvr'] - player['dpvr']) + ((player['obvr'] + player['tbvr']) * CONST_OBTB) + (player['hrvr'] * CONST_HR) + (player['bpvr'] * CONST_BP) 
	if player['throw'] == "L":
		right_pitching = right_pitching * CONST_OPPOSIDE
	elif player['throw'] == "R":
		right_pitching = right_pitching * CONST_SAMESIDE

	if player['ip'] <= 50:
		right_pitching = right_pitching * 0.65
	elif player['ip'] > 50 and player['ip'] <= 100:
		right_pitching = right_pitching * 0.75
	elif player['ip'] > 100 and player['ip'] <= 150:
		right_pitching = right_pitching * 0.85
	else:
		right_pitching = right_pitching * 0.9


	return round(right_pitching, 2)	


def userInput(dialog, default):
	value = input(f"What is your K/BB measurement? (Default {default})")
	if value == "":
		return default
	else:
		return int(value)

if __name__ == "__main__":
	score_sheet = {}

	filename = input(f"What is the CSV rile you want to use?  Needs to be in the same directory")

	CONST_SOBB = userInput("What is your K - BB weight? (Default 0.8)", 0.8)
	CONST_OBTB = userInput("What is your OB + TB weight? (Default 1.6)", 1.6)
	CONST_HR = userInput("What is your HR weight? (Default 1.4)", 1.4)
	CONST_BP = userInput("What is your Diamonds weight? (Default 1.4)", 1.4)
	CONST_OPPOSIDE = userInput("What is your weight as hitter/pitcher opposite side? (Default .095)", .095)
	CONST_SAMESIDE = userInput("What is your weight as hitter/pitcher same side? (Default 1.05)", 1.05)

	with open(filename, 'r') as filevar:
	    reader = csv.DictReader(filevar, delimiter=',', quotechar='"')
	    for row in reader:
	    	player = gatherPlayer(row)
	    	#if player['ip'] > 49:
	    	endurance_score = getEndurance(player)
	    	field_score = getFielding(player)
	    	hold_score = getHold(player)
	    	speed_score = getSpeed(player)
	    	left_pitching = getLeftPitching(player)
	    	right_pitching = getRightPitching(player)

	    	score = endurance_score + field_score + hold_score + left_pitching + (right_pitching * 1.2) + speed_score
	    	score = round(score, 2)

	    	string_score = (f"Score: {score} vsL: {left_pitching} vsR: {right_pitching} Field: {field_score} Hold: {hold_score} Endurance: {endurance_score} Speed: {speed_score}")
	    	score_sheet[player['name']] = string_score

	writevar = open('pitchers_output.csv', 'w', newline='')
	writer = csv.writer(writevar)
	score_sheet = dict(sorted(score_sheet.items(), key=lambda item: item[1]))
	for key, value in score_sheet.items():
		print(f'{key}: {value}')
		row = [key, value]
		writer.writerow(row)