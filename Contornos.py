# # import the necessary packages
# import numpy as np
# import argparse
# import imutils
# import cv2
# def sort_contours(cnts, method="left-to-right"):
# 	# initialize the reverse flag and sort index
# 	reverse = False
# 	i = 0
# 	# handle if we need to sort in reverse
# 	if method == "right-to-left" or method == "bottom-to-top":
# 		reverse = True
# 	# handle if we are sorting against the y-coordinate rather than
# 	# the x-coordinate of the bounding box
# 	if method == "top-to-bottom" or method == "bottom-to-top":
# 		i = 1
# 	# construct the list of bounding boxes and sort them from top to
# 	# bottom
# 	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
# 	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
# 		key=lambda b:b[1][i], reverse=reverse))
# 	# return the list of sorted contours and bounding boxes
# 	return (cnts, boundingBoxes)
#
# def draw_contour(image, c, i):
# 	# compute the center of the contour area and draw a circle
# 	# representing the center
# 	M = cv2.moments(c)
# 	cX = int(M["m10"] / M["m00"])
# 	cY = int(M["m01"] / M["m00"])
# 	# draw the countour number on the image
# 	cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
# 		1.0, (0, 0, 255), 2)
# 	# return the image with the contour number drawn on it
# 	return image
#
# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# # ap.add_argument("-i", "--image", required=True, help="Path to the input image")
# # ap.add_argument("-m", "--method", required=True, help="Sorting method")
# args = vars(ap.parse_args())
# # load the image and initialize the accumulated edge image
# image = cv2.imread(r'Imagenes/pliegomitad.jpg')
# accumEdged = np.zeros(image.shape[:2], dtype="uint8")
# # loop over the blue, green, and red channels, respectively
# for chan in cv2.split(image):
# 	# blur the channel, extract edges from it, and accumulate the set
# 	# of edges for the image
# 	chan = cv2.medianBlur(chan, 11)
# 	edged = cv2.Canny(chan, 200, 255)
# 	accumEdged = cv2.bitwise_or(accumEdged, edged)
# # show the accumulated edge map
# imgResizeie = cv2.resize(accumEdged , (1600, 800))
# cv2.imshow("Edge Map", imgResizeie)
#
# # find contours in the accumulated image, keeping only the largest
# # ones
# cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
# l1v = cv2.line(image, ( 3700,  70), ( 3680, 3000), (0, 0, 0), 8)
# l1h = cv2.line(image, (180, 70), (3705,  70), (0, 0, 0), 8)
# orig = image.copy()
# # loop over the (unsorted) contours and draw them
# for (i, c) in enumerate(cnts):
# 	orig = draw_contour(orig, c, i)
# # show the original, unsorted contour image
# imgResizeiu = cv2.resize(orig , (1600, 800))
# cv2.imshow("Unsorted", imgResizeiu)
# # sort the contours according to the provided method
# cnts, boundingBoxes = sort_contours(cnts)
# # loop over the (now sorted) contours and draw them
# for (i, c) in enumerate(cnts):
# 	draw_contour(image, c, i)
# # show the output image
# imgResizei = cv2.resize(image , (1600, 800))
# cv2.imshow("Sorted", imgResizei)
# cv2.waitKey(0)


import cv2
import numpy as np

original_image = cv2.imread(r'Imagenes/pliegomitad.jpg')
image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

ret, image = cv2.threshold(image, 70, 255, 0)

# cv2.imshow("image",image)


contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

sorted_contours = sorted(contours, key=cv2.contourArea, reverse=False)[:3]

for i, cnt in enumerate(sorted_contours):
	m = cv2.moments(cnt)
	cx = int(m["m10"] / m["m00"])
	cy = int(m["m01"] / m["m00"])

	cv2.drawContours(original_image, [cnt], -1, (200, 100, 0), 3)
	cv2.putText(original_image, str(i + 1), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 0), 1)

	cv2.imshow("sorted", original_image)
	cv2.waitKey()
# cv2.imshow("original_image",original_image)
cv2.waitKey()
cv2.destroyAllWindows()