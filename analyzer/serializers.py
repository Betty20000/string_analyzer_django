from rest_framework import serializers
from .models import AnalyzedString
import hashlib


class CreateStringSerializer(serializers.Serializer):
    value = serializers.CharField()

    def validate_value(self, value):
        # 422 — Not a string
        if not isinstance(value, str):
            raise serializers.ValidationError("Value must be a string", code="invalid_type")
        # 400 — Missing or empty string
        if not value.strip():
            raise serializers.ValidationError("Value cannot be empty", code="missing_value")
        return value

    def create(self, validated_data):
        value = validated_data["value"].strip()
        sha256_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()

        # Check for duplicates (409)
        existing = AnalyzedString.objects.filter(id=sha256_hash).first()
        if existing:
            # Return the existing object (handled in views)
            return existing, False

        # Compute string properties
        length = len(value)
        is_palindrome = value.lower() == value.lower()[::-1]
        unique_characters = len(set(value))
        word_count = len(value.split())
        char_freq = {ch: value.count(ch) for ch in set(value)}

        obj = AnalyzedString.objects.create(
            id=sha256_hash,
            value=value,
            length=length,
            is_palindrome=is_palindrome,
            unique_characters=unique_characters,
            word_count=word_count,
            sha256_hash=sha256_hash,
            character_frequency_map=char_freq,
        )

        return obj, True


class AnalyzedStringSerializer(serializers.ModelSerializer):
    """Used for read (GET) endpoints."""
    properties = serializers.SerializerMethodField()

    class Meta:
        model = AnalyzedString
        fields = ["id", "value", "properties", "created_at"]

    def get_properties(self, obj):
        return {
            "length": obj.length,
            "is_palindrome": obj.is_palindrome,
            "unique_characters": obj.unique_characters,
            "word_count": obj.word_count,
            "sha256_hash": obj.sha256_hash,
            "character_frequency_map": obj.character_frequency_map,
        }
