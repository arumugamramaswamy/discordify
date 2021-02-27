import cv2

def to_gray(img):
    if len(img.shape) == 2:
        return img
    if img.shape[-1] == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def histogram_eq(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return cv2.equalizeHist(img)

def otsu_thresholding(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 

def canny(img):
    return cv2.Canny(img,100,200)
 
def contour_detection(image):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = cv2.drawContours(image, contours, -1, (0,255,0), 3) 
    return cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB)

def gaussian_blur(img):
    blurred = cv2.GaussianBlur(img,(15,15),0)
    return cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
