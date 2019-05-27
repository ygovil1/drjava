import os
import numpy as np
import tensorflow as tf

charset = {'0': 0,  '1': 1,  '2': 2,  '3': 3,  '4': 4,  '5': 5,
           '6': 6,  '7': 7,  '8': 8,  '9': 9,  'A': 10, 'B': 11,
           'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17,
           'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23,
           'O': 24, 'P': 25, 'R': 26, 'S': 27, 'T': 28, 'U': 29,
           'V': 30, 'X': 31, 'Z': 32, '<': 33, '>': 34, '(': 35,
           ')': 36, '$': 37, '#': 38, '^': 39, 's': 40, '-': 41,
           '*': 42, '%': 43, '?': 44, '!': 45, '+': 46} # <nul> = +

class CharacterRecognizer:
  def __init__(self, graph_path=None):
    self.graph_path = graph_path
    self.session = None
    self.input = None
    self.output = []
    self.class_num = 1

    self.idx_lbl = {}
    for key in charset.keys():
      self.idx_lbl[charset[key]] = key
    self.__init_recognizer__()
    print('Character recognizer initialized!')

  def __init_recognizer__(self):

    # load graph and label map from default folder
    if self.graph_path is None:
      self.graph_path = './frozen_model/ocr_graph.pb'

    # check existence of the two files
    if not os.path.exists(self.graph_path):
      raise IOError('Invalid ocr_graph path! {}'.format(self.graph_path))

    # load frozen graph
    detection_graph = tf.Graph()
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(self.graph_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    self.session = tf.Session(graph=detection_graph)

    # prepare input and output request
    self.input = detection_graph.get_tensor_by_name('ocr_input:0')
    # self.output.append(detection_graph.get_tensor_by_name('chars_logit:0'))
    # self.output.append(detection_graph.get_tensor_by_name('chars_log_prob:0'))
    self.output.append(detection_graph.get_tensor_by_name('predicted_chars:0'))
    self.output.append(detection_graph.get_tensor_by_name('predicted_scores:0'))
    # self.output.append(detection_graph.get_tensor_by_name('predicted_text:0'))

  def clear_session(self):
    if self.session is not None:
      self.session.close()

  def predict(self, image_np):
    assert image_np.shape == (180, 180, 3)
    img_in = np.expand_dims(image_np, axis=0)
    codes, scores = self.session.run(self.output, feed_dict={self.input: img_in})
    codes, scores = [np.squeeze(x) for x in [codes, scores]]

    score_ave = 0
    text = ''
    for char, score in zip(codes, scores):
      if not self.idx_lbl[char] == '+':
        score_ave += score
        text += self.idx_lbl[char]
    score_ave /= len(text)

    return text, score_ave