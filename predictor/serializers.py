from rest_framework import serializers
from .models import CSVFile
import csv
import io

class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = ('id', 'file', 'uploaded_at', 'processed')
        read_only_fields = ('uploaded_at', 'processed')
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Validate CSV format (basic check)
        try:
            decoded_file = value.read().decode('utf-8')
            csv_reader = csv.reader(io.StringIO(decoded_file))
            # Read first few rows to check format
            for i, row in enumerate(csv_reader):
                if i >= 5:  # Just check first 5 rows
                    break
            
            # Reset file pointer for later processing
            value.seek(0)
        except Exception as e:
            raise serializers.ValidationError(f"Invalid CSV format: {str(e)}")
        
        return value