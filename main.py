from utils.video_utils import read_video, save_video 
from trackers.tracker import Tracker

def main():
    # reading in video
    video_frames = read_video("artifacts/input_videos/08fd33_4.mp4")

    # initializing Tracker
    tracker = Tracker("../models/best.pt")
    
    tracks = tracker.get_object_tracks(video_frames)
    
    # saving video
    save_video(video_frames, "artifacts/output_videos/output_video.avi")


if __name__== "__main__":
    main()