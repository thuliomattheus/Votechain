from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from nodeProject.nodeApp import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('blockchain/', views.BlockList, name='blockList'),
    path('blockchain/lastValidBlock/', views.LastValidBlock, name='lastValidBlock'),
    path('blockchain/status/', views.Status, name='blockchainStatus'),
    path('blockchain/vote/', views.ToVote, name='vote'),
    path('blockchain/createConnection/', views.ToConnect, name='createConnection'),
    path('blockchain/block/<int:pk>/', views.BlockDetail, name='blockDetail'),
    path('blockchain/syncBlocks/', views.SynchronizeBlocks, name='syncBlocks'),
    path('blockchain/syncNodes/', views.SynchronizeNodes, name='syncNodes'),
    path('', RedirectView.as_view(pattern_name='blockList'))
]

urlpatterns = format_suffix_patterns(urlpatterns)