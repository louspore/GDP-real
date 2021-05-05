#!/usr/bin/env python
import rospy, actionlib, line_follower_turtlebot.msg
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32, String


class TurnAction(object):
    _feedback = line_follower_turtlebot.msg.TurnFeedback()
    _result = line_follower_turtlebot.msg.TurnResult()

    def __init__(self,name):
        self.first_step_done=False      #robot has to move straight first, then turn
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        self.twist=Twist()


        self._action_name=name
        self._as = actionlib.SimpleActionServer(self._action_name, line_follower_turtlebot.msg.TurnAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        rospy.on_shutdown(self.fnShutdown)


    def execute_cb(self,goal):
        r=rospy.Rate(10)
        success=True
        t0=rospy.get_time()
        rospy.loginfo("Goal received")

        while True:
            if self._as.is_preempt_requested():
                    rospy.loginfo('%s: Preempted' % self._action_name)
                    self._as.set_preempted()
                    success = False
                    break

            if rospy.get_time()-t0>3.0:
                break

            elif rospy.get_time()-t0>1.0:

                if goal.turn_direction=="Straight":
                    break

                elif goal.turn_direction=="Left":
                    self.twist.linear.x=0
                    self.twist.angular.z=0.785
                    self.cmd_pub.publish(self.twist)

                elif goal.turn_direction=="Right":
                    self.twist.linear.x=0
                    self.twist.angular.z=-0.785
                    self.cmd_pub.publish(self.twist)

                else:
                    assert goal.turn_direction == "Back"
                    self.twist.linear.x=0
                    self.twist.angular.z=1.57
                    self.cmd_pub.publish(self.twist)

            else:
                self.twist.linear.x=0.08
                self.twist.angular.z=0
                self.cmd_pub.publish(self.twist)

            r.sleep

        if success:
            self.cmd_pub.publish(Twist())
            self._result.result="Success"
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)


    def fnShutdown(self):
        cmd=Twist()
        self.cmd_pub.publish(cmd)
        rospy.loginfo("Shutting down, cmd vel 0")
            
if __name__ == '__main__':
    rospy.init_node('turn_action_server')
    server = TurnAction(rospy.get_name())
    rospy.spin()

