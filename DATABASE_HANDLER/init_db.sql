CREATE TABLE IF NOT EXISTS ADMIN_USERS (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS blogs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE,
    blog JSONB NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    keyword JSONB,
    category VARCHAR(100),
    redirect_url TEXT,
    isDeleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_blogs_status ON blogs(status) WHERE isDeleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_blogs_date ON blogs(date DESC) WHERE isDeleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_blogs_category ON blogs(category) WHERE isDeleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_blogs_slug ON blogs(slug) WHERE isDeleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_blogs_isDeleted ON blogs(isDeleted);
CREATE INDEX IF NOT EXISTS idx_blogs_keyword ON blogs USING GIN(keyword);
CREATE INDEX IF NOT EXISTS idx_blogs_blog ON blogs USING GIN(blog);
