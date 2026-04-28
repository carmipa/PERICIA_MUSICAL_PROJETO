import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import glob
import os


def gerar_espectrograma():
    # Localiza o arquivo
    base_path = r"G:\PROJETOS-OPEN\analisador_musica"
    arquivos = glob.glob(os.path.join(base_path, "downloads", "*.mp3"))
    if not arquivos: return
    caminho = arquivos[0]

    # Carrega o áudio
    y, sr = librosa.load(caminho, sr=None)

    # 1. Calcula a Transformada de Fourier de Curta Duração (STFT)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    # 2. Configura a visualização (Estilo "Software de Engenharia")
    plt.figure(figsize=(12, 6))

    # Criamos o espectrograma
    img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', cmap='magma')

    plt.colorbar(img, format='%+2.0f dB')
    plt.title(f'Análise de Espectro - {os.path.basename(caminho)}')
    plt.ylabel('Frequência (Hz)')
    plt.xlabel('Tempo (min:seg)')

    # Limitamos a visão até 15kHz para ver melhor a "sujeira" do metal
    plt.ylim(0, 15000)

    print(f"[*] Gerando gráfico espectral... Aguarde.")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    gerar_espectrograma()