from django.urls import path
from .views import explain_view, debug_view, convert_view,download_pdf_view,generate_view




urlpatterns = [
    path('explain/', explain_view, name='explain_code'),
     path('debug/', debug_view, name='debug_code'),
     path("convert/", convert_view, name="convert"),
     path("download/", download_pdf_view, name="download_pdf"),
     path("generate/", generate_view, name="generate"),



]
