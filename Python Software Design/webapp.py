from datasource import*
import flask
from flask import render_template
from flask import request
import json
import sys
import os

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

'''
Renders the homepage when the user connects to http://perlman.mathcs.carleton.edu:5134/
'''
@app.route('/')
def renderHomepage():
    return render_template('Homepage.html')

'''
Renders the create page when the user directs to http://perlman.mathcs.carleton.edu:5134/create/
'''
@app.route('/create/')
def renderCreatePage():
    return render_template('Create.html')

@app.route('/analyze/')
def renderAnalyzePage():
    return render_template('Analyze.html')

@app.route('/aboutpage/')
def renderAboutPage():
    return render_template('AboutPage.html')

@app.route('/explore/')
def renderExplorePage():
    return render_template('Explore.html')
'''
Renders the analyze page when the user directs to http://perlman.mathcs.carleton.edu:5134/create/
**THIS HTML PAGE IS NOT RELEVANT TO THE SPECIFIC USER QUERY FOR THIS DELIVERABLE**
**DO NOT GRADE**
'''

@app.route('/countgraph/', methods=['GET', 'POST'])
def displayCountsGraph():
    comparecounts = request.form['comparecounts']
    ds = DataSource()
    connection = ds.connect()
    ds.countProjectsGraph(connection, comparecounts)

    return render_template('Image.html')

@app.route('/proportiongraph/', methods=['GET', 'POST'])
def displayProportionGraph():
    compareproportion = request.form['compareproportion']
    ds = DataSource()
    connection = ds.connect()
    ds.proportionProjectsGraph(connection, compareproportion)

    return render_template('Image.html')

@app.route('/averagesgraph/', methods=['GET', 'POST'])
def displayAveragesGraph():
    filter = request.form['filter']
    averagecompare = request.form['averagecompare']
    ds = DataSource()
    connection = ds.connect()
    ds.averagedVariableGraph(connection, averagecompare, filter)
    return render_template('Image.html')


'''
Renders the results page when the user is directed to http://perlman.mathcs.carleton.edu:5134/results/
Assigns variables 'category', 'currency', and 'goal' to their corresponding form submissions using 'request' from flask
Creates a datasource object and calculates the probabilityOfSuccess based of the given variables
'Results.html' is rendered using the form submissions and the probabilityOfSuccess variable
'''
@app.route('/results/', methods=['GET', 'POST'])
def displayProbabilityOfSuccess():
    category = request.form['category']
    currency = request.form['currency']
    goal = request.form['goal']
    if goal == '0' or goal == '' or goal == None:
        goal = 1
    ds = DataSource()
    #note: connection is not passed because this function can be ran independently of the database
    probabilityOfSuccess = ds.calculateProbabilityOfSuccess(category, currency, goal)
    return render_template('Results.html', category = category, currency = currency, goal = goal, probabilityOfSuccess = probabilityOfSuccess)


'''
Renders the various sites associated with explore in the same sort of function
style as the results page above
'''

@app.route('/explore/random/', methods=['GET', 'POST'])
def renderRandomPage():
    ds = DataSource()
    connection = ds.connect()
    name = ds.getRandomProject(connection)
    return render_template('Random.html', name = name)

@app.route('/explore/minmax/', methods=['GET', 'POST'])
def renderMinmaxPage():
    category = request.form['category']
    ds = DataSource()
    connection = ds.connect()
    minProj, minimum = ds.getMinimumValueOfVariable(connection, category)
    maxProj, maximum = ds.getMaximumValueOfVariable(connection, category)
    return render_template('Minmax.html', minProj = minProj, maxProj = maxProj, minimum = minimum, maximum = maximum, category = category)

@app.route('/explore/topten/', methods=['GET', 'POST'])
def renderToptenPage():
    category = request.form['category']
    ds = DataSource()
    connection = ds.connect()
    topTen = ds.mostSuccessfulProjects(connection, category)
    topList = ""
    for i in range(10):
        topList = topList + str(i + 1) + ". "
        topList = topList + "Name: " + topTen[i][0] + " "
        topList = topList + "Backers: " + str(int(topTen[i][1])) + " "
        topList = topList + "Goal: $" + str(int(topTen[i][2])) + " "
        topList = topList + "Pledged $" + str(int(topTen[i][3])) + "\r\n" + "        "
    return render_template('Topten.html', category = category, topList = topList)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
