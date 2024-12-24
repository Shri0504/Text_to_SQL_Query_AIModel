# from django.urls import path
# from .views import generate_sql_query
#
# urlpatterns = [
#     path('generate-sql/', generate_sql_query, name='generate_sql_query'),  # Map /text-to-sql/generate-sql/
# ]

from django.urls import path
from .views import generate_sql_query

urlpatterns = [
    path('', generate_sql_query, name='text_to_sql_home'),  # Handle /text-to-sql/
    path('generate-sql/', generate_sql_query, name='generate_sql_query'),  # Map /text-to-sql/generate-sql/
]

