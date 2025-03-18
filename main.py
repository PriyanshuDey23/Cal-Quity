import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch

from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit Configuration
st.set_page_config(page_title="AI Financial & Market Analyst", page_icon="📊", layout="wide")
st.title("📊 AI Financial & Market Analyst")
st.write("Ask about stocks, market trends, or general finance. Get expert insights instantly!")



def initialize_agents():

    # Financial Data Agent
    financial_agent = Agent(
        name="Financial AI Agent",
        model=Gemini(id="gemini-2.0-flash"),
        tools=[
            YFinanceTools(
                stock_price=True, company_info=True, stock_fundamentals=True,
                income_statements=True, key_financial_ratios=True, analyst_recommendations=True,
                company_news=True, technical_indicators=True, historical_prices=True
            )
        ],
        show_tool_calls=False,
        markdown=True,
        instructions=[
            "Always create tables for comparisons when comparing multiple stocks.",
            "Include stock price, P/E ratio, EPS growth, debt-to-equity ratio, analyst recommendations, and key financial metrics in comparisons.",
            "Provide a clear investment recommendation based on financial analysis and risk tolerance.",
            "If additional financial data is unavailable, proceed with available information."
        ],
        debug=True
    )


    # Web Research Agent
    web_researcher = Agent(
        name="Web Researcher Agent",
        model=Gemini(id="gemini-2.0-flash"),
        tools=[GoogleSearch()],
        show_tool_calls=False,
        markdown=True,
        instructions=[
            "Always include sources of the information that you gather.",
            "If no additional data is found, proceed with available financial data."
        ],
        debug=True
    )

    # Multi-Agent Team
    agents_team = Agent(
        team=[financial_agent, web_researcher],
        model=Gemini(id="gemini-2.0-flash"),
        show_tool_calls=False,
        markdown=True,
        instructions=[
            "Always include sources of the information gathered.",
            "Always create tables for comparisons.",
            "Ensure stock comparison includes key financial metrics and qualitative insights.",
            "Provide an investment recommendation based on financial analysis and market trends.",
            "If web research data is unavailable, generate insights based on financial data alone."
        ],
        debug=True
    )

    return agents_team

# Initialize agents
agents_team = initialize_agents()

def main():

    # User Input
    question = st.text_area(
        "📊 Ask a question:",
        placeholder="e.g., 'What is Tesla's stock price?' or 'Summarize today's market news.'"
    )

    if st.button("🚀 Get Insights"):
        if not question.strip():
            st.warning("⚠️ Please enter a valid question.")
        else:
            with st.spinner("🔎 Analyzing data... please wait."):
                try:
                    # Run query through AI agents
                    response = agents_team.run(question)
                    final_output = response.content if hasattr(response, 'content') else str(response)

                    if not final_output.strip():
                        st.error("❌ No relevant data found. Try a different question.")
                    else:
                        st.success("✅ Analysis Complete!")
                        st.subheader("📢 AI-Generated Insights")
                        st.markdown(final_output)

                except Exception as e:
                    st.error(f"⚠️ An error occurred: {e}")

if __name__ == "__main__":
    main()


