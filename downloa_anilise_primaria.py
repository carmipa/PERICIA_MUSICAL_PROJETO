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
        report = []
        report.append("\n" + "=" * 30)
        report.append("ANÁLISE DE GRAVAÇÃO CONCLUÍDA")
        report.append("=" * 30)
        for chave, valor in resultado.items():
            report.append(f"{chave.ljust(15)}: {valor}")
        
        final_output = "\n".join(report)
        print(final_output)

        # SALVAR LOG (Markdown)
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        nome_base = resultado.get("Título", "audio_downloaded").replace(" ", "_")
        log_path = os.path.join(log_dir, f"pericia_download_{nome_base}.md")
        
        # Formatação Markdown
        md_report = [f"# 📥 Download e Extração - {nome_base}", ""]
        md_report.extend([line.replace("=", "").strip() for line in report if line.strip()])

        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_report))
        print(f"\n[OK] Log Markdown de download salvo em: {log_path}")
    else:
        print(f"\n[!] Falha no Processamento:\n{resultado}")