import asyncpg
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

async def get_blog_data():
    """
    Fetch blog data from the database for 'Latest Gossips' and 'Editor's Choice' sections
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Fetch latest gossips (most recent blogs)
        latest_gossips_query = """
            SELECT id, blog, date, category, created_at, editors_choice
            FROM blogs
            WHERE isdeleted = FALSE AND status = 'published'
            ORDER BY created_at DESC
            LIMIT 12
        """
        latest_gossips = await conn.fetch(latest_gossips_query)
        
        # Fetch editor's choice blogs (blogs marked as editor's choice)
        editors_choice_query = """
            SELECT id, blog, date, category, created_at, editors_choice
            FROM blogs
            WHERE isdeleted = FALSE AND status = 'published' AND editors_choice = 'Y'
            ORDER BY created_at DESC
            LIMIT 12
        """
        editors_choice = await conn.fetch(editors_choice_query)
        
        await conn.close()
        
        # Process the data to extract blog titles, summaries, etc.
        latest_gossips_data = []
        for blog in latest_gossips:
            blog_content = blog['blog']
            if isinstance(blog_content, str):
                blog_content = json.loads(blog_content)
            
            title = blog_content.get('blogTitle', 'Untitled Blog')
            summary = blog_content.get('blogSubHeading', '')[:150] + '...' if len(blog_content.get('blogSubHeading', '')) > 150 else blog_content.get('blogSubHeading', '')
            created_at = blog['created_at'].strftime('%B %d, %Y') if blog['created_at'] else ''
            category = blog['category'] or 'General'
            slug = blog_content.get('slug', f"blog-{blog['id']}")
            
            latest_gossips_data.append({
                'id': blog['id'],
                'title': title,
                'summary': summary,
                'created_at': created_at,
                'category': category,
                'slug': slug
            })
        
        editors_choice_data = []
        for blog in editors_choice:
            blog_content = blog['blog']
            if isinstance(blog_content, str):
                blog_content = json.loads(blog_content)
            
            title = blog_content.get('blogTitle', 'Untitled Blog')
            summary = blog_content.get('blogSubHeading', '')[:150] + '...' if len(blog_content.get('blogSubHeading', '')) > 150 else blog_content.get('blogSubHeading', '')
            created_at = blog['created_at'].strftime('%B %d, %Y') if blog['created_at'] else ''
            category = blog['category'] or 'General'
            slug = blog_content.get('slug', f"blog-{blog['id']}")
            
            editors_choice_data.append({
                'id': blog['id'],
                'title': title,
                'summary': summary,
                'created_at': created_at,
                'category': category,
                'slug': slug
            })
        
        return latest_gossips_data, editors_choice_data
        
    except Exception as e:
        print(f"Error fetching blogs: {e}")
        return [], []

def generate_blog_card_html(blog, color_index):
    """
    Generate HTML for a single blog card based on the existing structure
    """
    return f'''
        <div class="blog-card" data-category="{blog['category']}" onclick="window.location.href='/blog/{blog['slug']}'">
            <div class="blog-card-header">
                <div class="blog-dot" style="background-color: {get_blog_color(color_index)}"></div>
                <span class="blog-read-time">5 mins read</span>
            </div>
            <h3 class="blog-title">{blog['title']}</h3>
            <p class="blog-date">{blog['created_at']}</p>
            <div class="blog-footer">
                <p class="blog-description">{blog['summary']}</p>
                <div class="blog-arrow">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M5 12h14m-7-7l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
            </div>
        </div>
    '''

def get_blog_color(index):
    """
    Get color based on index to match existing color pattern
    """
    colors = ['#22c55e', '#ef444', '#06b6d4', '#22c5e', '#eab308', '#3b82f6', '#22c55e', '#ec4899', '#06b6d4', '#eab308', '#a855f7', '#22c55e']
    return colors[index % len(colors)]

async def update_blogs_html():
    """
    Update the blogs_landing.html file with dynamic content
    """
    latest_gossips_data, editors_choice_data = await get_blog_data()
    
    # Generate HTML for latest gossips
    latest_gossips_html = ""
    for i, blog in enumerate(latest_gossips_data):
        latest_gossips_html += generate_blog_card_html(blog, i)
    
    # Generate HTML for editor's choice
    editors_choice_html = ""
    for i, blog in enumerate(editors_choice_data):
        editors_choice_html += generate_blog_card_html(blog, i)
    
    # Read the original HTML file
    with open("PAGE_SERVING_ROUTERS/PAGES/blogs_landing.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    # Replace the placeholders with dynamic content
    # Replace latest gossips section
    start_marker_latest = '<!-- LATEST GOSSIPS BLOGS WILL BE INSERTED HERE DYNAMICALLY -->'
    end_marker_latest = '</div>\n            <div class="pagination-container" id="latest-gossips-pagination">'
    
    start_pos_latest = html_content.find(start_marker_latest) + len(start_marker_latest)
    end_pos_latest = html_content.find(end_marker_latest)
    
    if start_pos_latest != -1 and end_pos_latest != -1:
        html_content = html_content[:start_pos_latest] + f"\n                {latest_gossips_html}\n            " + html_content[end_pos_latest:]
    
    # Replace editor's choice section
    start_marker_editors = '<!-- EDITOR\'S CHOICE BLOGS WILL BE INSERTED HERE DYNAMICALLY -->'
    end_marker_editors = '</div>\n            <div class="pagination-container" id="editors-choice-pagination">'
    
    start_pos_editors = html_content.find(start_marker_editors) + len(start_marker_editors)
    end_pos_editors = html_content.find(end_marker_editors)
    
    if start_pos_editors != -1 and end_pos_editors != -1:
        html_content = html_content[:start_pos_editors] + f"\n                {editors_choice_html}\n            " + html_content[end_pos_editors:]
    
    # Write the updated HTML back to the file
    with open("PAGE_SERVING_ROUTERS/PAGES/blogs_landing.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print("Successfully updated blogs_landing.html with dynamic content")
    
    return latest_gossips_data, editors_choice_data

if __name__ == "__main__":
    import asyncio
    asyncio.run(update_blogs_html())