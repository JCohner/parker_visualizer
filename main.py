import time

import cv2 as cv
import numpy as np


step = 804 # number of points that make up the curve, increase to get line
t = np.linspace(-np.pi, np.pi, step)
A = 80
B = 100
a = 5
b = 4
theta_step = 60
theta_index = 0
deltas = np.linspace(0, 2 * np.pi, theta_step)
x = (256 * np.sin(a * t)).astype(int) + 512
y = (256 * np.sin(b*t)).astype(int) + 512

window_x = 1024
window_y = 1024

movie = np.zeros((1024,1024,3,deltas.shape[0]))

def main():
	global x, delta, theta_index
	
	# TODO: what does 1000 mean in this context
	color = 0
	image = np.zeros((window_x, window_y, 3))
	for m in range(theta_step):
		now = time.time()
		for i in range(step):
			image *= 0.99
			cv.circle(image, (x[i%step], y[i%step]), 4, (255, 0 ,255), -1)
		movie[:,:,:,m] = image
		print(f"time elapsed: {time.time() - now}\r")
		x = (256 * np.sin(a * t + deltas[theta_index])).astype(int) + 512
		theta_index += 1
		color = (color + 30) % 255
		cv.waitKey(30)

	while(True):
		for i in range(theta_step):
			cv.imshow("image", movie[:,:,:,i])
			cv.waitKey(20)


if __name__ == "__main__":
	main()
