# fileupload/views.py
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload
from django.http import HttpResponse
import torch, gc
from diffusers import StableDiffusionPipeline
from datetime import datetime
import time
import io
def fileUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        upimg = request.FILES["imgfile"]
        gc.collect()
        torch.cuda.empty_cache()
        prompt=content
        pipeline = StableDiffusionPipeline.from_single_file('/home/mercury/django/stdtest/teststd/v1-5-pruned-emaonly.safetensors')
        pipeline.to("cuda")
        pipeline.safety_checker=None
        return_dict=True
        hgight=512
        width=512
        num_inference_steps=20
        guidance_scale=8.5
        negative_prompt=""
        num_images_per_prompt=1
        eta=0.0
        generator=None
        latents =None
        prompt_embeds=None
        negative_prompt_embeds =None
        output_type="pil"
        return_dict=True
        callback =None
        callback_steps=1
        cross_attention_kwargs=None
        guidance_rescale=0.0
        images = 	pipeline(prompt,hgight,width,num_inference_steps,guidance_scale,negative_prompt,num_images_per_prompt,eta,)
        for i in range(len(images.images)):
        	images.images[i].save('/home/mercury/django/mysite/media/logo.png','png')
    		#images.images[i].save(datetime.now().strftime('/home/mercury/django/stdtest/teststd/expimg/%Y%m%d%H%M%S%F.png'),'png')
        img = images.images[0]
        fileupload = FileUpload(
            title=title,
            content=content,
            imgfile=upimg,
        )
        fileupload.save()
        page_obj={
            'page_obj' : [fileupload] ,
        }
        img_io=io.BytesIO()
        img.save(img_io,format='PNG')
        img_data=img_io.getvalue()
        img_io.close()
        response = HttpResponse(content_type='image/png')
        response.write(img_data)
        return response
        #return render(request, 'showimg.html',page_obj)
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)
def showimg(request):

	return render(request,'showimg.html')
