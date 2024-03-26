import os
import zipfile


def compress_file_to_zip(input_file, output_zip):
    """
    Сжимает файл и добавляет его в архив ZIP.

    Args:
    input_file (str): Путь к файлу, который нужно сжать и добавить в архив.
    output_zip (str): Путь к архиву ZIP, в который будет добавлен сжатый файл.
    """
    file_name = os.path.basename(input_file)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_file, arcname=file_name, compress_type=zipfile.ZIP_DEFLATED)
