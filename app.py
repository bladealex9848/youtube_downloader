import subprocess
import os
from pathlib import Path

# Define la carpeta de descargas
DOWNLOADS_DIR = 'downloads'
Path(DOWNLOADS_DIR).mkdir(exist_ok=True)

def download_video(url):
    # Lista de comandos de yt-dlp para intentar
    commands_download = [
        [
            'yt-dlp',
            url,
            '-f', 'best[height<=720]',
            '--merge-output-format', 'mp4',
            '--no-part',
            '-o', f"{DOWNLOADS_DIR}/%(title)s.%(ext)s"
        ],
        [
            'yt-dlp',
            url,
            '-f', 'best[ext=mp4]',
            '--merge-output-format', 'mp4',
            '--restrict-filenames',
            '-o', f"{DOWNLOADS_DIR}/%(title)s.%(ext)s"
        ],
        [
            'yt-dlp',
            url,
            '-o', f"{DOWNLOADS_DIR}/%(title)s.%(ext)s"
        ]
    ]
    
    # Intentar cada comando hasta que uno funcione o todos fallen
    for command_download in commands_download:
        result_download = subprocess.run(command_download, capture_output=True, text=True)
        if result_download.returncode == 0:
            print('Descarga completada con éxito.')
            return
        else:
            print(f'Error durante la descarga con el comando {command_download}: {result_download.stderr}')

    # Si llegamos a este punto, todos los intentos han fallado
    print('Todos los intentos de descarga han fallado.')

if __name__ == '__main__':
    print("Descargador de Videos de YouTube")
    url = input("Ingrese la URL del video de YouTube aquí: ")
    if url:
        download_video(url)
    else:
        print("No se ingresó una URL válida.")