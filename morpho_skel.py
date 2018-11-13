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
        # Otsu's thresholding after Gaussian filtering
        # blur = cv2.GaussianBlur(self.img,(5,5),0)
        # ret3,bin_img = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        # bin_img = cv2.adaptiveThreshold(self.img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #     cv2.THRESH_BINARY,11,2)

        self.detect_contours(self.img)
        
        ret, bin_img = cv2.threshold(self.img, 127, 255, cv2.THRESH_TOZERO)
        ret, bin_img = cv2.threshold(bin_img, np.min(bin_img), 255, cv2.THRESH_BINARY)

        # cv2.imshow("bin", bin_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 3x3 cross-shaped kernel (4-connexity)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)) #MORPH_CROSS
        self.img = bin_img
        return element

    # def detect_blobs(self, im):      
    #     # Set up the detector with default parameters.
    #     detector = cv2.SimpleBlobDetector_create()
         
    #     # Detect blobs.
    #     keypoints = detector.detect(im)
    #     print(keypoints)
         
    #     # Draw detected blobs as red circles.
    #     # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    #     im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #     cv2.imshow("Keypoints", im_with_keypoints)
    #     cv2.waitKey(0)

    def detect_contours(self, im): 
        ret, blob_img = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY_INV)
        im2, contours, hierarchy = cv2.findContours(blob_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        cv2.drawContours(im2, contours, -1, (139,0,0), 3)
        cv2.imshow("Keypoints", im2)
        cv2.waitKey(0)


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
    # ms = MorphoSkel('example.png')
    element = ms.get_binary()
    ms.get_skeleton(element)
    ms.show_img()

if __name__ == '__main__': 
    main()

