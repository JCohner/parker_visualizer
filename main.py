import signal
import sys
import time
import os
import argparse

from multiprocessing import Process, Value
from ctypes import c_bool

import cv2 as cv
import numpy as np

class Visualizer():
  def __init__(self, args):
    '''
    function generation values
    '''
    self.step = 402 # number of points that make up the curve, increase to get line
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
    argparse things
    '''
    self.should_display = args.display
    self.should_generate = args.generate
    # hacky josh way of generating the file path we should save to
    self.should_save = False if args.save == "" else True # set boolean value to true, meaning we should save files IF a file path was specified
    self.form_of_file_path = lambda inp: f"{args.save}_{inp}.png"
    save_dir = args.save.split('/')[0]
    # directory needs to exist if we want to save it to that directory
    if (self.should_save and not os.path.isdir(save_dir)):
      # warn: only works for single level directory
      print(f"making directory: {save_dir}")
      os.mkdir(save_dir)
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

  def generate(self):
    color = 0
    image = np.zeros((self.window_x, self.window_y, 3))
    for frame in range(self.theta_step):
      now = time.time()
      if (not self.should_run.value):
          break
      for circle_idx in range(self.step):
        image *= 0.99
        cv.circle(image, (self.x[circle_idx%self.step], self.y[circle_idx%self.step]), 4, (color, 0 ,255), -1)
      self.movie[:,:,:,frame] = image
      if (self.should_save):
        cv.imwrite(self.form_of_file_path(frame), image)

      print(f"time elapsed: {(time.time() - now):.2f} [seconds / rendered_frame] |\t frame count: {frame+1}/{self.theta_step}\r", end="")
      self.x = (256 * np.sin(self.a * self.t + self.deltas[self.theta_index])).astype(int) + 512
      self.theta_index += 1
      color = (color + 10) % 255

  def display(self):
    for frame in range(self.theta_step):
      print(f"running {frame}\r", end="")
      # implcitly: if we have generated frames this run: display those. if not read in frames from save location
      if (self.should_generate):
        cv.imshow("image", self.movie[:,:,:,frame])
      else:
        cv.imshow("image", cv.imread(self.form_of_file_path(frame)))
      cv.waitKey(20)

  def work_func(self):    
    if (self.should_generate):
      self.generate()

    if (self.should_display):
      while(self.should_run.value):
        self.display()

    print("")
    self.should_run.value = False

  def is_working(self):
    return self.should_run.value


def build_parser():
  parser = argparse.ArgumentParser(prog='visualizer.py')
  parser.add_argument("-generate", "-g", type=bool, default=False, help="Should we generate images (time intensive)")
  parser.add_argument("-save", "-s", type=str, default="", help="form of filepath to save image to")
  parser.add_argument("-display", "-d", type=bool, default=False, help="should we display the movie")
  return parser

if __name__ == "__main__":
  # parse args
  parser = build_parser()
  args = parser.parse_args()

  egg = Visualizer(args)
  signal.signal(signal.SIGINT, egg.stop_run)
  egg.start_run()
  while(egg.is_working()):
    time.sleep(0.5)