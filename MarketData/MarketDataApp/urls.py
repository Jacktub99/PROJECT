from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('market-data/', views.market_data, name="market-data"),
    path('market-data/<str:azione>/<str:data_inizio>/<str:data_fine>', views.market_data, name="market-data"),
    path('get-data/<str:azione>/<str:data_inizio>/<str:data_fine>', views.get_data, name='get-data'),
    path('signup/', views.signup, name="signup-login"),
    path('logout/', views.do_logout, name="logout"),
    path('favourite/', views.favourite, name="favourite"),
    path('add-favourite/<str:azione>/<str:data_inizio>/<str:data_fine>', views.add_favourite, name="add-favourite"),
    path('delete/<int:id>', views.delete_favourite, name="delete-fav")
]
