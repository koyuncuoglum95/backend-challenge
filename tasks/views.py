from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the Task model.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed']

    def get_queryset(self):
        """
        This method restricts the returned tasks to those owned by the current authenticated user.
        """
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        This method sets the owner of the task to the current authenticated user.
        """
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new task.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific task.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update an existing task.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an existing task.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing task.
        """
        return super().destroy(request, *args, **kwargs)


class LabelViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the Label model.
    """
    serializer_class = LabelSerializer
    queryset = Label.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_queryset(self):
        """
        This method restricts the returned labels to those owned by the current authenticated user.
        """
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        This method sets the owner of the label to the current authenticated user.
        """
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new label.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific label.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update an existing label.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an existing label.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing label.
        """
        return super().destroy(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Include custom data in the response
        data.update({'custom_key': 'custom_value'})

        # Call your custom function here
        self.custom_function()

        # Invalidate existing tokens
        self.invalidate_previous_tokens(self.user)

        return data

    def custom_function(self):
        # Implement your custom logic here
        print("Custom function executed!")

    def invalidate_previous_tokens(self, user):
        # Get all outstanding tokens for the user and blacklist them
        from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            try:
                token.blacklist()
            except Exception:
                continue

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer