# IMPORTING LIBRARIES
import streamlit as st
st.set_page_config(page_title='YOGA APP', page_icon="🖖")
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import math
import keyboard as kb

from scipy import spatial

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# CALCULATING ANGLES
def calculateAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians =  np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0]- b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
#     print(f'Angle between {a}, {b}, {c} = {angle}')
    return angle


# ASSIGN NUMBERS TO ANGLES AND CALCULATES ANGLES 
current_pose = 2
# path = "video/yoga" + str(current_pose) + ".jpg"
path = "yogapose/yoga"
# print(path)
IMAGE_FILES = [path] 
IMAGE_FILES
# print(len(IMAGE_FILES))
# path = "video/yoga"
# image = cv2.imread(path)   
# cv2.imshow('im',image) 
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# for idx, file in enumerate(IMAGE_FILES):
#     print(idx,file)
#     image = cv2.imread(file)   
#     cv2.imshow('im',image)    
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def extractKeypoint(path):
    IMAGE_FILES = [path]             #['video/yoga1.jpg']
    stage = None
    joint_list_video = pd.DataFrame([])
    count = 0

    with mp_pose.Pose(min_detection_confidence =0.5, min_tracking_confidence = 0.5) as pose:

        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)   
            
            dim = (560,800)
            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            
            

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_h, image_w, _ = image.shape
            
#             dim = (560,800)
#             image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

            try:
                # 33 landmarks
                landmarks = results.pose_landmarks.landmark
#                 print(landmarks)
                
                # coordinates(x,y) of each point
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                joint_list = pd.DataFrame([])
                for i,data_point in zip(range(len(landmarks)),landmarks):
                    joints = pd.DataFrame({
                                               'frame': count,
                                               'id': i,
                                               'x': data_point.x,
                                               'y': data_point.y,
                                               'z': data_point.z,
                                               'vis': data_point.visibility 
                                                }, index = [0]
                                                )
                    joint_list = pd.concat([joint_list, joints], axis=0,ignore_index=True)


                keypoints = []
                for point in landmarks:
                    keypoints.append({
                             'X': point.x,
                             'Y': point.y,
                             'Z': point.z,
                             }) 

                angle = []
                angle_list = pd.DataFrame([])
                angle1 = calculateAngle(right_shoulder, right_elbow, right_wrist)
                angle.append(int(angle1))
                angle2 = calculateAngle(left_shoulder, left_elbow, left_wrist)
                angle.append(int(angle2))
                angle3 = calculateAngle(right_elbow, right_shoulder, right_hip)
                angle.append(int(angle3))
                angle4 = calculateAngle(left_elbow, left_shoulder, left_hip)
                angle.append(int(angle4))
                angle5 = calculateAngle(right_shoulder, right_hip, right_knee)
                angle.append(int(angle5))
                angle6 = calculateAngle(left_shoulder, left_hip, left_knee)
                angle.append(int(angle6))
                angle7 = calculateAngle(right_hip, right_knee, right_ankle)
                angle.append(int(angle7))
                angle8 = calculateAngle(left_hip, left_knee, left_ankle)
                angle.append(int(angle8))
                
#                 garbage = tuple(np.multiply(right_elbow,[image_w, image_h,]).astype(int))
#                 print(garbage)
#                 print(image.shape)
                
#                 print(np.multiply(right_elbow,[image_w, image_h,]).astype(int))
#                 cv2.putText(image, 'why so tiny?',(1935, 1758), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA )
                cv2.putText(image, str(1), tuple(np.multiply(right_elbow,[image_w, image_h,]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,153,76], 2, cv2.LINE_AA )
                cv2.putText(image, str(2), tuple(np.multiply(left_elbow,[image_w, image_h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,153,76], 2, cv2.LINE_AA )
                cv2.putText(image, str(3), tuple(np.multiply(right_shoulder,[image_w, image_h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,153,76], 1, cv2.LINE_AA )
                cv2.putText(image, str(4), tuple(np.multiply(left_shoulder,[image_w, image_h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,153,76], 1, cv2.LINE_AA )
                cv2.putText(image, str(5), tuple(np.multiply(right_hip,[image_w, image_h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,153,76], 1, cv2.LINE_AA )
                cv2.putText(image, str(6), tuple(np.multiply(left_hip,[image_w, image_h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,153,76], 1, cv2.LINE_AA )
                cv2.putText(image, str(7), tuple(np.multiply(right_knee,[image_w, image_h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,153,76], 1, cv2.LINE_AA )
                cv2.putText(image, str(8), tuple(np.multiply(left_knee,[image_w, image_h]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, [0,153,76], 1, cv2.LINE_AA )
            except:
                pass
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                     mp_drawing.DrawingSpec(color = (50, 168, 158), thickness = 3, circle_radius = 2),
                                     mp_drawing.DrawingSpec(color = (168, 168, 50),thickness = 3, circle_radius = 2))
#         cv2.imshow('MediaPipe Feed',image)
            
#             image = cv2.resize(image, (int(image_width * (860 / image_height)), 860))
            cv2.rectangle(image,(0,0), (100,255), (255,255,255), -1)
#             cv2.rectangle(image, (0,0), (   int(image_w - (image_w*0.8)), int(image_h - (image_h*0.75))   ), (255,255,255), -1)

            cv2.putText(image, 'ID', (10,14), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [50, 168, 113], 2, cv2.LINE_AA)
            cv2.putText(image, str(1), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(2), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(3), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(4), (10,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(5), (10,160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(6), (10,190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(7), (10,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(8), (10,250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)

            cv2.putText(image, 'Angle', (40,12), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [50, 168, 113], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle1)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle2)), (40,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle3)), (40,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle4)), (40,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle5)), (40,160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle6)), (40,190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle7)), (40,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)
            cv2.putText(image, str(int(angle8)), (40,250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [153,153,0], 2, cv2.LINE_AA)

            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
            
        cv2.destroyAllWindows()          
    return landmarks, keypoints, angle, image


# CORRECTING HUMAN
def compare_pose(image,angle_point,angle_user, angle_target ):
    #image - human captured
    #angle_point - human angles points coordinates
    #angle_user - human angles
    #angle_target - angles(8) of the image(video/yoga)
    angle_user = np.array(angle_user)
    angle_target = np.array(angle_target)
    angle_point = np.array(angle_point)
    stage = 0
    cv2.rectangle(image,(0,0), (370,40), (255,255,255), -1)
#     cv2.rectangle(image,(0,40), (370,370), (0,0,0), -1)
    cv2.rectangle(image,(0,40), (370,370), (255,255,255), -1)
    cv2.putText(image, str("Score:"), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    height, width, _ = image.shape   
    
    if angle_user[0] < (angle_target[0] - 15):
        #print("Extend the right arm at elbow")
        stage = stage + 1
        cv2.putText(image, str("Extend the right arm at elbow"), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[0][0]*width), int(angle_point[0][1]*height)),30,(0,0,255),5) 
        
    if angle_user[0] > (angle_target[0] + 15):
        #print("Fold the right arm at elbow")
        stage = stage + 1
        cv2.putText(image, str("Fold the right arm at elbow"), (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[0][0]*width), int(angle_point[0][1]*height)),30,(0,0,255),5)

        
    if angle_user[1] < (angle_target[1] -15):
        #print("Extend the left arm at elbow")
        stage = stage + 1
        cv2.putText(image, str("Extend the left arm at elbow"), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[1][0]*width), int(angle_point[1][1]*height)),30,(0,0,255),5)
        
    if angle_user[1] >(angle_target[1] + 15):
        #print("Fold the left arm at elbow")
        stage = stage + 1
        cv2.putText(image, str("Fold the left arm at elbow"), (10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[1][0]*width), int(angle_point[1][1]*height)),30,(0,0,255),5)

        
    if angle_user[2] < (angle_target[2] - 15):
        #print("Lift your right arm")
        stage = stage + 1
        cv2.putText(image, str("Lift your right arm"), (10,140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[2][0]*width), int(angle_point[2][1]*height)),30,(0,0,255),5)

    if angle_user[2] > (angle_target[2] + 15):
        #print("Put your arm down a little")
        stage = stage + 1
        cv2.putText(image, str("Put your arm down a little"), (10,160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[2][0]*width), int(angle_point[2][1]*height)),30,(0,0,255),5)

    if angle_user[3] < (angle_target[3] - 15):
        #print("Lift your left arm")
        stage = stage + 1
        cv2.putText(image, str("Lift your left arm"), (10,180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[3][0]*width), int(angle_point[3][1]*height)),30,(0,0,255),5)

    if angle_user[3] > (angle_target[3] + 15):
        #print("Put your arm down a little")
        stage = stage + 1
        cv2.putText(image, str("Put your arm down a little"), (10,200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[3][0]*width), int(angle_point[3][1]*height)),30,(0,0,255),5)

    if angle_user[4] < (angle_target[4] - 15):
        #print("Extend the angle at right hip")
        stage = stage + 1
        cv2.putText(image, str("Extend the angle at right hip"), (10,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[4][0]*width), int(angle_point[4][1]*height)),30,(0,0,255),5)

    if angle_user[4] > (angle_target[4] + 15):
        #print("Reduce the angle at right hip")
        stage = stage + 1
        cv2.putText(image, str("Reduce the angle of at right hip"), (10,240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[4][0]*width), int(angle_point[4][1]*height)),30,(0,0,255),5)

    if angle_user[5] < (angle_target[5] - 15):
        #print("Extend the angle at left hip")
        stage = stage + 1
        cv2.putText(image, str("Extend the angle at left hip"), (10,260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[5][0]*width), int(angle_point[5][1]*height)),30,(0,0,255),5)
        
    if angle_user[5] > (angle_target[5] + 15):
        #print("Reduce the angle at left hip")
        stage = stage + 1
        cv2.putText(image, str("Reduce the angle at left hip"), (10,280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[5][0]*width), int(angle_point[5][1]*height)),30,(0,0,255),5)

    if angle_user[6] < (angle_target[6] - 15):
        #print("Extend the angle of right knee")
        stage = stage + 1
        cv2.putText(image, str("Extend the angle of right knee"), (10,300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[6][0]*width), int(angle_point[6][1]*height)),30,(0,0,255),5)
        
    if angle_user[6] > (angle_target[6] + 15):
        #print("Reduce the angle of right knee")
        stage = stage + 1
        cv2.putText(image, str("Reduce the angle at right knee"), (10,320), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[6][0]*width), int(angle_point[6][1]*height)),30,(0,0,255),5)

    if angle_user[7] < (angle_target[7] - 15):
        #print("Extend the angle at left knee")
        stage = stage + 1
        cv2.putText(image, str("Extend the angle at left knee"), (10,340), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[7][0]*width), int(angle_point[7][1]*height)),30,(0,0,255),5)

    if angle_user[7] > (angle_target[7] + 15):
        #print("Reduce the angle at left knee")
        stage = stage + 1
        cv2.putText(image, str("Reduce the angle at left knee"), (10,360), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
        cv2.circle(image,(int(angle_point[7][0]*width), int(angle_point[7][1]*height)),30,(0,0,255),5)
    
    if stage!=0:
        cv2.putText(image, str("FIGHTING!"), (170,30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)
        pass
    else:
        cv2.putText(image, str("PERFECT"), (170,30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)


def Average(lst):
    return sum(lst) / len(lst)


# CALCULATING SCORE
def dif_compare(x,y):
    #y = target (keypoint) - [{x:, y:, z:}]
    #x = human (keypoint) - [{x:, y:, z:}] 
    average = []
    for i,j in zip(range(len(list(x))),range(len(list(y)))):
#         . It is a value between -1 and 1, with 1 indicating that the two vectors are identical in direction and -1 indicating that they are opposite in direction.
# A value of 0 indicates that the two vectors are orthogonal (perpendicular) to each other.
        result = 1 - spatial.distance.cosine(list(x[i].values()),list(y[j].values()))
        average.append(result)
    score = math.sqrt(2*(1-round(Average(average),2)))
    return score

def diff_compare_angle(x,y):
    new_x = []
    for i,j in zip(range(len(x)),range(len(y))):
        z = np.abs(x[i] - y[j])/((x[i]+ y[j])/2)
        new_x.append(z)
    return Average(new_x)

# change_pose(path = "Video/yoga" + str(current_pose) + ".jpg")
def change_pose(path):
    current_pose = 2
    # path = "Video/yoga13.jpg"

    # deatils get written on the image with keypoints
    x = extractKeypoint(path)
    
    x_height, x_width, _ = x[3].shape
    dim = (560,800)
    
    resized = cv2.resize(x[3], dim, interpolation = cv2.INTER_AREA)
#     resized = cv2.resize(x[3], (0,0), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
    cv2.imshow('target',resized)
    angle_target = x[2]
    point_target = x[1]


    with mp_pose.Pose(min_detection_confidence =0.5, min_tracking_confidence = 0.5) as pose:

        while cap.isOpened():
            ret,frame= cap.read()

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_height, image_width, _ = image.shape
            image = cv2.resize(image, (int(image_width * (760 / image_height)), 800))
            
            try:
                landmarks = results.pose_landmarks.landmark

                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,
                              round(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility*100, 2)]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z,
                              round(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility*100, 2)]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z,
                              round(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility*100, 2)]

                angle_point = []

                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                angle_point.append(right_elbow)

                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                angle_point.append(left_elbow)

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                angle_point.append(right_shoulder)

                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                angle_point.append(left_shoulder)

                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                angle_point.append(right_hip)

                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                angle_point.append(left_hip)

                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                angle_point.append(right_knee)

                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                angle_point.append(left_knee)
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                keypoints = []
                for point in landmarks:
                    keypoints.append({
                         'X': point.x,
                         'Y': point.y,
                         'Z': point.z,
                         })

                p_score = dif_compare(keypoints, point_target)      

                angle = [] 

                angle1 = calculateAngle(right_shoulder, right_elbow, right_wrist)
                angle.append(int(angle1))
                angle2 = calculateAngle(left_shoulder, left_elbow, left_wrist)
                angle.append(int(angle2))
                angle3 = calculateAngle(right_elbow, right_shoulder, right_hip)
                angle.append(int(angle3))
                angle4 = calculateAngle(left_elbow, left_shoulder, left_hip)
                angle.append(int(angle4))
                angle5 = calculateAngle(right_shoulder, right_hip, right_knee)
                angle.append(int(angle5))
                angle6 = calculateAngle(left_shoulder, left_hip, left_knee)
                angle.append(int(angle6))
                angle7 = calculateAngle(right_hip, right_knee, right_ankle)
                angle.append(int(angle7))
                angle8 = calculateAngle(left_hip, left_knee, left_ankle)
                angle.append(int(angle8))

                compare_pose(image, angle_point,angle, angle_target)
                a_score = diff_compare_angle(angle,angle_target)

                if (p_score >= a_score):
                    cv2.putText(image, str(int((1 - a_score)*100)), (80,30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)

                else:
                    cv2.putText(image, str(int((1 - p_score)*100)), (80,30), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)

            except:
                pass

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                     mp_drawing.DrawingSpec(color = (0,0,255), thickness = 4, circle_radius = 4),
                                     mp_drawing.DrawingSpec(color = (0,255,0),thickness = 3, circle_radius = 3)
                                      )
            cv2.imshow('MediaPipe Feed',image)


            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            if (kb.is_pressed("right")):
                # print("changed pose")
                # print("cuurent pose", current_pose)
                if current_pose <= 10:
                    kb.press('space')
                    kb.release('space')
                    current_pose += 1
                    path = "yogapose/yoga" + str(current_pose) + ".jpg"
                    # print(path)
                    x = extractKeypoint(path)
                    dim = (560,800)
                    resized = cv2.resize(x[3], dim, interpolation = cv2.INTER_AREA)
                    cv2.imshow('target',resized)
                    angle_target = x[2]
                    point_target = x[1]
                    
                else:
                    # print("changed pose")
                    # print("cuurent pose", current_pose)
                    kb.press('space')
                    kb.release('space')
                    current_pose = 2
                    path = "yogapose/yoga" + str(current_pose) + ".jpg"
                    # print(path)
                    x = extractKeypoint(path)
                    dim = (560,800)
                    resized = cv2.resize(x[3], dim, interpolation = cv2.INTER_AREA)
                    cv2.imshow('target',resized)
                    angle_target = x[2]
                    point_target = x[1]
                                                        
            if (kb.is_pressed("left")):
                if current_pose > 3:
                    # print('hereee')
                    # print("changed pose")
                    # print("cuurent pose", current_pose)
                    kb.press('space')
                    kb.release('space')
                    current_pose -= 1
                    path = "yogapose/yoga" + str(current_pose) + ".jpg"
                    # print(path)
                    x = extractKeypoint(path)
                    dim = (560,800)
                    resized = cv2.resize(x[3], dim, interpolation = cv2.INTER_AREA)
                    cv2.imshow('target',resized)
                    angle_target = x[2]
                    point_target = x[1]
                    
                # else:
                else:
                    # print('hereee')
                    # print("changed pose")
                    # print("cuurent pose", current_pose)
                    kb.press('space')
                    kb.release('space')
                    current_pose = 11
                    # kb.press('space')
                    # kb.release('space')
                    path = "yogapose/yoga" + str(current_pose) + ".jpg"
                    print(path)
                    x = extractKeypoint(path)
                    dim = (560,800)
                    resized = cv2.resize(x[3], dim, interpolation = cv2.INTER_AREA)
                    cv2.imshow('target',resized)
                    angle_target = x[2]
                    point_target = x[1]                
                
        cap.release()
        cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)

def toRun():
    change_pose(path = "yogapose/yoga" + str(current_pose) + ".jpg")


def main_loop():
        # title = '<p style="roboto; color:Black; font-size: 42px; font-weight: 700;">At home YOGA...  <br>with AI trainer</p>'
    
    
    # st.title(title)
    st.subheader("YOGA TRAINING APP")
    st.subheader("At home YOGA...  \nwith AI trainer")
    
    # st.markdown(title, unsafe_allow_html=True)
    # st.text(title)

    def add_bg_from_url():
        st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.template.net/96208/aesthetic-international-yoga-day-wallpaper-aoew4.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

    add_bg_from_url() 

    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(255, 194, 153);
        color: Black;
        font-weight: 700;
    }
    </style>""", unsafe_allow_html=True)

    # b = st.button("LAUNCH")
    
    if st.button("LET'S BEGIN"):
        st.text("Wait for few seconds.....")
        toRun()
        # instructions = '<p style="roboto; color:Black; font-size: 42px; font-weight: 700;">At home YOGA...  <br>with AI trainer</p>'
    # st.markdown(instructions, unsafe_allow_html=True)

    # if st.checkbox("Main Checkbox"):
    #     st.text("Check Box Active")
    #     toRun()

    st.sidebar.text("INSTRUCTIONS - ")
    st.sidebar.text("-> Click on 'Let's Begin' button to launch camera")
    st.sidebar.text("-> Make sure your device has access to the camera")
    st.sidebar.text("-> Stand afar from the device")
    st.sidebar.text("-> To change pose click on left/right buttons of the keyboard")
    st.sidebar.text("-> Score will get displayed on the screen with instructions")
    st.sidebar.text("GOOD LUCK")
    
if __name__ == '__main__':
    main_loop()
