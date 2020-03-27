import cv2


def merge_smart(n):
    list =[]
    for i in range(1,n+1):
        list.append(i)

    if n%2 ==0:
        a = list[int(n/2):n]
        b = list[0:int(n/2)]
    else:
        a = list[int(n/2 +1):n]
        b = list[0:int(n/2 +1)]
    list = a+b
    return list



dim = (640,480) #for logitech
#dim = (704,576)  #IP CAM

images =[]

pan_list = merge_smart(36)

for i in range(1,37):

    images.append(cv2.resize(cv2.imread("%s.jpg" % str(i),cv2.IMREAD_COLOR),dim,interpolation= cv2.INTER_AREA))



stitcher = cv2.Stitcher_create()
ret, panorama = stitcher.stitch(images)

if ret == cv2.STITCHER_OK:
    cv2.imshow("PANAROMA",panorama)
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("STITCH ERROR")


