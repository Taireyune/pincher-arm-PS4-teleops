import time, zmq, rospy, sys, cv2
from threading import Thread
import numpy as np

address = "ipc:///tmp/blackfly_video_relay_1"

def receiver():
    context = zmq.Context()
    socket_sub = context.socket(zmq.SUB)
    socket_sub.setsockopt(zmq.CONFLATE, 1)
    socket_sub.connect(address)
    socket_sub.subscribe("")

    writer = cv2.VideoWriter("video.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 50, (1240,1240))

    print("socket bound")
    rospy.init_node('binocular_subscriber', anonymous = True)
    rate = rospy.Rate(60)
    time_now = rospy.Time.now()
    
    while not rospy.is_shutdown():
        print("Frame rate : ", 1 / (rospy.Time.now() - time_now).to_sec(), " hz" )
        time_now = rospy.Time.now()
        try:
            msg = socket_sub.recv(zmq.NOBLOCK, copy=False)
            image = np.fromstring(msg, np.uint8)
            image = image.reshape(1240, 1240, 3)
            print(image.shape)
            cv2.imshow("receiver feed", image)
            # writer.write(image)
        except Exception as e:
            print(e)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        rate.sleep()

    socket_sub.close()
    context.term()
    writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    receiver()

