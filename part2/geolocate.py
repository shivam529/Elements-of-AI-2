import re

def read():
    path = "C:\\Files_for_programming\\tweets.train.clean.txt"
    file = open(path)
    cities_words = dict()
    cities = dict()
    while True:
        line = file.readline().split(',')
        message = list()
        city = ''
        if line != ['']:
            for m in range(0,len(line)):
                message.extend(line[m].split())
            message = [re.sub('[^a-zA-Z0-9]','',i) for i in message]
            message = [i.lower() for i in message if i != '']
            city = str(line[0] + ',_' + message[1].upper())
            message.pop(0)
            message.pop(0)
            message = list(set(message))
            if city not in cities:
                cities[city] = 1
            else:
                cities[city] += 1
            if city not in cities_words:
                cities_words[city] = [message] 
            else:
                cities_words[city].append(message)
        else:
            break
    file.close()
    return cities_words,cities

def probablity(cities_words,cities):
    probabilty_dict = dict()
    count = 0
    for x,y in cities_words.items():
        probabilty_dict[x] = dict()
        for tweet in y:            
            for word in tweet:
                if word not in probabilty_dict[x]:                    
                    probabilty_dict[x][word] = 1/cities[x]
                else:
                    probabilty_dict[x][word] += (1/cities[x])
    return probabilty_dict
            
def read_test(liklyness,cities):
    path = "C:\\Files_for_programming\\tweets.test1.clean.txt"
    file = open(path)
    output = open("C:\\Files_for_programming\\output.txt","w+")
    while True:
        l = file.readline()
        line = l.split(',')
        message = list()
        if line != ['']:
            for m in range(0,len(line)):
                message.extend(line[m].split())
            message = [re.sub('[^a-zA-Z0-9]','',i) for i in message]
            message = [i.lower() for i in message if i != '']
            message.pop(0)
            message.pop(0)
            city = ''
            Posterior_Probability = 0            
            for x,y in liklyness.items():
                temp_posterior_probability = cities[x]
                for word in message:
                    if word in y:
                        temp_posterior_probability = temp_posterior_probability * y[word]
                if temp_posterior_probability > Posterior_Probability:
                    Posterior_Probability = temp_posterior_probability
                    city = x
            output.write(city+ ',' +l)
        else:
            break
    output.close()    
    file.close()

def accuracy():
    file = open("C:\\Files_for_programming\\output.txt")
    count = 0
    while True:
        line = file.readline().split(',')
        message = list()
        if line != ['']:
            if line[0] == line[2]:
                count += 1
        else:
            break    
    file.close()
    return (count/5)


cities_and_tweets,cities_dict = read()
for x,y in cities_dict.items():
    cities_dict[x] = cities_dict[x]/32000
likelihood = probablity(cities_and_tweets,cities_dict)
read_test(likelihood,cities_dict)
print(accuracy())