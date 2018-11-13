import cv2
import numpy as np

class MorphoSkel(): 

    def __init__(self, i): 
        self.orig_img = cv2.imread(i, 0)
        self.img = cv2.imread(i, 0)
        self.size = np.size(self.img)
        self.skel = np.zeros(self.img.shape, np.uint8)
        # self.isVideo = isVideo

    def get_binary(self): 
        ret, bin_img = cv2.threshold(self.img, 127, 255, 0)
        # 3x3 cross-shaped kernel (4-connexity)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)) #MORPH_CROSS
        self.img = bin_img
        return element

    def get_skeleton(self, element): 
        done = False 

        while not done: 
            # remove some of the white space 
            eroded = cv2.erode(self.img, element)
            # bring a little back 
            temp = cv2.dilate(eroded, element)
            # get diff 
            temp = cv2.subtract(self.img, temp)
            # re-binarize and smooth skeleton
            self.skel = cv2.bitwise_or(self.skel, temp)
            # 
            self.img = eroded.copy()

            zeros = self.size - cv2.countNonZero(self.img)
            if zeros == self.size: 
                done = True

    def get_skeleton2(self, element): 
        done = False 

        while not done: 
            # erosion + dilation to remove noise 
            temp = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, element)
            temp = cv2.bitwise_not(temp, temp)
            temp = cv2.bitwise_and(self.img, temp, temp)
            self.skel = cv2.bitwise_or(self.skel, temp)
            self.img = cv2.erode(self.img, element)

            zeros = self.size - cv2.countNonZero(self.img)
            if zeros == self.size: 
                done = True

    def show_img(self): 
        cv2.imshow("skel", self.skel)
        cv2.imshow("img", self.orig_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main(): 
    ms = MorphoSkel('depth_example.png')
    element = ms.get_binary()
    ms.get_skeleton(element)
    ms.show_img()

if __name__ == '__main__': 
    main()

