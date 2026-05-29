import cv2
from ultralytics import YOLO

model = YOLO("yolov8n-seg.pt")
cap = cv2.VideoCapture(0)

total_cellphones = 0
tracked_ids = set()  # Para no contar el mismo celular dos veces

while True:
    ret, im0 = cap.read()
    if not ret:
        break

    results = model.track(im0, persist=True)  # track en lugar de __call__

    if results[0].boxes is not None:
        boxes = results[0].boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            # Verificar que tiene ID de tracking
            if label == "cell phone" and box.id is not None:
                track_id = int(box.id[0])

                # Solo sumar si es un ID nuevo
                if track_id not in tracked_ids:
                    tracked_ids.add(track_id)
                    total_cellphones += 1

    im0 = results[0].plot()

    cv2.putText(im0, f"Cellphones vistos: {total_cellphones}",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, (0, 255, 0), 3)

    cv2.imshow("instance-segmentation", im0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()