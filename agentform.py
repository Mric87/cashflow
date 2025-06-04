import streamlit as st
import requests
import json
from typing import Dict, Optional

def add_bot_personality_form():
    """
    Streamlit form component for adding new bot personalities
    """
    st.subheader("🤖 Add New Bot Personality")
    
    with st.form("add_bot_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            agent_name = st.text_input(
                "Bot Name*", 
                placeholder="e.g., Marketing Guru, Code Assistant",
                help="Enter a unique name for your bot personality"
            )
            
            github_owner = st.text_input(
                "GitHub Owner*",
                placeholder="your-github-username",
                help="GitHub repository owner username"
            )
            
            github_repo = st.text_input(
                "GitHub Repository*",
                placeholder="your-repo-name",
                help="Name of the GitHub repository"
            )
        
        with col2:
            description = st.text_area(
                "Bot Description*",
                placeholder="Describe the bot's personality, expertise, and role...",
                height=100,
                help="Detailed description of the bot's capabilities and personality"
            )
            
            file_path = st.text_input(
                "File Path",
                value="streamlit_app.py",
                help="Path to the Python file containing bot personalities"
            )
            
            n8n_webhook_url = st.text_input(
                "n8n Webhook URL*",
                placeholder="https://your-n8n-instance.com/webhook/update-bot-personality",
                help="Your n8n workflow webhook URL"
            )
        
        submitted = st.form_submit_button("Add Bot Personality", type="primary")
        
        if submitted:
            if not all([agent_name, description, github_owner, github_repo, n8n_webhook_url]):
                st.error("Please fill in all required fields marked with *")
            else:
                with st.spinner("Adding bot personality..."):
                    result = send_to_n8n_workflow(
                        agent_name=agent_name,
                        description=description,
                        github_owner=github_owner,
                        github_repo=github_repo,
                        file_path=file_path,
                        webhook_url=n8n_webhook_url
                    )
                    
                    if result["success"]:
                        st.success(f"✅ {result['message']}")
                        st.info(f"Commit SHA: {result.get('commit_sha', 'N/A')}")
                        
                        # Clear form by rerunning
                        if st.button("Add Another Bot"):
                            st.rerun()
                    else:
                        st.error(f"❌ Failed to add bot: {result['message']}")

def send_to_n8n_workflow(
    agent_name: str,
    description: str,
    github_owner: str,
    github_repo: str,
    file_path: str,
    webhook_url: str
) -> Dict:
    """
    Send bot personality data to n8n workflow
    
    Args:
        agent_name: Name of the bot
        description: Bot's personality description
        github_owner: GitHub repository owner
        github_repo: GitHub repository name
        file_path: Path to the file to update
        webhook_url: n8n webhook URL
    
    Returns:
        Dict with success status and message
    """
    payload = {
        "agent_name": agent_name,
        "description": description,
        "github_owner": github_owner,
        "github_repo": github_repo,
        "file_path": file_path
    }
    
    try:
        response = requests.post(
            webhook_url,
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

def manage_bot_personalities():
    """
    Main function to manage bot personalities with form and current list
    """
    st.title("🤖 Bot Personality Manager")
    
    # Configuration section
    with st.expander("⚙️ Configuration", expanded=False):
        st.info("""
        **Setup Instructions:**
        1. Import the n8n workflow JSON into your n8n instance
        2. Configure your GitHub credentials in n8n
        3. Update the webhook URL in the form below
        4. Fill in your GitHub repository details
        """)
        
        st.code("""
        Required n8n Setup:
        - GitHub API credentials configured
        - Webhook trigger activated
        - All nodes properly connected
        """)
    
    # Current bot personalities display
    with st.expander("📋 Current Bot Personalities", expanded=True):
        current_bots = {
            "Startup Strategist": "You specialize in helping new businesses with planning and execution.",
            "Hip-Hop Guru": "Welcome to Hip-Hop Guru, the chatbot that knows the beats, rhymes, and stories of the hip-hop world!",
            "Generational Copy": "At Generational Copy, LLC, we specialize in helping each generation write and share their unique stories.",
            "Jasmine Renee": "I am a motivational speaker with a message sharing God's love that inspires others to align with their Divine Connection."
        }
        
        for bot_name, description in current_bots.items():
            with st.container():
                st.write(f"**{bot_name}**")
                st.write(f"_{description[:100]}{'...' if len(description) > 100 else ''}_")
                st.divider()
    
    # Add new bot form
    add_bot_personality_form()
    
    # Usage tips
    with st.expander("💡 Tips for Creating Bot Personalities"):
        st.markdown("""
        **Good Bot Personality Descriptions:**
        - Be specific about the bot's expertise area
        - Include the tone and style of communication
        - Mention any special knowledge or focus areas
        - Keep descriptions concise but informative
        
        **Examples:**
        - "I'm a fitness coach specializing in strength training and nutrition guidance for beginners."
        - "I help students with math problems, explaining concepts step-by-step in simple terms."
        - "I'm a creative writing assistant focused on storytelling techniques and character development."
        """)

if __name__ == "__main__":
    manage_bot_personalities()
