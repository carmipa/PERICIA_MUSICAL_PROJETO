import librosa
import numpy as np
import glob
import os


def analise_pericial():
    # Busca automaticamente qualquer MP3 na pasta downloads (caminho robusto)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_path = os.path.join(script_dir, "downloads")
    arquivos = glob.glob(os.path.join(downloads_path, "*.mp3"))

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

        report = []
        report.append("\n" + "=" * 35)
        report.append(f"RESULTADO DA PERÍCIA DE ÁUDIO")
        report.append("=" * 35)
        report.append(f"Volume Médio (RMS) : {avg_rms:.2f} dB")
        report.append(f"Pico de Sinal      : {peak_db:.2f} dB")
        report.append(f"Dynamic Range (DR) : {dr:.2f} dB")
        report.append("-" * 35)

        # Interpretação para o seu Corolla
        if dr < 10:
            report.append("DIAGNÓSTICO: Áudio com ALTA COMPRESSÃO (Loudness War).")
            report.append("Isso explica por que no volume 12 parece 'morto'.")
            report.append("A falta de dinâmica exige o volume 20 para mover os falantes.")
        else:
            report.append("DIAGNÓSTICO: Áudio com Boa Dinâmica.")
            report.append("Se o som está ruim, o gargalo é o bitrate ou o rádio.")

        # Exibir no console
        final_output = "\n".join(report)
        print(final_output)

        # 4. SALVAR LOG (Markdown)
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        nome_base = os.path.splitext(os.path.basename(caminho))[0]
        log_path = os.path.join(log_dir, f"pericia_secundaria_{nome_base}.md")
        
        # Formatação Markdown
        md_report = [f"# 📈 Dinâmica de Áudio - {nome_base}", ""]
        md_report.extend([line.replace("=", "").replace("-", "").strip() for line in report if line.strip()])
        
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_report))
        print(f"\n[OK] Log Markdown salvo em: {log_path}")

    except Exception as e:
        print(f"[-] Erro ao processar o arquivo: {e}")


if __name__ == "__main__":
    analise_pericial()