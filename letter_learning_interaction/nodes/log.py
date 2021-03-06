#!/usr/bin/env python
#coding: utf-8
"""
Created on Wed Apr 15 17:27:12 2015

@author: ferran
"""
import time
import rospy
import datetime
from std_msgs.msg import Int16, Int32, String, Empty, Float32

import csv

word = ""
timeWriting = ""
timeResponse = ""
path = ""
repetition = ""
learn = ""

child_counter = 1
    
class log():
    
    def __init__(self):
        # Cues to evaluate:
        rospy.Subscriber("lookAt", String, self.look_robot_callback)            # Where the child is looking at
        rospy.Subscriber("smile", Empty, self.smile_robot_callback)             # The child is smiling
        rospy.Subscriber("movement", Int16, self.movement_callback)             # The child is moving while sitting
        rospy.Subscriber("sizeHead", Int16, self.proximity_callback)            # The child is getting closer
        rospy.Subscriber("novelty", Float32, self.novelty_callback)             # Something new happen in the scenario
        #rospy.Subscriber("activity_time", Int32, self.time_callback)            # For how long the activity was done
        rospy.Subscriber("nb_repetitions", Int16, self.repetitions_callback)    # The number of word repetitions
        rospy.Subscriber("time_response", Float32, self.response_callback)      # Response time till the child writes
        rospy.Subscriber("time_writing", Float32, self.writing_callback)        # Writing time during demostration
        
        rospy.Subscriber("activity", String, self.activity_callback)            # Current activity
        rospy.Subscriber("words_to_write", String, self.word_callback)          # Word to be written
        rospy.Subscriber("new_child", String, self.child_callback)              # New child in da house
        rospy.Subscriber("current_demo", String, self.correctness_callback)     # Path of the demo
        rospy.Subscriber("current_learn", String, self.learn_word_callback)     # Path of the learn
        
        
        date_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        self.filePath = '/home/ferran/.ros/visionLog/' + date_time + '.csv'
        
        with open(self.filePath, 'wb') as csvfile:
            intro = '********************************NEW SESSION********************************'
            wr = csv.writer(csvfile, delimiter='-', quoting=csv.QUOTE_NONE, quotechar='')
            wr.writerow(intro)
        
        # Initialize the node and name it.       
        rospy.init_node('log', anonymous = True)
                            
        # Simply keeps python from exiting until this node is stopped
        rospy.spin()

    def look_robot_callback(self, data):
        timestamp = self.getTime()
        lookAt = "look: " + data.data   
                
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, lookAt])
        
    def smile_robot_callback(self, data):
        timestamp = self.getTime()
        smile = "child smiles"   
                
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, smile])
        
    def movement_callback(self, data):
        timestamp = self.getTime()
        movement = "movement: " + str(data.data)
                
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, movement])
        
    def proximity_callback(self, data):
        timestamp = self.getTime()
        proximity = "proximity: " + str(data.data)
                
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, proximity])
    
    def novelty_callback(self, data):
        timestamp = self.getTime()
        novelty = "novelty: " + str(data.data)
                
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, novelty])
    
    
    # TODO: Counts the activity time including all children!!
    # Make a reset when new_child receives sth
    #def time_callback(self, data):   
    #    pass
    
    def repetitions_callback(self, data):
        global repetition
        repetition = "repetition:" + str(data.data)
    
    
    def response_callback(self, data):
        global timeResponse
        timeResponse = "timeResponse:" + str(data.data)

        
    def writing_callback(self, data):
        global timeWriting
        timeWriting = "writeTime:" + str(data.data)

    
    def activity_callback(self, data):
        timestamp = self.getTime()
        activity = "activity:" + data.data
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, activity])
        
    def word_callback(self, data):
        global word
        word = "word: " + data.data
    

    def child_callback(self, data):
        global child_counter
        timestamp = self.getTime()
        child = "child:" + str(child_counter)
        child_counter = child_counter + 1
        
        date_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        self.filePath = '/home/ferran/.ros/visionLog/' + date_time + '.csv'
        
        with open(self.filePath, 'wb') as csvfile:
            intro = "********************************NEW SESSION********************************"
            wr = csv.writer(csvfile, delimiter='-', quoting=csv.QUOTE_NONE, quotechar='')
            wr.writerow(intro)
            #wr.writerow([timestamp, child])

               
    # TODO: Manage with the cluster distance     
    def correctness_callback(self, data):
        global path
        path = data.data
        self.addRep()
        

    def addRep(self):
        global word
        global timeWriting
        global timeResponse
        global path
        global repetition
        timestamp = self.getTime()
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, word, repetition, timeResponse, timeWriting, path])       
        
    def getTime(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S:%f')
    
    def learn_word_callback(self, data):
        global learn
        global word
        learn = data.data
        timestamp = self.getTime()
        with open(self.filePath, 'a') as csvfile:
            wr = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            wr.writerow([timestamp, word, learn])  
        
        
def main():
    
    log()
    
# Main function.   
if __name__ == "__main__":
    main()  