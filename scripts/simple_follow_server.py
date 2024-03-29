#! /usr/bin/env python

import rospy
import actionlib
import threading
from simple_follow.msg import SimpleFollowAction
from simple_follow.human_follow import SimpleFollow


class SimpleFollowServer(object):

    def __init__(self):
        # self.load_params()
        self.agent = SimpleFollow()
        self.server = actionlib.SimpleActionServer('simple_follow',
                                                   SimpleFollowAction,
                                                   self.execute, False)
        rospy.loginfo("Starting Simple Follow Server...")
        self.server.start()

    def execute(self, goal):
        rospy.loginfo('Receiving goal...')
        timestart = rospy.get_time()
        smach_thread = threading.Thread(target=self.agent.execute_sm)
        smach_thread.start()

        while not rospy.is_shutdown():
            if rospy.get_time() - timestart > goal.time:
                rospy.signal_shutdown('Timeout')
                return


if __name__ == '__main__':
    rospy.init_node('simple_follow_server')
    server = SimpleFollowServer()
    rospy.spin()
