#!/usr/bin/env python3
# Geolocate program for tweet classification

import re, sys
from queue import PriorityQueue

# Stop words list obtained from Google
stop_words = ['','ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

# Function to read the training file
# Here we are reading the training file, line by line and storing the distinct city names in 
# cities dictionary.
# While storing the city names in cities dictionary we are also counting the number of tweets for 
# that particular city and storing that number as value in the same dictionary.
# cities = {'City1 name':count of tweets for city1, 'City2 Name': count of tweets for city2......}
# The cities_words dictionary is used to store city names as keys, and the values here are a list of lists
# Each sub-list is a tweet with each word as individual string.
# cities_words = {'City1 name':[[words in tweet1 for city1],[words in tweet2 for city1],...], 'City2 name':[[words in tweet1 for city2],[words in tweet2 for city2],....]}
def read(path):
    file = open(path)
    cities_words = dict()
    cities = dict()
    count_tweets = 0
    while True:
        line = file.readline().split(',')
        message = list()
        city = ''

        # Read till EOF
        if line != ['']:
            for m in range(0,len(line)):
                # Split each line into words
                message.extend(line[m].split())

            # Remove everything except alphabets and numbers and convert to lower case
            message = [re.sub('[^a-zA-Z0-9]','',i.lower()) for i in message]
            # Remove stop words
            message = [i for i in message if i not in stop_words]
            # Get the city name and remove it from the message, i.e separate tweet and location
            city = str(line[0] + ',_' + message[1].upper())
            message.pop(0)
            message.pop(0)
            # Remove duplicate words in a tweet
            message = list(set(message))

            # Store cities and their tweet count in cities dictionary
            if city not in cities:
                cities[city] = 1
            else:
                cities[city] += 1

            # Store each tweet of a particular location as list in cities_Words dictionary
            if city not in cities_words:
                cities_words[city] = [message]
                count_tweets += 1
            else:
                cities_words[city].append(message)
                count_tweets += 1
        else:
            break
    file.close()

    # Return both dictionary and total tweet count
    return cities_words,cities,count_tweets

# Function to calculate the P(W|L) that is probability of a word 'W' given a location L
# P(W|L) = P(W intersection L)/P(L)
# P(L) has been already calculate in cities dictionary
# P(W intersection L) = (no. of tweets of city L and containing word W)/(Total number of tweets)
# P(W|L) is stored in probabilty_dict dictionary as
# probabilty_dict = {'city1 name':{'W1':P(W1|L1), 'W2':P(W2|L1)...}, 'city2 name':{'W1':P(W1|L2), 'W2':P(W2|L2)..}...}
# This function takes inputs as below
# cities_words dictionary containing cities and their respective tweets list
# cities dictionary contain P(L) values for each city
# and total tweet_count
def probablity(cities_words,cities,tweet_count):
    probabilty_dict = dict()
    count = 0
    for city,tweet_list in cities_words.items():

        # Create a new dictionary for words and respective probability inside probablity_dict
        probabilty_dict[city] = dict()
        for tweet in tweet_list:            
            for word in tweet:

                # If its a new word store the word and its probability as 1/((total tweet count)*P(L))
                # Else if the word appears again in a tweet of a location
                # add 1/((total tweet count)*P(L))
                # (1+1+...no of times the word appears)/(total tweet count) is equal to P(W intersection L)
                # and P(W intersection L)/P(L) is equal to P(W|L)
                if word not in probabilty_dict[city]:                    
                    probabilty_dict[city][word] = 1/(tweet_count*cities[city]) 
                else:
                    probabilty_dict[city][word] = probabilty_dict[city][word] + (1/(tweet_count*cities[city]))
    return probabilty_dict
            

# Function to read the testing file line by line and find P(L|W1,W2,...) = P(L)*P(W1|L)*P(W2|L)*...P(Wn|L) i.e. Bayes Law
# This function takes below inputs
# likeliness dictionary which contains P(W|L) for each location and each word
# cities dictionary which contains P(L) values
# Path as testing file name
# Output as output file name
def read_test(path,likeliness,cities,output):
    file = open(path)
    output = open(output,"w+")
    while True:
        l = file.readline()
        line = l.split(',')
        message = list()
        if line != ['']:

            # Splitting the tweet into words and removal of unnecessary characters/words
            for m in range(0,len(line)):
                message.extend(line[m].split())
            message = [re.sub('[^a-zA-Z0-9]','',i.lower()) for i in message]
            message = [i for i in message if i not in stop_words]
            message.pop(0)
            message.pop(0)

            # Calculation of posterior probabilities for all cities for this particular tweet
            # Set initial value of Posterior probability to 0 and city as empty string 
            city = ''
            Posterior_Probability = 0            
            for x,y in likeliness.items():

                # setting Temp posterior to P(L) as it needs to be multiplied in the below formula
                # P(L|W1,W2,...) = P(L)*P(W1|L)*P(W2|L)*...P(Wn|L)
                temp_posterior_probability = cities[x]

                # For each word in tweet check if P(W|L) is in the likeliness dictionary
                # If yes then multiply it else multiple by 0.00001(some low probability) 
                for word in message:
                    if word in y:
                        temp_posterior_probability = temp_posterior_probability * y[word] 
                    else:
                        temp_posterior_probability = temp_posterior_probability * 0.00001

                # If this posterior is largest store it along with city value
                if temp_posterior_probability > Posterior_Probability:
                    Posterior_Probability = temp_posterior_probability
                    city = x

            # Write the city name with the highest posterior probability for this tweet to the output file
            output.write(city+ ',' +l)
        else:
            break
    output.close()    
    file.close()


# Function to find the top 5 words for each city
# Here we invert the key value pairs in likelihood dictionary and store it in a priority queue
# and then pop from the priority queue to get top 5 words
def top_words(word_dict):
    for x,y in word_dict.items():

        # Here y is a dictionary containing {word:P(W|L)} as key:value pairs
        # We invert this and store it in priority queue 'q' as (P(W|L):word)
        q = PriorityQueue()
        for i,j in y.items():

            # store probability as negative values so that the highest probable word as a negative value 
            # becomes the most negative(or least value) and hence gets poped first from the priority queue
            q.put(((-j),i)) 
        print("\nTop Words of Location %s are" % x)
        for count in range(0,5):
            word = q.get()
            print(word[1],end = ', ')


# Main

# Get the file names
Training_file = str(sys.argv[1])
Test_file = str(sys.argv[2])
Output_file = str(sys.argv[3])

# Call read function on training file and get cities dictionary containing city name and respective count of tweets, 
# cities_and_tweets dictionary containing city names and respective tweets for that city
# and the total tweet count
cities_and_tweets,cities_dict,tweet_count = read(Training_file)

# Calculate P(L) probability of a tweet belonging to a particular location
# P(L) = (no. of tweets for that location)/(total number of tweets)
for x,y in cities_dict.items():
    cities_dict[x] = cities_dict[x]/tweet_count

# Call the probability function to calculate the likelihood probabilities i.e. P(W|L)
likelihood = probablity(cities_and_tweets,cities_dict,tweet_count)

# Call this function to read the test file and calculate the posterior probabilities
read_test(Test_file,likelihood,cities_dict,Output_file)

# Call this function to get the top 5 words for each location from likelihood dictionary
top_words(likelihood)