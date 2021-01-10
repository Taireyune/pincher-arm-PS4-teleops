from scripts.node import run_node
import rospy, sys

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            run_node(sys.argv[1])
        else:
            run_node()
    except rospy.ROSInterruptException:
        pass