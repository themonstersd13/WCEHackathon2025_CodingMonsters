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
cap1 = cv2.VideoCapture("road_video1.mp4")
cap2 = cv2.VideoCapture("road_video2.mp4")
cap3 = cv2.VideoCapture("road_video3.mp4")
cap4 = cv2.VideoCapture("road_video4.mp4")

# ---------------------------
# ROI Definitions
# ---------------------------
roi_top_left = (50, 100)
roi_bottom_right = (300, 400)

# Process every nth frame
nth_frame = 15
frame_count = 0

def detect_vehicles_in_roi(frame, roi_top_left, roi_bottom_right):
    """
    Run YOLO detection on a single frame, filter for vehicles, 
    and count how many bounding boxes fall fully (based on center) in the ROI.
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
                # YOLO gives box coords relative to image size
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
            class_id = class_ids[i]
            label = classes[class_id]
            conf = confidences[i]

            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Count if the center of the bounding box is within the ROI
            bb_center_x = x + w // 2
            bb_center_y = y + h // 2
            if (roi_top_left[0] <= bb_center_x <= roi_bottom_right[0] and
                roi_top_left[1] <= bb_center_y <= roi_bottom_right[1]):
                roi_count += 1

    # Draw the ROI rectangle and display the count
    cv2.rectangle(frame, roi_top_left, roi_bottom_right, (0, 255, 255), 2)
    cv2.putText(frame, f"ROI Count: {roi_count}",
                (roi_top_left[0], roi_top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    return roi_count

# Store last detected counts to prevent flickering
last_roi_counts = [0, 0, 0, 0]  # [cap1, cap2, cap3, cap4]

while True:
    frame_count += 1

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()
    ret4, frame4 = cap4.read()

    # Break loop if any video stream ends
    if not ret1 or not ret2 or not ret3 or not ret4:
        break

    # Always draw ROI boxes to avoid flickering
    cv2.rectangle(frame1, roi_top_left, roi_bottom_right, (0, 255, 255), 2)
    cv2.rectangle(frame2, roi_top_left, roi_bottom_right, (0, 255, 255), 2)
    cv2.rectangle(frame3, roi_top_left, roi_bottom_right, (0, 255, 255), 2)
    cv2.rectangle(frame4, roi_top_left, roi_bottom_right, (0, 255, 255), 2)

    # Run detection only on every nth frame
    if frame_count % nth_frame == 0:
        last_roi_counts[0] = detect_vehicles_in_roi(frame1, roi_top_left, roi_bottom_right)
        last_roi_counts[1] = detect_vehicles_in_roi(frame2, roi_top_left, roi_bottom_right)
        last_roi_counts[2] = detect_vehicles_in_roi(frame3, roi_top_left, roi_bottom_right)
        last_roi_counts[3] = detect_vehicles_in_roi(frame4, roi_top_left, roi_bottom_right)

        # Write the latest ROI counts to the file
        with open("carsCount.txt", "w") as f:
            f.write(f"{last_roi_counts[0]} {last_roi_counts[1]} {last_roi_counts[2]} {last_roi_counts[3]}")

    # Always display the last detected ROI count to prevent flickering
    cv2.putText(frame1, f"ROI Count: {last_roi_counts[0]}",
                (roi_top_left[0], roi_top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame2, f"ROI Count: {last_roi_counts[1]}",
                (roi_top_left[0], roi_top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame3, f"ROI Count: {last_roi_counts[2]}",
                (roi_top_left[0], roi_top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame4, f"ROI Count: {last_roi_counts[3]}",
                (roi_top_left[0], roi_top_left[1] - 10),
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

    # Using waitKey(1) to reduce delay between frames
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()
cap3.release()
cap4.release()
cv2.destroyAllWindows()