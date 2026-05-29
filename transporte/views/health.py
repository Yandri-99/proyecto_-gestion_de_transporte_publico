from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'service': 'transporte-publico', 'status': 'ok', 'version': '1.0'})


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_cicd(request):
    return Response({'service': 'transporte-publico', 'status': 'ok', 'version': '1.0', 'message': 'CI/CD Successfully'})
