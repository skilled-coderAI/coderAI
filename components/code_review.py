import streamlit as st
import os
from services.code_analysis_service import CodeAnalysisService

def render_code_review():
    """Render the code review and analysis interface"""
    # Create a header with logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        logo_path = os.path.join(os.getcwd(), "Logo.png")
        st.image(logo_path, width=100)
    with col2:
        st.markdown("<h1 class='main-header'>Code Review & Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subheader'>AI-Powered Code Insights</p>", unsafe_allow_html=True)
    
    # Initialize code analysis service if not exists
    if 'code_analysis_service' not in st.session_state:
        st.session_state.code_analysis_service = CodeAnalysisService()
    
    # Code input section
    st.subheader("Code Input")
    code = st.text_area(
        "Enter or paste your code here",
        height=300,
        help="Paste your code here for analysis"
    )
    
    # Analysis options
    col1, col2, col3 = st.columns(3)
    with col1:
        analyze_complexity = st.checkbox("Analyze Complexity", value=True)
    with col2:
        check_best_practices = st.checkbox("Check Best Practices", value=True)
    with col3:
        detect_smells = st.checkbox("Detect Code Smells", value=True)
    
    # Analyze button
    if st.button("Analyze Code", type="primary", disabled=not code):
        with st.spinner("Analyzing code..."):
            # Get analysis results
            analysis = st.session_state.code_analysis_service.analyze_code(code)
            metrics = st.session_state.code_analysis_service.get_code_metrics(code)
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Code Smells", "Best Practices", "Suggestions"])
            
            # Overview tab
            with tab1:
                st.subheader("Code Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Lines of Code", metrics['loc'])
                with col2:
                    st.metric("Classes", metrics['classes'])
                with col3:
                    st.metric("Functions", metrics['functions'])
                with col4:
                    st.metric("Imports", metrics['imports'])
                
                st.subheader("Complexity Analysis")
                st.progress(min(analysis['complexity_score'] / 20, 1.0))
                st.write(f"Complexity Score: {analysis['complexity_score']}")
            
            # Code Smells tab
            with tab2:
                st.subheader("Detected Code Smells")
                if analysis['code_smells']:
                    for smell in analysis['code_smells']:
                        with st.expander(f"{smell['type']} at line {smell['location']}"):
                            st.write(smell['message'])
                else:
                    st.success("No code smells detected!")
            
            # Best Practices tab
            with tab3:
                st.subheader("Best Practices Analysis")
                if analysis['best_practices']:
                    for violation in analysis['best_practices']:
                        with st.expander(f"Issue at line {violation['location']}"):
                            st.write(violation['message'])
                else:
                    st.success("All best practices are followed!")
            
            # Suggestions tab
            with tab4:
                st.subheader("Improvement Suggestions")
                if analysis['suggestions']:
                    for suggestion in analysis['suggestions']:
                        st.info(suggestion)
                else:
                    st.success("No immediate improvements suggested!")
    
    # Help section
    with st.expander("How to use the Code Review"):
        st.markdown("""
        1. **Paste your code** in the text area above
        2. Select the analysis options you want to run
        3. Click 'Analyze Code' to get insights
        4. Review the results in different tabs:
            - Overview: Basic metrics and complexity analysis
            - Code Smells: Potential issues in code structure
            - Best Practices: Adherence to coding standards
            - Suggestions: AI-powered improvement recommendations
        """)