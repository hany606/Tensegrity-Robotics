#!/usr/bin/env python
import json
import rospy
import threading
from std_msgs.msg import String

main_path = "/home/hany/repos/Tensegrity-Robot-IU-Internship19/build/dev/"
application_name = "test"

application_full_path = main_path+application_name+"/data.json"

with open(application_full_path,"r") as read_file:
    default_json = json.load(read_file)

print("DONE")
def reloadJson():
    with open(application_full_path, "r") as read_file:
        try:
            # print("try")
            json_data = json.load(read_file)
            global default_json
            default_json = json_data
        except:
            print("Error in loading")
            json_data = default_json
        finally:
            # for i in range(0,6):
            #     print("Controller {}: {}".format(i,json_data["Controllers"][i]))
            return json_data



def talker():
    pub = []
    for i in range(0,6):
        pub.append(rospy.Publisher('controller'+str(i), String, queue_size=10))
        #next step to create custome msg
    rospy.init_node('tenegrity_controllers', anonymous=True)
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        json_data = reloadJson()
        for i in range(0,6):
            pub[i].publish(str(json_data["Controllers"][i]))
        rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass