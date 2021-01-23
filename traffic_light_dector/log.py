import csv
from datetime import datetime
import argparse

import numpy as np
from math import ceil
import cv2

class Log:

    base_dir = "Dataset/"
    log_cvs_file_name = "carla_dataset"
    data = {"Filename":[], "Annotation tag": [], "Upper left corner X": [], "Upper left corner Y": [],
            "Lower right corner X": [], "Lower right corner Y": [], "Origin file": [],
            "Origin frame number": [], "Origin track": [], "Origin track frame number": []}
    town = "town01"    
    header_list = []
    scale = 2.70 # w/h

    def __init__(self, file_name = None, town = None):
        now = datetime.now()
        local_time = now.strftime("%d_%m_%Y-H_%M_%S_")
        
        if(town is None):
            town  = self.town
        else:
            self.town = town

        if(file_name is None):
            self.log_cvs_file_name = self.base_dir + local_time + self.log_cvs_file_name + "_" + town + ".csv"
        else: 
            self.log_cvs_file_name = self.base_dir + local_time + file_name + "_" + town + ".csv"
        
        self.getHeaders_list()

    def __del__(self):
        pass
    
    def getHeaders_list(self):
        for key in self.data.items():
            self.header_list.append(key[0])
            
    def retifyBBx(self, bbx):
        w_h = (bbx[1]-bbx[0])/ (bbx[3] - bbx[2]) #w/h
        print(w_h)
        if( w_h < self.scale):
            print("Retified {}".format(self.scale - w_h))
            bbx[0] = ceil(bbx[0] * 1 + (self.scale))
            bbx[1] = ceil(bbx[1] * 1 + (self.scale))
            bbx[2] = ceil(bbx[2] * 1 + (self.scale))
            bbx[3] = ceil(bbx[3] * 1 + (self.scale))
            print((bbx[1]-bbx[0])/ (bbx[3] - bbx[2]))
        print(bbx)

        return bbx    
    def getData(self, frame, frame_num, bbx, label):
        self.data["Filename"].append(self.town + "_" + str(frame_num))
        self.data["Annotation tag"].append(label)
        self.data["Upper left corner X"].append(bbx[0])
        self.data["Upper left corner Y"].append(bbx[2])
        self.data["Lower right corner X"].append(bbx[1])
        self.data["Lower right corner Y"].append(bbx[3])
        self.data["Origin file"].append("None")
        self.data["Origin frame number"].append(frame_num)
        self.data["Origin track"].append("None")
        self.data["Origin track frame number"].append(frame_num)
        cv2.imwrite(self.base_dir + "/Img/" + self.data["Filename"] + self.img_extension, frame)

    def recDataCSV(self):
        # names=self.header_list
        # rows = zip(list1,list2,list3,list4,list5)
        print(self.log_cvs_file_name)
        row = ""
        with open(self.log_cvs_file_name,'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.header_list)
            writer.writeheader()
            writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(self.data["Filename"])):
                for j in self.header_list:
                    row += str(self.data[j][i])
                    row += ";"
                print(row)
                writer.writerow(row)
                row = ""
            csvfile.close()


def correctBBx(frame, bbx):
    state = None
    i = 0
    j = 0
    q = False
    # MASK
    (B, G, R) = cv2.split(frame)
    R[R < 200] = 0
    G[G < 200] = 0
    B[B > 0] = 0

    frame = cv2.merge([B,G,R])    
    # cv2.imshow("frame", frame)
    # cv2.waitKey(0)
    
    for i in range(0, frame.shape[0]):
        for j in range(0, frame.shape[1]):
            if(np.mean(frame[i][j]) > 0 and np.mean(frame[i][j+1]) > 0 and np.mean(frame[i][j+2]) > 0):
                q = True
                break
        if(q == True):
            break

    if(frame[..., 1].max() == 255 and not frame[..., 2].max() == 255):
        state ="Green"
        print(i, j)
        if(i >= 5):
            bbx[0] -= 2*i
            bbx[1] -= 2*i

    elif(frame[..., 2].max() == 255 and frame[..., 1].mean() < 20):
        state = "Red"
        if(i <= 5):
            bbx[0] += i
            bbx[1] += i

    elif(frame[..., 1].max() == 255 and frame[..., 2].max() == 255):
        state = "Yellow"

def main():
    # bbx = []
    # bbx.append([478, 505, 1089, 1102])
    # bbx.append([477, 504, 1088, 1101])
    # bbx.append([499, 527, 1120, 1135])
    # bbx.append([478, 512, 1117, 1133])
    # bbx.append([477, 512, 1117, 1134])
    # bbx.append([483, 510, 1034, 1049])
    # bbx.append([483, 509, 1033, 1047])
    # bbx.append([498, 518, 1036, 1049])
    # bbx.append([498, 518, 1036, 1049])
    # bbx.append([499, 518, 1038, 1051])
    # bbx.append([498, 518, 1036, 1050])
    # bbx.append([499, 519, 1038, 1051])

    log = Log()
    # i=3
    # bbx[i-1] = log.retifyBBx(bbx[i-1])
    
    # frame = cv2.imread("data/frame_{}.png".format(i))
    # frame_cropped = frame[bbx[i-1][0]:bbx[i-1][1], bbx[i-1][2]:bbx[i-1][3]]
    # print(bbx[i-1])
    
    # bbx[i] = correctBBx(frame_cropped, bbx[i])
    # cv2.imshow("frame", frame_cropped)
    # cv2.waitKey(0)
    
    # print(bbx[i-1])

    # frame_cropped = frame[bbx[i-1][0]:bbx[i-1][1], bbx[i-1][2]:bbx[i-1][3]]
    # cv2.imshow("frame", frame_cropped)
    # cv2.waitKey(0)
    
    log.getData(0, [1,1,1,1], "go")
    log.getData(1, [1,1,1,1], "go")
    log.recDataCSV()

if __name__ == "__main__":
    main()