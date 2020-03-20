import psycopg2
import getpass
import math
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import os

'''
AMY
Some of these implementations are works in progress, so please grade
getNumberOfProjects
getRandomProject
getMinimumValueOfVariable
'''

class DataSource:
	'''
	DataSource executes all of the queries on the database.
	It also formats the data to send back to the frontend, typically in a list
	or some other collection or object.
	'''

	def __init__(self):
		#self.user = 'nystromk'
		#self.password = 'java692spam'
		self.user = 'santosb'
		self.password = 'book347winter'
		#self.user = 'loye'
		#self.password = 'tablet984spring'

	def connect(self):
		'''
		Establishes a connection to the database with the following credentials:

		PARAMETERS:
			user - username, which is also the name of the database
			password - the password for this database on perlman

		RETURNS: a database connection.

		Note: exits if a connection cannot be established.
		Note: Code written by Amy Csizmar Dalal
		'''
		try:
			connection = psycopg2.connect(database=self.user, user=self.user, password= self.password)
		except Exception as e:
			print("Connection error: ", e)
			exit()
		return connection

	def getNumberOfProjects(self, connection):
		'''
		Gives the total number of projects(entries) in the data table. This is done to avoid having a 'magic number'

		PARAMETERS:
			connection - the connection to the database

		RETURNS:
			an int that is the total number of entries in the datatable.
		'''
		try:
			cursor = connection.cursor()
			query = "SELECT COUNT(ID) FROM ksdata"
			cursor.execute(query)
			numberOfProjects = int(cursor.fetchall()[0][0])
			return numberOfProjects

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()

	def getRandomProject(self, connection):
		'''
        All the information of a random project in list form from the Kickstarter dataset

        PARAMETERS:
            connection - the connection to the database

        RETURNS:
            list of variables for the random project
        '''

		try:
			cursor = connection.cursor()
			query = "SELECT title FROM ksdata ORDER BY RANDOM() LIMIT 1"
			cursor.execute(query)
			return cursor.fetchall()[0][0]

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()


	def getCountOfVariableSuccess(self, connection, nameOfVariable, variableCondition):
		'''
        Returns the count (an integer) of all projects of one variable that meet a certain condition AND were successful.

        PARAMETERS:
			connection - the connection to the database
            nameOfVariable - the variable of the project we are counting from.
	    	variableCondition - the condition that needs to be met for the project to be counted.
	    	For example, if the nameOfVariable is 'country', a variableCondition could be 'US' or 'GB'

        RETURN:
            an integer that is a total of all the projects in the database that fit these two variables AND is successful (the count of successful Film & Video Projects)
		'''
		try:
			cursor = connection.cursor()
			query = "SELECT COUNT(state) FROM ksdata WHERE state = 'successful' AND " + str(nameOfVariable) + " = '" + str(variableCondition) + "'"
			cursor.execute(query)
			count = int(cursor.fetchall()[0][0])
			return count

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getCountOfVariableFailure(self, connection, nameOfVariable, variableCondition):
		'''
        Gets the count (an integer) of all projects of one variable that meet a certain condition AND were successful.

        PARAMETERS:
        	connection - the connection to the database
        	nameOfVariable - the variable of the project we are counting from.
        	variableCondition - the condition that needs to be met for the project to be counted.
        	For example, if the nameOfVariable is 'country', a variableCondition could be 'US' or 'GB'

        RETURN:
        	an integer that is a total of all the projects in the database that fit these two variables AND is successful (the count of successful Film & Video Projects)
        '''
		try:
			cursor = connection.cursor()
			query = "SELECT COUNT(state) FROM ksdata WHERE state = 'failed' AND " + str(nameOfVariable) + " = '" + str(variableCondition) + "'"
			cursor.execute(query)
			count = int(cursor.fetchall()[0][0])
			return count

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None


	def getMinimumValueOfVariable(self, connection, nameOfVariable):
		'''
		Returns the smallest value (a float) in the dataset for a given variable (filter)

		PARAMETERS:
			connection - the connection to the database
			nameOfVariable - the major variable from which the minimum value is being taken
			For example, nameOfVariable could be 'usd_goal'

		RETURN:
			a float that is the smallest value in the dataset for the variable provided
		'''

		try:
			cursor = connection.cursor()
			query = "SELECT Title FROM ksdata WHERE Main_Category = '" + str(nameOfVariable) + "' ORDER BY usd_pledged_real ASC LIMIT 1"
			cursor.execute(query)
			smallestName = cursor.fetchall()[0][0]
			query = "SELECT usd_pledged_real FROM ksdata WHERE Main_Category = '" + str(nameOfVariable) + "' ORDER BY usd_pledged_real ASC LIMIT 1"
			cursor.execute(query)
			smallestValue = int(cursor.fetchall()[0][0])
			return smallestName, smallestValue

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getMaximumValueOfVariable(self, connection, nameOfVariable):
		'''
		Returns the largest value (a float) in the dataset for a given variable (filter)

		PARAMETERS:
			connection - the connection to the database
			nameOfVariable - the major variable from which the maximum value is being taken
			For example, nameOfVariable could be 'currency'

		RETURN:
			a float that is the largest value in the dataset for the variable provided
		'''

		try:
			cursor = connection.cursor()
			query = "SELECT Title FROM ksdata WHERE Main_Category = '" + str(nameOfVariable) + "' AND usd_pledged_real IS NOT NULL ORDER BY usd_pledged_real DESC LIMIT 1"
			cursor.execute(query)
			largestName = cursor.fetchall()[0][0]
			query = "SELECT usd_pledged_real FROM ksdata WHERE Main_Category = '" + str(nameOfVariable) + "' AND usd_pledged_real IS NOT NULL ORDER BY usd_pledged_real DESC LIMIT 1"
			cursor.execute(query)
			largestValue = int(cursor.fetchall()[0][0])
			return largestName, largestValue

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getAverageOfVariable(self, connection, nameOfVariable):
		'''
        Returns an average of all the entries for one variable in the data set.

        PARAMETERS:
			connection - the connection to the database
			nameOfVariable - the name of the variable we wish to calculate the average of.
			For example, nameOfVariable could be 'backers'


        RETURN:
            an integer that is the average of the provided parameter

		RAISES:
			NeedQuantitaveVariableError - If parameter entered is a categorical variable
		'''
		try:
			cursor = connection.cursor()
			query = "SELECT AVG(" + str(nameOfVariable) + ") FROM ksdata"
			cursor.execute(query)
			averageValue = float(cursor.fetchall()[0][0])
			return averageValue

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getAverageOfConditionedVariable(self, connection, averagedVariable, nameOfVariable, variableCondition):
		'''
        Returns an average of all the entries for one variable conditioned on another in the data set.

        PARAMETERS:
        	connection - the connection to the database
        	averagedVariable - the type of variable that is being average
        	nameOfVariable - the name of the variable we wish to calculate the average of
        	variableCondition - the condition that needs to be met to be included in the average
        	For example, averagedVariable is 'backers', nameOfVariable is 'country', and variableCondition is 'US'

        RETURN:
    		an integer that is the average of the provided parameters
        	For example, the average number of backers for all Kickstarters from the US
        '''
		try:
			cursor = connection.cursor()
			query = "SELECT AVG(" + str(averagedVariable) + ") FROM ksdata WHERE " +str(nameOfVariable) + " =  '" + str(variableCondition) + "'"
			cursor.execute(query)
			averageValue = float(cursor.fetchall()[0][0])
			return averageValue

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None


	def getProportionOfSuccess(self, connection, nameOfVariable, variableCondition):
		'''
        Calculates the proportion of successful projects based on the name of a column and the filter of that column.

        PARAMETERS:
            connection - the connection to the database
            nameOfVariable - the str variable of the project we are creating a proportion for
            variableCondition - a str attribute of the main variable (i.e category, country, currency)
            For example, nameOfVariable could be 'main_category' with the variableCondition being 'Arts'

        RETURNS:
            an int proportion between 0 and 1 inclusive
        '''
		try:
			cursor = connection.cursor()

			query = "SELECT COUNT(" + str(nameOfVariable) + ") FROM ksdata WHERE "  + str(nameOfVariable) + "= '" + str(variableCondition) +"'"
			cursor.execute(query)
			totalCount = float(float(cursor.fetchall()[0][0]))

			query = "SELECT COUNT(state) FROM ksdata WHERE state = 'successful' AND " + str(nameOfVariable) + "= '" + str(variableCondition) +"'"
			cursor.execute(query)
			successCount = float(cursor.fetchall()[0][0])

			proportionOfSuccess = successCount/totalCount
			return proportionOfSuccess

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()


	def mainCategoryCoefficient(self,nameOfVariable):
		'''
		Gets the coefficient associated with the probability of the given nameOfVariable
        PARAMETERS:
            connection - the connection to the database
            nameOfVariable - the str variable of the project we want a coefficient for
            Each if statement below contains the possibilities for nameOfVariable

        RETURNS:
            an int that depends on the category or -1 if the category does not exist in our dataset
		'''
		if str(nameOfVariable) == 'Arts':
			return 0
		elif str(nameOfVariable) == 'Comics':
			return 0.6494
		elif str(nameOfVariable) == 'Crafts':
			return -0.8739
		elif str(nameOfVariable) == 'Dance':
			return 0.9299
		elif str(nameOfVariable) == 'Design':
			return 0.2445
		elif str(nameOfVariable) == 'Fashion':
			return -0.5401
		elif str(nameOfVariable) == 'Film & Video':
			return 0.1279
		elif str(nameOfVariable) == 'Food':
			return -0.4783
		elif str(nameOfVariable) == 'Games':
			return 0.2531
		elif str(nameOfVariable) == 'Journalism':
			return -0.7870
		elif str(nameOfVariable) == 'Music':
			return 0.4117
		elif str(nameOfVariable) == 'Photography':
			return -0.3656
		elif str(nameOfVariable) == 'Publishing':
			return -0.3063
		elif str(nameOfVariable) == 'Technology':
			return -0.4427
		elif str(nameOfVariable) == 'Theater':
			return 0.8702
		else:
			return -1

	def currencyCoefficient(self, currency):
		'''
		Gets the coefficient associated with the probability of the given currency
		PARAMETERS:
		    connection - the connection to the database
		    currency - the str currency of the project we want a coefficient for
		    Each if statement below contains the possibilities for currency

		RETURNS:
		    an int that depends on the currency or -1 if the currency does not exist in our dataset
		'''
		if str(currency) == 'AUD':
			return 0
		elif str(currency) == 'CAD':
			return 0.0995
		elif str(currency) == 'CHF':
			return 0.2178
		elif str(currency) == 'DKK':
			return 0.3417
		elif str(currency) == 'EUR':
			return -0.0677
		elif str(currency) == 'GBP':
			return 0.3486
		elif str(currency) == 'HKD':
			return 0.7594
		elif str(currency) == 'JPY':
			return 0.1313
		elif str(currency) == 'MXN':
			return -0.3702
		elif str(currency) == 'NOK':
			return -0.1847
		elif str(currency) == 'NZD':
			return 0.1909
		elif str(currency) == 'SEK':
			return 0.1097
		elif str(currency) == 'SGD':
			return 0.4328
		elif str(currency) == 'USD':
			return 0.4391
		else:
			return -1


	def calculateProbabilityOfSuccess(self, nameOfVariable, currency, usd_goal):
		'''
        Returns the probability of success for a project given input values for the user's
        project idea. R software will be used to generate the formula

        PARAMETERS:


            str and int variables that are shown to be statistically significant to determining
            success of a project

        RETURN:
            a probability of success between 0 and 1 inclusive
        '''
		categoryCoefficient = self.mainCategoryCoefficient(nameOfVariable)
		currencyCoefficient = self.currencyCoefficient(currency)
		if categoryCoefficient != -1 and currencyCoefficient != -1:
			probabilityOfSuccess = 1.652 + categoryCoefficient + currencyCoefficient + (-0.2872) * math.log(float(usd_goal))
			if probabilityOfSuccess > 1:
				return '100%'
			elif probabilityOfSuccess < 0.01:
				return 'Less than 1%'
			else:
				return str(round(probabilityOfSuccess*100,2))+'%'
		else:
			return 'Please Enter a Valid Parameters'

	def getDistinctXVariables(self, connection, nameOfVariable):
		'''
		Creates a list of distinct elements to be placed on the x-axis of a graph given a variable

		PARAMETERS:
			connection - the connection to the database
			nameOfVariable - str of the variable for which we need the distinct elements
			For example, nameOfVariable is 'country' and some of the distinct elements include 'US' and 'GB'

		RETURNS:
			a list of distinct str element names
		'''

		try:
			cursor = connection.cursor()

			# Getting all the distinct variables
			# gets all the distnct x-values - for setting up x-axis
			xVariableQuery = "SELECT DISTINCT " + str(nameOfVariable) + " FROM ksdata"
			cursor.execute(xVariableQuery)

			# Creating a list of all the distinct variables to feed into plt function
			xVariables = []
			for i in cursor.fetchall():
				if nameOfVariable == "projectyear":
					int(i[0])
				xVariables.append(str(i[0]))

			xVariables.sort()
			return xVariables

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()


	#input a column name
	def countProjectsGraph(self, connection, nameOfVariable):
		'''
		Creates a bar plot graph and image of the graph. The function graphs the count of all projects of a given variable

		PARAMETERS:
			connection - the connection to the database
			nameOfVariable - str of variable for which we are counting distinct projects
			For example, nameOfVariable could be 'country' and the function would create a graph of the count
			for 'US', 'GB', 'JP', etc. and save it to the static directory

		RETURNS:
			nothing, simply saves the graph as a .png
		'''
		try:
			cursor = connection.cursor()
			fig = plt.figure()

			#Getting all the distinct variables
			#gets all the distnct x-values - for setting up x-axis
			#Creating a list of all the distinct variables to feed into plt function
			xVariables = self.getDistinctXVariables(connection, nameOfVariable)

			#Creating a list of the counts for each x value
			#Iterates through x variable list and gets the count, appends to a empty y list
			yVariables = []
			for i in xVariables:
				yVariableQuery = "SELECT COUNT(" + str(nameOfVariable) + ") FROM ksdata WHERE " + str(nameOfVariable) + " = '" + i +"'"
				cursor.execute(yVariableQuery)
				yVariables.append(cursor.fetchall()[0][0])

			#Creating the graph labels and the graph itself
			plt.title("Number of Projects for each " + str(nameOfVariable).capitalize())
			plt.xlabel(str(nameOfVariable).upper())
			plt.ylabel("COUNT")
			plt.bar(xVariables, yVariables, align='center')
			plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
			fig.tight_layout()

			#Saving the image in the same directory, there is no need to return anything
			strFile = "static/plot.svg"
			if os.path.isfile(strFile):
				os.remove(strFile)
			fig.savefig('static/plot.svg', format='svg')

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()

	#the average variable for a column - all colums displayed on x-axis
	def averagedVariableGraph(self, connection, averagedVariable, nameOfVariable):
		'''
		Creates a bar plot graph and image of the graph.
		The function graphs the average of a variable for all projects of a distinct instances of a variable

		PARAMETERS:
			connection - the connection to the database
			averagedVariable - the value that would be averaged for each distinct values from nameOfVariable
			nameOfVariable - str of variable for which we are counting distinct projects
			For example, averagedVariable is 'backers' and nameOfVariable is 'country'
			The function would create a graph of the average number of backers for 'US', 'GB', 'JP', etc. and save it to the static directory

		RETURNS:
			nothing, simply saves the graph as a .png
		'''
		#averagedVariagle= goal funding or Backers
		#name of variable = year, country, both categories, currency
		#for goal, funding, and backers
		try:
			cursor = connection.cursor()
			fig = plt.figure()

			xVariables = self.getDistinctXVariables(connection, nameOfVariable)


			yVariables = []
			for i in xVariables:
				average = self.getAverageOfConditionedVariable(connection, averagedVariable, nameOfVariable, i)
				roundAverage = round(average,0)
				yVariables.append(roundAverage)

			#Creating the graph labels and the graph itself
			plt.title("The Average Number of " + str(averagedVariable).capitalize() +  " for each " + str(nameOfVariable).capitalize())
			plt.xlabel(str(nameOfVariable).upper())
			plt.ylabel("COUNT")
			plt.bar(xVariables, yVariables, align='center')
			plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
			fig.tight_layout()

			# Saving the image in the same directory, there is no need to return anything
			strFile = "static/plot.svg"
			if os.path.isfile(strFile):
				os.remove(strFile)
			fig.savefig('static/plot.svg', format='svg')

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()

	def proportionProjectsGraph(self, connection, nameOfVariable):
		'''
		Creates a stacked bar plot graph and image of the graph.
		The function graphs the proportion of success and failures for distinct instances of a variable

		PARAMETERS:
			connection - the connection to the database
			nameOfVariable - str of variable for which we are getting success/failure proportions for each distinct projects
			For example, nameOfVariable is 'country'
			The function would stacked proportions of success to failures for 'US', 'GB', 'JP', etc. and save it to the static directory

		RETURNS:
			nothing, simply saves the graph as a .png
		'''
		try:
			cursor = connection.cursor()
			fig = plt.figure()

			xVariables = self.getDistinctXVariables(connection, nameOfVariable)

			ind = [x for x, _ in enumerate(xVariables)]

			successesList = []
			failuresList = []
			for i in xVariables:
				successesList.append(self.getCountOfVariableSuccess(connection, nameOfVariable, i))
				failuresList.append(self.getCountOfVariableFailure(connection, nameOfVariable, i))

			#make into array, add the two arrays together - has to be array for barplot
			successes= np.array(successesList)
			failures = np.array(failuresList)
			total = failures + successes

			proportion_failures = np.true_divide(failures, total) * 100
			proportion_successes = np.true_divide(successes, total) * 100

			plt.bar(ind, proportion_failures, width = 0.5, label = 'failures', color = '#e57373', bottom = proportion_successes)
			plt.bar(ind, proportion_successes, width = 0.5, label = 'successes', color = '#b2ebf2')

			# Creating the graph labels and the graph itself
			plt.title("Proportion of Project Success for each " + str(nameOfVariable).capitalize())
			plt.xticks(ind, xVariables)
			plt.xlabel(str(nameOfVariable).upper())
			plt.ylabel("PROPORTION")
			plt.setp(plt.gca().get_xticklabels(), rotation = 45, horizontalalignment = 'right')
			fig.tight_layout()

			#Creating a legend
			ax = plt.subplot(111)
			chartBox = ax.get_position()
			ax.set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.6, chartBox.height])
			ax.legend(loc='upper center', bbox_to_anchor=(1.3, 0.8), shadow=True, ncol=1)

			# Saving the image in the same directory, there is no need to return anything
			strFile = "static/plot.svg"
			if os.path.isfile(strFile):
				os.remove(strFile)
			fig.savefig('static/plot.svg', format='svg')

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()


	def mostSuccessfulProjects(self, connection, variableCondition):
		'''
        Returns a list of the given length of the 10 most successful projects by success score

        PARAMETERS:
        	connection - the connection to the database
			variableCondition - a str attribute of the main category (i.e Dance, Art, Theatre)

        RETURN:
            A list of the most successful projects
        '''
		try:
			cursor = connection.cursor()
			query = "SELECT Title, backers, usd_goal_real, usd_pledged_real  FROM ksdata WHERE state = 'successful' AND main_category = '" + str(variableCondition) + "' ORDER BY success_score DESC LIMIT 10"
			cursor.execute(query)
			return cursor.fetchall()

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()

	def getListOfAllProjectsOfOneCategory(self, connection, nameOfVariable, variableCondition):
		'''
        Returns a list of every project for a given category

        PARAMETERS:
        	connection - the connection to the database
            nameOfVariable - str of the chosen category in the dataset
            variableCondition - a str attribute of the main variable (i.e category, country, currency)

        RETURN:
            A list of each project for the user chosen category
        '''
		try:
			cursor = connection.cursor()
			query = "SELECT * FROM ksdata WHERE " + str(nameOfVariable) + " = '" + str(variableCondition) + "'"
			cursor.execute(query)
			return cursor.fetchall()

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return connection.cursor()

def main():
	ds = DataSource()
	connection = ds.connect()

	#ds.countProjectsGraph(connection, 'currency')
	#ds.proportionProjectsGraph(connection, 'currency')
	#ds.averagedVariableGraph(connection, 'backers', 'main_category')
	#ds.averagedVariableGraph(connection, 'usd_goal_real', 'main_category')

	#print(str(ds.calculateProbabilityOfSuccess('Fashion', 'USD', 10000)))
	#print(ds.getCountOfVariableFailure(connection, 'currency', 'JPY'))
	#print(str(ds.calculateProbabilityOfSuccess('Music', 'USD', 5)))
	#print(str(ds.calculateProbabilityOfSuccess('Dance', 'US', 500)))
	#print(str(ds.getListOfAllProjectsOfOneCategory(connection,'category','Printing')))
	#print("The total number of projects is:" + str(ds.getNumberOfProjects(connection)))
	#print("A random project is:" + str(ds.getRandomProject(connection)))
	#print("The minimum value of the 'backers' is:" + str(ds.getMinimumValueOfVariable(connection,'backers')))
	#print("The average days for a project is: " + str(ds.getAverageOfVariable(connection, 'total_days')))
	#print("The proportion of Music projects that were successful is: " + str(ds.getProportionOfSuccess(connection, 'main_category', 'Music')))


main()
