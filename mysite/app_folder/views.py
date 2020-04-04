"""View for app"""
from django.shortcuts import render, redirect
from django.views import View, generic
from bs4 import BeautifulSoup
from app_folder import scraping
from .forms import SearchForm
from .models import BaseInfo, DetailInfo


class HomeView(View):
    """HOME画面"""

    def get(self, request, *args, **kwargs):
        """get func"""
        return render(request, 'app_folder/top_page.html')


class SearchView(View):
    """Search_id画面"""

    def get(self, request, *args, **kwargs):
        """get func"""
        form = SearchForm()
        insert = '広告主のidを入力してください。'
        context = {
            'form': form,
            'insert': insert,
        }
        return render(request, 'app_folder/search_id.html', context)

    def post(self, request, *args, **kwargs):
        """post func"""
        form = SearchForm(request.POST)
        soup = BeautifulSoup(str(form), "html.parser")
        check_form = soup.select_one("input").get("value")
        if form.is_valid:
            try:
                form.save()
                scraping.main(check_form)
                return redirect('app_folder:list')
            except ValueError:
                print("すでにidが存在しています。")
                form = SearchForm(request.POST)
                insert = "すでにidが存在しています。"
                context = {
                    'form': form,
                    'insert': insert,
                }
                return render(request, 'app_folder/search_id.html', context)
        else:
            form = SearchForm()
            insert = '入力が有効ではありません。'
            context = {
                'form': form,
                'insert': insert,
            }
        return render(request, 'app_folder/search_id.html', context)


class ListViews(generic.ListView):
    model = BaseInfo
    paginate_by = 10
    template_name = "app_folder/List.html"


class DetailViews(View):
    def get(self, request, base_id, *args, **kwargs):
        context = {
            "baseinfo": BaseInfo.objects.get(base_id= base_id),
            "detailinfo_list": DetailInfo.objects.filter(detail_id=base_id).order_by("-advertise_register"),
        }
        return render(request, 'app_folder/Detail.html', context)

#
# class DetailViews_date(View):
#     def get(self, request, base_id, *args, **kwargs):
#         context = {
#             "baseinfo": BaseInfo.objects.get(base_id= base_id),
#             "detailinfo_list": DetailInfo.objects.filter(detail_id=base_id).order_by("-advertise_register"),
#         }
#         return render(request, 'app_folder/Detail.html', context)
