# tasks/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.template import loader
from .serializers import UserSerializer, TaskSerializer, TokenSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

def registerfunc(request):
    return HttpResponse(request, 'templates/register.html')

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # template = loader.get_template("register.html")
        return render(request, 'register.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return HttpResponse('User already exists', status=400)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        # Authenticate and log in the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # login(request, user)
            return redirect('login')  # Redirect to home page or wherever after successful registration
        else:
            return HttpResponse('Registration failed', status=400)
        # return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # template = loader.get_template("register.html")
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print("token: ", token)
            respon = render(request, 'login.html', {"message": "Login successfull", "success": True})
            respon.set_cookie(key='auth_token', value=token)
            return respon
            # Pass token to the template context
            # return render(request, 'tasks.html', {'token': token.key, 'message': 'Login successful'})
            # return HttpResponse({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials'})
            # return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class TaskListCreateAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        token = request.COOKIES.get("auth_token")
        user = Token.objects.get(key=token).user

        tasks = Task.objects.filter(user=user).order_by('-due_date')
        serializer = TaskSerializer(tasks, many=True)
        data = serializer.data

        if len(serializer.data) == 0:
            return render(request, 'tasks.html', {'tasks': 'No tasks for you. Please add one', 'count': len(tasks)})
        else:
            return render(request, "tasks.html", {'tasks': data, 'count': len(tasks), 'success': True})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print(user)
            title = request.data.get('title')
            due_date = request.data.get('due_date')
            print(title)
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                data = serializer.data
                data["success"] = True
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if User.objects.filter(username=username).exists():
        #     return HttpResponse('User already exists', status=400)
        
        # user = User.objects.create_user(username=username, password=password)
        # user.save()

    # permission_classes = [IsAuthenticated]  # Ensure the view requires authentication
    # def get(self, request):
    #     # template = loader.get_template("register.html")
    #     return render(request, 'tasks.html')
    
    # def get(self, request):
    #     user = request.user
    #     print("RRED", user)
    #     if user.is_authenticated:
    #         print("ATUHEENTICATE")
    #         # return render(request, 'tasks.html')
    #         title = request.query_params.get('title')
    #         order_by = request.query_params.get('order_by')
    #         order_by = order_by if order_by in ['title', 'due_date'] else 'due_date'
    #         if title:
    #             tasks = Task.objects.filter(user=user, title__icontains=title).order_by('due_date')
    #         else:
    #             tasks = Task.objects.filter(user=user).order_by(order_by)

    #         serializer = TaskSerializer(tasks, many=True)
    #         if len(serializer.data) == 0:
    #             return Response({'tasks': 'No tasks for you. Please add one', 'count': len(tasks)}, status=status.HTTP_200_OK)

    #         return Response({'tasks': serializer.data, 'count': len(tasks)}, status=status.HTTP_200_OK)
    #     return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    #     print(request)
    #     tasks = Task.objects.filter(user=request.user).order_by('due_date')
    #     serializer = TaskSerializer(tasks, many=True)
    #     return Response({'tasks': serializer.data, 'count': len(tasks)}, status=status.HTTP_200_OK)

    # def post(self, request):
    #     user = request.user
    #     print("USER: ", user)
    #     if user.is_authenticated:
    #         serializer = TaskSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save(user=user)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    #     serializer = TaskSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskSearch(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        token = request.COOKIES.get("auth_token")
        user = Token.objects.get(key=token).user
        title = request.GET.get('title')
        search_sort = request.GET.get('search_sort')
        search_sort = search_sort if search_sort else 'due_date'
        print("INSIDE: ", title, search_sort)
        search_sort = f'-{search_sort}'
        
        if title:
            tasks = Task.objects.filter(title__icontains=title, user=user).order_by(search_sort)
        else:
            tasks = Task.objects.filter(user=user).order_by(search_sort)

        serializer = TaskSerializer(tasks, many=True)
        data = serializer.data

        return JsonResponse({'tasks': data, 'success': True, 'count': len(data)})

        # print(data)
        # if len(serializer.data) == 0:
        #     return render(request, 'tasks.html', {'tasks': 'No tasks for you. Please add one', 'count': len(tasks)})
        # else:
        #     return render(request, "tasks.html", {'tasks': data, 'count': len(tasks)})
        # # tasks = Task.objects.filter()
        # serializer = TaskSerializer(tasks, many=True)
        # data = serializer.data

        # print(data)
        # if len(serializer.data) == 0:
        #     return render(request, 'tasks.html', {'tasks': 'No tasks for you. Please add one', 'count': len(tasks)})
        # else:
        #     return render(request, "tasks.html", {'tasks': data, 'count': len(tasks)})


class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response({'message': 'Task deleted successfully', 'success': True}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'Task does not exists', 'success': False}, status=status.HTTP_404_NOT_FOUND)
