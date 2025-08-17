from django.http import StreamingHttpResponse, FileResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import  *
import os

def dashboard(request):
    videolar = Videolar.objects.all()
    testlar = Test.objects.all()
    context = {
        'videolar': videolar,
        'testlar': testlar,
    }
    return render(request, 'main/index.html', context)

def nazariy_qisim(request):
    nazariylar = NazariyMavzular.objects.all()
    context = {
        'nazariylar': nazariylar,
    }
    return render(request, 'main/nazariy.html', context)

def amaliy_qisim(request):
    amaliylar = AmaliyMavzular.objects.all()
    context = {
        'amaliylar': amaliylar,
    }
    return render(request, 'main/amaliy.html', context)

def media_qisim(request):
    videolar = Videolar.objects.all()
    context = {
        'videolar': videolar,
    }
    return render(request, 'main/video.html', context)

def masala_qisim(request):
    masalalar = Masalalar.objects.all()
    context = {
        'masalalar': masalalar,
    }
    return render(request, 'main/masala.html', context)

def masala_detail(request, pk):
    # masala = get_object_or_404(Masalalar, pk=pk)
    masala = Masalalar.objects.get(pk=pk)
    return render(request, 'main/masala_detail.html', {'masala': masala})

def test_qisim(request):
    testlar = Test.objects.all()
    context = {
        'testlar': testlar,
    }
    return render(request, 'main/test.html', context)

def video_detail(request, pk):
    video = get_object_or_404(Videolar, pk=pk)
    return render(request, 'main/video_detail.html', {'video': video})

def get_savollar_soni(test_id):
    test = Test.objects.annotate(savollar_soni=Count('savollar')).filter(id=test_id).first()
    return test.savollar_soni if test else 0

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    savollar_soni = get_savollar_soni(pk)
    context = {
        'test': test,
        'savollar_soni' : savollar_soni,
    }
    return render(request, 'main/test_detail.html', context)

def test_tasks(request, pk):
    test = get_object_or_404(Test, pk=pk)
    savollar = test.savollar.all()

    if request.method == 'POST':
        correct_answers = 0
        total_questions = savollar.count()

        for savol in savollar:
            user_answer = request.POST.get(f"savol_{savol.id}")
            if user_answer and user_answer.strip().lower() == savol.togri_javob.strip().lower():
                correct_answers += 1

        wrong_answers = total_questions - correct_answers
        score_percent = round((correct_answers / total_questions) * 100)

        # Baholash
        if score_percent >= 90:
            grade = "A'lo"
        elif score_percent >= 75:
            grade = "Yaxshi"
        elif score_percent >= 60:
            grade = "Qoniqarli"
        else:
            grade = "Qoniqarsiz"

        TestNatija.objects.create(
            foydalanuvchi=request.user,
            test=test,
            togri_savollar_soni=correct_answers,
            jami_savollar_soni=total_questions,
            no_togri_savollar_soni=wrong_answers,
            foiz=score_percent,
            grade=grade
        )
        # Natijani sahifaga yuborish
        return render(request, 'main/test_result.html', {
            'test' : test,
            'togri_savollar_soni' : correct_answers,
            'jami_savollar_soni' : total_questions,
            'no_togri_savollar_soni' : wrong_answers,
            'foiz' : score_percent,
            'grade' : grade
        })

    return render(request, 'main/test_tasks.html', {
        'test': test,
        'savollar': savollar
    })

def range_video_view(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.exists(file_path):
        raise Http404("Fayl topilmadi")

    if not file_path.lower().endswith('.mp4'):
        # Video bo'lmasa oddiy download
        return FileResponse(open(file_path, 'rb'))

    file_size = os.path.getsize(file_path)
    content_type = 'video/mp4'

    range_header = request.headers.get('Range', '').strip()
    start = 0
    end = file_size - 1

    if range_header:
        bytes_range = range_header.replace('bytes=', '').split('-')
        if bytes_range[0]:
            start = int(bytes_range[0])
        if len(bytes_range) > 1 and bytes_range[1]:
            end = int(bytes_range[1])

    length = end - start + 1

    def file_iterator(file_path, start, length, chunk_size=8192):
        with open(file_path, 'rb') as f:
            f.seek(start)
            remaining = length
            while remaining > 0:
                chunk = f.read(min(chunk_size, remaining))
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)

    response = StreamingHttpResponse(
        file_iterator(file_path, start, length),
        status=206 if range_header else 200,
        content_type=content_type
    )
    response['Content-Length'] = str(length)
    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
    response['Accept-Ranges'] = 'bytes'
    return response

def custom_404_view(request, exception):
    return render(request, "errors/404.html", status=404)

def custom_500_view(request):
    return render(request, "errors/500.html", status=500)

def custom_403_view(request, exception):
    return render(request, "errors/403.html", status=403)

