import streamlit as st
import subprocess
import os
from pathlib import Path

DOWNLOADS_DIR = 'downloads'
Path(DOWNLOADS_DIR).mkdir(exist_ok=True)

def clean_downloads_folder():
    for f in Path(DOWNLOADS_DIR).iterdir():
        if f.is_file() and not f.suffix.endswith('.part'):
            try:
                f.unlink()
            except PermissionError as e:
                st.error(f"No se pudo eliminar {f.name}: {e}")

def download_video(url):
    command_get_filename = [
        'yt-dlp',
        '--get-filename',
        '-o', '%(title)s.%(ext)s',
        url
    ]
    result_get_filename = subprocess.run(command_get_filename, capture_output=True, text=True)
    if result_get_filename.returncode != 0:
        st.error(f"Error obteniendo nombre del archivo: {result_get_filename.stderr}")
        return None
    filename = result_get_filename.stdout.strip()
    if not filename:
        st.error("No se pudo obtener el nombre del archivo del video.")
        return None
    download_path = Path(DOWNLOADS_DIR) / filename

    command_download = [
        'yt-dlp',
        url,
        '-f', 'best[height<=720]',
        '--merge-output-format', 'mp4',
        '--no-part',
        '-o', str(download_path)
    ]
    result_download = subprocess.run(command_download, capture_output=True, text=True)
    if result_download.returncode != 0:
        error_message = result_download.stderr
        if "HTTP Error 404: Not Found" in error_message:
            st.error("El video no se pudo encontrar. Puede haber sido eliminado o es privado.")
        elif "HTTP Error 403: Forbidden" in error_message:
            st.error("Acceso denegado al video. Puede requerir autenticación o estar restringido geográficamente.")
        else:
            st.error(f"Error durante la descarga: {error_message}")
        return None

    if not download_path.is_file():
        st.error("El video se descargó, pero no se encontró el archivo. Verifique la carpeta de descargas.")
        return None
    return download_path

def main():
    st.title('Descargador de Videos de YouTube')

    url = st.text_input('Ingrese la URL del video de YouTube aquí:')

    if st.button('Descargar Video'):
        if url:
            clean_downloads_folder()
            with st.spinner('Descargando...'):
                file_path = download_video(url)
                if file_path:
                    st.success('Video descargado con éxito.')
                    file_name = file_path.name
                    with open(file_path, "rb") as file:
                        st.download_button("Guardar Video", file, file_name=file_name, mime="video/mp4")
        else:
            st.error('Por favor, ingrese una URL válida.')

if __name__ == '__main__':
    main()