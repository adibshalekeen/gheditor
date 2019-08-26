import cv2
import numpy as np
class ConsolidatedFrame:
    def __init__(self, frames, offsets, frame_sizes, resolution):
        self._frames = frames
        self._offsets = offsets
        self._frame_sizes = frame_sizes
        self._resolution = resolution
        self._output_frame = np.zeros(shape=(self._resolution[1], self._resolution[0],3))
        self._consolidate()
    
    def _consolidate(self):
        resized_frames = []
        for i in range(0, len(self._frames)):
            resized_frame = cv2.resize(self._frames[i], dsize=(self._frame_sizes[i][0], self._frame_sizes[i][1]))
            width_offset = self._offsets[i][0]
            height_offset = self._offsets[i][1]
            self._output_frame[height_offset : (height_offset + self._frame_sizes[i][1]), width_offset : (width_offset + self._frame_sizes[i][0]), :] = resized_frame 

    @property
    def Raw(self):
        return np.uint8(self._output_frame)

class ConsolidatedVideo:
    def __init__(self, videos, params):
        self._videos = videos
        self._params = params
        
        self._video_captures = []
        for video in self._videos:
            self._video_captures.append(cv2.VideoCapture(video))

        self._video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (1920, 1080))
        self._frame_sizes = []
        self._offsets = []
        for i in range(0, len(self._videos)):
            frame_width = int(1920 / self._params["dims"][i][1])
            frame_height = int(1080 / self._params["dims"][i][0])
            self._frame_sizes.append((frame_width, frame_height))
            
            frame_offset = self._params["dims"][i][2] - 1

            width_offset = int(frame_width * frame_offset)
            rows_travelled = 0
            while width_offset >= 1920:
                rows_travelled += 1
                width_offset -= 1920
            height_offset = int(frame_height * rows_travelled)

            self._offsets.append((width_offset, height_offset))

        self.consolidate_video()

    def consolidate_video(self):
        consolidating = True        
        while consolidating:
            frames = []
            for i in range(0, len(self._video_captures)):
                ret , frame = self._video_captures[i].read()
                consolidating = ret
                if not ret:
                    break
                frames.append(frame)
            output_frame = ConsolidatedFrame(frames,
                                             self._offsets,
                                             self._frame_sizes,
                                             (1920,1080))
            self._video_writer.write(output_frame.Raw)
            cv2.imshow('Output', output_frame.Raw)
            cv2.waitKey(1)

        self._video_writer.release()
        for cap in self._video_captures:
            cap.release()

videos = ['./1.mp4', './2.mp4', './3.mp4']
params = {"dims":[[2,2,1], [2,2,2], [2,1,2]]}
vid = ConsolidatedVideo(videos, params)