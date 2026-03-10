// Types for Layout components

// Section
export type SectionSize = 'tight' | 'default' | 'large';
export type SectionVariant = 'default' | 'dark' | 'light' | 'primary' | 'gradient' | 'glass';
export type SectionAnimation = 'fade' | 'slide' | 'scale' | 'none';

// Header
export interface SocialLink {
    name: string;
    icon: string;
    url: string;
}

// Footer Contact
export interface FooterContactProps {
    title?: string;
    email?: string;
    phone?: string;
    address?: string;
}

// Footer Contact Item
export type ContactItemLinkType = 'email' | 'phone' | 'url' | 'none';

export interface FooterContactItemProps {
    icon: string;
    text: string;
    isLink?: boolean;
    linkType?: ContactItemLinkType;
}

// Footer Social
export interface FooterSocialProps {
    title?: string;
    links: SocialLink[];
}

// Admin Layouts
export interface AdminMenuItem {
    label: string;
    path: string;
    icon: string;
    badge?: number | string;
    children?: AdminMenuItem[];
}

export interface AdminHeaderProps {
    collapsed: boolean;
}

export interface AdminSidebarProps {
    collapsed: boolean;
    mobileOpen?: boolean;
    menuItems?: AdminMenuItem[];
}

export interface AdminBreadcrumb {
    label: string;
    path: string;
    icon?: string;
}

export interface AdminBreadcrumbProps {
    items?: AdminBreadcrumb[];
    separator?: string;
}
