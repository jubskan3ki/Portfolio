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

type BreadcrumbVariant = 'default' | 'pills' | 'minimal' | 'hero';

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

export interface MobileMenuProps {
    isOpen?: boolean;
    customClass?: string;
}

export interface MobileMenuToggleProps {
    isActive?: boolean;
}

export interface MobileMenuItemProps {
    item: NavItem;
    index: number;
}

export type SideBarItemBadgeType = 'info' | 'success' | 'warning' | 'danger';

export interface SideBarItemBadge {
    type?: SideBarItemBadgeType;
    value?: string | number;
}

export interface SideBarItemProps {
    text: string;
    to: string;
    icon?: string;
    badge?: SideBarItemBadge;
    isCollapsed?: boolean;
}

export type NavigationTabsVariant = 'default' | 'glass' | 'minimal';

export interface NavigationTab {
    key: string;
    label: string;
    icon?: string;
}

export interface NavigationTabsProps {
    tabs: NavigationTab[];
    modelValue: string;
    variant?: NavigationTabsVariant;
    iconSize?: number;
    customClass?: string;
}

export interface PaginationItemProps {
    page: number;
    isActive?: boolean;
    isEllipsis?: boolean;
}

export interface NavBarProps {
    sticky?: boolean;
    transparent?: boolean;
    elevated?: boolean;
    ariaLabel?: string;
    customClass?: string;
}

export interface TabItemBadge {
    text: string | number;
    type?: string;
    variant?: string;
}

export interface TabsItemProps {
    id: string;
    tabsId: string;
    isActive?: boolean;
    isTab?: boolean;
    label?: string;
    icon?: string;
    disabled?: boolean;
    badge?: TabItemBadge | null;
}
