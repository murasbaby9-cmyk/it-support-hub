from django.urls import path
from django.contrib import admin
from tickets import views
urlpatterns=[path('',views.index,name='home'),path('track/',views.track,name='lookup'),path('track/<uuid:code>/',views.track,name='track'),path('review/',views.review),path('chat/',views.chat),path('admin/export/',views.export),path('admin/',admin.site.urls)]
