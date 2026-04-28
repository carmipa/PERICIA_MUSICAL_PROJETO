import librosa
import numpy as np
import mutagen
from mutagen.mp3 import MP3
import os
import glob


def pericia_audiometrica_avancada():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_path = os.path.join(script_dir, "downloads")
    arquivos = glob.glob(os.path.join(downloads_path, "*.mp3"))
    if not arquivos:
        print("[-] Arquivo não encontrado.")
        return
    caminho = arquivos[0]

    # 1. Metadados de Baixo Nível (Mutagen)
    audio_info = MP3(caminho)
    bitrate = audio_info.info.bitrate / 1000
    frequencia_amostragem = audio_info.info.sample_rate
    duracao = audio_info.info.length
    encoder_info = audio_info.get("TSS", "Desconhecido")

    # 2. Processamento de Sinal com Librosa
    # Carregamos o áudio sem resampling para manter a fidelidade do Sawano
    y, sr = librosa.load(caminho, sr=None)

    # --- ANÁLISE DE ENERGIA POR BANDA (O SEGREDO DO VOLUME 12) ---
    # Calculamos o Espectrograma de Mel
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)

    # Dividimos o espectro em 3 zonas críticas:
    sub_grave = np.mean(S_dB[0:10, :])  # 20Hz - 100Hz
    medios = np.mean(S_dB[20:80, :])  # 400Hz - 3kHz (Voz e Guitarras)
    agudos = np.mean(S_dB[100:128, :])  # 8kHz - 20kHz (Brilho/Pratos)

    # --- ANÁLISE DE TRANSIENTES (PUNCH) ---
    # Separação Harmônica (Melodia) vs Percussiva (Bateria)
    y_harm, y_perc = librosa.effects.hpss(y)
    energia_perc = np.mean(librosa.feature.rms(y=y_perc))
    energia_harm = np.mean(librosa.feature.rms(y=y_harm))

    report = []
    report.append("\n" + "█" * 60)
    report.append(f"      RELATÓRIO DE ENGENHARIA ACÚSTICA - COROLLA EDITION")
    report.append("█" * 60)

    report.append(f"\n[SISTEMA DE ARQUIVOS]")
    report.append(f"    Bitrate Real      : {bitrate:.0f} kbps (CBR/VBR)")
    report.append(f"    Sample Rate       : {frequencia_amostragem} Hz")
    report.append(f"    Duração           : {duracao:.2f}s")
    report.append(f"    Encoder           : {encoder_info}")

    report.append(f"\n[PSICOACÚSTICA E DINÂMICA]")
    report.append(f"    Energia de Impacto (Percussão): {energia_perc:.4f}")
    report.append(f"    Energia Melódica  (Harmonia) : {energia_harm:.4f}")
    report.append(f"    Razão Melodia/Bateria        : {energia_harm / energia_perc:.2f}")

    report.append(f"\n[ANÁLISE DE ESPECTRO (dB Relativo)]")
    report.append(f"    Sub-Grave (Corpo) : {sub_grave:.2f} dB")
    report.append(f"    Médios (Presença) : {medios:.2f} dB")
    report.append(f"    Agudos (Brilho)   : {agudos:.2f} dB")

    report.append(f"\n[VEREDITO PERICIAL]")
    # Lógica de diagnóstico baseada nos dados extraídos
    if sub_grave < -50:
        report.append("    (!) CONCLUSÃO: A gravação tem um 'Roll-off' agressivo nos graves.")
        report.append("    O Corolla precisa de volume 20+ porque não há sinal real abaixo de 60Hz.")

    if (agudos - medios) > 10:
        report.append("    (!) CONCLUSÃO: Mixagem 'V-Shape' detectada.")
        report.append("    O som parece 'oco' no volume 12 porque os médios estão enterrados.")

    if (energia_harm / energia_perc) > 2.0:
        report.append("    (!) CONCLUSÃO: Transientes fracos (Baixa percussividade).")
        report.append("    A música carece de 'punch'. O volume 12 parecerá sem vida.")

    report.append("█" * 60)

    # Exibir no console
    final_output = "\n".join(report)
    print(final_output)

    # 3. SALVAR LOG (Markdown)
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    nome_base = os.path.splitext(os.path.basename(caminho))[0]
    log_path = os.path.join(log_dir, f"pericia_profunda_{nome_base}.md")
    
    # Formatação Markdown para o arquivo
    md_report = [f"# 🔊 Engenharia Acústica - {nome_base}", ""]
    md_report.extend([line.replace("█", "").strip() for line in report if line.strip()])
    
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_report))
    print(f"\n[OK] Log Markdown salvo em: {log_path}")


if __name__ == "__main__":
    pericia_audiometrica_avancada()