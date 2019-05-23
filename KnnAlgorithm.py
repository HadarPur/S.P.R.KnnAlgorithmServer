import math
import json
import csv
import operator
from flask import Response, jsonify
from enum import Enum

fieldnames = ['AGE', 'GENDER', 'SECTOR', 'SEX', 'LATITUDE', 'LONGITUDE']
k = 3
fileName = 'persons.csv'
numOfFeathers = 6


class Weights(Enum):
    AGE = 10
    GENDER = 70
    SECTOR = 40
    SEX = 100
    LATITUDE = 100
    LONGITUDE = 100


class Religion(Enum):
    JEWISH = 1
    MUSLIM = 2
    CHRISTIAN = 3
    UNDECIDED = 4


class Sex(Enum):
    MALE = 1
    FEMALE = 2


class Gender(Enum):
    STRAIGHT = 1
    LESBIAN = 2
    HOMOSEXUAL = 3
    BISEXUAL = 4
    TRANSGENDER = 5
    UNDECIDED = 6


data = [
    [  ##4
        '17', 'STRAIGHT', 'CHRISTIAN', 'MALE', '32.184448', '34.870766', 'agent id 4'  # Ra'anana, Israel
    ],
    [  ##1
        '8', 'STRAIGHT', 'JEWISH', 'FEMALE', '31.801447', '34.643497', 'agent id 1'  # Ashdod
    ],
    [  ##5
        '16', 'UNDECIDED', 'UNDECIDED', 'MALE', '32.109333', '34.855499', 'agent id 5'  # TEL-AVIV
    ],
    [  ##2
        '14', 'STRAIGHT', 'JEWISH', 'MALE', '31.771959', '35.217018', 'agent id 2'  # Jerusalem
    ],
    [  ##4
        '12', 'LESBIAN', 'JEWISH', 'FEMALE', '31.894756', '34.809322', 'agent id 4'  # REHOVOT
    ],
    [  ##4
        '16', 'STRAIGHT', 'MUSLIM', 'FEMALE', '32.109333', '34.855499', 'agent id 4'  # TEL-AVIV
    ],
    [  ##3
        '17', 'STRAIGHT', 'CHRISTIAN', 'MALE', '32.794044', '34.989571', 'agent id 3'  # HAIFA
    ],
    [  ##5
        '16', 'STRAIGHT', 'JEWISH', 'FEMALE', '32.017136', '34.745441', 'agent id 5'  # Bat Yam
    ],
    [  ##2
        '15', 'BISEXUAL', 'JEWISH', 'MALE', '32.919945', '35.290146', 'agent id 2'  # Karmiel
    ],
    [  ##5
        '10', 'STRAIGHT', 'JEWISH', 'FEMALE', '32.166313', '34.843311', 'agent id 5'  # Herzilya
    ],
    [  ##6
        '11', 'HOMOSEXUAL', 'MUSLIM', 'MALE', '32.017136', '34.745441', 'agent id 6'  # Bat Yam
    ],
    [  ##6
        '15', 'HOMOSEXUAL', 'JEWISH', 'MALE', '32.109333', '34.855499', 'agent id 6'  # TEL-AVIV
    ],
    [  ##7
        '12', 'TRANSGENDER', 'UNDECIDED', 'MALE', '32.109333', '34.855499', 'agent id 7'  # TEL-AVIV
    ],
    [  ##3
        '15', 'BISEXUAL', 'JEWISH', 'MALE', '31.771959', '35.217018', 'agent id 3'  # Jerusalem
    ],
    [  ##6
        '13', 'STRAIGHT', 'CHRISTIAN', 'MALE', '31.801447', '34.643497', 'agent id 6'  # Ashdod
    ],
    [  # 1
        '29', 'STRAIGHT', 'CHRISTIAN', 'FEMALE', '31.771959', '35.217018', 'agent id 1'  # Jerusalem
    ],
    [  # 2
        '35', 'STRAIGHT', 'JEWISH', 'FEMALE', '32.919945', '35.290146', 'agent id 2'  # Karmiel
    ],
    [  # 3
        '38', 'HOMOSEXUAL', 'JEWISH', 'FEMALE', '32.794044', '34.989571', 'agent id 3'  # HAIFA
    ],
    [  # 4
        '25', 'LESBIAN', 'JEWISH', 'FEMALE', '32.184448', '34.870766', 'agent id 4'  # Ra'anana, Israel
    ],
    [  # 5
        '47', 'BISEXUAL', 'JEWISH', 'FEMALE', '32.017136', '34.745441', 'agent id 5'  # Bat Yam
    ],
    [  # 6
        '30', 'HOMOSEXUAL', 'MUSLIM', 'FEMALE', '31.801447', '34.643497', 'agent id 6'  # Ashdod
    ],
    [  # 7
        '34', 'TRANSGENDER', 'UNDECIDED', 'MALE', '32.109333', '34.855499', 'agent id 7'  # TEL-AVIV
    ]
]
test = [
    [
        '18', 'TRANSGENDER', 'JEWISH', 'MALE', '32.109333', '34.855499'  # TEL-AVIV
    ],
    [
        '12', 'STRAIGHT', 'JEWISH', 'FEMALE', '31.771959', '35.217018'  # Jerusalem
    ],
    [
        '16', 'HOMOSEXUAL', 'MUSLIM', 'MALE', '32.794044', '34.989571'  # HAIFA
    ]
]


def writeDataToCsv(fileName, data):
    # Writing the data into VCS file
    csvfile = open(fileName, 'w', newline='')
    obj = csv.writer(csvfile)
    for person in data:
        obj.writerow(person)
    csvfile.close()


def readDataFromCsv(fileName):
    # Reading data from VCS file
    csvfile = open(fileName, 'r', newline='')
    obj = csv.reader(csvfile)
    for row in obj:
        print(row)


def convertRowToNumericValues(row):
    for indx, val in enumerate(row):
        if (indx == 0):
            row[indx] = float(val) * (Weights[fieldnames[indx]].value)
        elif (indx == 1):
            row[indx] = int(Gender[val].value) * (Weights[fieldnames[indx]].value)
        elif (indx == 2):
            row[indx] = int(Religion[val].value) * (Weights[fieldnames[indx]].value)
        elif (indx == 3):
            row[indx] = int(Sex[val].value) * (Weights[fieldnames[indx]].value)
        elif (indx == 4):
            row[indx] = float(val) * 100 * (Weights[fieldnames[indx]].value)
        elif (indx == 5):
            row[indx] = float(val) * 100 * (Weights[fieldnames[indx]].value)
        else:
            row[indx] = val

    return row


def loadDataSet(trainingSet=[]):
    # Reading data from VCS file
    # csvfile = open(fileName, 'r', newline='')
    # lines = csv.reader(csvfile)
    trainingSet = data
    for curIndex in range(len(trainingSet)):
        # print(trainingSet[curIndex], "Before convertion")
        trainingSet[curIndex] = convertRowToNumericValues(trainingSet[curIndex])
        # print(trainingSet[curIndex], "After Convertion")
    return trainingSet


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        respone = neighbors[x][-1]
        if (respone in classVotes):
            classVotes[respone] += 1
        else:
            classVotes[respone] = 1

    values = list(classVotes.values())
    keys = list(classVotes.keys())

    return keys[values.index(max(values))]


def knn_service(request):
    received_data = request.get_json()
    userData = received_data['data']

    trainingSet = loadDataSet(trainingSet=[])
    testRow = convertRowToNumericValues(userData)
    neighbors = getNeighbors(trainingSet, testRow, k)

    response_dict = {}
    response_dict['agent_uid'] = getResponse(neighbors)
    return Response(jsonify(response_dict))

# Respone.body.string -> make Json

