import librosa
import numpy as np
import glob
import os


def analise_pericial():
    # Busca automaticamente qualquer MP3 na pasta downloads
    arquivos = glob.glob("downloads/*.mp3")

    if not arquivos:
        print("[-] Nenhum arquivo MP3 encontrado na pasta downloads.")
        return

    caminho = arquivos[0]
    print(f"[*] Analisando: {os.path.basename(caminho)}")

    try:
        # Carrega o áudio (sr=None mantém a taxa original de 48kHz do Sawano)
        y, sr = librosa.load(caminho, sr=None)

        # 1. Cálculo de RMS (Energia Média)
        rms = librosa.feature.rms(y=y)
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        avg_rms = np.mean(rms_db)

        # 2. Cálculo de Pico (True Peak)
        peak_abs = np.max(np.abs(y))
        peak_db = librosa.amplitude_to_db(np.array([peak_abs]), ref=1.0)[0]

        # 3. Dynamic Range (DR)
        # Em termos simples: a distância entre o topo e a média
        dr = peak_db - avg_rms

        print("\n" + "=" * 35)
        print(f"RESULTADO DA PERÍCIA DE ÁUDIO")
        print("=" * 35)
        print(f"Volume Médio (RMS) : {avg_rms:.2f} dB")
        print(f"Pico de Sinal      : {peak_db:.2f} dB")
        print(f"Dynamic Range (DR) : {dr:.2f} dB")
        print("-" * 35)

        # Interpretação para o seu Corolla
        if dr < 10:
            print("DIAGNÓSTICO: Áudio com ALTA COMPRESSÃO (Loudness War).")
            print("Isso explica por que no volume 12 parece 'morto'.")
            print("A falta de dinâmica exige o volume 20 para mover os falantes.")
        else:
            print("DIAGNÓSTICO: Áudio com Boa Dinâmica.")
            print("Se o som está ruim, o gargalo é o bitrate ou o rádio.")

    except Exception as e:
        print(f"[-] Erro ao processar o arquivo: {e}")


if __name__ == "__main__":
    analise_pericial()