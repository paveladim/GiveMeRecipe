from ultralytics import YOLO


def get_ingredients(path_to_image):
    # Загрузка модели YOLO
    model = YOLO('yolov8x.pt')
    results = model.predict(path_to_image)
    products = set()

    for result in results:
        if result.boxes:
            for box in result.boxes:
                class_id = int(box.cls)
                object_name = model.names[class_id]
                if object_name not in ['person', 'skateboard', 'etc']:
                    products.add(object_name)

    return list(products)
