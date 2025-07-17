# from ultralytics import YOLO

# model = YOLO("best.pt")
# model.export(format="onnx")
# import onnx
# from onnx_tf.backend import prepare

# model = onnx.load("best.onnx")
# tf_rep = prepare(model)
# tf_rep.export_graph("best_tf")

import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

img = cv2.imread("debug1.jpg")  # saved from your web app
results = model.predict(img, conf=0.1)

results[0].show()  # open image with detection
