from django.db import models


class StreamingRecord(models.Model):
    artist_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    service_name = models.CharField(max_length=100)
    stream_duration = models.PositiveIntegerField(help_text="Stream duration in seconds")

    PLAYBACK_TYPE_CHOICES = [
        ('interactive', 'Interactive'),
        ('non-interactive', 'Non-Interactive'),
    ]
    playback_type = models.CharField(
        max_length=20,
        choices=PLAYBACK_TYPE_CHOICES
    )

    class Meta:
        db_table = 'streaming_record'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['artist_id']),
            models.Index(fields=['timestamp']),
        ]
        verbose_name = "Streaming Record"
        verbose_name_plural = "Streaming Records"

    def __str__(self):
        return f"Artist {self.artist_id} on {self.service_name} at {self.timestamp}"
