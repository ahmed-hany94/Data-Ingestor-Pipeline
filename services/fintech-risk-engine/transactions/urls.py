from django.urls import path

from . import views

urlpatterns = [
    path("score", views.ScoreTransactionView.as_view(), name="score-transaction"),
    path("transactions", views.TransactionListView.as_view(), name="list-transactions"),
]
