from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.

# using @api_view decorator

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    
    """
    Django REST Framework API*
    GET /api
    
    """
    data = {
        'api': 'v1',
        'description': 'This is the first version API on Real Estate',
        'company': 'Real Estate Company',
        'predictor': reverse('predictor', request=request),
    }
    
    return Response(data)
