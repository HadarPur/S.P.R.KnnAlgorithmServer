import math
import json
import csv
import operator
from flask import Response, jsonify
from enum import Enum

fieldnames = ["AGE", "GENDER", "SECTOR", "SEX", "LATITUDE", "LONGITUDE"]
k_value = 3
fileName = "persons.csv"
numOfFeathers = 6


# firebase = firebase.FirebaseApplication('https://sprfinalproject.firebaseio.com',None)
# result = firebase.get('/Available Agents',None)
# print('Result from firebase call: /Available Agent -> ',result)


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


synthetic_data = [
    [
        '17', 'STRAIGHT', 'CHRISTIAN', 'MALE', '32.184448', '34.870766', None
    ],
    [
        '8', 'STRAIGHT', 'JEWISH', 'FEMALE', '31.801447', '34.643497', None
    ],
    [
        '16', 'UNDECIDED', 'UNDECIDED', 'MALE', '32.109333', '34.855499', None
    ],
    [
        '14', 'STRAIGHT', 'JEWISH', 'MALE', '31.771959', '35.217018', None
    ],
    [
        '12', 'LESBIAN', 'JEWISH', 'FEMALE', '31.894756', '34.809322', None
    ],
    [
        '16', 'STRAIGHT', 'MUSLIM', 'FEMALE', '32.109333', '34.855499', None
    ],
    [
        '17', 'STRAIGHT', 'CHRISTIAN', 'MALE', '32.794044', '34.989571', None
    ],
    [
        '16', 'STRAIGHT', 'JEWISH', 'FEMALE', '32.017136', '34.745441', None
    ],
    [
        '15', 'BISEXUAL', 'JEWISH', 'MALE', '32.919945', '35.290146', None
    ],
    [
        '10', 'STRAIGHT', 'JEWISH', 'FEMALE', '32.166313', '34.843311', None
    ],
    [
        '11', 'HOMOSEXUAL', 'MUSLIM', 'MALE', '32.017136', '34.745441', None
    ],
    [
        '15', 'HOMOSEXUAL', 'JEWISH', 'MALE', '32.109333', '34.855499', None
    ],
    [
        '12', 'TRANSGENDER', 'UNDECIDED', 'MALE', '32.109333', '34.855499', None
    ],
    [
        '15', 'BISEXUAL', 'JEWISH', 'MALE', '31.771959', '35.217018', None
    ],
    [
        '13', 'STRAIGHT', 'CHRISTIAN', 'MALE', '31.801447', '34.643497', None
    ],
    [
        '29', 'STRAIGHT', 'CHRISTIAN', 'FEMALE', '31.771959', '35.217018', None
    ],
    [
        '35', 'STRAIGHT', 'JEWISH', 'FEMALE', '32.919945', '35.290146', None
    ],
    [
        '38', 'HOMOSEXUAL', 'JEWISH', 'FEMALE', '32.794044', '34.989571', None
    ],
    [
        '25', 'LESBIAN', 'JEWISH', 'FEMALE', '32.184448', '34.870766', None
    ],
    [
        '47', 'BISEXUAL', 'JEWISH', 'FEMALE', '32.017136', '34.745441', None
    ],
    [
        '30', 'HOMOSEXUAL', 'MUSLIM', 'FEMALE', '31.801447', '34.643497', None
    ],
    [
        '34', 'TRANSGENDER', 'UNDECIDED', 'MALE', '32.109333', '34.855499', None
    ]
]

test = [
    [
        '18', 'TRANSGENDER', 'JEWISH', 'MALE', '32.109333', '34.855499'
    ],
    [
        '12', 'STRAIGHT', 'JEWISH', 'FEMALE', '31.771959', '35.217018'
    ],
    [
        '16', 'HOMOSEXUAL', 'MUSLIM', 'MALE', '32.794044', '34.989571'
    ]
]


def write_data_to_csv(file_name, data):
    # Writing the data into VCS file
    csv_file = open(file_name, 'w', newline='')
    obj = csv.writer(csv_file)
    for person in data:
        obj.writerow(person)
    csv_file.close()


def read_data_from_csv(file_name):
    # Reading data from VCS file
    csv_file = open(file_name, 'r', newline='')
    obj = csv.reader(csv_file)
    for row in obj:
        print(row)


def convert_row_to_numeric_values(row):
    new_converted_row = [None for _ in range(7)]
    for index, val in enumerate(row):
        if index == 0:
            new_converted_row[index] = int(val) * Weights[fieldnames[index]].value
        elif index == 1:
            new_converted_row[index] = int(Gender[val].value) * Weights[fieldnames[index]].value
        elif index == 2:
            new_converted_row[index] = int(Religion[val].value) * Weights[fieldnames[index]].value
        elif index == 3:
            new_converted_row[index] = int(Sex[val].value) * Weights[fieldnames[index]].value
        elif index == 4:
            new_converted_row[index] = float(val) * 100 * Weights[fieldnames[index]].value
        elif index == 5:
            new_converted_row[index] = float(val) * 100 * Weights[fieldnames[index]].value
        else:
            new_converted_row[index] = val

    return new_converted_row


# Other imlementation
def loadDataSet(data_list, training_set=[]):
    # Reading data from VCS file
    # csvfile = open(fileName, 'r', newline='')
    # lines = csv.reader(csvfile)
    for curIndex in range(len(data_list)):
        received_data = data_list[curIndex]
        agent_data = []
        agent_data.extend([received_data['age'],
                           received_data['gender'],
                           received_data['sector'],
                           received_data['sex'],
                           received_data['latitude'],
                           received_data['longitude'],
                           received_data['uid']])
        # print(trainingSet[curIndex], "Before convertion")
        training_set.append(convert_row_to_numeric_values(agent_data))
    # print(trainingSet[curIndex], "After Convertion")

    for ind in range(len(training_set)):
        print(training_set[ind])
    return training_set


def euclidean_distance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def get_neighbors(training_set, test_instance, k):
    distances = []
    length = len(test_instance) - 1
    for x in range(len(training_set)):
        dist = euclidean_distance(test_instance, training_set[x], length)
        distances.append((training_set[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def get_knn_response(neighbors):
    class_votes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in class_votes:
            class_votes[response] += 1
        else:
            class_votes[response] = 1

    values = list(class_votes.values())
    keys = list(class_votes.keys())

    return keys[values.index(max(values))]


# Used for to delimit offline agent from to be used as validate data in KNN algorithm
def is_list_contains_one_of_other_list(values_list, checked_list=[]):
    for cur_val_index in range(len(values_list)):
        if values_list[cur_val_index] in checked_list:
            return True

    return False


# Main
def knn_service(request):
    received_data = request.get_json()
    user_data = []
    user_data.extend([received_data['age'],
                      received_data['gender'],
                      received_data['sector'],
                      received_data['sex'],
                      received_data['latitude'],
                      received_data['longitude']])
    online_agents_list = received_data['onlineAgents']

    # PACE 1
    training_set = loadDataSet(online_agents_list, training_set=[])

    # PACE 2
    training_set = creation_of_points_in_space(training_set)

    test_row = convert_row_to_numeric_values(user_data)
    neighbors = get_neighbors(training_set, test_row, k_value)

    response_dict = {}
    response_dict['agent_uid'] = get_knn_response(neighbors)
    print(response_dict['agent_uid'])
    return jsonify(response_dict)


def creation_of_points_in_space(training_set):
    for cur_data_index in range(len(synthetic_data)):
        # For each synthetic data: activate Knn and obtain result
        cur_convert_data = convert_row_to_numeric_values(synthetic_data[cur_data_index])
        neighbors = get_neighbors(training_set, cur_convert_data, 1)
        cur_result = get_knn_response(neighbors)

        # put the result in last index of converted data list
        cur_convert_data.append(cur_result)

        # Append the current complete data in the training list
        training_set.append(cur_convert_data)

    return training_set




