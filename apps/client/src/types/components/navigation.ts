// Types for Navigation components

// Tabs
type TabsVariant = 'default' | 'outline' | 'pills' | 'underlined' | 'segmented';

type TabsAlign = 'left' | 'center' | 'right';

interface TabBadge {
    text: string | number;
    type?: string;
    variant?: string;
}

interface TabItem {
    id: string;
    label: string;
    icon?: string;
    content?: string;
    disabled?: boolean;
    badge?: TabBadge;
}

export interface TabsProps {
    modelValue?: string | number;
    tabs?: TabItem[];
    variant?: TabsVariant;
    vertical?: boolean;
    align?: TabsAlign;
    scrollable?: boolean;
    fullWidth?: boolean;
    showIndicator?: boolean;
    animated?: boolean;
    customClass?: string;
}

// Breadcrumb
type BreadcrumbVariant = 'default' | 'pills' | 'minimal';

export type BreadcrumbSeparator = 'chevron' | 'slash' | 'dot' | 'arrow';

interface BreadcrumbItem {
    label: string;
    to: string;
    icon?: string;
}

export interface BreadcrumbProps {
    items: BreadcrumbItem[];
    variant?: BreadcrumbVariant;
    separator?: BreadcrumbSeparator;
    customClass?: string;
}

// Pagination
export type PaginationSize = 'sm' | 'md' | 'lg';

export type PaginationVariant = 'default' | 'rounded' | 'minimal';

export interface PaginationProps {
    currentPage: number;
    totalPages: number;
    maxVisiblePages?: number;
    showText?: boolean;
    showInfo?: boolean;
    size?: PaginationSize;
    variant?: PaginationVariant;
    ariaLabel?: string;
    customClass?: string;
}

// SideBar
type SidebarVariant = 'light' | 'dark' | 'glass';

interface SidebarBadge {
    type?: 'info' | 'success' | 'warning' | 'danger';
    value?: string | number;
}

interface SidebarNavItem {
    text: string;
    to: string;
    icon?: string;
    badge?: SidebarBadge;
}

interface SidebarNavSection {
    title?: string;
    items: SidebarNavItem[];
}

export interface SideBarProps {
    sections?: SidebarNavSection[];
    variant?: SidebarVariant;
    collapsible?: boolean;
    defaultCollapsed?: boolean;
    ariaLabel?: string;
    customClass?: string;
}

// NavBar
interface NavChildItem {
    label: string;
    path: string;
    icon?: string;
}

export interface NavItem {
    label: string;
    path: string;
    icon?: string;
    children?: NavChildItem[];
}

export interface NavbarItemProps {
    item: NavItem;
    index: number;
    isActive: boolean;
}

// MobileMenu
export interface MobileMenuProps {
    isOpen?: boolean;
    customClass?: string;
}
