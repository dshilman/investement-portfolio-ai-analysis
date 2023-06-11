from flask import Flask, request, render_template
import os
import logging
import traceback

from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, QuestionAnswerPrompt, download_loader


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')


@app.route("/api/ask",  methods=['GET'])
def ask_question():
    query_str = request.args.get('question', None)
    if not query_str:
        return {"error": "Please provide a question."}

    # Load the index from disk
    load_dotenv()
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    
    logging.debug ("path " + os.getcwd())
    index_file_path = os.path.join(os.getcwd(), 'indexed_files', 'data.json')
    index = GPTSimpleVectorIndex.load_from_disk(index_file_path)

    logging.debug ("Index Created")
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
        logging.debug(f"Answer {answer.response}")
        return {'answer': answer.response}

    except Exception as e:
        logging.error (f"Error while calling chatGPT: {e}")
        tb = traceback.format_exc()
        logging.error (f"Error trace: {tb}")
        return {'answer': e}


    


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)
