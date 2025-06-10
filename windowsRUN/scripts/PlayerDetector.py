from ultralytics import YOLO
import cv2
import numpy as np



model = YOLO('../referee_detection/runs/detect/train5/weights/best.pt')

# Open the video file
cap = cv2.VideoCapture('../data/videos/1074166f-fd9e-4543-a9ff-04685a6cf92e.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    if not ret:
        break

    # Perform object detection on the frame
    results = model(frame)

    top_box = [frame.shape[0], []]
    bottom_box = [0, []]
    for result in results:
        for det in result.boxes:
            box = det.xyxy.int().tolist()[0]
            if box[3] < top_box[0]:
                top_box[0] = box[3]
                top_box[1] = box
            if box[1] > bottom_box[0]:
                bottom_box[0] = box[1]
                bottom_box[1] = box

    field_mask = np.zeros(frame.shape[:2], dtype = 'uint8')

    field_points = np.array([
        [0, top_box[0]],
        [frame.shape[1], top_box[0]],
        [frame.shape[1], bottom_box[0]],
        [0, bottom_box[0]]
    ])
    field_points.reshape((-1, 1, 2))

    cv2.fillPoly(field_mask, [field_points], (255, 255, 255))

    masked_frame = cv2.bitwise_and(frame, frame, mask = field_mask)

    ref_mask = np.zeros(frame.shape[:2], dtype = 'uint8')

    ref_points = np.array([
        [0, top_box[0]],
        [top_box[1][2] + 25, top_box[0]],
        [bottom_box[1][2] + 25, bottom_box[1][3]],
        [0, bottom_box[0]]
    ])
    ref_points.reshape((-1, 1, 2))

    cv2.fillPoly(ref_mask, [ref_points], (255, 255, 255))

    masked_frame = cv2.bitwise_and(frame, frame, mask = ref_mask)

    #masked_frame = cv2.cvtColor(masked_frame, cv2.COLOR_RGB2GRAY)

    #Display the image
    cv2.imshow('YOLOv8 Detection', masked_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()