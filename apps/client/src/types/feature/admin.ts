export interface ArticleBase {
    id: number;
    title: string;
    slug: string;
    excerpt?: string;
    image?: string;
}

export interface CategoryBase {
    id: number;
    name: string;
    slug: string;
    count?: number;
}

export interface TagBase {
    id: number;
    name: string;
    count?: number;
}

interface ProjectBase {
    id: number;
    title: string;
    slug: string;
    description?: string;
    image?: string;
}

interface StackBase {
    id: number;
    name: string;
    slug: string;
    logo?: string;
    icon?: string;
    color?: string;
}

interface ExperienceBase {
    id: number;
    title: string;
    type: 'professional' | 'education';
}

export interface AdminArticle extends ArticleBase {
    content: string;
    coverImage?: string;
    category?: AdminCategory | null;
    tags?: AdminTag[];
    status: 'draft' | 'published' | 'archived';
    isPublished?: boolean;
    viewsCount: number;
    createdAt: string;
    updatedAt?: string;
    publishedDate?: string;
}

export interface AdminCategory extends CategoryBase {
    description?: string;
}

export interface AdminTag extends TagBase {
    slug?: string;
}

export interface AdminProject extends ProjectBase {
    content?: string;
    longDescription?: string;
    thumbnail?: string;
    category?: AdminCategory | null;
    status: 'planned' | 'in_progress' | 'completed' | 'archived';
    technologies?: AdminStack[];
    links?: {
        demo?: string;
        github?: string;
        documentation?: string;
    };
    isFeatured?: boolean;
    order?: number;
    createdAt: string;
    updatedAt?: string;
}

export interface AdminStack extends StackBase {
    level?: number;
    proficiency?: number;
    order?: number;
    category?: AdminCategory | null;
    description?: string;
    createdAt?: string;
}

export interface AdminExperience extends ExperienceBase {
    company?: string;
    institution?: string;
    location?: string;
    startDate: string;
    endDate?: string;
    isCurrent?: boolean;
    description?: string;
    technologies?: AdminStack[];
    achievements?: string[];
    logo?: string;
    createdAt?: string;
}

export interface AdminMessage {
    id: number;
    name: string;
    email: string;
    subject?: string;
    message: string;
    status: 'unread' | 'read' | 'replied' | 'archived';
    isRead?: boolean;
    createdAt: string;
    readAt?: string;
    repliedAt?: string;
}

// Re-export for backward compatibility
export type { DjangoPaginatedResponse as PaginatedResponse } from '@/types/api/common';

export type AdminEntity = AdminArticle | AdminProject | AdminStack | AdminExperience | AdminMessage;

export type DataItem = AdminEntity | Record<string, unknown>;

export interface SessionDevice {
    browser?: string;
    os?: string;
    isMobile?: boolean;
    ipAddress?: string;
}

export interface Session {
    id: string;
    device?: SessionDevice;
    createdAt?: string;
    lastActivity?: string;
    isCurrent?: boolean;
}
