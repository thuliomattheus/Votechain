from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from nodeProject.nodeApp import views

urlpatterns = [
    path('blockchain/', views.BlockList, name='blockList'),
    path('blockchain/lastBlock/', views.LastBlock, name='lastBlock'),
    path('blockchain/status/', views.Status, name='blockchainStatus'),
    path('blockchain/newVote/', views.VoteList.as_view(), name='newVote'),
    path('blockchain/block/<int:pk>/', views.BlockDetail.as_view(), name='blockDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)