export interface ArticleStats {
    count: number;
    published: number;
    featured: number;
    totalViews: number;
}

export interface ProjectStats {
    count: number;
    totalViews: number;
}

export interface StackStats {
    count: number;
}

export interface ExperienceStats {
    count: number;
}

export interface MessageStats {
    count: number;
    new: number;
    responded: number;
}

export interface DashboardModuleStats {
    articles: ArticleStats;
    projects: ProjectStats;
    stacks: StackStats;
    experiences: ExperienceStats;
    messages: MessageStats;
    totalViews: number;
}

export interface ViewsDataPoint {
    date: string;
    views: number;
}

export interface MessagesDataPoint {
    month: string;
    count: number;
}

export interface ChartData {
    viewsOverTime: ViewsDataPoint[];
    messagesPerMonth: MessagesDataPoint[];
}

export interface ActivityItem {
    id: number;
    type: ActivityType;
    action: ActivityAction;
    title: string;
    timestamp: string;
    module: string;
}

export type ActivityType = 'project' | 'article' | 'stack' | 'message' | 'experience' | 'user';
type ActivityAction = 'created' | 'updated' | 'received';

export interface QuickStats {
    newMessagesToday: number;
    totalViews: number;
    popularArticle: string | null;
    popularProject: string | null;
}

export interface DashboardOverview {
    stats: DashboardModuleStats;
    charts: ChartData;
    activity: ActivityItem[];
    quickStats: QuickStats;
}

// Legacy aliases (backward compat)
export type DashboardStats = DashboardModuleStats;
export type RecentActivity = ActivityItem[];
