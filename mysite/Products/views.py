from django.shortcuts import render
from django.views import generic

# Create your views here.
class ModelDetailView(generic.DetailView):
    model = Model
    #template_name = ".html"
    def __str__(self):
        return self.model
