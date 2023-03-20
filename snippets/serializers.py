from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetBaseSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight", format="html"
    )

    class Meta:
        model = Snippet
        fields = (
            "id",
            "url",
            "highlight",
            "title",
            "owner",
        )


class SnippetSerializer(SnippetBaseSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta(SnippetBaseSerializer.Meta):
        model = Snippet
        fields = SnippetBaseSerializer.Meta.fields + (
            "code",
            "linenos",
            "language",
            "style",
            "code_screen",
            "owner",
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="snippet-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ("url", "id", "username", "snippets")
