# investement-portfolio-ai-analysis

```markdown
# Investment Portfolio GPT Companion

Welcome to the Investment Portfolio GPT Companion project! In this tutorial, we dive into the exciting world of OpenAI and LLaMA, sharing our experience of building an Investment Portfolio GPT Companion web application using OpenAI, LLaMA, and Python Flask. If you're curious to see a product demo and explore the code behind this app, we invite you to read the rest of this article, which includes step-by-step guidance on how we brought together these cutting-edge technologies to create an insightful tool for investment portfolio analysis.

## Overview

The Investment Portfolio GPT Companion is a single-page application (SPA) that utilizes a proprietary investment portfolio LLM model to provide answers and insights related to the assets in the investment portfolio. We will explain how to construct the LLaMA model using OpenAI and contextual information obtained from a market data API. You can find the complete code for this application in this [GitHub repository](link_to_repository).

## Inspiration

The idea for the Investment Portfolio LLM Companion came about from our own, only sometimes successful investment experience and our interest in algo trading strategies, market data APIs, and LLM models. As fintech technologists, we saw the opportunity to combine these diverse domains into a practical use case and educational content.

## Product Demo

We hope this product demo will give you a better understanding of the application’s features. Below is a brief overview of the application's functionality:

1. **Define Knowledge Base**: Before building the investment LLM model (also referred to as GPT), we need to define the investment knowledge base that includes information specific to our made-up investment portfolio.

2. **API Integration**: We used the Mboum Finance API, a market data provider freely available on the Rapid API Hub, to build the GPT model knowledgebase. The Mboum Finance API offers various market and instrument endpoints.

3. **Create GPT Index**: We used the VectorStoreIndex type index, created from an Article type array converted into a Document type array.

4. **Flask Application**: With the GPT index saved and available for use, we started the Flask app. The Flask application instantiates the VectorStoreIndex type global variable loaded from local storage during startup.

5. **User Interface**: We defined a route that renders a single-page HTML template and an API endpoint to query the LLaMA index engine based on the user-submitted query. The LLaMA engine response is returned to UI in JSON format and displayed to the user.

## Getting Started

To get started with this project, make sure you have an OpenAI account and API Key, which should be configured as environment variables in your project. Additionally, you will need the following properties in your environment configuration file:

```properties
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
OPENAI_API_KEY=***********************************
X-RapidAPI-Key=***********************************
X-RapidAPI-Host=mboum-finance.p.rapidapi.com
QUOTE_API_URL=https://mboum-finance.p.rapidapi.com/qu/quote
NEWS_API_URL=https://mboum-finance.p.rapidapi.com/ne/news/
```
