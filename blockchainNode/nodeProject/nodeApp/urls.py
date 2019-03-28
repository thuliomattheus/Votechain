from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from nodeProject.nodeApp import views

urlpatterns = [
    path('blockchain/', views.BlockchainList.as_view()),
    path('blockchain/block/<int:pk>/', views.BlockDetail.as_view()),
    path('blockchain/info/', views.info),
    path('blockchain/lastBlock/', views.last),
    path('blockchain/newVote/', views.VoteList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)