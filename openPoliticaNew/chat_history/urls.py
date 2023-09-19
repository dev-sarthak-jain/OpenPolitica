from django.urls import path
from . import views

urlpatterns = [
    path('transactions/<user_id>', views.allTranscripts, name='transaction_list'),
]


