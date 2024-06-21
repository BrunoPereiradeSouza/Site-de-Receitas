from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from tag.models import Tag
from recipes.serializers import RecipeSerializer, TagSerializer


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    # def get(self, request):
    #     recipes = Recipe.objects.get_published()[:10]
    #     serializer = RecipeSerializer(
    #         instance=recipes,
    #         many=True,
    #         context={'request': request},
    #         )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = RecipeSerializer(
    #         data=request.data,
    #         context={'request': request},
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(
    #         author_id=1, category_id=1,
    #         tags=[1, 2]
    #     )
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )


class RecipeAPIv2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)
        return recipe

    def get(self, request, pk):
        serializer = RecipeSerializer(
            instance=self.get_recipe(pk),
            context={'request': request},
            )
        return Response(serializer.data)

    def patch(self, request, pk):
        serializer = RecipeSerializer(
            instance=self.get_recipe(pk),
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_recipe(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(
        instance=tag,
        context={'request': request},
        )
    return Response(serializer.data)
