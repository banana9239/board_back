from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import LargeCategory, MediumCategory, SmallCategory, Board


class LargeCategories(APIView):
    
    def post(self, request):
        serializer = serializers.LargeCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class MediumCategories(APIView):
    
    def post(self, request):
        serializer = serializers.MediumCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class SmallCategories(APIView):
    
    def post(self, request):
        serializer = serializers.SmallCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class LargeCategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return LargeCategory.objects.get(pk=pk)
        except LargeCategory.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        large_category = self.get_object(pk)
        serializer = serializers.LargeCategorySerializer(large_category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        large_category = self.get_object(pk)
        serializer = serializers.LargeCategorySerializer(large_category, data=request.data, partial=True)
        if serializer.is_valid():
            large_category = serializer.save()
            return Response(serializers.LargeCategorySerializer(large_category).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        large_category = self.get_object(pk)
        large_category.delete()
        return Response({'message': 'Deleted successfully'})
    
class MediumCategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return MediumCategory.objects.get(pk=pk)
        except MediumCategory.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = serializers.MediumCategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = serializers.MediumCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            category = serializer.save()
            return Response(serializers.MediumCategorySerializer(category).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({'message': 'Deleted successfully'})
    
class SmallCategoryDetail(APIView):
    
    def get_object(self, pk):
        try:
            return SmallCategory.objects.get(pk=pk)
        except SmallCategory.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = serializers.SmallCategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = serializers.SmallCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            category = serializer.save()
            return Response(serializers.SmallCategorySerializer(category).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({'message': 'Deleted successfully'})
    
class LargeCategoryList(APIView):
    def get(self, request):
        categories = LargeCategory.objects.all()
        serializer = serializers.LargeCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class MediumCategoryList(APIView):
    def get(self, request, pk):
        categories = MediumCategory.objects.filter(large_category=pk)
        serializer = serializers.MediumCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class SmallCategoryList(APIView):
    def get(self, request, pk):
        categories = SmallCategory.objects.filter(medium_category=pk)
        serializer = serializers.SmallCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class Boards(APIView):
    
    def post(self, request):
        serializer = serializers.BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class BoardList(APIView):
    def get(self, request, pk):
        boards = Board.objects.filter(board_category=pk)
        serializer = serializers.BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
class BoardDetail(APIView):
        
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        board = self.get_object(pk)
        serializer = serializers.BoardDetailSerializer(board)
        return Response(serializer.data)
    
    def put(self, request, pk):
        board = self.get_object(pk)
        serializer = serializers.BoardDetailSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            board = serializer.save()
            return Response(serializers.BoardDetailSerializer(board).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        board = self.get_object(pk)
        board.delete()
        return Response({'message': 'Deleted successfully'})