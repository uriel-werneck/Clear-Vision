from django.core.files.uploadedfile import InMemoryUploadedFile
from ultralytics import YOLO
import cv2 as cv
import numpy as np
from skimage import color
import PIL
import os
from PIL import Image, ImageOps
from django.conf import settings

yolo_model = YOLO(os.path.join('classifier', 'models','Classificator_YOLOv8n_Refined (16 epochs).pt'))


def remove_shadows(image):
    # Converte para tons de cinza
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    # Aplica um pequeno desfoque para reduzir ruído
    blur = cv.GaussianBlur(gray, (5, 5), 0)

    # Binariza usando Otsu (boa para fundo escuro)
    _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Inverte: queremos o ovo branco sobre fundo preto
    thresh = cv.bitwise_not(thresh)

    # Pintando por cima da imagem original
    imagem_sem_sombra = cv.cvtColor(thresh.copy(), cv.COLOR_GRAY2BGR)
    height, width = imagem_sem_sombra.shape[:2]

    for h in range(height):
        for w in range(width):
            if thresh[h, w] == 255:
                imagem_sem_sombra[h, w] = image[h, w]
    
    return imagem_sem_sombra


def segment_algorithm_2(image):
  # 1) Segmentar o ovo do fundo
  gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
  blur = cv.GaussianBlur(gray, (5, 5), 0)
  _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
  thresh = cv.bitwise_not(thresh)  # ovo branco, fundo preto

  contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  filtered = [c for c in contours if cv.contourArea(c) > 1000]
  main = max(filtered, key=cv.contourArea)

  mask = np.zeros_like(gray)
  cv.drawContours(mask, [main], -1, 255, -1)
  segmented = cv.bitwise_and(image, image, mask=mask)
  x, y, w, h = cv.boundingRect(main)
  egg_rgb = segmented[y:y+h, x:x+w]

  # 2) Converte para YIQ e extrai luminância em 8-bits
  egg_yiq = color.rgb2yiq(egg_rgb)
  Y, I, Q = cv.split(egg_yiq)
  Y_8b = (Y * 255).astype(np.uint8)

  from skimage.filters import frangi

  # 3) Realce de estruturas finas (rachaduras)
  frangi_img = frangi(Y_8b, sigmas=(5,5), scale_step=2)

  # Normalizar para 0–255
  frangi_norm = (255 * (frangi_img - frangi_img.min()) / np.ptp(frangi_img)).astype(np.uint8)

  # 6) Focar na faixa clara (percentil + delta)
  p = 98
  min_i = int(np.percentile(frangi_norm, p))
  delta = 10
  max_i = min(255, min_i + delta)
  foco = np.clip(frangi_norm, min_i, max_i)
  foco_norm = ((foco - min_i) / (max_i - min_i) * 255).astype(np.uint8)

  # 7) Threshold final (Otsu ou manual)
  _, bin_final = cv.threshold(foco_norm, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

  return bin_final


def crack_classification(django_file: InMemoryUploadedFile) -> str:
    """
    Makes a classification prediction for cracked/uncracked eggs.
    """
    results_folder = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(results_folder, exist_ok=True)
    
    pil_image = Image.open(django_file)
    pil_image = ImageOps.exif_transpose(pil_image)
    image = np.array(pil_image.convert('RGB'))
    no_shadow_img = remove_shadows(image)
    segmented_image = segment_algorithm_2(no_shadow_img)
    
    # Convert to BGR (YOLO expects BGR)
    bgr_image = cv.cvtColor(segmented_image, cv.COLOR_RGB2BGR)
    
    # Run prediction
    yolo_result = yolo_model.predict(bgr_image, verbose=False)[0]
    cracked_conf, uncracked_conf = yolo_result.probs.data.tolist()
    result_img_bgr = yolo_result.plot()
    result_img_rgb = PIL.Image.fromarray(cv.cvtColor(result_img_bgr, cv.COLOR_BGR2RGB))

    filename = f'result_{django_file.name}'
    full_path = os.path.join(results_folder, filename)
    result_img_rgb.save(full_path)

    return f'results/{filename}', cracked_conf, uncracked_conf


