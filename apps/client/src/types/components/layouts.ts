export type SectionSize = 'tight' | 'default' | 'large';
export type SectionVariant = 'default' | 'dark' | 'light' | 'primary' | 'gradient' | 'glass';
export type SectionAnimation = 'fade' | 'slide' | 'scale' | 'none';

export interface SocialLink {
    name: string;
    icon: string;
    url: string;
}

export interface FooterContactProps {
    title?: string;
    email?: string;
    phone?: string;
    address?: string;
    isAvailable?: boolean;
    availabilityLabel?: string;
}

export type ContactItemLinkType = 'email' | 'phone' | 'url' | 'none';

export interface FooterContactItemProps {
    icon: string;
    text: string;
    isLink?: boolean;
    linkType?: ContactItemLinkType;
}

export interface FooterSocialProps {
    title?: string;
    links: SocialLink[];
}

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

export interface MainLayoutProps {
    id?: string;
    title?: string;
    subtitle?: string;
    size?: SectionSize;
    variant?: SectionVariant;
    withContainer?: boolean;
    withGlassBackground?: boolean;
    glassVariant?: 'primary' | 'secondary' | 'light' | 'dark';
    showDots?: boolean;
    glassAnimated?: boolean;
    bubbleCount?: number;
    customClass?: string;
}

export interface DetailPageLayoutProps {
    sidebarWidth?: string;
}

export interface SectionProps {
    id?: string;
    title?: string;
    subtitle?: string;
    size?: SectionSize;
    variant?: SectionVariant;
    withContainer?: boolean;
    animated?: boolean;
    animationType?: SectionAnimation;
    customClass?: string;
}
