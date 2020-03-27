import cv2


dim = (640,480) #for logitech
#dim = (704,576)  #IP CAM

images =[]

for i in range(1,12):
    images.append(cv2.resize(cv2.imread("%s.jpg" % str(i),cv2.IMREAD_COLOR),dim,interpolation= cv2.INTER_AREA))


stitcher = cv2.Stitcher_create()
ret, panorama = stitcher.stitch(images)

if ret == cv2.STITCHER_OK:
    cv2.imshow("PANAROMA",panorama)
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("STITCH ERROR")

