import logging,uuid,csv
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from .models import Request,Service,Review,Chat
from .forms import EntryForm,ReviewForm
logger=logging.getLogger(__name__)
def index(request):
    form=EntryForm(request.POST if request.method=='POST' else None)
    if request.method=='POST':
        if form.is_valid():
            item=form.save(); logger.info('Өтінім сақталды ID=%s',item.pk)
            return redirect('track',code=item.code)
        logger.warning('Өтінім формасы тексеруден өтпеді')
    return render(request,'index.html',dict(form=form,services=Service.objects.all(),reviews=Review.objects.filter(approved=True),reviewform=ReviewForm()))
def track(request,code=None):
    raw=code or request.GET.get('code',''); item=None
    try: item=Request.objects.filter(code=uuid.UUID(str(raw))).first()
    except ValueError: pass
    return render(request,'track.html',dict(item=item,searched=bool(raw)))
@require_POST
def review(request):
    f=ReviewForm(request.POST)
    if f.is_valid(): f.save(); return render(request,'notice.html',{'message':'Спасибо! Отзыв отправлен на модерацию.'})
    return render(request,'notice.html',{'message':'Проверьте имя и текст отзыва.'},status=400)
@require_POST
def chat(request):
    key='chat:'+request.META.get('REMOTE_ADDR','unknown')
    n=cache.get(key,0)
    if n>=30: return JsonResponse({'answer':'Попробуйте позже или напишите в WhatsApp.'},status=429)
    cache.set(key,n+1,60)
    msg=request.POST.get('message','').strip()[:500]; low=msg.lower()
    if not msg: return JsonResponse({'answer':'Напишите вопрос.'})
    answer='Опишите проблему в форме заявки или свяжитесь с мастером в WhatsApp. / Өтінім қалдырыңыз.'
    for words,reply in [(('windows','виндов','жүйе'),'Установка Windows — ориентировочно от 6000 ₸. Сохраните важные файлы перед установкой.'),(('wifi','wi-fi','интернет','роутер','желі'),'Проверьте питание роутера и перезапустите его. Настройка сети — от 5000 ₸.'),(('цен','стоим','баға'),'Цены указаны в каталоге. Итог согласуется после диагностики.'),(('выезд','адрес','келу'),'Оставьте заявку с адресом. Мастер согласует время выезда.'),(('привет','здрав','сәлем'),'Здравствуйте! Сәлем! Чем помочь: Windows, сеть, ремонт или выезд?')]:
        if any(w in low for w in words): answer=reply; break
    Chat.objects.create(message=msg,answer=answer)
    return JsonResponse({'answer':answer})
@staff_member_required
def export(request):
    response=HttpResponse(content_type='text/csv; charset=utf-8'); response['Content-Disposition']='attachment; filename=requests.csv'; response.write('\ufeff'); w=csv.writer(response); w.writerow(['ID','Name','Phone','Service','Status'])
    def safe(v):
        s=str(v); return "'"+s if s.startswith(('=','+','-','@','\t','\r')) else s
    for r in Request.objects.select_related('service'): w.writerow([r.pk,safe(r.name),safe(r.phone),safe(r.service),r.status])
    return response
