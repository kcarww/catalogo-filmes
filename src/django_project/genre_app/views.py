from ast import Delete
from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.application.use_cases.delete_genre import DeleteGenre
from core.genre.application.use_cases.list_genre import ListGenre
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.genre_app.serializers import CreateGenreInputSerializer, CreateGenreOutputSerializer, DeleteGenreInputSerializer, ListGenreOutputSerializer

class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(ListGenre.Input())
        response_serializer = ListGenreOutputSerializer(output)
        return Response(
            status=status.HTTP_200_OK,
            data=response_serializer.data
        )
        
    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository())
        
        try:
            output = use_case.execute(CreateGenre.Input(**serializer.validated_data)) # type: ignore
        except (
            InvalidGenre,
            RelatedCategoriesNotFound
        ) as error:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(error)}
            )
        
        return Response(
            status=status.HTTP_201_CREATED,
            data=CreateGenreOutputSerializer(output).data
        )
        
    def destroy(self, request: Request, pk: UUID = None) -> Response: # type: ignore
        request_data = DeleteGenreInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)
        
        input = DeleteGenre.Input(**request_data.validated_data) # type: ignore
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
        
        try:
            use_case.execute(input)
        except GenreNotFound as error:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": str(error)}
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    