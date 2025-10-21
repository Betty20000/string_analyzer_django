from django.db import models
from django.utils import timezone


class AnalyzedString(models.Model):
    """
    Stores an analyzed string and its computed properties.
    Each string is uniquely identified by its SHA256 hash.
    """

    id = models.CharField(max_length=64, primary_key=True)  # SHA256 hash (hex)
    value = models.TextField(unique=True)
    length = models.PositiveIntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.PositiveIntegerField()
    word_count = models.PositiveIntegerField()
    sha256_hash = models.CharField(max_length=64)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["length"]),
            models.Index(fields=["word_count"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.value[:50]  # For better readability in admin

    def to_representation(self):
        """Consistent JSON representation for API responses."""
        return {
            "id": self.id,
            "value": self.value,
            "properties": {
                "length": self.length,
                "is_palindrome": self.is_palindrome,
                "unique_characters": self.unique_characters,
                "word_count": self.word_count,
                "sha256_hash": self.sha256_hash,
                "character_frequency_map": self.character_frequency_map,
            },
            "created_at": self.created_at.isoformat().replace("+00:00", "Z"),
        }
