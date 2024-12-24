
from django.shortcuts import render
from django.http import JsonResponse
import json
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from typing import Any
from django.views.decorators.csrf import csrf_exempt

# HuggingFace API Setup
HUGGINGFACEHUB_API_TOKEN = "Your_API_Token"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=50, temperature=0.7, token=HUGGINGFACEHUB_API_TOKEN)

db_user = "abc"
db_password = "abc"
db_host = "abc"
db_name = "abc"
table_name = "abc"

db = SQLDatabase.from_uri(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
    include_tables=[table_name],
    sample_rows_in_table_info=3,
)

class BaseCache:
    def get(self, key: str) -> Any:
        return None

    def set(self, key: str, value: Any) -> None:
        pass

class Callbacks:
    def on_request_start(self, *args: Any, **kwargs: Any) -> None:
        pass

    def on_request_end(self, *args: Any, **kwargs: Any) -> None:
        pass

SQLDatabaseChain.BaseCache = BaseCache
SQLDatabaseChain.Callbacks = Callbacks
SQLDatabaseChain.model_rebuild()

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

@csrf_exempt
def generate_sql_query(request):
    if request.method == "POST" and request.headers.get('Content-Type') == 'application/json':
        try:
            data = json.loads(request.body)
            question = data.get("question", "")
            if not question:
                return JsonResponse({"error": "Question is required"}, status=400)
            response = db_chain.run(question)
            return JsonResponse({"query": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request, "text_to_sql_app.html")



