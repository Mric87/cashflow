import streamlit as st
import requests
import json
from typing import Dict

# Hardcoded n8n webhook URL - update this with your actual webhook URL
N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/update-bot-personality"

def add_bot_personality_form():
    """
    Simplified Streamlit form for adding new bot personalities
    """
    st.title("🤖 Add New Bot Personality")
    
    # Simple form with only required fields
    with st.form("add_bot_form", clear_on_submit=True):
        st.markdown("### Bot Details")
        
        agent_name = st.text_input(
            "Bot Name",
            placeholder="e.g., Marketing Guru, Code Assistant, Travel Advisor",
            help="Enter a unique name for your bot personality"
        )
        
        description = st.text_area(
            "Bot Description",
            placeholder="Describe the bot's personality, expertise, and role in detail...",
            height=150,
            help="Detailed description of the bot's capabilities, tone, and expertise"
        )
        
        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("Add Bot Personality", type="primary", use_container_width=True)
        
        if submitted:
            if not agent_name.strip():
                st.error("❌ Please enter a bot name")
            elif not description.strip():
                st.error("❌ Please enter a bot description")
            else:
                with st.spinner("Adding bot personality..."):
                    result = send_to_n8n_workflow(agent_name.strip(), description.strip())
                    
                    if result["success"]:
                        st.success(f"✅ {result['message']}")
                        if result.get('commit_sha'):
                            st.info(f"📝 Commit SHA: {result['commit_sha']}")
                        
                        # Show success animation
                        st.balloons()
                        
                    else:
                        st.error(f"❌ Failed to add bot: {result['message']}")

def send_to_n8n_workflow(agent_name: str, description: str) -> Dict:
    """
    Send bot personality data to n8n workflow
    """
    payload = {
        "agent_name": agent_name,
        "description": description
    }
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "message": f"HTTP {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Request failed: {str(e)}"
        }

def show_current_bots():
    """Display current bot personalities"""
    st.subheader("📋 Current Bot Personalities")
    
    current_bots = {
        "Startup Strategist": "You specialize in helping new businesses with planning and execution.",
        "Hip-Hop Guru": "Welcome to Hip-Hop Guru, the chatbot that knows the beats, rhymes, and stories of the hip-hop world!",
        "Generational Copy": "At Generational Copy, LLC, we specialize in helping each generation write and share their unique stories.",
        "Jasmine Renee": "I am a motivational speaker with a message sharing God's love that inspires others to align with their Divine Connection."
    }
    
    for i, (bot_name, description) in enumerate(current_bots.items()):
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"**{i+1}. {bot_name}**")
            with col2:
                st.write(f"_{description[:120]}{'...' if len(description) > 120 else ''}_")
            
            if i < len(current_bots) - 1:
                st.divider()

def show_tips():
    """Show tips for creating good bot personalities"""
    with st.expander("💡 Tips for Creating Great Bot Personalities"):
        st.markdown("""
        **Guidelines for Effective Bot Descriptions:**
        
        ✅ **Be Specific:** Clearly define the bot's area of expertise
        - ❌ "I help with business stuff"
        - ✅ "I specialize in startup fundraising and pitch deck creation"
        
        ✅ **Include Personality:** Define tone and communication style
        - ❌ "I answer questions about fitness"
        - ✅ "I'm an energetic personal trainer who motivates you to reach your fitness goals"
        
        ✅ **Set Clear Boundaries:** Mention what the bot focuses on
        - ✅ "I help with Python programming, debugging, and code optimization"
        
        ✅ **Add Context:** Include relevant background or approach
        - ✅ "I'm a meditation teacher who guides you through mindfulness practices with patience and compassion"
        """)

def main():
    """Main function for the bot management page"""
    st.set_page_config(
        page_title="Bot Manager",
        page_icon="🤖",
        layout="wide"
    )
    
    # Header
    st.markdown("---")
    
    # Main content in columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        add_bot_personality_form()
    
    with col2:
        show_current_bots()
        st.markdown("---")
        show_tips()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🔧 Bot personalities are automatically added to your GitHub repository"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
