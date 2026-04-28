import librosa
import numpy as np
import glob
import os


def pericia_integral_completa():
    # 1. Configuração de Caminho
    # Localiza a pasta downloads relativa ao diretório deste script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_path = os.path.join(script_dir, "downloads")
    
    arquivos = glob.glob(os.path.join(downloads_path, "*.mp3")) + \
               glob.glob(os.path.join(downloads_path, "*.webm"))

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
    report = []
    report.append("\n" + "█" * 55)
    report.append(f"       RELATÓRIO DE PERÍCIA FORENSE COMPUTACIONAL")
    report.append("█" * 55)

    report.append(f"\n[ESTRUTURA RÍTMICA]")
    report.append(f"  BPM (Pulso Mecânico)  : {bpm_final:.2f}")
    report.append(f"  Total de Beats        : {len(beats)}")

    report.append(f"\n[PROPRIEDADES HARMÔNICAS]")
    report.append(f"  Tonalidade Dominante  : {tom_da_musica}")
    report.append(f"  Frequência Central    : {brilho_medio:.2f} Hz")
    report.append(f"  Energia Harmônica     : {energia_harmonica:.4f}")

    report.append(f"\n[TEXTURA E TIMBRE (METAL & TECH)]")
    report.append(f"  Taxa de Rugosidade    : {rugosidade_zcr:.4f} (ZCR)")
    report.append(f"  Energia Percussiva    : {energia_percussiva:.4f}")
    report.append(f"  Densidade Espectral   : {'Brilhante (Agudos)' if brilho_medio > 2500 else 'Encorpada (Graves)'}")

    report.append("\n" + "█" * 55)

    # Diagnóstico Final para o Corolla
    report.append("\n[VEREDITO PARA SISTEMA AUTOMOTIVO]:")
    if rugosidade_zcr > 0.05:
        report.append(" > Música com alta 'sujeira' harmônica intencional.")
        report.append(" > No volume 12, isso vira ruído de fundo.")
        report.append(" > No volume 20, vira a 'força' do metal que você percebeu.")

    # Exibir no console
    final_output = "\n".join(report)
    print(final_output)

    # 9. SALVAR LOG (Markdown)
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    nome_base = os.path.splitext(os.path.basename(caminho))[0]
    log_path = os.path.join(log_dir, f"pericia_metadados_{nome_base}.md")
    
    # Formatação Markdown para o arquivo
    md_report = [f"# 🧬 Perícia de Metadados - {nome_base}", ""]
    md_report.extend([line.replace("█", "").strip() for line in report if line.strip()])
    
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_report))
    print(f"\n[OK] Log Markdown salvo em: {log_path}")


if __name__ == "__main__":
    pericia_integral_completa()