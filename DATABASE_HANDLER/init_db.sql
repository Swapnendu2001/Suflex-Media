-- Create tables for Suflex Media application based on provided schema

-- Create admin users table (with proper naming for PostgreSQL)
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    email TEXT,
    username TEXT,
    password TEXT
);

-- Insert default admin user only if it doesn't exist
INSERT INTO admin_users (email, username, password)
SELECT '7932b2e116b076a54f452848eaabd5857f61bd957fe8a218faf216f24c9885bb', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
WHERE NOT EXISTS (
    SELECT 1 FROM admin_users WHERE username = 'admin'
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    email TEXT,
    username TEXT,
    password TEXT
);

-- Create main_pages table
CREATE TABLE IF NOT EXISTS main_pages (
    page_id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    page_name TEXT,
    page_data JSONB,
    status TEXT DEFAULT 'DRAFT',
    href TEXT
);

-- Create leadership_table
CREATE TABLE IF NOT EXISTS leadership_table (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    leader_image_url TEXT,
    leader_name TEXT,
    leader_designation TEXT,
    leader_desc TEXT,
    web_stories_url TEXT DEFAULT '#'
);

-- Create organization table
CREATE TABLE IF NOT EXISTS organization (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    organization TEXT,
    logo TEXT,
    percentage DOUBLE PRECISION
);

-- Create blogs table
CREATE TABLE IF NOT EXISTS blogs (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by TEXT,
    updated_by TEXT,
    json_data JSONB,
    history JSONB,
    status TEXT,
    category TEXT,
    sub_category TEXT,
    meta_tags TEXT,
    redirect_url TEXT,
    labels JSONB
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_blogs_status ON blogs(status);
CREATE INDEX IF NOT EXISTS idx_blogs_category ON blogs(category);
CREATE INDEX IF NOT EXISTS idx_blogs_created_at ON blogs(created_at DESC);
