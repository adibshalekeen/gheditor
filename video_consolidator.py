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
        while consolidating:
            output_frame = np.zeros(shape=(1080,1920,3))
            for i in range(0, len(self._video_captures)):
                ret , frame = self._video_captures[i].read()
                consolidating = ret
                if not ret:
                    break
                
                slice_height = int(1080 / self._params["dims"][i][0])
                slice_width = int(1920 / self._params["dims"][i][1])

                frame = cv2.resize(frame, dsize=(slice_width, slice_height))

                slice_offset = self._params["dims"][i][2] - 1

                width = int(slice_width * slice_offset)
                rows_travelled = 0
                while width >= 1920:
                    rows_travelled += 1
                    width -= 1920
                height = int(slice_height * rows_travelled)

                output_frame[height : (height + slice_height), width : (width + slice_width), :] = frame

            output_frame = np.uint8(output_frame)
            self._video_writer.write(output_frame)
            cv2.imshow('Output', output_frame)
            cv2.waitKey(1)

        self._video_writer.release()
        for cap in self._video_captures:
            cap.release()

videos = ['./1.mp4', './2.mp4', './3.mp4']
params = {"dims":[[2,2,1], [2,2,2], [2,1,2]]}
vid = ConsolidatedVideo(videos, params)