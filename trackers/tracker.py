from ultralytics import YOLO
import supervision as sv
class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
    
    def detect_frames(self, frames):
        # batch sizes to avoid memory issues
        batch_size=20
        detections = []
        for i in range(0, len(frames), batch_size):
            detections_batch = self.model.predict(frames[i:i+batch_size], conf=0.1)
            detections += detections_batch
            break
        return detections
    
    def get_object_tracks(self, frames):
        detections = self.detect_frames(frames)
        
        tracks= {"players":[],
                 "referees":[],
                 "ball":[]
                }       
        
        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inverse = {v:k for k,v in cls_names.items()}
            
            # convert to supervision detection format
            detection_supervision = sv.Detections.from_ultralytics(detection)
            
            # convert goalkeeper to player object (to avoid overhead)
            # initial analysis does not particularly need goalkeeper defined/differentiated
            # comment out if looking specifically have goalkeeper included in analysis 
            for object_index, class_id in enumerate(detection_supervision.class_id): # Detection object:(..., class_id=array([2,3,...,0]), ..., data={'class_name': array(['player', 'goalkeeper', ..., 'ball'], ...)})
                if cls_names[class_id] == "goalkeeper":
                    detection_supervision.class_id[object_index] = cls_names_inverse["player"]
            
            # Track Objects
            # adding Tracker object to Detections
            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)
            
            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})
            
            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]
                track_id = frame_detection[4]
                
                if cls_id == cls_names_inverse["player"]:
                    tracks["players"][frame_num][track_id] = {"bbox": bbox}
                
                if cls_id == cls_names_inverse["referee"]:
                    tracks["referees"][frame_num][track_id] = {"bbox": bbox}
                    
            for frame_detection in detection_supervision:
                bbox = frame_dete
            # print Detections object (bounding boxes, class labels, confidence scores)
            print(detection_with_tracks)