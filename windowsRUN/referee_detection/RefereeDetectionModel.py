from ultralytics import YOLO
import cv2
import numpy as np

'''#Load a model
model = YOLO('yolov8n.yaml')

#Train the model
results = model.train(data = 'config.yaml', epochs = 50, dropout = .25)'''



model = YOLO('runs/detect/train5/weights/best.pt')

# Open the video file
cap = cv2.VideoCapture('../data/videos/1074166f-fd9e-4543-a9ff-04685a6cf92e.mp4')

frame_count = 0

while(cap.isOpened()):
    #frame_count += 1
    ret, frame = cap.read()
    if not ret or frame_count > 100:
        break

    # Perform object detection on the frame
    results = model(frame)

    # Render the results on the frame
    annotated_frame = results[0].plot()

    top_box = [1080, []]
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
            
    cropped_frame = frame[top_box[0]+((top_box[1][3]-top_box[1][1]) // 2):bottom_box[0], :]

    #Draw the far sideline
    cv2.line(
        annotated_frame, 
        (0, (top_box[1][3] + (top_box[1][3] - top_box[1][1]))), 
        (1920, (top_box[1][3] + (top_box[1][3] - top_box[1][1]))), 
        (255, 255, 255), 
        3
    )

    #Draw the close sideline
    cv2.line(
        annotated_frame, 
        (0, (bottom_box[1][3] + (bottom_box[1][3] - bottom_box[1][1]))), 
        (1920, (bottom_box[1][3] + (bottom_box[1][3] - bottom_box[1][1]))), 
        (255, 255, 255), 
        3
    )

    #Draw the line of scrimmage
    cv2.line(
        annotated_frame, 
        ((top_box[1][0] + top_box[1][2]) // 2, (top_box[1][3] + (top_box[1][3] - top_box[1][1]))), 
        ((bottom_box[1][0] + bottom_box[1][2]) // 2, (bottom_box[1][3] + (bottom_box[1][3] - bottom_box[1][1]))), 
        (0, 255, 255), 
        3
    )

    #Create a mask for the left side of the line of scrimmage


    #Display the image
    cv2.imshow('YOLOv8 Detection', cropped_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()