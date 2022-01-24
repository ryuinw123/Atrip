def makeList_Of_DistanceBetweenPointToPoint_From_DictFromGooglemapsAPI(dictFromGooglemapsAPI):
    dataOut = list()
    for i in range(len(dictFromGooglemapsAPI["rows"])):
        counters = 0
        for j in dictFromGooglemapsAPI["rows"][i]["elements"]:
            if i != counters:
                dataOut.append(float((j["distance"]["text"].strip(" km")).strip(",").replace(',', '')))
            counters += 1
    return dataOut

def makeList_Of_DurationBetweenPointToPoint_From_DictFromGooglemapsAPI(dictFromGooglemapsAPI):
    dataOut = list()
    for i in range(len(dictFromGooglemapsAPI["rows"])):
        counters = 0
        for j in dictFromGooglemapsAPI["rows"][i]["elements"]:
            if i != counters:
                dataOut.append(j["duration"]["text"])
            counters += 1
    return dataOut

def makeList_Of_ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_From_ListOfKeyOfSelectedPlace(listOfKeyOfSelectedPlace):
    data = list()
    for i in listOfKeyOfSelectedPlace:
        for j in listOfKeyOfSelectedPlace:
            listOfKeyOfPointToKeyOfPoint = list()
            if(j is not i):
                listOfKeyOfPointToKeyOfPoint.append(i)
                listOfKeyOfPointToKeyOfPoint.append(j)
                data.append(listOfKeyOfPointToKeyOfPoint)
    return data

def makeList_of_ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_And_DurationBetweenPointToPoint(ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint, DistanceBetweenPointToPoint, DurationBetweenPointToPoint):
    data = list()
    for i in range(len(ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint)):
        temp = list()
        temp.append(ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint[i])
        temp.append(DistanceBetweenPointToPoint[i])
        temp.append(DurationBetweenPointToPoint[i])
        data.append(temp)
    return data

def makeList_Of_ListOf_AllListOfRoute_ListofDistance_ListofDuration_And_SumOfDistance(numberOfSelectedPlace, ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_And_DistanceBetweenPointToPoint, path, distance, duration, data, currentPoint = None):
    if currentPoint is None:
        for i in ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_And_DistanceBetweenPointToPoint:
            path.append(i[0][0])
            distance.append(i[1])
            duration.append(i[2])
            nextPoint = i[0][1]
            makeList_Of_ListOf_AllListOfRoute_ListofDistance_ListofDuration_And_SumOfDistance(numberOfSelectedPlace,ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_And_DistanceBetweenPointToPoint,path, distance, duration, data, nextPoint)
            path.pop()
            distance.pop()
            duration.pop()
        return data
    else:
        for i in ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_And_DistanceBetweenPointToPoint:
            if i[0][0] == currentPoint and path.count(i[0][1]) == 0:
                path.append(i[0][0])
                distance.append(i[1])
                duration.append(i[2])
                nextPoint = i[0][1]
                makeList_Of_ListOf_AllListOfRoute_ListofDistance_ListofDuration_And_SumOfDistance(numberOfSelectedPlace,ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_And_DistanceBetweenPointToPoint,path, distance, duration, data, nextPoint)
                if len(path) == numberOfSelectedPlace-1:
                    listPath = list()
                    listDistance = list()
                    listDuration = list()
                    sumOfDistance = 0.
                    path.append(nextPoint)
                    for j in path:
                        listPath.append(j)
                    for j in distance:
                        listDistance.append(j)
                        sumOfDistance += j
                    for j in duration:
                        listDuration.append(j)
                    data.append([listPath,listDistance,listDuration,round(sumOfDistance,2)])
                    path.pop()
                path.pop()
                distance.pop()
                duration.pop()


def allResults(listOfKeyOfSelectedPlace, dictFromGooglemapsAPI):
    temp = makeList_of_ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_And_DurationBetweenPointToPoint(makeList_Of_ListOfAllOutcomeBetweenKeyOfPointToKeyOfPoint_From_ListOfKeyOfSelectedPlace(listOfKeyOfSelectedPlace), makeList_Of_DistanceBetweenPointToPoint_From_DictFromGooglemapsAPI(dictFromGooglemapsAPI), makeList_Of_DurationBetweenPointToPoint_From_DictFromGooglemapsAPI(dictFromGooglemapsAPI))
    return makeList_Of_ListOf_AllListOfRoute_ListofDistance_ListofDuration_And_SumOfDistance(len(listOfKeyOfSelectedPlace),temp,list(), list() ,list(), list())

def sortResult(result): 
    for _ in range(len(result)):
        for i in range(len(result)-1):
            if result[i][3] > result[i+1][3]:
                result[i], result[i+1] = result[i+1], result[i]
    return result
            
