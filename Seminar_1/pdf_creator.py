# pip install Pillow reportlab
import os
import re
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

def create_pdf_from_screenshots():
    """
    Создает PDF-документ из скриншотов, сортируя их по номеру в имени файла.
    Пользователь задает количество изображений на страницу PDF.
    """
    print("--- Создание PDF из скриншотов ---")

    # 1. Запрос пути к папке со скриншотами
    while True:
        folder_path = input("Введите полный путь к папке со скриншотами (например, C:\\Users\\User\\Screenshots): ").strip()
        if os.path.isdir(folder_path):
            break
        else:
            print("Ошибка: Указанный путь не является существующей папкой. Попробуйте снова.")

    # 2. Запрос количества изображений на страницу
    while True:
        try:
            images_per_page_str = input("Сколько изображений разместить на одной странице PDF? (1, 2, 4): ").strip()
            images_per_page = int(images_per_page_str)
            if images_per_page in [1, 2, 4]:
                break
            else:
                print("Ошибка: Пожалуйста, введите 1, 2 или 4.")
        except ValueError:
            print("Ошибка: Введите число.")

    # 3. Поиск скриншотов и сортировка
    image_files = []
    # Регулярное выражение для извлечения чисел из имени файла (например, "screenshot_001.png" -> 1)
    # Ищет последовательность цифр, которая может быть в начале, конце или середине имени.
    # Предполагаем, что числовой индекс является основным критерием сортировки.
    numeric_pattern = re.compile(r'(\d+)')

    print(f"\nСканирование папки: {folder_path}...")
    for filename in os.listdir(folder_path):
        # Проверяем, является ли файл изображением (расширения можно добавить/изменить)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            match = numeric_pattern.search(filename)
            if match:
                # Извлекаем первое найденное число как индекс
                index = int(match.group(1))
                image_files.append((index, filename))
            else:
                print(f"Предупреждение: Файл '{filename}' не содержит числового индекса и будет пропущен.")

    if not image_files:
        print("В указанной папке не найдено подходящих файлов изображений с числовым индексом.")
        return

    # Сортируем файлы по числовому индексу
    image_files.sort(key=lambda x: x[0])

    # Извлекаем только имена файлов после сортировки
    sorted_filenames = [filename for index, filename in image_files]

    print(f"Найдено {len(sorted_filenames)} изображений. Будут обработаны в следующем порядке:")
    for i, name in enumerate(sorted_filenames[:10]): # Показываем первые 10 для примера
        print(f"  {i+1}. {name}")
    if len(sorted_filenames) > 10:
        print("  ...")

    # 4. Создание PDF-документа
    output_pdf_name = os.path.join(folder_path, "Screenshots_Combined.pdf")
    c = canvas.Canvas(output_pdf_name, pagesize=A4)
    width, height = A4  # Размеры страницы A4

    # Определение размеров и позиций для изображений
    if images_per_page == 1:
        # Одно изображение на страницу, максимально возможное заполнение A4
        # Сделаем небольшой отступ
        margin = 10 * mm
        img_width = width - 2 * margin
        img_height = height - 2 * margin
        positions = [(margin, margin)] # Нижний левый угол
        dims = [(img_width, img_height)]
    elif images_per_page == 2:
        # Два изображения на страницу (например, одно над другим)
        margin = 10 * mm
        img_width = width - 2 * margin
        img_height = (height / 2) - margin * 1.5 # Учитываем промежуток
        positions = [
            (margin, height / 2 + margin / 2),  # Верхнее изображение
            (margin, margin)                    # Нижнее изображение
        ]
        dims = [(img_width, img_height), (img_width, img_height)]
    elif images_per_page == 4:
        # Четыре изображения на страницу (сетка 2x2)
        margin = 10 * mm
        img_width = (width / 2) - margin * 1.5
        img_height = (height / 2) - margin * 1.5
        positions = [
            (margin, height / 2 + margin / 2),      # Верхний левый
            (width / 2 + margin / 2, height / 2 + margin / 2), # Верхний правый
            (margin, margin),                       # Нижний левый
            (width / 2 + margin / 2, margin)        # Нижний правый
        ]
        dims = [(img_width, img_height)] * 4
    else:
        print("Неподдерживаемое количество изображений на страницу.")
        return

    current_page_images = []
    for i, filename in enumerate(sorted_filenames):
        full_image_path = os.path.join(folder_path, filename)
        try:
            # Открываем изображение, чтобы убедиться, что оно корректно и получить размеры
            # PIL.Image.open() может вызвать исключение, если файл поврежден
            Image.open(full_image_path).verify()
            current_page_images.append(full_image_path)
        except Exception as e:
            print(f"Ошибка при обработке файла '{filename}': {e}. Файл будет пропущен.")
            continue

        if len(current_page_images) == images_per_page or i == len(sorted_filenames) - 1:
            # Добавляем изображения на текущую страницу
            for j, img_path in enumerate(current_page_images):
                if j < len(positions): # Убедимся, что у нас есть позиция для этого изображения
                    x_pos, y_pos = positions[j]
                    target_width, target_height = dims[j]

                    # Пропорциональное изменение размера изображения для размещения на странице
                    # Используем ImageReader для ReportLab, который сам управляет пропорциями
                    img = ImageReader(img_path)
                    original_width, original_height = img.getSize()

                    # Вычисляем масштаб, чтобы изображение вписалось в target_width/height,
                    # сохраняя пропорции
                    scale_width = target_width / original_width
                    scale_height = target_height / original_height
                    scale = min(scale_width, scale_height)

                    drawn_width = original_width * scale
                    drawn_height = original_height * scale

                    # Центрируем изображение внутри отведенной области
                    centered_x = x_pos + (target_width - drawn_width) / 2
                    centered_y = y_pos + (target_height - drawn_height) / 2

                    c.drawImage(img_path, centered_x, centered_y, width=drawn_width, height=drawn_height, preserveAspectRatio=True)

            c.showPage() # Завершаем текущую страницу и начинаем новую
            current_page_images = [] # Очищаем список для следующей страницы

    c.save()
    print(f"\nPDF-документ успешно создан: {output_pdf_name}")
    print("Программа завершена.")

if __name__ == "__main__":
    create_pdf_from_screenshots()