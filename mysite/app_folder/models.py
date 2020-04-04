"""Model for app"""
from django.db import models

# master_id, base_id, detail_idは同一です。
class FacebookSearch(models.Model):
    """idリスト"""
    class Meta:
        db_table = '広告主idリスト'
    master_id = models.BigIntegerField(verbose_name='広告主id', primary_key=True, default=0)

    def __str__(self):
        return self.master_id


class BaseInfo(models.Model):
    """広告概要"""
    class Meta:
        db_table = 'fb_base'

    base_id = models.BigIntegerField(verbose_name='広告主id', default=0)
    key = models.ForeignKey(FacebookSearch, on_delete=models.CASCADE, null=True)
    master = models.CharField(verbose_name='広告主', max_length=255, null=True, blank=True)
    nice = models.CharField(verbose_name='いいね!', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.master


class DetailInfo(models.Model):
    """広告情報リスト"""
    class Meta:
        db_table = 'fb_detail'

    detail_id = models.BigIntegerField(verbose_name='広告主id', default=0)
    ad_id = models.BigIntegerField(verbose_name='広告id', primary_key=True, default=0)
    name = models.CharField(verbose_name='広告者名', max_length=255, null=True, blank=True)
    main_text = models.CharField(verbose_name='メインテキスト', max_length=255, null=True, blank=True)
    sub_text = models.CharField(verbose_name='サブテキスト', max_length=255, null=True, blank=True)
    sample_img = models.URLField(verbose_name='画像リンク', max_length=255, null=True, blank=True)
    register_date = models.DateTimeField(verbose_name='データベース登録日', auto_now_add=True,)
    advertise_register = models.DateTimeField(verbose_name='広告登録日', blank=True, null=True)
    latest_update = models.DateTimeField(verbose_name='更新日', auto_now=True)
    memo = models.TextField(verbose_name="memo", max_length=300, blank=True, null=True)
    connect = models.ForeignKey(BaseInfo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


