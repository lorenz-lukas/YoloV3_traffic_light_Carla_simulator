import cv2
import numpy as np
from tensorflow_yolov3.carla.config import cfg
from tensorflow_yolov3.carla.utils import read_class_names
from log import Log
from os import listdir

class Light(Log):
    state = None
    classes = None
    bbx = []
    scores = []
    img_index = 0
    score_th = 0.50
    key = None

    def __init__(self, town = "town01" ):
        self.classes = read_class_names(cfg.YOLO.CLASSES)
        Log.__init__(self, "carla_dataset", town)

    def __del__(self):
        pass
    
    def getScore_Label(self, bboxes):
        for i, bbox in enumerate(bboxes):
            if(self.classes[bbox[5]] == "traffic light" and bbox[4] >= self.score_th):
                self.bbx.append([int(bbox[1]), int(bbox[3]), int(bbox[0]) , int(bbox[2])])
                self.scores.append(bbox[4])

    def get_state(self,frame, score):
        self.state = None
        # MASK
        (B, G, R) = cv2.split(frame)
        R[R < 200] = 0
        G[G < 200] = 0
        B[B > 0] = 0
        frame = cv2.merge([B,G,R])

        if(frame[..., 1].max() == 255 and not frame[..., 2].max() == 255):
            self.state = "{}, {}".format("Green", score)
        elif(frame[..., 2].max() == 255 and frame[..., 1].mean() < 20):
            self.state = "{}, {}".format("Red",score )
        elif(frame[..., 1].max() == 255 and frame[..., 2].max() == 255):
            self.state = "{}, {}".format( "Yellow", score)
        
        return frame

    def process_traffic_light(self, frame, bboxes):
        self.getScore_Label(bboxes)
        key = None
        semaphore = np.zeros_like(frame)
        j = 0
        bbox = None
        for i in range(0,len(self.bbx)):
            semaphore = frame[self.bbx[i][0]:self.bbx[i][1], self.bbx[i][2]:self.bbx[i][3]]    
            if(semaphore.shape[0] > 0 and semaphore.shape[1] > 0 and np.mean(semaphore) > 0):
                semaphore_color = self.get_state(semaphore, self.scores[i])
                # print(self.state)
                cv2.imshow("Traffic Light", semaphore)
                cv2.imshow("Traffic Light COLOR", semaphore_color)
                self.key = cv2.waitKey(1) & 0xFF

                if(self.key == ord("r")):
                    self.img_index+=1
                    print("bbx ",self.bbx[i])
                    cv2.imwrite("data/{}.png".format(self.img_index), semaphore)
                    cv2.imwrite("data/frame_{}.png".format(self.img_index), frame)
                if(self.state is not None):
                    bbox = [(self.bbx[i][2], self.bbx[i][0]), (self.bbx[i][3], self.bbx[i][1])]
                    break
            j+=1
        self.bbx = []
        self.scores = []
        return bbox
        

if __name__ == "__main__":
    l = Light()
    im_list = listdir("data/")
    base_dir = "data/"

    for im in im_list:
        print(im)
        img = cv2.imread(base_dir + im)
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = l.Hog(img, 0)
        print("Result = {}".format(l.state))
        cv2.imshow("Traffic Light", img)
        key = cv2.waitKey(0) & 0xFF
        if(key == ord("q")):
            break
    
