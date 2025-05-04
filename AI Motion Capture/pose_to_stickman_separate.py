import cv2
import mediapipe as mp
import numpy as np

# Inicializa o módulo de pose do MediaPipe, responsável por detectar articulações do corpo.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,         # True: processa imagens estáticas; False: trata como vídeo.
    model_complexity=1,              # Nível de complexidade da rede (0, 1 ou 2).
    enable_segmentation=False,       # Se ativado, segmenta o corpo da pessoa do fundo.
    min_detection_confidence=0.5,    # Confiança mínima para considerar uma pose detectada.
    min_tracking_confidence=0.5      # Confiança mínima para manter o rastreio entre frames.
)

# Utilitário para desenhar as conexões da pose
mp_drawing = mp.solutions.drawing_utils

# Carrega o vídeo de entrada. Substitua o nome pelo seu arquivo.
cap = cv2.VideoCapture("1_1Formated.mp4")

# Prepara um vídeo de saída (onde o boneco será gravado).
out = cv2.VideoWriter('output_boneco.mp4',
                      cv2.VideoWriter_fourcc(*'mp4v'),
                      30,  # FPS do vídeo
                      (640, 480))  # Resolução (deve bater com o seu vídeo)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Sai do loop se o vídeo acabar

    # Converte o frame de BGR (padrão do OpenCV) para RGB (padrão do MediaPipe)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processa o frame para extrair as poses
    results = pose.process(image_rgb)

    # Cria uma "tela em branco" onde o boneco palito será desenhado
    boneco = np.ones((480, 640, 3), dtype=np.uint8) * 255  # fundo branco

    if results.pose_landmarks:
        # Para cada conexão entre pontos (ex: ombro-esquerdo até cotovelo-esquerdo)
        for connection in mp_pose.POSE_CONNECTIONS:
            start_idx, end_idx = connection

            # Pega os pontos de início e fim da conexão
            start = results.pose_landmarks.landmark[start_idx]
            end = results.pose_landmarks.landmark[end_idx]

            # Converte coordenadas normalizadas (0 a 1) para pixels da imagem
            h, w = boneco.shape[:2]
            x1, y1 = int(start.x * w), int(start.y * h)
            x2, y2 = int(end.x * w), int(end.y * h)

            # Desenha a linha do boneco
            cv2.line(boneco, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # Mostra o boneco em tempo real
        cv2.imshow('Boneco Palito', boneco)

        # Salva o frame do boneco no arquivo de saída
        out.write(boneco)

    # Exibe o vídeo original com a pose
    cv2.imshow('Pose Estimation', frame)

    # Encerra o loop se a tecla 'q' for pressionada
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Libera os recursos após o término
cap.release()
out.release()
cv2.destroyAllWindows()
