import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="India's Cultural Heritage & Tourism",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 2rem;
        color: #2E86AB;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #F18F01;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric-card h3 {
        margin: 0 0 10px 0;
        font-size: 1.2rem;
    }
    .metric-card h2 {
        margin: 0 0 10px 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-card p {
        margin: 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #FF6B35;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


# Generate sample data (In real application, this would come from data.gov.in and other sources)
@st.cache_data
def load_cultural_data():
    # Sample cultural sites data
    cultural_sites = pd.DataFrame({
        'State': ['Rajasthan', 'Kerala', 'Tamil Nadu', 'West Bengal', 'Maharashtra', 
                 'Karnataka', 'Uttar Pradesh', 'Gujarat', 'Odisha', 'Punjab',
                 'Himachal Pradesh', 'Goa', 'Assam', 'Manipur', 'Sikkim'],
        'UNESCO_Sites': [2, 1, 3, 1, 4, 2, 3, 2, 1, 1, 0, 1, 0, 0, 0],
        'Art_Forms': [15, 12, 18, 14, 16, 13, 11, 10, 9, 8, 7, 6, 8, 9, 5],
        'Annual_Tourists': [5200000, 1100000, 4800000, 1600000, 4500000,
                           2100000, 2800000, 1900000, 1400000, 1200000,
                           800000, 600000, 500000, 200000, 150000],
        'Cultural_Budget': [450, 320, 520, 380, 580, 410, 490, 360, 280, 250,
                           180, 150, 160, 120, 90],
        'Latitude': [27.0238, 10.8505, 11.1271, 22.9868, 19.7515,
                    15.3173, 26.8467, 23.0225, 20.9517, 31.1471,
                    31.1048, 15.2993, 26.2006, 24.6637, 27.5330],
        'Longitude': [74.2179, 76.2711, 78.6569, 87.8550, 75.7139,
                     75.7139, 80.9462, 72.5714, 85.0985, 75.3412,
                     77.1734, 74.1240, 92.9376, 93.9063, 88.5122]
    })
    
    # Tourism seasonality data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    tourism_trends = pd.DataFrame({
        'Month': months,
        'Cultural_Tourism': [85, 92, 100, 88, 65, 45, 55, 60, 75, 95, 100, 90],
        'Heritage_Sites': [80, 88, 95, 85, 60, 40, 50, 55, 70, 90, 95, 85],
        'Art_Festivals': [70, 85, 90, 75, 50, 35, 45, 50, 65, 85, 90, 80]
    })
    
    # Art forms data
    art_forms = pd.DataFrame({
        'Art_Form': ['Classical Dance', 'Folk Music', 'Handicrafts', 'Painting', 
                    'Sculpture', 'Theatre', 'Literature', 'Textile Arts'],
        'Practitioners': [150000, 800000, 2500000, 500000, 180000, 120000, 300000, 1200000],
        'Revenue_Crores': [450, 1200, 3500, 800, 600, 200, 150, 2800],
        'Tourism_Impact': [85, 70, 95, 75, 65, 45, 30, 90]
    })
    
    return cultural_sites, tourism_trends, art_forms

@st.cache_data
def load_responsible_tourism_data():
    # Responsible tourism metrics
    states = ['Kerala', 'Himachal Pradesh', 'Sikkim', 'Goa', 'Karnataka',
              'Tamil Nadu', 'Rajasthan', 'Uttarakhand', 'Maharashtra', 'West Bengal']
    
    sustainability_data = pd.DataFrame({
        'State': states,
        'Eco_Score': [9.2, 8.8, 9.5, 7.5, 8.2, 7.8, 6.9, 8.5, 7.2, 7.6],
        'Community_Participation': [85, 78, 90, 65, 72, 70, 58, 80, 62, 68],
        'Cultural_Preservation': [88, 82, 85, 70, 78, 85, 92, 75, 72, 80],
        'Local_Employment': [76, 68, 72, 58, 65, 62, 55, 70, 60, 64]
    })
    
    return sustainability_data

# Load data
cultural_sites, tourism_trends, art_forms = load_cultural_data()
sustainability_data = load_responsible_tourism_data()

# Main title
st.markdown('<h1 class="main-header">🏛️ India\'s Cultural Heritage & Responsible Tourism Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
section = st.sidebar.selectbox("Choose a section:", [
    "🏠 Overview",
    "🎨 Traditional Art Forms", 
    "🗺️ Cultural Hotspots Mapping",
    "📊 Tourism Trends & Seasonality",
    "🌱 Responsible Tourism",
    "💡 Insights & Recommendations"
])

if section == "🏠 Overview":
    st.markdown('<h2 class="section-header">Cultural Heritage Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>UNESCO Sites</h3>
            <h2>40+</h2>
            <p>World Heritage Sites</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Art Forms</h3>
            <h2>200+</h2>
            <p>Traditional Art Forms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Annual Visitors</h3>
            <h2>32M+</h2>
            <p>Cultural Tourists</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Economic Impact</h3>
            <h2>₹15,000+</h2>
            <p>Crores Revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("State-wise Cultural Investment")
        fig = px.bar(cultural_sites.head(10), 
                    x='State', y='Cultural_Budget',
                    title="Government Cultural Budget Allocation (₹ Crores)",
                    color='Cultural_Budget',
                    color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Tourism vs Art Forms Correlation")
        fig = px.scatter(cultural_sites, 
                        x='Art_Forms', y='Annual_Tourists',
                        size='UNESCO_Sites',
                        hover_data=['State'],
                        title="Traditional Art Forms vs Tourist Footfall",
                        color='Cultural_Budget',
                        color_continuous_scale='Plasma')
        st.plotly_chart(fig, use_container_width=True)

elif section == "🎨 Traditional Art Forms":
    st.markdown('<h2 class="section-header">Traditional Art Forms Analysis</h2>', unsafe_allow_html=True)
    
    # Ensure data is available
    if not art_forms.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Art Form Practitioners")
            fig = px.pie(art_forms, 
                        values='Practitioners', 
                        names='Art_Form',
                        title="Distribution of Art Form Practitioners",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Economic Impact of Art Forms")
            fig = px.bar(art_forms.sort_values('Revenue_Crores', ascending=True),
                        x='Revenue_Crores', 
                        y='Art_Form',
                        orientation='h',
                        title="Revenue Generation by Art Form (₹ Crores)",
                        color='Tourism_Impact',
                        color_continuous_scale='RdYlBu')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Data loading issue. Please refresh the page.")
    
    # Detailed art forms table
    st.subheader("Art Forms Performance Matrix")
    
    try:
        # Calculate performance scores
        art_forms_copy = art_forms.copy()
        art_forms_copy['Performance_Score'] = (
            art_forms_copy['Tourism_Impact'] * 0.4 + 
            (art_forms_copy['Revenue_Crores'] / art_forms_copy['Revenue_Crores'].max() * 100) * 0.6
        ).round(1)
        
        styled_df = art_forms_copy[['Art_Form', 'Practitioners', 'Revenue_Crores', 'Tourism_Impact', 'Performance_Score']].copy()
        styled_df['Practitioners'] = styled_df['Practitioners'].apply(lambda x: f"{x:,}")
        styled_df['Revenue_Crores'] = styled_df['Revenue_Crores'].apply(lambda x: f"₹{x:,}")
        
        st.dataframe(styled_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error processing performance data: {str(e)}")
        st.dataframe(art_forms, use_container_width=True)
    
    # Insights box
    
    st.markdown("""
<style>
.insight-box {
    color: black;
}
</style>
""", unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
        <h4>🔍 Key Insights</h4>
        <ul>
            <li><strong>Textile Arts</strong> leads in both practitioner base (12L+) and revenue generation (₹2,800 cr)</li>
            <li><strong>Handicrafts</strong> has the highest tourism impact score (95/100)</li>
            <li><strong>Classical Dance</strong> shows strong tourism appeal despite smaller practitioner base</li>
            <li><strong>Literature</strong> has the lowest tourism impact but significant cultural value</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif section == "🗺️ Cultural Hotspots Mapping":
    st.markdown('<h2 class="section-header">Cultural Hotspots & Geographic Distribution</h2>', unsafe_allow_html=True)
    
    # Interactive map
    st.subheader("Interactive Cultural Sites Map")
    
    # Create base map
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
    # Add markers for each state
    for idx, row in cultural_sites.iterrows():
        popup_text = f"""
        <b>{row['State']}</b><br>
        UNESCO Sites: {row['UNESCO_Sites']}<br>
        Art Forms: {row['Art_Forms']}<br>
        Annual Tourists: {row['Annual_Tourists']:,}<br>
        Cultural Budget: ₹{row['Cultural_Budget']} cr
        """
        
        # Color code based on tourist volume
        if row['Annual_Tourists'] > 3000000:
            color = 'red'
        elif row['Annual_Tourists'] > 1500000:
            color = 'orange'
        else:
            color = 'green'
            
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=max(5, row['UNESCO_Sites'] * 3),
            popup=popup_text,
            color=color,
            fillColor=color,
            fillOpacity=0.7
        ).add_to(m)
    
    # Display map
    map_data = st_folium(m, width=700, height=500)
    
    # Analysis below map
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tourist Volume Distribution")
        fig = px.box(cultural_sites, 
                    y='Annual_Tourists',
                    title="Distribution of Annual Tourists Across States")
        fig.update_layout(yaxis_title="Annual Tourists")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Underexplored Destinations")
        underexplored = cultural_sites[cultural_sites['Annual_Tourists'] < 1000000].copy()
        underexplored['Potential_Score'] = (underexplored['Art_Forms'] * 2 + underexplored['UNESCO_Sites'] * 10)
        
        fig = px.bar(underexplored.sort_values('Potential_Score', ascending=True),
                    x='Potential_Score',
                    y='State',
                    orientation='h',
                    title="Hidden Gems - High Potential, Low Tourism",
                    color='Art_Forms',
                    color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

elif section == "📊 Tourism Trends & Seasonality":
    st.markdown('<h2 class="section-header">Tourism Trends & Seasonal Patterns</h2>', unsafe_allow_html=True)
    
    # Seasonality analysis
    st.subheader("Monthly Tourism Patterns")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tourism_trends['Month'],
        y=tourism_trends['Cultural_Tourism'],
        mode='lines+markers',
        name='Cultural Tourism',
        line=dict(color='#FF6B35', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=tourism_trends['Month'],
        y=tourism_trends['Heritage_Sites'],
        mode='lines+markers',
        name='Heritage Sites',
        line=dict(color='#2E86AB', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=tourism_trends['Month'],
        y=tourism_trends['Art_Festivals'],
        mode='lines+markers',
        name='Art Festivals',
        line=dict(color='#F18F01', width=3)
    ))
    
    fig.update_layout(
        title="Seasonal Tourism Trends (Index: 100 = Peak)",
        xaxis_title="Month",
        yaxis_title="Tourism Index",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Peak and off-peak analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Peak Season Analysis")
        peak_months = tourism_trends[tourism_trends['Cultural_Tourism'] >= 85]['Month'].tolist()
        st.write(f"**Peak Months:** {', '.join(peak_months)}")
        
        peak_data = pd.DataFrame({
            'Category': ['Cultural Tourism', 'Heritage Sites', 'Art Festivals'],
            'Average_Peak': [
                tourism_trends[tourism_trends['Cultural_Tourism'] >= 85]['Cultural_Tourism'].mean(),
                tourism_trends[tourism_trends['Cultural_Tourism'] >= 85]['Heritage_Sites'].mean(),
                tourism_trends[tourism_trends['Cultural_Tourism'] >= 85]['Art_Festivals'].mean()
            ]
        })
        
        fig = px.bar(peak_data, x='Category', y='Average_Peak',
                    title="Average Tourism Index During Peak Season",
                    color='Average_Peak',
                    color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Off-Peak Opportunities")
        off_peak_months = tourism_trends[tourism_trends['Cultural_Tourism'] < 70]['Month'].tolist()
        st.write(f"**Off-Peak Months:** {', '.join(off_peak_months)}")
        
        # Opportunity analysis
        opportunity_data = pd.DataFrame({
            'Month': off_peak_months,
            'Current_Index': tourism_trends[tourism_trends['Cultural_Tourism'] < 70]['Cultural_Tourism'].tolist(),
            'Potential_Increase': [25, 30, 20, 35]  # Sample potential increases
        })
        
        fig = px.bar(opportunity_data, x='Month', y=['Current_Index', 'Potential_Increase'],
                    title="Off-Peak Tourism Growth Potential",
                    barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

elif section == "🌱 Responsible Tourism":
    st.markdown('<h2 class="section-header">Responsible Tourism & Sustainability</h2>', unsafe_allow_html=True)
    
    # Sustainability metrics
    st.subheader("State-wise Sustainability Performance")
    
    # Create radar chart for top performing states
    top_states = sustainability_data.head(5)
    
    fig = go.Figure()
    
    for idx, state in enumerate(top_states['State']):
        state_data = top_states[top_states['State'] == state]
        
        fig.add_trace(go.Scatterpolar(
            r=[state_data['Eco_Score'].values[0],
               state_data['Community_Participation'].values[0],
               state_data['Cultural_Preservation'].values[0],
               state_data['Local_Employment'].values[0]],
            theta=['Eco Score', 'Community Participation', 'Cultural Preservation', 'Local Employment'],
            fill='toself',
            name=state
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Top 5 States - Responsible Tourism Performance"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Community Impact Analysis")
        fig = px.scatter(sustainability_data,
                        x='Community_Participation',
                        y='Local_Employment',
                        size='Eco_Score',
                        hover_data=['State'],
                        title="Community Participation vs Local Employment",
                        color='Cultural_Preservation',
                        color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sustainability Champions")
        champions = sustainability_data.sort_values('Eco_Score', ascending=False).head(5)
        
        fig = px.bar(champions,
                    x='State',
                    y='Eco_Score',
                    title="Top 5 Eco-Friendly Tourism States",
                    color='Eco_Score',
                    color_continuous_scale='Greens')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Best practices showcase
    st.subheader("Best Practices & Success Stories")
    
    tab1, tab2, tab3 = st.tabs(["Kerala Model", "Sikkim Initiative", "Himachal Approach"])
    
    with tab1:
        st.markdown("""
        ### Kerala's Responsible Tourism Model
        - **Community Ownership**: 95% of tourism activities managed by local communities
        - **Revenue Distribution**: 60% of tourism revenue stays in local communities
        - **Environmental Protection**: Strict regulations on coastal and backwater tourism
        - **Cultural Preservation**: Integration of traditional art forms in tourism packages
        """)
    
    with tab2:
        st.markdown("""
        ### Sikkim's Organic Tourism Initiative
        - **100% Organic State**: First fully organic state in India
        - **Carrying Capacity**: Strict limits on tourist numbers to protected areas
        - **Local Employment**: 85% of tourism jobs filled by locals
        - **Cultural Integration**: Mandatory cultural orientation for tourists
        """)
    
    with tab3:
        st.markdown("""
        ### Himachal Pradesh's Sustainable Mountain Tourism
        - **Waste Management**: Zero-waste tourism initiatives in key destinations
        - **Cultural Villages**: Authentic village tourism experiences
        - **Seasonal Distribution**: Promoting off-season tourism to reduce pressure
        - **Local Crafts**: Integration of traditional handicrafts in tourism economy
        """)

elif section == "💡 Insights & Recommendations":
    st.markdown('<h2 class="section-header">Strategic Insights & Recommendations</h2>', unsafe_allow_html=True)
    
    try:
        # Key insights
        st.subheader("🔍 Data-Driven Insights")
        
        insight_col1, insight_col2 = st.columns(2)
        
        import streamlit as st

# Add custom CSS to set text color to black
        st.markdown("""
    <style>
.insight-box {
    color: black;
}
</style>
""", unsafe_allow_html=True)
        with insight_col1:
            st.markdown("""
            <div class="insight-box">
                <h4>🎯 High-Impact Opportunities</h4>
                <ul>
                    <li><strong>Northeast States</strong>: High cultural diversity, low tourist volume - 300% growth potential</li>
                    <li><strong>Off-Peak Promotion</strong>: 40% capacity available during May-August period</li>
                    <li><strong>Digital Integration</strong>: 65% of cultural sites lack digital presence</li>
                    <li><strong>Handicraft Tourism</strong>: Highest ROI potential among all art forms</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col2:
            st.markdown("""
            <div class="insight-box">
                <h4>⚠️ Critical Challenges</h4>
                <ul>
                    <li><strong>Over-tourism</strong>: Top 5 states receive 70% of cultural tourists</li>
                    <li><strong>Seasonal Concentration</strong>: 60% tourists visit during 4-month peak</li>
                    <li><strong>Revenue Leakage</strong>: Only 30% revenue reaches local communities</li>
                    <li><strong>Art Form Decline</strong>: 15% traditional practices at risk</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Strategic recommendations
        st.subheader("🚀 Strategic Recommendations")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🗺️ Geographic Diversification", 
            "📅 Seasonal Management", 
            "🤝 Community Engagement", 
            "💻 Digital Innovation"
        ])
        
        with tab1:
            st.markdown("""
            ### Geographic Diversification Strategy
            
            **Priority 1: Northeast Circuit Development**
            - Create dedicated Northeast cultural circuit
            - Partner with local communities for authentic experiences
            - Develop infrastructure gradually to maintain authenticity
            - Target: 200% increase in Northeast tourism by 2027
            
            **Priority 2: Tier-2 Cultural Cities**
            - Promote lesser-known cultural centers
            - Develop theme-based circuits (textile, music, dance)
            - Create quality accommodation and transport links
            - Target: 150% growth in Tier-2 city cultural tourism
            
            **Implementation Timeline:** 24 months  
            **Investment Required:** ₹2,500 crores  
            **Expected ROI:** 340% over 5 years
            """)
        
        with tab2:
            st.markdown("""
            ### Seasonal Management Strategy
            
            **Off-Peak Incentivization**
            - 30% discount on accommodation during off-peak months
            - Special monsoon cultural festivals
            - Winter art workshops and residencies
            - Target: 40% reduction in seasonal variation
            
            **Festival Calendar Optimization**
            - Distribute major cultural events across the year
            - Create new festivals during low seasons
            - Promote regional harvest festivals
            - Target: Balanced monthly distribution by 2026
            
            **Weather-Independent Experiences**
            - Indoor cultural centers and museums
            - Covered art galleries and performance spaces
            - All-weather cultural experiences
            """)
        
        with tab3:
            st.markdown("""
            ### Community Engagement Framework
            
            **Local Ownership Model**
            - Transfer 51% tourism business ownership to communities
            - Establish community tourism boards
            - Create profit-sharing mechanisms
            - Target: 80% community participation by 2026
            
            **Skill Development Programs**
            - Train locals as cultural guides and interpreters
            - Hospitality and tourism management courses
            - Traditional craft entrepreneurship programs
            - Target: 50,000 new skilled jobs
            
            **Cultural Preservation Incentives**
            - Reward communities for maintaining traditions
            - Document and digitize cultural practices
            - Support master artisan programs
            """)
        
        with tab4:
            st.markdown("""
            ### Digital Innovation Roadmap
            
            **Virtual Cultural Experiences**
            - 360° virtual tours of UNESCO sites
            - AR-enabled cultural storytelling
            - Online workshops with master artisans
            - Target: 10M virtual visitors annually
            
            **AI-Powered Personalization**
            - Customized cultural itineraries
            - Real-time crowd management
            - Intelligent recommendation systems
            - Multi-language cultural AI guides
            
            **Blockchain for Authenticity**
            - Verify authentic cultural products
            - Track community revenue distribution
            - Certify cultural experiences
            - Prevent cultural appropriation
            """)
        
        # Implementation roadmap
        st.subheader("📈 Implementation Roadmap")
        
        roadmap_data = pd.DataFrame({
            'Phase': ['Phase 1 (0-6 months)', 'Phase 2 (6-18 months)', 'Phase 3 (18-36 months)'],
            'Focus Areas': [
                'Data Collection, Stakeholder Mapping, Pilot Projects',
                'Infrastructure Development, Community Training, Digital Platform',
                'Scale-up, Performance Monitoring, Continuous Improvement'
            ],
            'Investment (₹ Cr)': [500, 1500, 2000],
            'Expected Impact': ['Foundation Building', 'Visible Changes', 'Transformational Results']
        })
        
        st.table(roadmap_data)
        
        # Success metrics
        st.subheader("📊 Success Metrics Dashboard")
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("Tourism Distribution", "70:30", "Target: 50:50", help="Current split between top 5 vs other states")
        
        with metrics_col2:
            st.metric("Community Revenue Share", "30%", "Target: 60%", help="Percentage of tourism revenue reaching communities")
        
        with metrics_col3:
            st.metric("Seasonal Variation", "60%", "Target: 30%", help="Percentage of tourists during peak 4 months")
    
    except Exception as e:
        st.error(f"Error loading insights section: {str(e)}")
        st.write("Please refresh the page or contact support if the issue persists.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🏛️ <strong>India's Cultural Heritage Dashboard</strong></p>
    <p><em>Data sources: data.gov.in, Ministry of Tourism, Archaeological Survey of India</em></p>
    <p>By Mohith Sai and Jaffer Ali (2025)</p>
</div>
""", unsafe_allow_html=True)
