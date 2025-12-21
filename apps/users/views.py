from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RequestCodeView(APIView):
    def post(self, request):
        return Response(
            {"detail": "Request code endpoint"},
            status=status.HTTP_200_OK
        )


class VerifyCodeView(APIView):
    def post(self, request):
        return Response(
            {"detail": "Verify code endpoint"},
            status=status.HTTP_200_OK
        )

