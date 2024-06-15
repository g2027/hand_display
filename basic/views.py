from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import RawMedidata
from .forms import CoordForm, MedidataForm, CompiledImages
from django.utils.text import *
from .thickness_mapping import *
from django.conf import settings

# Create your views here.


def create_rawdata(request):
    a = RawMedidata()
    a.create_rawmedidata()
    return HttpResponse("done")


def medidata_get_view(request):
    try:
        med_form = MedidataForm(request.GET)
        coord_form = CoordForm(request.GET)
        a = request.GET.get('sex', '')
        b = request.GET.get('race', '')
        c = int(request.GET.get('age', ''))
        d = int(request.GET.get('bmi', ''))
        obj_k = RawMedidata()
        obj_l = RawMedidata.objects.filter(sex = a, race = b, age = c, bmi = d).values("heatmap")
        x = int(request.GET.get('x_coord', ''))
        y = int(request.GET.get('y_coord', ''))
        a_display = [item for item in obj_k.SEX_CHOICES if item[0]==a]
        b_display = [item for item in obj_k.RACE_CHOICES if item[0]==b]
        c_display = [item for item in obj_k.AGE_CHOICES if item[0]==str(c)]
        d_display = [item for item in obj_k.BMI_CHOICES if item[0]==str(d)]
        avg_heatmap, err_heatmap, avg_point, err_point, num_heatmaps = get_maps(obj_l, x, y)
        if num_heatmaps>0:
            visualize_combined_heatmaps(f"{a_display[0][1]}, {b_display[0][1]}, {c_display[0][1]}, {d_display[0][1]}", avg_heatmap, err_heatmap, num_heatmaps, [[[x, y], avg_point, err_point]])
            temp_location = "temp/test.png"
            temp_image = CompiledImages(filtered_images = temp_location)
          
            context = {
            
            "temp": temp_image,
            "med_form": med_form,
            "coord_form":coord_form
            }
            # fields = str(fields)
            # fields_values = str(fields_values)
            # fields = fields+fields_values 
            # return HttpResponse(fields)

            return render(request, "basic/medidata_display.html", context)
        else:
            context = {
            "med_form": med_form,
            "coord_form":coord_form
            }
            return render(request, "basic/medidata_display.html", context)
    except:
        med_form = MedidataForm(request.GET)
        coord_form = CoordForm(request.GET)
        a = "1"
        b = "2"
        c = 1
        d = 2
        obj_k = RawMedidata()
        obj_l = RawMedidata.objects.filter(sex = a, race = b, age = c, bmi = d).values("heatmap")
        x = 0
        y = 0
        a_display = [item for item in obj_k.SEX_CHOICES if item[0]==a]
        b_display = [item for item in obj_k.RACE_CHOICES if item[0]==b]
        c_display = [item for item in obj_k.AGE_CHOICES if item[0]==str(c)]
        d_display = [item for item in obj_k.BMI_CHOICES if item[0]==str(d)]
        avg_heatmap, err_heatmap, avg_point, err_point, num_heatmaps = get_maps(obj_l, x, y)
        if num_heatmaps>0:
            visualize_combined_heatmaps(f"{a_display[0][1]}, {b_display[0][1]}, {c_display[0][1]}, {d_display[0][1]}", avg_heatmap, err_heatmap, num_heatmaps, [[[x, y], avg_point, err_point]])

            temp_location = "temp/test.png"
            temp_image = CompiledImages(filtered_images = temp_location)

            context = {
            "temp": temp_image,
            "med_form": med_form,
            "coord_form":coord_form
            }
            return render(request, "basic/medidata_display.html", context)
        else:
            context = {
            "med_form": med_form,
            "coord_form":coord_form
            }
            return render(request, "basic/medidata_display.html", context)


def get_maps(qset, x_coord, y_coord):
    try:
        qset_dict = list(qset)
        # print(qset_dict)
        qset_heatmaps = []
    
        for k in qset_dict:
            heat = k.get("heatmap")
            heat = settings.MEDIA_ROOT + heat
            qset_heatmaps.append(heat)
        print(qset_heatmaps)
    
        avg_heatmap, err_heatmap, num_heatmaps =  filter_combined_heatmaps(qset_heatmaps)
        # print(avg_heatmap)
        # print(err_heatmap)
        # print(num_heatmaps)
        
        avg_point = avg_heatmap.item(y_coord, x_coord)
        err_point = err_heatmap.item(y_coord, x_coord)
        # print(avg_point)
        # print(err_point)
        return avg_heatmap, err_heatmap, avg_point, err_point, num_heatmaps
        # mean_thicknesses, err_thicknesses = visualize_combined_heatmaps("average heatmap", avg_heatmap, err_heatmap, num_heatmaps)
    except:
        print("nope")
        
        return 0, 0, 0, 0, 0
