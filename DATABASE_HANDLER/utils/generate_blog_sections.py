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
            WHERE isdeleted = FALSE
            ORDER BY created_at DESC
        """
        latest_gossips = await conn.fetch(latest_gossips_query)
        
        # Fetch editor's choice blogs (blogs marked as editor's choice)
        editors_choice_query = """
            SELECT id, blog, date, category, created_at, editors_choice
            FROM blogs
            WHERE isdeleted = FALSE AND editors_choice = 'Y'
            ORDER BY created_at DESC
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
            # Try to get blog summary from multiple possible fields
            summary = blog_content.get('blogSummary', '')
            if not summary:
                # If blogSummary is not available, try to get first paragraph or content preview
                content = blog_content.get('blogContent', {})
                if isinstance(content, dict) and 'content' in content:
                    content_items = content['content']
                    for item in content_items:
                        if item.get('type') == 'paragraph' and item.get('data', {}).get('content'):
                            summary = item['data']['content'][:150] + '...' if len(item['data']['content']) > 150 else item['data']['content']
                            break
                elif isinstance(content, str):
                    summary = content[:150] + '...' if len(content) > 150 else content
            else:
                summary = summary[:150] + '...' if len(summary) > 150 else summary
            created_at = blog['created_at'].strftime('%B %d, %Y') if blog['created_at'] else ''
            category = blog['category'] or 'General'
            slug = blog.get('slug', f"{title}")
            
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
            summary = blog_content.get('blogSummary', '')[:150] + '...' if len(blog_content.get('blogSummary', '')) > 150 else blog_content.get('blogSummary', '')
            created_at = blog['created_at'].strftime('%B %d, %Y') if blog['created_at'] else ''
            category = blog['category'] or 'General'
            slug = blog.get('slug', f"{title}")
            
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
            <p class="blog-date">{blog['created_at']} • {blog['category']}</p>
            <p class="blog-description">{blog['summary']}</p>
            <div class="blog-footer">
                <a href="/blog/{blog['slug']}" class="blog-arrow-link">
                    <div class="blog-arrow">
                        <svg viewBox="0 24 24" fill="none">
                            <path d="M5 12h14m-7-7l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                </a>
            </div>
        </div>
    '''

def get_blog_color(index):
    """
    Get color based on index to match existing color pattern
    """
    colors = ['#22c55e', '#ef4444', '#06b6d4', '#22c55e', '#eab308', '#3b82f6', '#22c55e', '#ec4899', '#06b6d4', '#eab308', '#a855f7', '#22c55e']
    return colors[index % len(colors)]

async def get_blogs_html():
    """
    Generate the HTML content for the blogs_landing.html page with dynamic content
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
    
    return latest_gossips_html, editors_choice_html, editors_choice_data[:3]


async def get_home_insights_html(editors_choice_data):
    """
    Generate the HTML content for the home page with top 3 editor's choice blogs
    """
    # Generate HTML for top 3 editor's choice blogs in home page style
    home_insights_html = ""
    for i, blog in enumerate(editors_choice_data):
        home_insights_html += generate_home_insight_card_html(blog, i)
    return home_insights_html


def generate_home_insight_card_html(blog, index):
    """
    Generate HTML for a single insight card on the home page based on the existing structure
    """
    # Map index to color markers: 0=green, 1=pink, 2=orange
    colors = ['green', 'pink', 'orange']
    color_class = colors[index % len(colors)] if index < len(colors) else 'green'
    
    return f'''
                    <div class="insight-card">
                        <div class="card-top">
                            <span class="color-marker {color_class}"></span>
                            <span class="read-time">5 mins read</span>
                        </div>
                        <h3>{blog['title']}</h3>
                        <p>{blog['summary']}</p>
                        <div class="card-content-bottom">
                            <a href="/blog/{blog['slug']}">
                                <img src="/icons/black_arrow.svg" alt="Read more" class="card-arrow-icon">
                            </a>
                        </div>
                    </div>'''

if __name__ == "__main__":
    import asyncio
    
    async def main():
        latest_gossips_html, editors_choice_html, top_editors_choice_data = await get_blogs_html()
        home_insights_html = await get_home_insights_html(top_editors_choice_data)
        
        print("Generated latest gossips HTML:\n", latest_gossips_html)
        print("Generated editor's choice HTML:\n", editors_choice_html)
        print("Generated home insights HTML:\n", home_insights_html)

    asyncio.run(main())