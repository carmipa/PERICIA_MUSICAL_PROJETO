import librosa
import numpy as np
import glob
import os


def pericia_integral_completa():
    # 1. Configuração de Caminho
    base_path = r"G:\PROJETOS-OPEN\analisador_musica"
    # Busca por MP3 ou WebM na pasta downloads
    arquivos = glob.glob(os.path.join(base_path, "downloads", "*.mp3")) + \
               glob.glob(os.path.join(base_path, "downloads", "*.webm"))

    if not arquivos:
        print("[-] Nenhum arquivo de mídia encontrado na pasta downloads.")
        return

    caminho = arquivos[0]
    print(f"[*] Analisando DNA do arquivo: {os.path.basename(caminho)}")

    # 2. Carregamento do Sinal (High-Fidelity)
    # sr=None evita resampling, preservando os 48kHz do original
    y, sr = librosa.load(caminho, sr=None)

    # 3. Análise Rítmica (BPM)
    # Correção: np.mean garante que extraímos um valor escalar do array retornado
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    bpm_final = float(np.mean(tempo))

    # 4. Análise de Tonalidade Dominante (Harmonic Key)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key_map = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key_idx = np.argmax(np.sum(chroma, axis=1))
    tom_da_musica = key_map[key_idx]

    # 5. Decomposição Harmônica-Percussiva (HSS)
    y_harm, y_perc = librosa.effects.hpss(y)
    energia_percussiva = np.mean(librosa.feature.rms(y=y_perc))
    energia_harmonica = np.mean(librosa.feature.rms(y=y_harm))

    # 6. Centroide Espectral (Brilho da Gravação)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    brilho_medio = np.mean(cent)

    # 7. Zero Crossing Rate (Rugosidade/Metal)
    zcr = librosa.feature.zero_crossing_rate(y)
    rugosidade_zcr = np.mean(zcr)

    # 8. Saída de Dados Formatada
    print("\n" + "█" * 55)
    print(f"       RELATÓRIO DE PERÍCIA FORENSE COMPUTACIONAL")
    print("█" * 55)

    print(f"\n[ESTRUTURA RÍTMICA]")
    print(f"  BPM (Pulso Mecânico)  : {bpm_final:.2f}")
    print(f"  Total de Beats        : {len(beats)}")

    print(f"\n[PROPRIEDADES HARMÔNICAS]")
    print(f"  Tonalidade Dominante  : {tom_da_musica}")
    print(f"  Frequência Central    : {brilho_medio:.2f} Hz")
    print(f"  Energia Harmônica     : {energia_harmonica:.4f}")

    print(f"\n[TEXTURA E TIMBRE (METAL & TECH)]")
    print(f"  Taxa de Rugosidade    : {rugosidade_zcr:.4f} (ZCR)")
    print(f"  Energia Percussiva    : {energia_percussiva:.4f}")
    print(f"  Densidade Espectral   : {'Brilhante (Agudos)' if brilho_medio > 2500 else 'Encorpada (Graves)'}")

    print("\n" + "█" * 55)

    # Diagnóstico Final para o Corolla
    print("\n[VEREDITO PARA SISTEMA AUTOMOTIVO]:")
    if rugosidade_zcr > 0.05:
        print(" > Música com alta 'sujeira' harmônica intencional.")
        print(" > No volume 12, isso vira ruído de fundo.")
        print(" > No volume 20, vira a 'força' do metal que você percebeu.")


if __name__ == "__main__":
    pericia_integral_completa()