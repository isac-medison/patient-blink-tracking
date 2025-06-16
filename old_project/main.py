from fastapi import FastAPI, Path
from fastapi.responses import StreamingResponse
import cv2
import mediapipe as mp
import math
import time
# Ініціалізація моделей MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Індекси точок на обличчі для очей
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_EYE = [362, 385, 387, 263, 373, 380]

# Функція для обчислення відстані між точками
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Функція для обчислення EAR (Eye Aspect Ratio)
def get_eye_aspect_ratio(eye_landmarks):
    vertical1 = euclidean(eye_landmarks[1], eye_landmarks[5])
    vertical2 = euclidean(eye_landmarks[2], eye_landmarks[4])
    horizontal = euclidean(eye_landmarks[0], eye_landmarks[3])
    return (vertical1 + vertical2) / (2.0 * horizontal)

# Параметри для детекції кліпання очей
EYE_AR_THRESH = 0.21   # Поріг EAR для визначення закритих очей (можна налаштувати)
EYE_AR_CONSEC_FRAMES = 12  # Кількість кадрів підряд для кліпання

# Лічильники
blink_counter = 0  # Лічильник для підрядних кліпань
total_blinks = 0   # Загальна кількість кліпань
consecutive_blinks = 0  # Лічильник підрядних кліпань для виклику медсестри
blink_times = []  # Час, коли сталося кліпання

app = FastAPI()

# Зберігаємо камери для кожного пацієнта, якщо потрібно розширити
camera = cv2.VideoCapture(0)
def generate_frames(patient_id: str):
    blink_counter=0
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        h, w = frame.shape[:2]

        # Перетворюємо кадр у RGB для MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            # Функція для отримання точок на обличчі
            def get_landmark_points(indices):
                return [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]

            # Отримуємо точки для обох очей
            right_eye = get_landmark_points(RIGHT_EYE)
            left_eye = get_landmark_points(LEFT_EYE)

            # Обчислюємо середній EAR
            right_ear = get_eye_aspect_ratio(right_eye)
            left_ear = get_eye_aspect_ratio(left_eye)
            ear = (right_ear + left_ear) / 2.0

            # Перевірка кліпання
            if ear <= EYE_AR_THRESH:
                blink_counter += 1

            # Виведення на екран
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, f"Blinks: {blink_counter} ", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

            # Малюємо контури очей
            for x, y in right_eye + left_eye:
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)


        # Показуємо результат
        # cv2.imshow("Eye Blink Tracker", frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


    # while True:
    #     success, frame = camera.read()
    #     if not success:
    #         break
    #
    #     # Тут можна додати індивідуальну обробку по patient_id, наприклад логування
    #     _, buffer = cv2.imencode('.jpg', frame)
    #     frame_bytes = buffer.tobytes()
    #
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video/{patient_id}")
def video_feed(patient_id: str = Path(..., description="Унікальний ідентифікатор пацієнта")):
    return StreamingResponse(generate_frames(patient_id), media_type="multipart/x-mixed-replace; boundary=frame")