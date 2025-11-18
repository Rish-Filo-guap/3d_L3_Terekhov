import struct
import numpy as np
from PIL import Image
import matplotlib.cm as cm


def read_dat_file(filename):
    """
    Читает dat файл с числами double
    Первые 2 числа - высота и ширина массива, затем сам массив
    """
    with open(filename, 'rb') as f:
        # Читаем высоту и ширину (double - 8 байт каждое)
        height_bytes = f.read(8)
        width_bytes = f.read(8)

        if len(height_bytes) < 8 or len(width_bytes) < 8:
            raise ValueError("Файл слишком короткий для чтения размеров")

        height = struct.unpack('d', height_bytes)[0]
        width = struct.unpack('d', width_bytes)[0]

        height = int(height)
        width = int(width)

        print(f"Размер массива: {height} x {width}")

        # Читаем остальные данные
        data_bytes = f.read()
        expected_size = height * width * 8  # 8 байт на каждый double

        if len(data_bytes) < expected_size:
            raise ValueError(f"Недостаточно данных. Ожидалось {expected_size} байт, получено {len(data_bytes)}")

        # Преобразуем байты в массив double
        data = struct.unpack(f'{height * width}d', data_bytes[:expected_size])

        # Преобразуем в numpy массив и reshape
        array = np.array(data).reshape(height, width)

        return array


def create_depth_bmp(depth_array, output_filename, colormap='viridis'):
    """
    Создает BMP изображение из массива глубины
    """
    # Нормализуем данные к диапазону [0, 1]
    depth_normalized = (depth_array - np.min(depth_array)) / (np.max(depth_array) - np.min(depth_array))

    # Применяем цветовую карту
    colormap_func = getattr(cm, colormap)
    colored_image = colormap_func(depth_normalized)

    # Преобразуем в 8-битное изображение
    image_8bit = (colored_image[:, :, :3] * 255).astype(np.uint8)

    # Создаем и сохраняем изображение
    img = Image.fromarray(image_8bit)
    img.save(output_filename, 'BMP')
    print(f"Изображение сохранено как: {output_filename}")


def create_grayscale_bmp(depth_array, output_filename):
    """
    Создает черно-белое BMP изображение из массива глубины
    """
    # Нормализуем данные к диапазону [0, 255]
    depth_normalized = (depth_array - np.min(depth_array)) / (np.max(depth_array) - np.min(depth_array))
    depth_8bit = (depth_normalized * 255).astype(np.uint8)

    # Создаем и сохраняем изображение
    img = Image.fromarray(depth_8bit, mode='L')
    img.save(output_filename, 'BMP')
    print(f"Черно-белое изображение сохранено как: {output_filename}")


# Основная функция
def main():
    for i in range(1,20):
        input_file = "files/DepthMap_"+str(i)+".dat"  # Замените на путь к вашему файлу
        output_color = "depth_color/Map_"+str(i)+".bmp"
        output_grayscale = "depth_grayscale/Map_"+str(i)+".bmp"

        try:
            # Читаем данные из файла
            depth_array = read_dat_file(input_file)

            print(f"Диапазон значений глубины: {np.min(depth_array):.4f} - {np.max(depth_array):.4f}")

            # Создаем цветное изображение
            create_depth_bmp(depth_array, output_color, 'viridis')

            # Создаем черно-белое изображение
            create_grayscale_bmp(depth_array, output_grayscale)

            print("Обработка завершена успешно!")

        except FileNotFoundError:
            print(f"Ошибка: Файл {input_file} не найден")
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")


if __name__ == "__main__":
    main()