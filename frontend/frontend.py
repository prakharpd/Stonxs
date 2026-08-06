import asyncio
import os

import streamlit as st
from agents import Runner

import security
import stock_agents


def setup_page():
    st.set_page_config(page_title="Stock Sentiment AI Agent", layout="wide")
    st.title("Stock Sentiment AI Agent")
    st.write(
        "Get stock price info, a quick sentiment read, and a detailed "
        "sentiment forecast report - side by side."
    )


def show_sidebar_settings():
    st.sidebar.header("LLM Provider Settings")

    provider_choice = st.sidebar.selectbox(
        "Provider",
        ["Ollama (local)", "Custom / Cloud"],
    )

    if provider_choice == "Ollama (local)":
        base_url = st.sidebar.text_input("Base URL", "http://localhost:11434/v1")
        api_key = "ollama"
        model_name = st.sidebar.text_input("Model name", "gemma4:31b-cloud")
    else:
        base_url = st.sidebar.text_input("Base URL", "https://api.openai.com/v1")
        api_key = st.sidebar.text_input("API Key", type="password")
        model_name = st.sidebar.text_input("Model name", "gpt-4o-mini")

    os.environ["OPENAI_BASE_URL"] = base_url
    os.environ["OPENAI_API_KEY"] = api_key or "ollama"

    return model_name


def update_agent_models(model_name):
    stock_agents.finance_agent.model = model_name
    stock_agents.news_sentiment_agent.model = model_name
    stock_agents.sentiment_forecast_agent.model = model_name
    security.security_agent.model = model_name


async def run_all_agents(user_input):
    price_result, sentiment_result, forecast_result = await asyncio.gather(
        Runner.run(stock_agents.finance_agent, user_input),
        Runner.run(stock_agents.news_sentiment_agent, user_input),
        Runner.run(stock_agents.sentiment_forecast_agent, user_input),
    )
    return (
        price_result.final_output,
        sentiment_result.final_output,
        forecast_result.final_output,
    )


def show_results(price_out, sentiment_out, forecast_out):
    st.markdown(
        f"""
        <div style="border:1px solid #444; border-radius:12px; padding:16px 20px;
                    margin-bottom:20px; background-color:rgba(255,255,255,0.04);">
            {price_out}
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["News Sentiment Agent", "Sentiment Forecast Agent"])

    with tab1:
        st.markdown(sentiment_out)

    with tab2:
        st.markdown(forecast_out)


def run_app():
    setup_page()

    model_name = show_sidebar_settings()
    update_agent_models(model_name)

    ticker_input = st.text_input("Write the ticker name of the stock", placeholder="e.g. TSLA")
    submit = st.button("Submit", type="primary")

    if not submit:
        return

    if not ticker_input.strip():
        st.warning("Please enter a ticker.")
        return

    if not security.check_message_basic(ticker_input):
        st.error("This input was blocked by the basic security check.")
        return

    with st.spinner("Checking input safety..."):
        is_safe, reason = security.check_message_with_ai(ticker_input)

    if not is_safe:
        st.error(f"This input was blocked by the AI security check. Reason: {reason}")
        return

    with st.spinner("Running agents..."):
        price_out, sentiment_out, forecast_out = asyncio.run(
            run_all_agents(ticker_input)
        )

    show_results(price_out, sentiment_out, forecast_out)