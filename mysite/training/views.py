from django.shortcuts import render, redirect, reverse  
from django.views import View 

class index(View):
    """ 最初アクセスするとトップページにとぶ """
    def get(self, request, *args, **kwargs):
        return render(request,'app_folder/top_page.html')
index = index.as_view()