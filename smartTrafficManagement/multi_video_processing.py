import cv2
import numpy as np

# ---------------------------
# YOLO Configuration
# ---------------------------
YOLO_CFG = "yolov3.cfg"        # Path to your YOLO config file
YOLO_WEIGHTS = "yolov3.weights" # Path to your YOLO weights file
COCO_NAMES = "coco.names"       # Path to the file with COCO class names

# Load the class names
with open(COCO_NAMES, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# We only want to count these classes as "vehicles"
vehicle_classes = {"car", "motorbike", "bus", "truck", "motorcycle"}

# Load the YOLO network
net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # Use DNN_TARGET_CUDA for GPU if available

# Determine output layers for YOLO
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Confidence and Non-max Suppression thresholds
CONF_THRESH = 0.5  # Confidence threshold
NMS_THRESH = 0.4   # NMS threshold

# ---------------------------
# Video Capture Initialization
# ---------------------------
# cap1 = cv2.VideoCapture("road_video1.mp4")
# cap2 = cv2.VideoCapture("road_video2.mp4")
cap3 = cv2.VideoCapture("road_video3.mp4")
cap4 = cv2.VideoCapture("road_video4.mp4")


cap1 = cv2.VideoCapture("./sampleVideos/demo.mp4")
cap2 = cv2.VideoCapture("./sampleVideos/demo2.mp4")
# cap3 = cv2.VideoCapture("./sampleVideos/demo3.mp4")
# cap4 = cv2.VideoCapture("./sampleVideos/Video.mp4")

roi_cam3 = ((50, 100), (300, 400))   # top-left, bottom-right for camera 3
roi_cam4 = ((50, 100), (300, 400)) 

# ---------------------------
# Separate ROI Definitions
# ---------------------------
# Adjust these coordinates individually for each camera's perspective.
roi_cam1 = ((200, 100), (500, 600))   # top-left, bottom-right for camera 1
roi_cam2 = ((100, 100), (580, 680))   # top-left, bottom-right for camera 2
# roi_cam3 = ((50, 100), (600, 630))   # top-left, bottom-right for camera 3
# roi_cam4 = ((400, 50), (800, 500))   # top-left, bottom-right for camera 4
# roi_top_left = (50, 100)
# roi_bottom_right = (300, 400)
# Process every nth frame (for efficiency)
nth_frame = 15
frame_count = 0

# Store last detected counts to prevent flickering (one per camera)
last_roi_counts = [0, 0, 0, 0]  # [cap1, cap2, cap3, cap4]

def detect_vehicles_in_roi(frame, roi_top_left, roi_bottom_right):
    """
    Run YOLO detection on a single frame, filter for vehicles,
    and count how many bounding boxes overlap with the ROI.
    """
    (H, W) = frame.shape[:2]

    # Create a 4D blob from the frame (using a smaller size for faster processing)
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    # Extract bounding boxes and confidences
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter for strong detections and relevant vehicle classes
            if confidence > CONF_THRESH and classes[class_id] in vehicle_classes:
                center_x = int(detection[0] * W)
                center_y = int(detection[1] * H)
                w = int(detection[2] * W)
                h = int(detection[3] * H)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-max Suppression to reduce duplicates
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESH, NMS_THRESH)

    roi_count = 0
    if len(idxs) > 0:
        for i in idxs.flatten():
            x, y, w, h = boxes[i]
            label = classes[class_ids[i]]
            conf = confidences[i]

            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Check overlap between the bounding box and the ROI
            roi_x1, roi_y1 = roi_top_left
            roi_x2, roi_y2 = roi_bottom_right
            box_x1, box_y1, box_x2, box_y2 = x, y, x + w, y + h

            overlap_x1 = max(roi_x1, box_x1)
            overlap_y1 = max(roi_y1, box_y1)
            overlap_x2 = min(roi_x2, box_x2)
            overlap_y2 = min(roi_y2, box_y2)

            # If there's any positive overlap, count it
            if overlap_x2 > overlap_x1 and overlap_y2 > overlap_y1:
                roi_count += 1

    # Draw the ROI rectangle and display the count
    cv2.rectangle(frame, roi_top_left, roi_bottom_right, (0, 255, 255), 2)
    cv2.putText(frame, f"ROI Count: {roi_count}",
                (roi_top_left[0], roi_top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    return roi_count

while True:
    frame_count += 1

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()
    ret4, frame4 = cap4.read()

    # Break loop if any video stream ends
    if not ret1 or not ret2 or not ret3 or not ret4:
        break

    # Draw ROI boxes on all frames (to avoid flickering)
    cv2.rectangle(frame1, roi_cam1[0], roi_cam1[1], (0, 255, 255), 2)
    cv2.rectangle(frame2, roi_cam2[0], roi_cam2[1], (0, 255, 255), 2)
    cv2.rectangle(frame3, roi_cam3[0], roi_cam3[1], (0, 255, 255), 2)
    cv2.rectangle(frame4, roi_cam4[0], roi_cam4[1], (0, 255, 255), 2)

    # Run detection only on every nth frame
    if frame_count % nth_frame == 0:
        # Camera 1
        last_roi_counts[0] = detect_vehicles_in_roi(
            frame1, roi_cam1[0], roi_cam1[1]
        )
        # Camera 2
        last_roi_counts[1] = detect_vehicles_in_roi(
            frame2, roi_cam2[0], roi_cam2[1]
        )
        # Camera 3
        last_roi_counts[2] = detect_vehicles_in_roi(
            frame3, roi_cam3[0], roi_cam3[1]
        )
        # Camera 4
        last_roi_counts[3] = detect_vehicles_in_roi(
            frame4, roi_cam4[0], roi_cam4[1]
        )

        # Write the latest ROI counts to a file
        with open("carsCount.txt", "w") as f:
            f.write(f"{last_roi_counts[0]} {last_roi_counts[1]} "
                    f"{last_roi_counts[2]} {last_roi_counts[3]}")

    # Always display the last detected ROI count (no flickering)
    cv2.putText(frame1, f"ROI Count: {last_roi_counts[0]}",
                (roi_cam1[0][0], roi_cam1[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame2, f"ROI Count: {last_roi_counts[1]}",
                (roi_cam2[0][0], roi_cam2[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame3, f"ROI Count: {last_roi_counts[2]}",
                (roi_cam3[0][0], roi_cam3[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame4, f"ROI Count: {last_roi_counts[3]}",
                (roi_cam4[0][0], roi_cam4[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Resize frames for a 2×2 grid display
    frame1_resized = cv2.resize(frame1, (640, 480))
    frame2_resized = cv2.resize(frame2, (640, 480))
    frame3_resized = cv2.resize(frame3, (640, 480))
    frame4_resized = cv2.resize(frame4, (640, 480))

    top_row = np.hstack((frame1_resized, frame2_resized))
    bottom_row = np.hstack((frame3_resized, frame4_resized))
    combined_frame = np.vstack((top_row, bottom_row))

    cv2.imshow("Combined 4 Videos - YOLO Vehicle Detection", combined_frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()
cap3.release()
cap4.release()
cv2.destroyAllWindows()
