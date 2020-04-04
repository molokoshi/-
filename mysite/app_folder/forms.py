"""Form for app"""
from django import forms
from .models import DetailInfo,FacebookSearch

class DatabaseForm(forms.ModelForm):
    """広告情報手入力フォーム"""
    class Meta:
        model = DetailInfo
        fields = '__all__'
        labels = {
            # 'ad_ud': '広告id',
            # 'name': '広告者名',
            # 'main_text': 'メインテキスト',
            # 'sub_text': 'サブテキスト',
            # 'sample_img': '画像リンク',
            # 'register_date': 'データベース登録日',
            # 'advertise_register': '広告登録日',
            # 'latest_update': '更新日',
            'memo': 'メモ',
        }
        help_texts = {
        #     'ad_ud': '広告id',
        #     'name': '広告者名',
        #     'main_text': 'メインテキスト',
        #     'sub_text': 'サブテキスト',
        #     'sample_img': '画像リンク',
        #     'register_date': 'データベース登録日',
        #     'advertise_register': '広告登録日',
        #     'latest_update': '更新日',
            'memo': 'メモ',
        }

class SearchForm(forms.ModelForm):
    """id入力フォーム"""
    class Meta:
        model = FacebookSearch
        fields = ('master_id',)
        # labels = {
        #     'master_id': '広告主id',
        # }
        # help_texts = {
        #     'master_id': '広告主id',
        # }
