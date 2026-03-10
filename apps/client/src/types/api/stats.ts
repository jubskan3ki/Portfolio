// Dashboard Statistics API Types - Aligned with backend response

// Module Stats (per module)
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

// Dashboard Stats (from /api/stats/ or /api/stats/overview/)
export interface DashboardModuleStats {
    articles: ArticleStats;
    projects: ProjectStats;
    stacks: StackStats;
    experiences: ExperienceStats;
    messages: MessageStats;
    totalViews: number;
}

// Chart Data Points
export interface ViewsDataPoint {
    date: string;
    views: number;
}

export interface MessagesDataPoint {
    month: string;
    count: number;
}

// Chart Data (from /api/stats/charts/)
export interface ChartData {
    viewsOverTime: ViewsDataPoint[];
    messagesPerMonth: MessagesDataPoint[];
}

// Activity Item (from /api/stats/activity/)
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

// Quick Stats (from /api/stats/quick/)
export interface QuickStats {
    newMessagesToday: number;
    totalViews: number;
    popularArticle: string | null;
    popularProject: string | null;
}

// Full Dashboard Overview (from /api/stats/overview/)
export interface DashboardOverview {
    stats: DashboardModuleStats;
    charts: ChartData;
    activity: ActivityItem[];
    quickStats: QuickStats;
}

// Legacy aliases for backwards compatibility
export type DashboardStats = DashboardModuleStats;
export type RecentActivity = ActivityItem[];
