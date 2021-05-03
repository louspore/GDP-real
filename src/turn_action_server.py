#!/usr/bin/env python
import rospy, actionlib, line_follower_turtlebot.msg
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32, String


class TurnAction(object):
    _feedback = line_follower_turtlebot.msg.TurnActionFeedback()
    _result = line_follower_turtlebot.msg.TurnActionResult()

    def __init__(self,name):
        self.first_step_done=False      #robot has to move straight first, then turn
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        self.twist=Twist()


        self._action_name=name
        self._as = actionlib.SimpleActionServer(self._action_name, line_follower_turtlebot.msg.TurnAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()


    def execute_cb(self,goal):
        r=rospy.Rate(10)
        success=True
        t0=rospy.get_time()

        while True
            if self._as.is_preempt_requested():
                    rospy.loginfo('%s: Preempted' % self._action_name)
                    self._as.set_preempted()
                    success = False
                    break

            if rospy.get_time()-t0>3.0:
                break

            elif rospy.get_time-t0>1.0:

                if goal.turn_direction=="Straight":
                    break

                elif goal.turn_direction=="Left":
                    self.twist.linear.x=0
                    self.twist.angular.z=0.1
                    self.cmd_pub.publish(self.twist)

                elif goal.turn_direction=="Right":
                    self.twist.linear.x=0
                    self.twist.angular.z=-0.1
                    self.cmd_pub.publish(self.twist)

                else:
                    assert goal.turn_direction == "Back"
                    self.twist.linear.x=0
                    self.twist.angular.z=0.2
                    self.cmd_pub.publish(self.twist)

            else:
                self.twist.linear.x=0.2
                self.twist.angular.z=0
                self.cmd_pub.publish(self.twist)

            r.sleep()

        if success:
            self._result.result="Success"
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)


if __name__ == '__main__':
    rospy.init_node('turn_action_client')
    server = TurnAction(rospy.get_name())
    rospy.spin()
