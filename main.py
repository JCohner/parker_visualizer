import signal
import sys
import time
import os

from multiprocessing import Process, Value
from ctypes import c_bool

import cv2 as cv
import numpy as np

class Visualizer():
  def __init__(self):
    '''
    function generation values
    '''
    self.step = 804 # number of points that make up the curve, increase to get line
    self.t = np.linspace(-np.pi, np.pi, self.step)
    self.A = 80 # TODO: unused
    self.B = 100 # TODO: unused
    self.a = 5
    self.b = 4
    self.theta_step = 60
    self.theta_index = 0
    self.deltas = np.linspace(0, 2 * np.pi, self.theta_step)
    self.x = (256 * np.sin(self.a * self.t)).astype(int) + 512
    self.y = (256 * np.sin(self.b*self.t)).astype(int) + 512

    '''
    opencv representation values
    '''
    self.window_x = 1024
    self.window_y = 1024
    self.movie = np.zeros((1024,1024,3,self.deltas.shape[0]))

    '''
    runtime values
    '''
    self.should_run = Value(c_bool, False)
    self.work_proc = Process(target=self.work_func)

  def start_run(self):
    self.should_run.value = True
    self.work_proc.run()

  def stop_run(self, sig, sign_frame):
    self.should_run.value = False
    if (self.work_proc.is_alive()):
      self.work_proc.join()
    sys.exit(0)

  def work_func(self):    
    color = 0
    image = np.zeros((self.window_x, self.window_y, 3))
    for m in range(self.theta_step):
      now = time.time()
      if (not self.should_run.value):
          break
      for i in range(self.step):
        image *= 0.99
        cv.circle(image, (self.x[i%self.step], self.y[i%self.step]), 4, (255, 0 ,255), -1)
      self.movie[:,:,:,m] = image
      print(f"time elapsed: {(time.time() - now):.2f}\r")
      self.x = (256 * np.sin(self.a * self.t + self.deltas[self.theta_index])).astype(int) + 512
      self.theta_index += 1
      color = (color + 30) % 255
      cv.waitKey(30)

    while(self.should_run.value):
      for i in range(self.theta_step):
        print(f"running {i}")
        cv.imshow("image", self.movie[:,:,:,i])
        cv.waitKey(20)

  def is_working(self):
    return self.should_run.value

if __name__ == "__main__":
  egg = Visualizer()
  signal.signal(signal.SIGINT, egg.stop_run)
  egg.start_run()
  while(egg.is_working()):
    time.sleep(0.5)