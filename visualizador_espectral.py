import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import glob
import os


def gerar_espectrograma():
    # Localiza o arquivo de forma robusta
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_path = os.path.join(script_dir, "downloads")
    arquivos = glob.glob(os.path.join(downloads_path, "*.mp3"))
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

    # 3. SALVAR LOG E IMAGEM
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    nome_base = os.path.splitext(os.path.basename(caminho))[0]
    img_path = os.path.join(log_dir, f"espectrograma_{nome_base}.png")
    
    print(f"[*] Gerando gráfico espectral... Aguarde.")
    plt.tight_layout()
    plt.savefig(img_path)
    print(f"[OK] Espectrograma salvo em: {img_path}")
    plt.show()


if __name__ == "__main__":
    gerar_espectrograma()