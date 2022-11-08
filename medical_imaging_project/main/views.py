import json
import base64

import pydicom
import numpy as np

from PIL import Image
from io import BytesIO
from django.http import JsonResponse 
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request, 'main/index.html')

def show_img(request):
    # ajax로부터 얻은 dictionary 에서 'dicom_file' request
    dcm_file = request.FILES['dicom_file']
    # pydicom library를 통해 dcm_file 읽기
    dcm = pydicom.dcmread(dcm_file)
    # 읽은 dcm의 pixel array를 np.stack을 통해 numpy로 변환
    dcm_image = np.stack(dcm.pixel_array)
    # numpy로 변환한 이미지를 fromarray를 통해 이미지로 변환
    rt_image = Image.fromarray(dcm_image)
    # 생성된 이미지를 base64 와 utf8을 통해 원본, web view용 인코딩
    buffered = BytesIO()
    rt_image.save(buffered, format="JPEG")
    rimg_str = base64.b64encode(buffered.getvalue()).decode('utf8')

    resize_image = rt_image.copy()
    resize_image.thumbnail((480,480), Image.ANTIALIAS)

    buffered = BytesIO()
    resize_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf8')

    image_dict = {
        # 원본 이미지 (다운로드용)
        "rdicom_image": rimg_str,
        # web view 이미지
        "dicom_image": img_str
    }

    return JsonResponse(image_dict)