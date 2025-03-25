#  backend/base/views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Note
from .serializer import NoteSerializer, UserRegisterSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data

          
            user = User.objects.get(username=request.data['username']) 

            access_token = tokens['access']
            refresh_token = tokens['refresh']

        
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }

            
            res = Response({
                'user': user_data, 
                'access_token': access_token,
                'refresh_token': refresh_token
            })

            
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            return res

        except User.DoesNotExist:
            
            return Response({'error': 'User not found'}, status=404)

        except Exception as e:
           
            return Response({'error': str(e)}, status=400)


class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            request.data['refresh'] = refresh_token

            response = super().post(request, *args, **kwargs)
            
            tokens = response.data
            access_token = tokens['access']

            res = Response()

            res.data = {'refreshed': True}

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='None',
                path='/'
            )
            
            return res

        except Exception as e:
            return Response({'refreshed': False})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):

    try:

        res = Response()
        res.data = {'success':True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('response_token', path='/', samesite='None')

        return res

    except Exception as e:
        print(e)
        return Response({'success':False})

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print(request.data) 
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
    user = request.user
    notes = Note.objects.filter(owner=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
     return Response({'authenticated':True})

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_authenticated_user(request):
    user = request.user
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "score1": getattr(user, "score1", 0),  
        "score2": getattr(user, "score2", 0)  
    }
    
    return Response(user_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def update_score(request):
    user = request.user
    new_score = request.data.get("score", None)

    if new_score is None:
        return Response({"error": "Score is required"}, status=400)

    try:
        new_score = int(new_score)
        user.score1 = new_score
        user.save()
        return Response({"message": "Score updated successfully", "score": user.score1})
    except ValueError:
        return Response({"error": "Invalid score"}, status=400)
    
@api_view(['PUT'])
def update_score2(request):
    user = request.user
    new_score = request.data.get("score2", None)

    if new_score is None:
        return Response({"error": "Score is required"}, status=400)

    try:
        new_score = int(new_score)
        user.score2 = new_score
        user.save()
        return Response({"message": "Score2 updated successfully", "score2": user.score2})
    except ValueError:
        return Response({"error": "Invalid score"}, status=400)