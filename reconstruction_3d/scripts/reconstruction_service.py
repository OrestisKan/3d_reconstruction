#!/usr/bin/env python3

from reconstruction_3d.srv import Reconstruct, ReconstructResponse
import cv2
import numpy as np
import rospy

def reconstruct(data: Reconstruct) -> ReconstructResponse:
    """
    Callback function for the server node 
    Attempts to format the Reconstruct message and call opencv's 
    triangulatePoints method which returns a 4x1 list 

    The result is converted to hogeneous coordinate space and 
    returned as part of the service
    """
    try:
        proj1 = np.array(Reconstruct.CameraInfo1.P).reshape(3, 4)

        proj2 = np.array(Reconstruct.CameraInfo2.P).reshape(3, 4)


        if len(point1 := Reconstruct.point1) == 3:
            # If in projective space convert to homogeneous
            point1 /= point1[2]
            point1 = np.array(point1[:2]).reshape(2,1)
        else:
            point1 = np.array(Reconstruct.point1).reshape(2,1)


        if len(point2 := Reconstruct.point2) == 3:
            # If in projective space convert to homogeneous
            point2 /= point2[2]
            point2 = np.array(point2[:2]).reshape(2,1)
        else:
            point2 = np.array(Reconstruct.point2).reshape(2,1)

        X = cv2.triangulatePoints(proj1, proj2, point1, point2)
        X /= X[3]
        return  ReconstructResponse(X[:3])
    except ValueError:
        rospy.logerr("Faulty array shapes")
        X = cv2.triangulatePoints(Reconstruct**)
        X /= X[3]
        return  ReconstructResponse(X[:3])

def reconstruction_server():
    """
    Server node
    """
    rospy.init_node('reconstruction_server')
    s = rospy.Service('reconstruct', Reconstruct, reconstruct)
    rospy.loginfo("Ready to reconstruct 3D points")
    rospy.spin()

if __name__ == "__main__":
    reconstruction_server()