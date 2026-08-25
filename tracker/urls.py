from django.urls import path
from . import views #we want to access teh views file from this file

urlpatterns = [
    path('', views.home, name="home"),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('about.html', views.about, name="about"), #points to the about function in our views file
    path('game.html', views.game, name="game"),
    path('cfa.html', views.cfa, name='cfa'),
    path('college_fed.html', views.college_fed, name='college_fed'),
    path('annual_report.html', views.annual_report, name='annual_report'),
    path('contact/', views.contact, name='contact'),
    path("competition/apply/", views.competition_apply, name="competition_apply"),
    path('api/portfolio/', views.portfolio_api, name='portfolio_api'),
]
