import rospy
from cortex_message_handling.msg import CortexCommands

def constant_message():
    pub = rospy.Publisher('px150/cortex_commands_S2', CortexCommands, queue_size=1)
    rospy.init_node('cortex_node_S2', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    content = CortexCommands()
    wrist_angle = 10
    count = 0 
    while not rospy.is_shutdown():

        if not count % 10:
            wrist_angle *= -1
        content.wrist_angle = wrist_angle
        print(f"wrist_angle is {wrist_angle}")
        pub.publish(content)
        count += 1
        rate.sleep()

if __name__ == '__main__':
    try:
        constant_message()
    except rospy.ROSInterruptException:
        pass