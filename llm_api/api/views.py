import os
import logging
import traceback

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt, download_loader
from rest_framework.decorators import api_view
from rest_framework.response import Response


logger = logging.getLogger("Views")
class AskView(View):

    def get(self, request, *args, **kwargs):
        query_str = request.GET.get('question', None)
        if not query_str:
            return JsonResponse({"error": "Please provide a question."}, status=400)

        # Load the index from disk
        load_dotenv()
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        index_file_path = os.path.join(settings.BASE_DIR, 'indexed_articles', 'django_custom_user_model.json')
        index = GPTSimpleVectorIndex.load_from_disk(index_file_path)

        logger.debug ("Index Created")
        QA_PROMPT_TMPL = (
            "Hello, I have some context information for you:\n"
            "---------------------\n"
            "{context_str}"
            "\n---------------------\n"
            "Based on this context, could you please help me understand the answer to this question: {query_str}?\n"
        )
        answer = None
        QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
        try:
            answer = index.query(query_str, text_qa_template=QA_PROMPT)
            logger.debug(f"Answer {answer.response}")
        except Exception as e:
            logger.error (f"Error while calling chatGPT: {e}")
            tb = traceback.format_exc()
            logger.error (f"Error trace: {tb}")


        return JsonResponse({'answer': answer.response})

    def post(self, request, *args, **kwargs):
        # Handle POST requests if needed
        pass
