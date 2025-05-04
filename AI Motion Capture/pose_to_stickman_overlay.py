import cv2
import mediapipe as mp
import numpy as np

# Inicializa o módulo de detecção de pose do MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,       # Indica que o vídeo está em movimento (não é imagem estática)
    model_complexity=1,            # Complexidade do modelo: 0 = mais leve, 2 = mais preciso
    enable_segmentation=False,     # Não usaremos segmentação (separa fundo e pessoa)
    min_detection_confidence=0.5,  # Confiabilidade mínima para detectar a pose
    min_tracking_confidence=0.5    # Confiabilidade mínima para continuar rastreando
)

# Utilitário do MediaPipe para desenhar as conexões da pose
mp_drawing = mp.solutions.drawing_utils

# Abre o vídeo original
cap = cv2.VideoCapture("1_1Formated.mp4")

# Captura dimensões do vídeo e taxa de quadros
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Cria um gravador de vídeo para salvar a saída
out = cv2.VideoWriter(
    'output_boneco_sobre_video.mp4',                  # Nome do arquivo final
    cv2.VideoWriter_fourcc(*'mp4v'),                  # Codec de vídeo
    fps,                                              # Taxa de quadros igual à original
    (frame_width, frame_height)                       # Tamanho igual ao do vídeo original
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Sai do loop se não conseguir ler o frame

    # Converte para RGB (MediaPipe espera imagens nesse formato)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processa o frame e tenta detectar o corpo humano
    results = pose.process(image_rgb)

    # Se o corpo for detectado, desenha as conexões dos membros sobre o vídeo
    if results.pose_landmarks:
        for connection in mp_pose.POSE_CONNECTIONS:
            start_idx, end_idx = connection
            start = results.pose_landmarks.landmark[start_idx]
            end = results.pose_landmarks.landmark[end_idx]

            # Converte as coordenadas normalizadas (0–1) para coordenadas de pixel
            x1, y1 = int(start.x * frame_width), int(start.y * frame_height)
            x2, y2 = int(end.x * frame_width), int(end.y * frame_height)

            # Desenha uma linha entre os dois pontos (como um "esqueleto")
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)  # preto, espessura 2

    # Mostra o frame com o boneco por cima
    cv2.imshow('Boneco sobre vídeo', frame)

    # Salva esse frame com as linhas desenhadas
    out.write(frame)

    # Sai do loop se apertar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
out.release()
cv2.destroyAllWindows()
