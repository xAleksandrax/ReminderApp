from django import forms
from .models import Reminder
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


class ListOfReminders(LoginRequiredMixin, ListView): 
    model = Reminder
    context_object_name = 'reminders'

    def get_context_data(self, **kwargs):
        user_data = super().get_context_data(**kwargs)
        user_data['reminders'] = user_data['reminders'].filter(user = self.request.user)
        return user_data
 
class ReminderDetails(LoginRequiredMixin, DetailView):
    model = Reminder
    context_object_name = 'reminder'
    template_name = 'base/reminder.html'

class NewReminder(LoginRequiredMixin, CreateView):
    model = Reminder
    fields = ['title', 'description']
    success_url = reverse_lazy('reminders')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['title'].widget.attrs.update({'placeholder': 'Wprowadź tytuł'})
        form.fields['description'].widget.attrs.update({'placeholder': 'Wprowadź opis'})
        return form
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Dodano przypomnienie')
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class EditReminder(LoginRequiredMixin, UpdateView):
    model = Reminder
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('reminders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['editing'] = True
        else:
            context['editing'] = False
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Zmiany zostały zapisane')
        return super().form_valid(form)

class DeleteReminder(LoginRequiredMixin, DeleteView):
    model = Reminder
    context_object_name = 'reminder'
    success_url = reverse_lazy('reminders')

    def form_valid(self, form):
        messages.success(self.request, 'Usunięto przypomnienie')
        return super().form_valid(form)

class myLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    widgets = {
        'username': forms.TextInput(attrs={'autocomplete': 'off'}),
        'password': forms.PasswordInput(attrs={'autocomplete': 'off'}),
    }

    def get_success_url(self):
        return reverse_lazy('reminders')

class CreateAccount(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('reminders')
    

    def form_valid(self, form):
        if form.save() is not None:
            login(self.request, form.save())
        return super(CreateAccount, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('reminders')
        return super(CreateAccount, self).get(*args, **kwargs)
        
