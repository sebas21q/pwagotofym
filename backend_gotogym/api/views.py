from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer

@api_view(['POST', 'OPTIONS'])
def register(request):
    if request.method == 'OPTIONS':
        response = Response()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
        
    try:
        data = request.data
        print("📩 Datos recibidos del frontend:", data)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        plan = data.get('plan', 'Gratis')

        if not username or not email or not password:
            return Response({'error': 'Faltan campos obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'El email ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

        # CORREGIDO: Usar create_user para hashear automáticamente la contraseña
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,  # Django hashea automáticamente
            plan=plan
        )
        
        serializer = UserSerializer(user)
        response = Response({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
        
        response['Access-Control-Allow-Origin'] = '*'
        return response
        
    except Exception as e:
        print("❌ Error en registro:", str(e))
        return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'OPTIONS'])
def login(request):
    if request.method == 'OPTIONS':
        response = Response()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
        
    try:
        data = request.data
        print("🔐 Intento de login:", data)

        username = data.get('username')
        password = data.get('password')

        # CORREGIDO: Mejor manejo de autenticación
        user = authenticate(request, username=username, password=password)
        if user is not None:
            serializer = UserSerializer(user)
            response = Response({
                'success': True,
                'message': 'Inicio de sesión correcto', 
                'user': serializer.data
            })
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            # CORREGIDO: Mejor diagnóstico del error
            if not User.objects.filter(username=username).exists():
                error_msg = 'Usuario no encontrado'
            else:
                error_msg = 'Contraseña incorrecta'
                
            return Response({
                'success': False,
                'error': error_msg
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        print("❌ Error en login:", str(e))
        return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)