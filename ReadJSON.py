import json
import os
class ReadJSON:

    def __init__(self,json_file_path):

        try:
            # Проверяем существование файла
            if not os.path.exists(json_file_path):
                raise FileNotFoundError(f"Файл не найден: {json_file_path}")

            # Открываем и читаем JSON файл
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Пытаемся извлечь путь для сохранения изображения
            # Проверяем различные возможные ключи

            self.depth_path=data['depth_path']
            self.save_im_path=data['save_image_path']
            self.camera_position=data['camera_position']
            self.light_position=data['light_position']
            self.reflection_model=data['reflection_model']
            self.save_model_path=data['save_model_path']



        except FileNotFoundError as e:
            raise e
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка при чтении JSON файла: {e}")
        except Exception as e:
            raise RuntimeError(f"Произошла ошибка: {e}")
