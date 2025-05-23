import cv2
import yaml
import os

DETECTIONS_FILE = 'detections.yaml'

class Camera:
    def __init__(self, device=8, frame_w=640, frame_h=480):
        self.cap = cv2.VideoCapture(device)
        self.detector = cv2.QRCodeDetector()
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.detections = set()
        self.current_detection = ''
        self.clear_detections()

    def clear_detections(self):
        with open(DETECTIONS_FILE, 'w') as f:
            yaml.dump([], f)
        self.detections = set()

    def save_detections(self):
        with open(DETECTIONS_FILE, 'w') as f:
            yaml.dump(sorted(list(self.detections)), f)

    def get_frame_and_detect(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, ''
        frame = cv2.resize(frame, (self.frame_w, self.frame_h))
        data, bbox, _ = self.detector.detectAndDecode(frame)
        if data:
            self.current_detection = data
            if data not in self.detections:
                self.detections.add(data)
                self.save_detections()
        else:
            self.current_detection = ''
        return frame, self.current_detection

    def release(self):
        self.cap.release()
