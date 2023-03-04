from django.urls import path
from .views import ListOfReminders, ReminderDetails, NewReminder, EditReminder, DeleteReminder, myLogin, LogoutView, CreateAccount

urlpatterns = [
    #strona główna
    path('',ListOfReminders.as_view(), name='reminders'),
    path('reminder/<int:pk>/',ReminderDetails.as_view(), name='reminder'),
    #funkcjonalność
    path('reminder-create/',NewReminder.as_view(), name='reminder-create'),
    path('reminder-update/<int:pk>/',EditReminder.as_view(), name='reminder-update'),
    path('reminder-delete/<int:pk>/',DeleteReminder.as_view(), name='reminder-delete'),
    #logowanie, rejestracja
    path('login/', myLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', CreateAccount.as_view(), name='register')
    ]