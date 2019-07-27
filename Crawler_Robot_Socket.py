'''
This program is Usefull For Digital Marketers and SEO C
THis program checks if robots.txt exists on a website and then fetches allow and disallow details which re then stored in a CSV file

'''

#Importing re for regular expressions
import re
#importing urllib libraries
import urllib.request, urllib.parse, urllib.error
#csv library was not used 
import csv

#creating lists to store all allowed and disallowed directories for each agent
list_allow = list()
list_disallow = list()
#below is a list used to store lengths of values of each agent(key), which is in for loop later
list_max = list()
#Dictionaries created to store each agent and their respective allowed or disallowed directories
#if nothing is present in any of those, 'NA' is typed
dict_disallow = dict()
dict_allow = dict()

#This string variable will hold the name of agent, from the list returned by findall()
User_agent_string= ''

#This will ask for url from user
Url = input('Kindly enter the Url:\n')
#User entered Url will be appended with robots.txt tp generate the url of robots file
RobotUrl = Url + '/robots.txt'
#Robot url is printed on the screen for transparency 
print(RobotUrl)

#urlopen() is used to open the url to robots.txt and its kept in try catch block
#if robots.txt file is not present it will throw and error
try:
	#urlopen() is similar to file open() which opens a handler to the file 
	fhandle = urllib.request.urlopen(RobotUrl)

except:
	#Text that wil be displayed if no file found
	print("The above URL has no robots.txt file\n")
	
#below hashed line is to read from system file
#fhandle = open('D:/Python/sample.txt', 'r')
print(fhandle)
#This will write to an exisitig file or open a new file at given path
newfile = open('D:/Python/3rd/Robot.csv', 'w+')


#for loop to loop through each line in the file handler
for line in fhandle:
	#each line is decoded and stripped to remove any whitespaces
	line = line.decode().strip()
	
	#condition to ignore a line if starts with # which means if the line is commented it is ignored 
	if re.search('^#', line):
		pass
	#This will check if line starts with User-agent:
	elif re.search('^User-agent:', line):
		#this will produce a list of text after 'User-agent: ''
		agent_name = re.findall('^User-agent: (\S+)', line) 
		
		#this will fetch string from the list
		User_agent_string = agent_name[0]

		#Loop to check next lines and seek for disallow and allow options
		while True:
			#next method will take the control to next line in the filehandle
			#this will return '' if end of fie reached
			next_line = next(fhandle,'')

			#kept the decoding of next line in try as got error, where the message wasnt encoded
			try:
				next_line = next_line.decode()
			except:
				pass

			#if the next line starts with 'Disallow: ',
			if re.search('^Disallow:', next_line):
				#This will fetche everythig after 'Disallow: '
				disallow = re.findall('^Disallow: ([\S]+)',next_line)
				#If the text is received, it is appended in a list

				if len(disallow)>0:
					x = disallow[0]
					list_disallow.append(x)
				

			#if the next line starts with 'Allow: ',
			elif re.search('^Allow:', next_line):
				#This will fetche everythig after 'Allow: '
				allow = re.findall('^Allow: ([\S]+)',next_line)
				#If the text is received, it is appended in a list
				if len(allow)>0:
					x = allow[0]
					list_allow.append(x)	

			#if next line starts with neither Allow or Disallow, it will break the loop
			else :
				break

		#If the User name is not blank
		if User_agent_string != '':
			#print(len(list_disallow))
			#name of the user-agent is added in dictionary of allow as key and list of allowed directories is added as value
			dict_disallow[User_agent_string]= dict_disallow.get(User_agent_string, []) + list_disallow
			#The list is cleared to be used for next agent
			list_disallow = []
			#name of the user-agent is added in dictionary of disallow as key and list of disallowed directories is added as value
			dict_allow[User_agent_string]= dict_allow.get(User_agent_string, []) + list_allow
			#The list is cleared to be used for next agent
			#print(User_agent_string,dict_disallow[User_agent_string])
			list_allow = []
			
			
	
#Column names added to the file
newfile.write('Agent,Allow,Disallow\n')

#Loop that goes through all the key's (User Agents) from allow dictionary
#You can use any of the two dictionaries allow or disallow as simultaneously both the dictionaries are updated with either a value or 'NA'
#Thus length of both ditionaries are same

for agent in dict_allow:
	
	#lengths of both the lists in values of each key(agent)
	list_max.append(len(dict_allow[agent]))
	list_max.append(len(dict_disallow[agent]))
	#maximun length is used for the loop
	y = max(list_max)
	print(agent,list_max)

	#maximun length is used for the loop
	if y >=1:
		#iterater variable defined
		loop_count = 0
		#loop iterates till it is less than the maximum length
		while loop_count < y:
			
			#if there is a list of allow for that agent it is stored in a variable, else 'NA' is stored
			try :
				a = dict_allow[agent][loop_count]
			except:
				a = 'NA'

			#if there is a list of disallow for that agent it is stored in a variable, else 'NA' is stored
			try : 
				b = dict_disallow[agent][loop_count]
			except:
				b = 'NA'

			#in the csv agents name, disallow directory from the list and disallow directory from the list is entered untill the maximum list iterator
			#\n is used to take the pointer to new line
			newfile.write(f'{agent},{a},{b}\n')
			
			#loop increment
			loop_count += 1	
	#list is cleare for using it for next agent
	list_max = []

#printed both dictionaries for reference
print(dict_allow)
print(dict_disallow)

#Created by Tejas Shinde Date :27-07-2019