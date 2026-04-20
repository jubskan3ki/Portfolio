// Types for the Colophon page

export interface StackItem {
    name: string;
    detail?: string;
}

export interface StackGroup {
    label: string;
    icon: string;
    items: StackItem[];
}
