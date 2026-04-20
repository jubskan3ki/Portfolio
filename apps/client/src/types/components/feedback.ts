// Types for Feedback components
import type { ButtonVariant } from './base';
import type { Alert } from '@/types/stores/alert';

export type { Alert, ButtonVariant };

// Common types
export type FeedbackType = 'info' | 'success' | 'warning' | 'error';

export type FeedbackPosition
    = | 'top-right'
        | 'top-left'
        | 'top-center'
        | 'bottom-right'
        | 'bottom-left'
        | 'bottom-center';

export interface AlertItemProps {
    alert: Alert;
}

// Toast
export interface ToastProps {
    type?: FeedbackType;
    title?: string;
    message?: string;
    autoClose?: boolean;
    duration?: number;
    dismissible?: boolean;
    showIcon?: boolean;
    progress?: boolean;
    customClass?: string;
}

// Modal
export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

export interface ModalOptions {
    title?: string;
    subtitle?: string;
    content?: string;
    component?: string;
    componentProps?: Record<string, unknown>;
    size?: ModalSize;
    closable?: boolean;
    closeOnClickOutside?: boolean;
    persistent?: boolean;
    hideCloseButton?: boolean;
    showFooter?: boolean;
}

export interface ModalProps {
    modelValue?: boolean;
    title?: string;
    subtitle?: string;
    size?: ModalSize;
    closable?: boolean;
    closeOnClickOutside?: boolean;
    persistent?: boolean;
    hideCloseButton?: boolean;
    showFooter?: boolean;
    customClass?: string;
}

// ConfirmDialog
export type ConfirmDialogVariant = 'info' | 'warning' | 'danger';

export interface ConfirmDialogProps {
    modelValue: boolean;
    title?: string;
    message: string;
    variant?: ConfirmDialogVariant;
    icon?: string;
    confirmText?: string;
    cancelText?: string;
    loading?: boolean;
    customClass?: string;
}

// QueryErrorBoundary
export interface QueryErrorBoundaryProps {
    isError: boolean;
    error?: Error | null;
    showRetry?: boolean;
    refetch?: () => void;
}

export type QueryErrorBoundaryErrorType
    = | 'not-found'
        | 'forbidden'
        | 'unauthorized'
        | 'server'
        | 'client'
        | 'network';

export interface QueryErrorBoundaryErrorConfig {
    icon: string;
    title: string;
    message: string;
}

// ErrorBoundary
export type ErrorBoundaryVariant = 'default' | 'compact' | 'inline';
export type ErrorBoundarySize = 'sm' | 'md' | 'lg';

export type ErrorBoundaryErrorType
    = | 'type'
        | 'reference'
        | 'syntax'
        | 'network'
        | 'timeout'
        | 'unknown';

export interface ErrorBoundaryProps {
    title?: string;
    fallbackMessage?: string;
    showHomeButton?: boolean;
    showDetails?: boolean;
    showRetry?: boolean;
    variant?: ErrorBoundaryVariant;
    size?: ErrorBoundarySize;
    onError?: (error: Error) => void;
}

// ErrorMessage
export interface ErrorMessageProps {
    message?: string;
    showIcon?: boolean;
    customClass?: string;
}

// QueryStateHandler
export interface QueryStateHandlerProps {
    loading?: boolean;
    error?: string | Error | null;
    empty?: boolean;
    loadingMessage?: string;
    loadingSize?: 'sm' | 'md' | 'lg';
    emptyTitle?: string;
    emptyDescription?: string;
    emptyIcon?: string;
    retryable?: boolean;
    retryText?: string;
}

// AlertList
export interface AlertListProps {
    position?: FeedbackPosition;
    maxAlerts?: number;
}

// EmptyState
export type EmptyStateSize = 'sm' | 'md' | 'lg';

export interface EmptyStateProps {
    icon?: string;
    iconSize?: number;
    title: string;
    description?: string;
    actionText?: string;
    actionIcon?: string;
    actionVariant?: ButtonVariant;
    size?: EmptyStateSize;
    centered?: boolean;
    customClass?: string;
}
