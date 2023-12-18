from ultralytics import YOLO

def give_recipe(path_to_image):
    model = YOLO('yolov8x.pt')
    results = model.predict(path_to_image)
    products = set()
 
    for result in results:
        if result.boxes:
            for box in result.boxes:
                class_id = int(box.cls)
                object_name = model.names[class_id]
                products.add(object_name)

    # превратить в список products (optional)
    # убрать фигню человеков, досков и типа такого
    # сформировать промпт и кинуть запрос сетке
    # ответ вернуть
    # ans = ''
    # return ans