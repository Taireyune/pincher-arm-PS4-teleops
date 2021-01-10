import rospy, sys
from cortex_message_handling.msg import CortexCommands

from scripts.teleops import Pincher_teleops

class Arm_commands:
    def __init__(self, controller):
        self.controller = controller
        self.content = CortexCommands()
        self.default()
        
    def default(self):
        self.content.waist = 0
        self.content.shoulder = 0
        self.content.elbow = 0
        self.content.wrist_angle = 0
        self.content.wrist_rotate = 0
        self.content.gripper = 0

    def update(self, count):
        # get pwm values from controller
        self.content.waist, self.content.shoulder, self.content.elbow, \
            self.content.wrist_angle, self.content.wrist_rotate, \
            self.content.gripper = self.controller.get_value(count)
        
    def to_string(self):
        str_message = "["
        str_message += str(self.content.waist) + ", "
        str_message += str(self.content.shoulder) + ", "
        str_message += str(self.content.elbow) + ", "
        str_message += str(self.content.wrist_angle) + ", "
        str_message += str(self.content.wrist_rotate) + ", "
        str_message += str(self.content.gripper) + ", "
        return str_message + "]"

def run_node(identifier_suffix='R'):
    print(sys.version)
    identifier = 'px150/cortex_commands_' + identifier_suffix

    pub = rospy.Publisher(identifier, CortexCommands, queue_size=1)
    rospy.init_node('cortex_node_' + identifier_suffix, anonymous=True)

    loop_rate = 400
    rate = rospy.Rate(loop_rate)
    publish_rate = loop_rate // 40

    # controller and message
    # rotate_wrist = Rotate_wrist()
    # arm_commands = Arm_commands(rotate_wrist)

    teleops = Pincher_teleops()
    arm_commands = Arm_commands(teleops)

    count = 0
    cntrl = 0
    while not rospy.is_shutdown():
        # message will update every loop but only publish at 10hz
        arm_commands.update(count)
        
        if cntrl == publish_rate:
            print(f"[PS4_teleops {identifier_suffix}] " + arm_commands.to_string())
            pub.publish(arm_commands.content)
            cntrl = 0

        cntrl += 1
        count += 1
        rate.sleep()

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            run_node(sys.argv[1])
        else:
            run_node()
    except rospy.ROSInterruptException:
        pass