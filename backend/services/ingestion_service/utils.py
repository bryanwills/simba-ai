def get_file_size_mb(file):
    current_position = file.file.tell()
    file.file.seek(0, 2)
    size_bytes = file.file.tell()
    file.file.seek(current_position)
    return round(size_bytes / (1024 * 1024), 2)  # Convertir en MB et arrondir à 2 décimales
