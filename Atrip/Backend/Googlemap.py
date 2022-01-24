import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCIHRdrSY885ctMMj_cvL-Ga69IktvnLs0')
origin = ['13.784158268087618,100.69431020698494','13.790968676528362, 100.69826503024926']
destination = ['13.784601838188108, 100.68815131749156','14.477319926342046, 100.09586506885088']
my_dist = gmaps.distance_matrix(origin,destination,mode='driving')

class Coldiness:
    def init(self, lat, lon):
        self.lat = lat
        self.lon = lon

place = []

def test(placeList):
    origin = []
    dest = []
    for i in placeList:
        for _ in range(1,len(placeList)):
            origin.append(i)
            #print(i)
        for j in placeList:
            if(j is not i):
                dest.append(j)
                #print(i)
    return origin, dest


place.append("A")
place.append("B")
place.append("C")
place.append("D")
place.append("E")

print(test(place))


print(my_dist)
