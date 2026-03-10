// Types for Admin pages

// History
export interface HistoryActivity {
    id: number;
    type: string;
    action: string;
    title: string;
    timestamp: string;
    link?: string;
}

export interface HistoryActivityResponse {
    activities: HistoryActivity[];
}
