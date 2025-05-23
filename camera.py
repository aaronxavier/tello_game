import cv2
import yaml
import os
import rclpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import threading

DETECTIONS_FILE = 'detections.yaml'

class Camera:
    def __init__(self, device=0, frame_w=640, frame_h=480, use_topic=False, topic='/image_raw'):
        self.use_topic = use_topic
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.detections = set()
        self.current_detection = ''
        self.clear_detections()
        self.last_frame = None
        if use_topic:
            self.bridge = CvBridge()
            self.topic = topic
            self._ros_thread = threading.Thread(target=self._ros_spin, daemon=True)
            self._ros_thread.start()
        else:
            self.cap = cv2.VideoCapture(device)
            self.detector = cv2.QRCodeDetector()

    def _ros_spin(self):
        rclpy.init()
        self.node = rclpy.create_node('camera_reader')
        self.detector = cv2.QRCodeDetector()
        self.node.create_subscription(Image, self.topic, self._ros_callback, 10)
        while rclpy.ok():
            rclpy.spin_once(self.node, timeout_sec=0.1)
        self.node.destroy_node()
        rclpy.shutdown()

    def _ros_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        frame = cv2.resize(cv_image, (self.frame_w, self.frame_h))
        self.last_frame = frame

    def clear_detections(self):
        with open(DETECTIONS_FILE, 'w') as f:
            yaml.dump([], f)
        self.detections = set()

    def save_detections(self):
        with open(DETECTIONS_FILE, 'w') as f:
            yaml.dump(sorted(list(self.detections)), f)

    def get_frame_and_detect(self):
        if self.use_topic:
            frame = self.last_frame
            if frame is None:
                return None, ''
            data, bbox, _ = self.detector.detectAndDecode(frame)
        else:
            ret, frame = self.cap.read()
            if not ret:
                return None, ''
            frame = cv2.resize(frame, (self.frame_w, self.frame_h))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
        if not self.use_topic:
            self.cap.release()
