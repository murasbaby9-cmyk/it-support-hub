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
    raw=str(code or request.GET.get('code','')).strip(); item=None
    if '/track/' in raw: raw=raw.split('/track/',1)[1].strip('/').split('?')[0]
    try: item=Request.objects.filter(code=uuid.UUID(str(raw))).first()
    except (ValueError, AttributeError): pass
    return render(request,'track.html',dict(item=item,searched=bool(raw),raw=raw))
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
    topics=[
        (('не включ','не запуска','қосылмай','черный экран','чёрный экран'),'Проверьте питание и кабель монитора. Есть ли индикаторы, шум вентиляторов или звуковые сигналы? Не вскрывайте блок питания.'),
        (('тормоз','медлен','завис','баяу'),'Откройте диспетчер задач Ctrl+Shift+Esc и проверьте загрузку CPU, памяти и диска. Какой показатель близок к 100%?'),
        (('перегрев','греется','шум','температур'),'Выключите устройство, если оно перегревается. Не закрывайте вентиляцию. Это ноутбук или настольный ПК?'),
        (('windows','виндов','драйвер','жүйе'),'Поможем с Windows и драйверами. Уточните: нужна переустановка, восстановление загрузки или устранение ошибки? Перед переустановкой сохраните файлы.'),
        (('wifi','wi-fi','интернет','роутер','желі','вайфай'),'Проверьте, работает ли интернет на другом устройстве. Если нет, перезапустите роутер. Проблема на всех устройствах или только одном?'),
        (('принтер','сканер','печата'),'Проверьте питание, бумагу и подключение. Какая модель принтера и какая ошибка отображается?'),
        (('вирус','реклама','взлом'),'Не вводите пароли на подозрительных страницах. Запустите проверку встроенным антивирусом. Что именно происходит?'),
        (('сервер','офис','локальн','бизнес'),'Настраиваем серверы и офисные сети. Сколько устройств нужно обслуживать и какая задача стоит?'),
        (('камер','видеонаблю'),'Уточните количество камер и требуется ли монтаж или настройка существующей системы.'),
        (('цен','стоим','баға','сколько','прайс'),'Ориентировочные цены: '+ '; '.join(f'{x.name}: от {x.price} ₸' for x in Service.objects.all())+'. Итог согласуется после диагностики.'),
        (('статус','номер заявки','өтінім'),'Откройте раздел «Статус» и вставьте полный код или ссылку, полученную после отправки заявки.'),
        (('выезд','адрес','келу','заказ','заявк'),'Нажмите «Оформить заявку» под чатом. Выберите услугу и оставьте контакты. Время выезда согласуем лично.'),
        (('привет','здрав','сәлем'),'Здравствуйте! Сәлем! Опишите неисправность: компьютер не включается, тормозит, нет интернета или нужна настройка?'),
    ]
    answer='Уточните модель устройства, симптомы и текст ошибки. Если нужна помощь мастера, нажмите «Оформить заявку» или WhatsApp.'
    for words,reply in topics:
        if any(w in low for w in words):
            answer=reply; request.session['chat_topic']=reply; break
    else:
        if request.session.get('chat_topic'):
            answer='Спасибо за уточнение. '+request.session['chat_topic']+' Если проблема сохраняется, оформите заявку для диагностики.'
    Chat.objects.create(message=msg,answer=answer)
    return JsonResponse({'answer':answer})
@staff_member_required
def export(request):
    response=HttpResponse(content_type='text/csv; charset=utf-8'); response['Content-Disposition']='attachment; filename=requests.csv'; response.write('\ufeff'); w=csv.writer(response); w.writerow(['ID','Name','Phone','Service','Status'])
    def safe(v):
        s=str(v); return "'"+s if s.startswith(('=','+','-','@','\t','\r')) else s
    for r in Request.objects.select_related('service'): w.writerow([r.pk,safe(r.name),safe(r.phone),safe(r.service),r.status])
    return response
