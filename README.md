# AI motion capture
##🤖 Hello World da Visão Computacional com IA

Este projeto é o equivalente ao clássico "Hello World" — mas para visão computacional com inteligência artificial! Utilizando a biblioteca [MediaPipe](https://github.com/google/mediapipe) da Google, detectamos movimentos humanos em vídeo e desenhamos um boneco palito que replica esses movimentos.

> 🎥 A ideia é capturar poses humanas de um vídeo e gerar uma visualização animada simples, ideal para iniciantes na área de visão computacional ou IA aplicada.

## 🛠 Tecnologias Utilizadas

- Python 3.8+
- [OpenCV](https://opencv.org/) (cv2)
- [MediaPipe](https://mediapipe.dev/)
- NumPy

## 📂 Estrutura do Projeto

| Arquivo                          | Descrição                                                                 |
|----------------------------------|---------------------------------------------------------------------------|
| `pose_to_stickman_overlay.py`   | Desenha o boneco palito **diretamente sobre o vídeo original**.          |
| `pose_to_stickman_separate.py`  | Desenha o boneco palito em **um fundo branco separado do vídeo original**.|
| `1_1Formated.mp4`                | (Você deve substituir por seu vídeo de entrada.)                         |
| `output_boneco*.mp4`             | Vídeo gerado com o resultado do processo.                                |

## ▶️ Como Executar

1. **Instale as dependências**:
   ```bash
   pip install opencv-python mediapipe numpy
