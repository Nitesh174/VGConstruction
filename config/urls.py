
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("contact-submit/", views.contact_submit, name="contact_submit"),
    path("chat/", views.chat, name="chat"),
]
