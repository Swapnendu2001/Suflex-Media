import asyncpg
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_URL")

def calculate_read_time(blog_content_json):
    """
    Calculate the estimated read time for a blog post.
    """
    text = ""
    
    # The content can be a stringified JSON or a dict
    if isinstance(blog_content_json, str):
        try:
            blog_content = json.loads(blog_content_json)
        except json.JSONDecodeError:
            blog_content = {}
    else:
        blog_content = blog_content_json

    # Extract text from title and summary
    text += blog_content.get('blogTitle', '') + " "
    text += blog_content.get('blogSummary', '') + " "
    
    # Extract text from the main content blocks
    content_data = blog_content.get('blogcontent', {})
    if isinstance(content_data, dict) and 'content' in content_data:
        content_items = content_data['content']
        for item in content_items:
            if item.get('type') == 'paragraph' and item.get('data', {}).get('content'):
                text += item['data']['content'] + " "
    
    word_count = len(text.split())
    read_time_minutes = round(word_count / 200)  # Assuming 200 WPM reading speed
    return max(1, read_time_minutes) # Ensure minimum 1 minute read time


async def get_blog_data():
    """
    Fetch blog data from the database for the three sections:
    1. Editor's Choice (carousel)
    2. Latest Gossip (3 most recent blogs)
    3. Read More (all other blogs with pagination)
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)

        # Fetch all published blogs of type 'BLOG'
        all_blogs_query = """
            SELECT id, blogContent, date, created_at, editors_choice, slug, type
            FROM blogs
            WHERE isdeleted = FALSE
            ORDER BY created_at DESC
        """
        all_blogs = await conn.fetch(all_blogs_query)

        await conn.close()

        processed_blogs = []
        for blog in all_blogs:
            blog_content = blog['blogcontent']
            if isinstance(blog_content, str):
                blog_content = json.loads(blog_content)

            title = blog_content.get('blogTitle', 'Untitled Blog')
            summary = blog_content.get('blogSummary', '')
            if not summary:
                content = blog_content.get('blogcontent', {})
                if isinstance(content, dict) and 'content' in content:
                    content_items = content['content']
                    for item in content_items:
                        if item.get('type') == 'paragraph' and item.get('data', {}).get('content'):
                            summary = item['data']['content']
                            break
                elif isinstance(content, str):
                    summary = content
            
            summary = summary[:150] + '...' if len(summary) > 150 else summary
            
            read_time = calculate_read_time(blog['blogcontent'])
            
            processed_blogs.append({
                'id': blog['id'],
                'title': title,
                'summary': summary,
                'created_at': blog['created_at'].strftime('%B %d, %Y') if blog['created_at'] else '',
                'slug': blog['slug'],
                'category': blog_content.get('blogCategory', 'General'),
                'editors_choice': blog['editors_choice'] == 'Y' or blog['editors_choice'] == "ON",
                'cover_image': extract_blog_image(blog_content),
                'read_time': read_time
            })
        print(f"Processed Blogs: {processed_blogs}") # Debug print
        # Separate blogs into the three sections
        editors_choice_data = [b for b in processed_blogs if b['editors_choice']]
        
        # All other blogs that are not editor's choice
        other_blogs = [b for b in processed_blogs if not b['editors_choice']]
        
        latest_gossip_data = other_blogs[:3]
        read_more_data = other_blogs[3:]

        top_blog = processed_blogs[0] if processed_blogs else None

        return editors_choice_data, latest_gossip_data, read_more_data, top_blog

    except Exception as e:
        print(f"Error fetching blogs: {e}")
        return [], [], [], None


def extract_blog_image(blog_content):
    """
    Extract the cover image URL from the blog content.
    The image is expected to be the first block of type 'image'.
    """
    if 'mainImageUrl' in blog_content and blog_content['mainImageUrl']:
        return blog_content['mainImageUrl']
    
    if 'blog_cover_image' in blog_content and blog_content['blog_cover_image']:
        return blog_content['blog_cover_image'].get('url')
        
    if 'blogcontent' in blog_content and 'blocks' in blog_content['blogcontent']:
        for block in blog_content['blogcontent']['blocks']:
            if block['type'] == 'image':
                return block['data']['file']['url']
    return None


def generate_unified_blog_card_html(blog):
    """
    Generate HTML for a unified blog card design with image, date, title, summary, and read more link.
    """
    image_html = ''
    if blog.get('cover_image'):
        image_html = f'''
            <div class="blog-card-image-container">
                <img src="{blog['cover_image']}" alt="{blog['title']}" class="blog-card-image">
            </div>
        '''
    
    return f'''
        <div class="blog-card-unified" onclick="window.location.href='/blog/{blog['slug']}'">
            {image_html}
            <div class="blog-card-body">
                <span class="blog-card-date">{blog['created_at']}</span>
                <h3 class="blog-card-title">{blog['title']}</h3>
                <p class="blog-card-summary">{blog['summary']}</p>
                <a href="/blog/{blog['slug']}" class="blog-card-read-more">Read More →</a>
            </div>
        </div>
    '''


def generate_editors_choice_vertical_card_html(blog):
    """
    Generate HTML for a single Editor's Choice blog card for the vertical list.
    """
    return f'''
        <div class="editor-pick-card" onclick="window.location.href='/blog/{blog['slug']}'">
            <div class="editor-pick-image-container">
                <img src="{blog.get('cover_image', '')}" alt="{blog.get('title', '')}" class="editor-pick-image">
            </div>
            <div class="editor-pick-content">
                <span class="editor-pick-category">{blog.get('category', 'General')}</span>
                <h4 class="editor-pick-title">{blog.get('title', '')}</h4>
                <p class="editor-pick-summary">{blog.get('summary', '')}</p>
                <a href="/blog/{blog['slug']}" class="editor-pick-read-more">Read More →</a>
            </div>
        </div>
    '''


def generate_editors_choice_mobile_html(editors_choice_data):
    """
    Generate HTML for the mobile-only Editor's Choice section.
    """
    mobile_html = ""
    for i, blog in enumerate(editors_choice_data):
        mobile_html += generate_unified_blog_card_html(blog)
    return mobile_html


def generate_blog_card_html(blog, color_index):
    """
    Generate HTML for a single blog card based on the unified structure.
    """
    return generate_unified_blog_card_html(blog)


def get_blog_color(index):
    """
    Get color based on index to match existing color pattern
    """
    colors = ['#22c55e', '#ef4444', '#06b6d4', '#22c55e', '#eab308', '#3b82f6', '#22c55e', '#ec4899', '#06b6d4', '#eab308', '#a855f7', '#22c55e']
    return colors[index % len(colors)]


async def get_blogs_html():
    """
    Generate the HTML content for the blogs_landing.html page with dynamic content
    for all three sections.
    """
    editors_choice_data, latest_gossip_data, read_more_data, top_blog = await get_blog_data()

    # Generate HTML for Editor's Choice carousel
    editors_choice_html = ""
    for blog in editors_choice_data[:3]:
        editors_choice_html += generate_editors_choice_vertical_card_html(blog)

    # NEW: Generate HTML for mobile Editor's Choice
    editors_choice_mobile_html = generate_editors_choice_mobile_html(editors_choice_data)

    # Generate HTML for Latest Gossip
    latest_gossips_html = ""
    for i, blog in enumerate(latest_gossip_data):
        latest_gossips_html += generate_blog_card_html(blog, i)

    # Generate HTML for Read More
    read_more_html = ""
    for i, blog in enumerate(read_more_data):
        # Start color index from 3 to avoid repeating colors from latest gossips
        read_more_html += generate_blog_card_html(blog, i + 3)

    return editors_choice_html, latest_gossips_html, read_more_html, editors_choice_data, top_blog, editors_choice_mobile_html


async def get_home_insights_html(editors_choice_data):
    """
    Generate the HTML content for the home page with top 3 editor's choice blogs
    """
    # Generate HTML for top 3 editor's choice blogs in home page style
    home_insights_html = ""
    for i, blog in enumerate(editors_choice_data):
        home_insights_html += generate_home_insight_card_html(blog, i)
        if i == 2:
            break  # Only take top 3
    return home_insights_html


def generate_home_insight_card_html(blog, index):
    """
    Generate HTML for a single insight card on the home page based on the new structure
    """
    return f'''
        <div class="insight-card" onclick="window.location.href='/blog/{blog['slug']}'">
            <img src="{blog['cover_image']}" alt="{blog['title']}" class="insight-card-image">
            <div class="insight-card-content">
                <span class="publication-date">{blog['created_at']}</span>
                <h3 class="insight-card-title">{blog['title']}</h3>
                <p class="insight-card-summary">{blog['summary']}</p>
                <a href="/blog/{blog['slug']}" class="read-more-link">Read More →</a>
            </div>
        </div>
    '''

if __name__ == "__main__":
    import asyncio
    
    async def main():
        editors_choice_html, latest_gossips_html, read_more_html, top_editors_choice_data, top_blog, editors_choice_mobile_html = await get_blogs_html()
        home_insights_html = await get_home_insights_html(top_editors_choice_data)
        
        print("Generated Editor's Choice HTML:\n", editors_choice_html)
        print("Generated Editor's Choice Mobile HTML:\n", editors_choice_mobile_html)
        print("Generated Latest Gossips HTML:\n", latest_gossips_html)
        print("Generated Read More HTML:\n", read_more_html)
        print("Generated home insights HTML:\n", home_insights_html)

    asyncio.run(main())