import cv2
import time
import numpy as np
import tensorflow as tf
from button_detection import ButtonDetector
from character_recognition import CharacterRecognizer

class Recognizer:
    def __init__(self, buttonGraph = None, charGraph = None, buttonLabel = None, verbose = True):
        self.detector = ButtonDetector(buttonGraph, buttonLabel)
        self.recognizer = CharacterRecognizer(charGraph)
        self.verbose = verbose
        print('Recognizer ready!')

    def __button_candidates__(self, boxes, scores, image):
        img_height = image.shape[0]
        img_width = image.shape[1]

        button_scores = []
        button_patches = []
        button_positions = []

        for box, score in zip(boxes, scores):
            if score < 0.5: continue

            y_min = int(box[0] * img_height)
            x_min = int(box[1] * img_width)
            y_max = int(box[2] * img_height)
            x_max = int(box[3] * img_width)

            button_patch = image[y_min: y_max, x_min: x_max]
            button_patch = cv2.resize(button_patch, (180, 180))

            button_scores.append(score)
            button_patches.append(button_patch)
            button_positions.append([x_min, y_min, x_max, y_max])
        
        return button_patches, button_positions, button_scores 
        
    # takes in PIL image
    # returns bounding box of button, recognized character
    def recognize(self, image):
      start = time.time()  
      
      img_np = np.asarray(image)
      boxes, scores, _ = self.detector.predict(img_np)
      button_patches, button_positions, _ = self.__button_candidates__(boxes, scores, img_np)

      button_text = []
      for button_img, button_pos in zip(button_patches, button_positions):
        text, score = self.recognizer.predict(button_img)
        button_text.append(text)

      end = time.time()
      if (self.verbose): 
          print('Recognition completed in %f seconds' % (end - start))
          return button_positions, button_text
      else:
          return button_positions, button_text, end - start