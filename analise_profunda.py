import librosa
import numpy as np
import mutagen
from mutagen.mp3 import MP3
import os
import glob


def pericia_audiometrica_avancada():
    base_path = r"G:\PROJETOS-OPEN\analisador_musica"
    arquivos = glob.glob(os.path.join(base_path, "downloads", "*.mp3"))
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

    print("\n" + "█" * 60)
    print(f"      RELATÓRIO DE ENGENHARIA ACÚSTICA - COROLLA EDITION")
    print("█" * 60)

    print(f"\n[SISTEMA DE ARQUIVOS]")
    print(f"    Bitrate Real      : {bitrate:.0f} kbps (CBR/VBR)")
    print(f"    Sample Rate       : {frequencia_amostragem} Hz")
    print(f"    Duração           : {duracao:.2f}s")
    print(f"    Encoder           : {encoder_info}")

    print(f"\n[PSICOACÚSTICA E DINÂMICA]")
    print(f"    Energia de Impacto (Percussão): {energia_perc:.4f}")
    print(f"    Energia Melódica  (Harmonia) : {energia_harm:.4f}")
    print(f"    Razão Melodia/Bateria        : {energia_harm / energia_perc:.2f}")

    print(f"\n[ANÁLISE DE ESPECTRO (dB Relativo)]")
    print(f"    Sub-Grave (Corpo) : {sub_grave:.2f} dB")
    print(f"    Médios (Presença) : {medios:.2f} dB")
    print(f"    Agudos (Brilho)   : {agudos:.2f} dB")

    print(f"\n[VEREDITO PERICIAL]")
    # Lógica de diagnóstico baseada nos dados extraídos
    if sub_grave < -50:
        print("    (!) CONCLUSÃO: A gravação tem um 'Roll-off' agressivo nos graves.")
        print("    O Corolla precisa de volume 20+ porque não há sinal real abaixo de 60Hz.")

    if (agudos - medios) > 10:
        print("    (!) CONCLUSÃO: Mixagem 'V-Shape' detectada.")
        print("    O som parece 'oco' no volume 12 porque os médios estão enterrados.")

    if (energia_harm / energia_perc) > 2.0:
        print("    (!) CONCLUSÃO: Transientes fracos (Baixa percussividade).")
        print("    A música carece de 'punch'. O volume 12 parecerá sem vida.")

    print("█" * 60)


if __name__ == "__main__":
    pericia_audiometrica_avancada()