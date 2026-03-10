// Authentication API Types

// Login
export interface LoginCredentials {
    email: string;
    password: string;
    rememberMe?: boolean;
}

// User Profile - complete type matching backend response
export interface UserProfile {
    id: number;
    email: string;
    firstName: string;
    lastName: string;
    phoneNumber?: string;
    isActive: boolean;
    bio?: string;
    avatar?: string;
    position?: string;
    publicEmail?: string;
    linkedin?: string;
    github?: string;
    twitter?: string;
    dateJoined?: string;
    updatedAt?: string;
}

export interface LoginResponse {
    user: UserProfile;
}

export interface UpdateProfileData {
    firstName?: string;
    lastName?: string;
    email?: string;
    phoneNumber?: string;
    bio?: string;
    avatar?: string;
    position?: string;
    publicEmail?: string;
    linkedin?: string;
    github?: string;
    twitter?: string;
}

// Password
export interface ChangePasswordData {
    currentPassword: string;
    newPassword: string;
    confirmPassword: string;
}

export interface RequestResetPasswordData {
    email: string;
}

export interface VerifyResetCodeData {
    email: string;
    code: string;
}

export interface ConfirmResetPasswordData {
    email: string;
    code: string;
    newPassword: string;
}

// Responses
export interface AuthMessageResponse {
    detail: string;
}

export interface VerifyCodeResponse {
    valid: boolean;
}
