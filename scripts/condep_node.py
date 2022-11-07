#!/usr/bin/env python

import spacy
import stanza
import argparse

#ROS
import std_msgs.msg
from std_srvs.srv import Empty
from std_srvs.srv import EmptyResponse
from ros_whisper_vosk.srv import GetSpeech

import rospy
import rospkg

parser = argparse.ArgumentParser()
parser.add_argument("--whisper", default=False, action='store_true', help="Whether to use Vosk (default) or Whisper")
parser.add_argument("--stanza", default=False, action='store_true', help="Whether to use spaCy (default) or Stanza")

args = parser.parse_args(rospy.myargv()[1:])

print("------------------------------------------------")
print(args)
print("------------------------------------------------")

is_whisper = args.whisper
is_stanza = args.stanza

#Start Client
service_name = "speech_recognition/vosk_service"
if (is_whisper):
    service_name = "speech_recognition/whisper_service"

rospy.wait_for_service(service_name)
speech_service = rospy.ServiceProxy(service_name, GetSpeech)   

#Start ROS Publishers
pub_final = rospy.Publisher('conceptual_dependencies/final_result',std_msgs.msg.String, queue_size=10)

#Callbacks
def callbackConDepNode(data):

    speech_text = ""
    try:
        speech_text = speech_service().data
    except:
        speech_text = ""

    if (is_stanza):
        print("Sample code with stanza")
    else:
        print("Sample code with spacy")

    #Process text to CD
    conceptual_deps = speech_text

    #########

    print(conceptual_deps)
    pub_final.publish(conceptual_deps)

#Main
def main():
    rospy.init_node('condep_node')
  
    #Start ROS Subscribers
    rospy.Subscriber("conceptual_dependencies/condep_node", std_msgs.msg.Empty, callbackConDepNode)

    rospy.loginfo("Conceptual Dependencies Node Initialized")
    
    #Infinite loop
    rospy.spin()

if __name__ == "__main__":
    main()
