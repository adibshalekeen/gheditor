import cv2
import numpy as np
class ConsolidatedVideo:
    def __init__(self, videos, params):
        self._videos = videos
        self._params = params
        
        self._video_captures = []
        for video in self._videos:
            self._video_captures.append(cv2.VideoCapture(video))

        self._video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (1920, 1080))
        self.consolidate_video()

    def consolidate_video(self):
        consolidating = True
        frames = []
        while consolidating:
            output_frame = np.zeros(shape=(1080,1920,3))
            for cap in self._video_captures:
                ret , frame = cap.read()
                consolidating = ret
                if not ret:
                    break
                frame = cv2.resize(frame, dsize=(int(1920/len(self._videos)), 1080))
                frames.append(frame)
            horizontal_slice = int(1920/len(self._videos))
            for i in range(0, len(frames)):
                output_frame[:, (i*horizontal_slice):((i+1)*horizontal_slice), :] = frames[i]
            output_frame = np.uint8(output_frame)
            self._video_writer.write(output_frame)
            print(output_frame.shape)
            cv2.imshow('frame', output_frame)
            frames.clear()
            cv2.waitKey(1)
        self._video_writer.release()
        for cap in self._video_captures:
            cap.release()

    def extract_dims(self):
        self._video_dimensions = {"fx": 0, "fy":0, "spans":[]}
        min_x = 20
        min_y = 20
        for dim in self._params["dims"]:
            if dim[0] < min_x:
                min_x = dim[0]

videos = ['./1.mp4', './2.mp4', './3.mp4']
params = {"dims":[[2,2,1], [2,2,2], [2,1,1]]}
vid = ConsolidatedVideo(videos, params)