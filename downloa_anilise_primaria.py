import yt_dlp
import os
import sys


def baixar_e_extrair_dados(url):
    # 1. Definição da pasta de saída
    output_dir = 'downloads'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Configurações técnicas do yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Pega o melhor áudio disponível
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Qualidade máxima para análise no Corolla
        }],
    }

    print(f"[*] Analisando URL: {url}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extrai informações e faz o download
            info = ydl.extract_info(url, download=True)

            # 3. Mapeamento de Metadados
            metadados = {
                "Título": info.get('title'),
                "Canal": info.get('uploader'),
                "Data": info.get('upload_date'),
                "Duração": f"{info.get('duration')} segundos",
                "Codec Original": info.get('acodec'),
                "Sample Rate": f"{info.get('asr')} Hz",
                "Bitrate (kbps)": info.get('abr'),
                "Caminho": f"{output_dir}/{info.get('title')}.mp3"
            }
            return metadados

        except Exception as e:
            return f"ERRO TÉCNICO: {str(e)}"


# --- BLOCO DE EXECUÇÃO ---
if __name__ == "__main__":
    # IMPORTANTE: Substitua pela URL do YouTube da música
    # Exemplo: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    url_target = "https://www.youtube.com/watch?v=T_kEs91V3b4"

    if "gemini.google.com" in url_target:
        print("[-] Erro: URLs do Gemini são privadas. Use um link do YouTube ou SoundCloud.")
        sys.exit(1)

    resultado = baixar_e_extrair_dados(url_target)

    if isinstance(resultado, dict):
        print("\n" + "=" * 30)
        print("ANÁLISE DE GRAVAÇÃO CONCLUÍDA")
        print("=" * 30)
        for chave, valor in resultado.items():
            print(f"{chave.ljust(15)}: {valor}")
    else:
        print(f"\n[!] Falha no Processamento:\n{resultado}")