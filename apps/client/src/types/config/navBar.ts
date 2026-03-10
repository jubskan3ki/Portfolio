// Type pour un element enfant de navigation (lien de sous-menu)
export interface NavChildItem {
    label: string;
    path: string;
    icon?: string;
}

// Type pour un element principal de navigation (peut contenir des enfants)
export interface NavItem {
    label: string;
    path: string;
    icon?: string;
    children?: NavChildItem[];
}

// Type pour la liste des elements de navigation
export type NavigationItems = NavItem[];

// Type pour la verification d'une route active
export type ActiveRouteChecker = (path: string, currentPath: string) => boolean;
