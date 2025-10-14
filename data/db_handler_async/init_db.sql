-- Create tables for Suflex Media application based on provided schema

-- Create admin users table (with proper naming for PostgreSQL)
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    email TEXT,
    username TEXT,
    password TEXT
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

-- Create ads table
CREATE TABLE IF NOT EXISTS ads (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    organization TEXT,
    title TEXT,
    description TEXT,
    url TEXT,
    image TEXT,
    aspect_ratio TEXT
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

-- Create magazine_details table
CREATE TABLE IF NOT EXISTS magazine_details (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    pdf_url TEXT,
    thumbnail_url TEXT,
    title TEXT,
    created_by TEXT DEFAULT 'internal'
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_blogs_status ON blogs(status);
CREATE INDEX IF NOT EXISTS idx_blogs_category ON blogs(category);
CREATE INDEX IF NOT EXISTS idx_blogs_created_at ON blogs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_main_pages_name ON main_pages(page_name);
CREATE INDEX IF NOT EXISTS idx_magazine_created_at ON magazine_details(created_at DESC);