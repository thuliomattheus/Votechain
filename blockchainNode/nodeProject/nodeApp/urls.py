from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from nodeProject.nodeApp import views

urlpatterns = [
    path('blockchain/', views.BlockList, name='blockList'),
    path('blockchain/lastValidBlock/', views.LastValidBlock, name='lastValidBlock'),
    path('blockchain/status/', views.Status, name='blockchainStatus'),
    path('blockchain/vote/', views.Vote.as_view(), name='vote'),
    path('blockchain/block/<int:pk>/', views.BlockDetail, name='blockDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)