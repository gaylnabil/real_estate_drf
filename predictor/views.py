from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import CSVFile
from .serializers import CSVFileSerializer
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_predictor(request, *args, **kwargs):
    
    """
    Django REST Framework API*
    GET /api
    
    """
    data = {
        'api': 'v1',
        'description': 'This is the first version API on Real Estate',
        'company': 'Real Estate Company',
        'predictor': reverse('predictor_upload', request=request),
    }
    
    return Response(data)

class CSVFileListCreateView(generics.ListCreateAPIView):
    queryset = CSVFile.objects.all()
    serializer_class = CSVFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.save()
            
            # Process the CSV file (this is a basic example)
            try:
                # Use pandas to read and process the CSV
                df = pd.read_csv(csv_file.file.path)
                
                # Here you can process your CSV data as needed
                # For example, count rows or get column info
                row_count = len(df)
                columns = list(df.columns)
                
                # Mark as processed
                csv_file.processed = True
                csv_file.save()
                
                return Response({
                    'id': csv_file.id,
                    'message': 'CSV file uploaded and processed successfully',
                    'rows': row_count,
                    'columns': columns
                }, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                # If processing fails, delete the file
                csv_file.delete()
                return Response({
                    'error': f'Error processing the CSV file: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

csv_file_list_create_view = CSVFileListCreateView.as_view()
class CSVFileDetailView(generics.RetrieveDestroyAPIView):
    queryset = CSVFile.objects.all()
    serializer_class = CSVFileSerializer

csv_file_detail_view = CSVFileDetailView.as_view()
class CSVFilePreviewView(APIView):
    """Get a preview of the CSV data"""
    
    def get(self, request, pk=None):
        try:
            csv_file = CSVFile.objects.get(pk=pk)
            df = pd.read_csv(csv_file.file.path)
            
            # Return first 5 rows as preview
            preview_data = df.head(5).to_dict(orient='records')
            
            return Response({
                'preview': preview_data,
                'total_rows': len(df),
                'columns': list(df.columns)
            })
        except CSVFile.DoesNotExist:
            return Response(
                {'error': 'CSV file not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({
                'error': f'Error generating preview: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
csv_file_preview_view = CSVFilePreviewView.as_view()
