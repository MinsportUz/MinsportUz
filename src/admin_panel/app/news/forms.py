from django.forms import ModelForm
from admin_panel.model import press_service as news


class NewsForm(ModelForm):
    class Meta:
        model = news.News
        fields = '__all__'


class NewsCategoryForm(ModelForm):
    class Meta:
        model = news.NewsCategory
        fields = '__all__'


class NewsHashtagForm(ModelForm):
    class Meta:
        model = news.NewsHashtag
        fields = '__all__'


class FAQForm(ModelForm):
    class Meta:
        model = news.FAQ
        fields = '__all__'


class PressForm(ModelForm):
    class Meta:
        model = news.Press
        fields = '__all__'


class ArticleForm(ModelForm):
    class Meta:
        model = news.PressArticleLink
        fields = '__all__'

class ImageUploadForm(ModelForm):
    class Meta:
        model = news.MediaImage
        fields = ['image']
