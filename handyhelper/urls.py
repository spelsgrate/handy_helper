from django.urls import path
from app_handyhelper import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.display),
    path('addjob', views.addJob),
    path('addjob_submit', views.addJobSubmit),
    path('edit/<int:id>', views.editJob),
    path('edit_submit/<int:id>', views.editJobSubmit),
    path('view/<int:id>', views.viewJobs), 
    path('savejob/<int:id>', views.saveJob), 
    path('canceljob/<int:id>', views.cancelJob), 
    path('deletejob/<int:id>', views.delJob), 
    path('logout', views.logout),
]
