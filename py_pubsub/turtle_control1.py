# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
import random

from std_msgs.msg import String
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class Turtle_control(Node):

    def __init__(self):
        super().__init__('turtle_controller')
        self.turtle_sub_pose_ = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10)
        self.turtle_sub_pose_  # prevent unused variable warning
        self.turtle_pub_vel_=self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.turn_dir =1.0
        self.in_turn=False

    def pose_callback(self, msg: Pose):
        new_vel_=Twist()
        x= msg.x
        y= msg.y
        #print(x,y)
        #self.get_logger().info('Pose is: "%s"' % msg)
        new_vel_.angular.z =0.0
        new_vel_.linear.x =1.0
    
        if x > 7 or x < 3 or y > 7 or y <3 :
            if self.in_turn == False:
                self.in_turn = True
                self.turn_dir =1.0
                if random.randint(0, 100) > 50 : self.turn_dir =-1.0
                self.turn_vel = 1.5* self.turn_dir
 
            new_vel_.angular.z = self.turn_vel
            new_vel_.linear.x =1.5
        if x < 7 and x >3 and y < 7 and y>3 :
            self.in_turn=False
        self.turtle_pub_vel_.publish(new_vel_)


    



def main(args=None):
    rclpy.init(args=args)

    pose_subscriber_ = Turtle_control()

    rclpy.spin(pose_subscriber_)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pose_subscriber_.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
