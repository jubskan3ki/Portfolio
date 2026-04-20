export interface Experience {
    id: number;
    title: string;
    company: string;
    location: string;
    period: string;
    startDate: string;
    endDate?: string;
    isCurrent: boolean;
    description: string;
    logo?: string;
    technologies: string[];
    skills: string[];
    achievements: string[];
    type: string;
}

export interface ExperienceType {
    id: number;
    name: string;
    icon: string;
}

export interface ExperienceStats {
    totalYears: number;
    companiesCount: number;
    topSkills: Array<{ skill: string; count: number }>;
    experienceByType: Array<{ type: string; count: number }>;
}

export interface ExperienceTimeline {
    year: number;
    experiences: Experience[];
}

export interface ExperienceCreateData {
    title: string;
    company: string;
    location?: string;
    startDate: string;
    endDate?: string;
    isCurrent?: boolean;
    description?: string;
    logo?: string;
    technologies?: string[];
    skills?: string[];
    achievements?: string[];
    type: string | number;
}

export type ExperienceUpdateData = Partial<ExperienceCreateData>;

export interface ExperienceTypeCreateData {
    name: string;
    icon?: string;
}

export type ExperienceTypeUpdateData = Partial<ExperienceTypeCreateData>;

export interface ExperienceFilterOption {
    label: string;
    value: string;
}

export interface ExperienceCardProps {
    title: string;
    company: string;
    logo?: string;
    location?: string;
    startDate: string;
    endDate?: string;
    period?: string;
    description?: string;
    skills?: string | string[];
    achievements?: string | string[];
    dateFormat?: string;
    currentText?: string;
}

export interface ExperienceTimelineProps {
    experiences?: Experience[];
    limit?: number;
    title?: string;
    subtitle?: string;
    showHeader?: boolean;
    showFilters?: boolean;
    filters?: ExperienceFilterOption[];
    filterLabel?: string;
    allFilterLabel?: string;
    defaultFilter?: string;
    dateFormat?: string;
    currentText?: string;
    emptyTitle?: string;
    emptyDescription?: string;
    loading?: boolean;
    loadingText?: string;
    customClass?: string;
}
