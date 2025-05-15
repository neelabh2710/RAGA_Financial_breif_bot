from utils import final_call
from utils import QueryProcessor
import streamlit as st

# Set page config
st.set_page_config(
    page_title="Financial Analysis App",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
        color: #1E1E1E;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #F8F9FA;
        border-left: 5px solid #2E5BFF;
    }
    .confidence-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #FFF4E5;
        margin: 15px 0;
    }
    .section-header {
        color: #2E5BFF;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("Financial Analysis Assistant")
    
    # Inputs in sidebar
    with st.sidebar:
        st.header("API Configuration")
        groq_api_key = st.text_input("Groq API Key", type="password")
        serpapi_key = st.text_input("SerpAPI Key", type="password")
    
    # Main query input
    query = st.text_area("Enter your financial query related to Nasdaq listed companies (please specify the name of the stock in the query):", 
                       placeholder="e.g., Do a momentum analysis of the Amazon for past 2 weeks, has it break the past high ?",
                       height=100)
    
    if st.button("Analyze", type="primary"):
        if not groq_api_key or not serpapi_key:
            st.warning("Please provide both API keys in the sidebar")
            return
        if not query:
            st.warning("Please enter a query")
            return
            
        try:
            processor = QueryProcessor(groq_api_key=groq_api_key, serpapi_key=serpapi_key)
            result = processor.process_query(query)
            results = final_call(query, groq_api_key, serpapi_key)
            
            # Split the answer into components
            answer_parts = results['answer'].split('**\n\n**')
            if len(answer_parts) >= 4:
                direct_answer = answer_parts[1].replace('**', '').strip()
                reasoning = answer_parts[3].replace('**', '').strip()
                citations = answer_parts[5].replace('**', '').strip()
                confidence = answer_parts[7].replace('**', '').strip()
            else:
                direct_answer = results['answer']
                reasoning = citations = confidence = "N/A"

            # Display results in structured format
            # Custom CSS for styling
            st.markdown("""
                <style>
                .main {
                    background-color: #FFFFFF;
                }
                .result-box {
                    padding: 1.5rem;
                    border-radius: 8px;
                    margin: 1rem 0;
                    background-color: #f0f2f6;
                    border-left: 4px solid #2e5bff;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .result-box h4 {
                    color: #2e5bff !important;
                    margin-bottom: 0.8rem;
                    font-size: 1.1rem;
                }
                .result-content {
                    color: #1e1e1e;
                    line-height: 1.6;
                    font-size: 1rem;
                }
                h3 {
                    color: #1e1e1e !important;
                    border-bottom: 2px solid #2e5bff;
                    padding-bottom: 0.5rem;
                }
                </style>
                """, unsafe_allow_html=True)

            # Modified container section
            with st.container():
                
                # Direct Answer
                st.markdown(
                    f"""
                    <div class='result-box'>
                        <h4>📌 Answer to your query with Reason</h4>
                        <div class='result-content'>{direct_answer}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
            # Error handling remains the same
                    
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    main()
