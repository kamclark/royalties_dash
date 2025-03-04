import csv
import boto3
import io
import pprint
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from stream_records.models import StreamingRecord


class Command(BaseCommand):
    help = 'Ingest CSV data from S3 and insert records into the database'

    def add_arguments(self, parser):
        parser.add_argument('bucket_name', type=str, help='S3 bucket name')
        parser.add_argument('file_key', type=str, help='CSV file key in S3')
        parser.add_argument('--bulk_size', type=int, default=1000, help='Number of records to bulk insert at a time')

    def handle(self, *args, **options):
        bucket_name = options['bucket_name']
        file_key = options['file_key']
        bulk_size = options['bulk_size']

        self.stdout.write(self.style.NOTICE("Starting CSV ingestion..."))

        # Access S3 resource with credentials
        s3 = boto3.resource(
            's3',
            aws_access_key_id="AKIARWT6ESRRCGY3XJG5",
            aws_secret_access_key="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"
        )

        s3_object = s3.Object(bucket_name, file_key)
        response = s3_object.get()

        # Wrap the binary stream in a TextIOWrapper for text processing
        stream = io.TextIOWrapper(response['Body'], encoding='utf-8')
        reader = csv.DictReader(stream)

        records = []
        count = 0

        for line in reader:
            pprint.pprint(line)  # For debugging; remove if not needed
            try:
                # Convert timestamp string to a datetime object
                timestamp = datetime.fromisoformat(line['timestamp'].replace("Z", "+00:00"))

                record = StreamingRecord(
                    artist_id=int(line['artist_id']),
                    amount=float(line['amount']),
                    timestamp=timestamp,
                    service_name=line['service_name'],
                    stream_duration=int(line['stream_duration']),
                    playback_type=line['playback_type']
                )
                records.append(record)
                count += 1

                if count % bulk_size == 0:
                    with transaction.atomic():
                        StreamingRecord.objects.bulk_create(records)
                    records = []  # Reset for the next batch
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing line {line}: {e}"))
                continue

        # Insert any remaining records
        if records:
            with transaction.atomic():
                StreamingRecord.objects.bulk_create(records)

        self.stdout.write(self.style.SUCCESS(f"Inserted {count} records into the database."))
