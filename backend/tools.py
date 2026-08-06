import yfinance as yf
from agents import function_tool
from ddgs import DDGS
from gnews import GNews
from edgar import Company


@function_tool
def get_stock_price(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")

        if history.empty:
            return f"No price data found for {ticker}."

        latest_close = history["Close"].iloc[-1]
        return f"The current price of {ticker} is ${latest_close:.2f}"

    except Exception as error:
        return f"Could not get the price for {ticker}. Reason: {error}"


@function_tool
def get_analyst_recommendations(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        recommendations = stock.recommendations

        if recommendations is None or recommendations.empty:
            return f"No analyst recommendations found for {ticker}."

        latest_recommendations = recommendations.tail(10)
        return latest_recommendations.to_markdown()

    except Exception as error:
        return f"Could not get recommendations for {ticker}. Reason: {error}"


@function_tool
def get_stock_news(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news

        if not news_items:
            return f"No recent news found for {ticker}."

        articles = []
        for item in news_items[:10]:
            content = item.get("content", {})
            title = content.get("title", "No title")

            if title == "No title":
                continue

            summary = content.get("summary", "")
            provider = content.get("provider", {})
            publisher = provider.get("displayName", "Unknown source")

            articles.append(f"- [{publisher}] {title}\n  {summary}")

        if not articles:
            return f"No recent news found for {ticker}."

        return "\n".join(articles)

    except Exception as error:
        return f"Could not get news for {ticker}. Reason: {error}"


@function_tool
def get_web_news_ddgs(ticker: str) -> str:
    try:
        query = f"{ticker} stock news"

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=10))

        if not results:
            return f"No web search results found for {ticker}."

        articles = []
        for result in results:
            title = result.get("title", "No title")
            body = result.get("body", "")
            link = result.get("href", "")
            articles.append(f"- {title}\n  {body}\n  Source: {link}")

        return "\n".join(articles)

    except Exception as error:
        return f"Could not search the web for {ticker}. Reason: {error}"


@function_tool
def get_web_news_gnews(ticker: str) -> str:
    try:
        google_news = GNews(max_results=10)
        news_items = google_news.get_news(f"{ticker} stock")

        if not news_items:
            return f"No Google News results found for {ticker}."

        articles = []
        for item in news_items:
            title = item.get("title", "No title")
            description = item.get("description", "")
            publisher_info = item.get("publisher", {})
            publisher = publisher_info.get("title", "Unknown source")
            articles.append(f"- [{publisher}] {title}\n  {description}")

        return "\n".join(articles)

    except Exception as error:
        return f"Could not get Google News for {ticker}. Reason: {error}"


@function_tool
def get_quarterly_report(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        quarterly_financials = stock.quarterly_financials

        if quarterly_financials is None or quarterly_financials.empty:
            return f"No quarterly financials found for {ticker}."

        return quarterly_financials.to_markdown()

    except Exception as error:
        return f"Could not get quarterly financials for {ticker}. Reason: {error}"


@function_tool
def get_edgar_filing(ticker: str) -> str:
    try:
        company = Company(ticker)
        filing = company.get_filings(form="10-Q").latest()
        income_statement = filing.obj().financials.income_statement()
        return income_statement.to_markdown()

    except Exception as error:
        return f"Could not get the SEC filing for {ticker}. Reason: {error}"