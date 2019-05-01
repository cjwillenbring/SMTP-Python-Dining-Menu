import bs4
import requests
import re
import datetime
import smtplib

def funTimes():
	msg = ''
	year = datetime.datetime.today().strftime('%Y')
	month = datetime.datetime.today().strftime('%m')
	day = datetime.datetime.today().strftime('%d')

	url1 = 'https://apps2.housing.k-state.edu/menu/index.php?l=2&M=3&y=' + year + '&m=' + month + '&d=' + day


	link = requests.get(url1, timeout=5)

	diningMenu = bs4.BeautifulSoup(link.text, features="html.parser")

	meal =  diningMenu.find('ul', id = 'tabs')

	#time = input("Type B for Breakfast, L for Lunch, A for Afternoon, or D for Dinner: ")
	#time = 'D'

	def findLink(n):
		line = str(n)
		y = re.sub('(amp;)','',line)
		x = re.findall('(index.*[0-9][0-9])',y)
		if len(x) > 0:
			return x[0]

	differentLinks = []
	for meals in meal.find_all('li'):
		if meals.text == 'Breakfast':
			breakfastLink = findLink(meals)
			differentLinks.append(breakfastLink)
		if meals.text == 'Lunch':
			lunchLink = findLink(meals)
			differentLinks.append(lunchLink)
		if meals.text == 'Afternoon':
			aftenoonLink = findLink(meals)
			differentLinks.append(aftenoonLink)
		if meals.text == 'Dinner':
			dinnerLink = findLink(meals)
			differentLinks.append(dinnerLink)

	newUrl = 'https://apps2.housing.k-state.edu/menu/'
	"""
	if time.upper() == 'B':
		newUrl += breakfastLink
	elif time.upper() == 'L':
		newUrl += lunchLink
	elif time.upper() == 'A':
		newUrl += aftenoonLink
	elif time.upper() == 'D':
		newUrl += dinnerLink
	else:
		print("You suck at typing, pick a correct letter next time")
		quit()
	"""

	for linkers in differentLinks:
		if linkers == breakfastLink:
			msg += 'BREAKFAST\n'
		elif linkers == lunchLink:
			msg += 'LUNCH\n'
		elif linkers == aftenoonLink:
			msg += 'AFTERNOON\n'
		else:
			msg += 'DINNER\n'

		newUrl += linkers
		newLink = requests.get(newUrl, timeout=5)

		newAndImprovedMenu = bs4.BeautifulSoup(newLink.text, features="html.parser")

		food = newAndImprovedMenu.find_all('ul', class_=None, id=None)
		categories = newAndImprovedMenu.find_all('h4')

		i = 1
		while i < len(categories):
			for f in food:
				msg += ("\n" + str(categories[i].text) + ":\n")
				for foods in f.find_all('li'):
					msg += str(foods.text) + '\n'
				i += 1

		msg += '\n--------------------------------------------\n\n'
	return msg

output = funTimes()
fromaddr = '' #redacted for security
toaddrs  = ''
username = ''
password = ''
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, output)
server.quit()
