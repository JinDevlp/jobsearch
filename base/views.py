from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Once submitted, creates User
from django.contrib.auth.forms import UserCreationForm

# allows users to be logged in after they register 
from django.contrib.auth import login

from django.urls import reverse_lazy
from .models import Job
from .forms import JobForm


# Login Views
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True 
    
    def get_success_url(self):
        return reverse_lazy('jobs')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url =reverse_lazy('jobs')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('jobs')
        return super(RegisterPage, self).get(*args, **kwargs)
    


class JobList(LoginRequiredMixin,ListView):
    model = Job 
    context_object_name = 'jobs'
    # User can only see data belonging to them. Use 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = context['jobs'].filter(user=self.request.user)
        
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['jobs'] = context['jobs'].filter(
                employer__icontains=search_input)

        context['search_input'] = search_input

        return context
        
        
    
    
# See Job Detail
class JobDetail(LoginRequiredMixin,DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'base/job_detail.html'

# Create Job
@login_required(login_url='login')
def create_job(request):
    profile = request.user
    form = JobForm()
    template_name = 'base/job_form.html'
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = profile
            job.save()
            
            return redirect('jobs')

    context = {'form':form}
    return render (request,template_name,context)

# Edit Job
@login_required(login_url='login')
def edit_job(request,pk):
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)
    template_name = 'base/job_form.html'
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES,instance=job)
        if form.is_valid():
            form.save()
            
            return redirect('jobs')
    context = {'form':form}
    return render(request, template_name, context)
       
# Delete Job
@login_required(login_url='login')
def delete_job(request,pk):
    job = Job.objects.get(id=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs')
    context = {'job':job}
    template_name = 'base/job_delete.html'
    return render(request, template_name,context)
        
     
    