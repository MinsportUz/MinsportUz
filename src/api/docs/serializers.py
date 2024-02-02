from rest_framework import serializers
from admin_panel.model import docs


class DocsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = docs.Docs
        fields = [
            'id', 'title', 'date', 'issued_by', 'law', 'url', 'link'
        ]

    def get_url(self, obj):
        return obj.url if obj.url else obj.file_url


class DocTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = docs.DocType
        fields = [
            'id', 'title', 'slug',
        ]


class AdmDocTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = docs.DocType
        fields = "__all__"


class AdmDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = docs.Docs
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['doc_type_title_uz'] = instance.doc_type.title_uz
        data['doc_type_title_ru'] = instance.doc_type.title_ru
        data['doc_type_title_en'] = instance.doc_type.title_en
        return data


class AdmUploadFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = docs.UploadFiles
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['file'] = instance.file_url
        return data