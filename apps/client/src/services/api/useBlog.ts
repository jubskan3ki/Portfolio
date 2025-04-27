import type { Ref } from 'vue';
import { ref } from 'vue';

import { API_ENDPOINTS } from '@/config/api';
import api from '@/services/utils/httpClient';

// Types
export interface BlogPost {
	id: number;
	title: string;
	content: string;
	status: 'draft' | 'published';
	tags: string[];
	meta_description: string;
	seo_keywords: string[];
	image?: string;
	created_at: string;
	updated_at: string;
	slug: string;
	views_count?: number;
}

export interface BlogPostInput {
	title: string;
	content: string;
	status: 'draft' | 'published';
	tags: string[];
	meta_description: string;
	seo_keywords: string[];
	image?: File;
}

export function useBlog() {
	const blogPosts: Ref<BlogPost[]> = ref([]);
	const currentPost: Ref<BlogPost | null> = ref(null);
	const isLoading = ref(false);
	const error = ref<string | null>(null);

	// Fetch all blog posts
	const fetchBlogPosts = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			blogPosts.value = await api.get<BlogPost[]>(API_ENDPOINTS.BLOG.BASE);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch blog posts';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch recent blog posts
	const fetchRecentBlogPosts = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			blogPosts.value = await api.get<BlogPost[]>(API_ENDPOINTS.BLOG.RECENT);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch recent blog posts';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch popular blog posts
	const fetchPopularBlogPosts = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			blogPosts.value = await api.get<BlogPost[]>(API_ENDPOINTS.BLOG.POPULAR);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch popular blog posts';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch draft blog posts
	const fetchDraftBlogPosts = async () => {
		isLoading.value = true;
		error.value = null;
		try {
			blogPosts.value = await api.get<BlogPost[]>(API_ENDPOINTS.BLOG.DRAFTS);
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch draft blog posts';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Fetch a single blog post by ID
	const fetchBlogPost = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;
		try {
			currentPost.value = await api.get<BlogPost>(API_ENDPOINTS.BLOG.DETAIL(id));
		} catch (err: any) {
			error.value = err.message || 'Failed to fetch blog post';
			console.error(error.value);
		} finally {
			isLoading.value = false;
		}
	};

	// Create a new blog post
	const createBlogPost = async (blogPost: BlogPostInput) => {
		isLoading.value = true;
		error.value = null;

		try {
			const formData = new FormData();
			formData.append('title', blogPost.title);
			formData.append('content', blogPost.content);
			formData.append('status', blogPost.status);
			formData.append('tags', JSON.stringify(blogPost.tags));
			formData.append('meta_description', blogPost.meta_description);
			formData.append('seo_keywords', JSON.stringify(blogPost.seo_keywords));

			if (blogPost.image) {
				formData.append('image', blogPost.image);
			}

			const newPost = await api.uploadForm<BlogPost>(API_ENDPOINTS.BLOG.BASE, formData);
			blogPosts.value.push(newPost);
			currentPost.value = newPost;

			return newPost;
		} catch (err: any) {
			error.value = err.message || 'Failed to create blog post';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Update a blog post
	const updateBlogPost = async (id: string | number, blogPost: Partial<BlogPostInput>) => {
		isLoading.value = true;
		error.value = null;

		try {
			const formData = new FormData();

			if (blogPost.title) formData.append('title', blogPost.title);
			if (blogPost.content) formData.append('content', blogPost.content);
			if (blogPost.status) formData.append('status', blogPost.status);
			if (blogPost.tags) formData.append('tags', JSON.stringify(blogPost.tags));
			if (blogPost.meta_description) formData.append('meta_description', blogPost.meta_description);
			if (blogPost.seo_keywords) formData.append('seo_keywords', JSON.stringify(blogPost.seo_keywords));
			if (blogPost.image) formData.append('image', blogPost.image);

			const updatedPost = await api.uploadForm<BlogPost>(API_ENDPOINTS.BLOG.DETAIL(id), formData, 'PATCH');

			if (currentPost.value && currentPost.value.id === updatedPost.id) {
				currentPost.value = updatedPost;
			}

			// Update the post in the posts array
			const index = blogPosts.value.findIndex((post) => post.id === updatedPost.id);
			if (index !== -1) {
				blogPosts.value[index] = updatedPost;
			}

			return updatedPost;
		} catch (err: any) {
			error.value = err.message || 'Failed to update blog post';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	// Delete a blog post
	const deleteBlogPost = async (id: string | number) => {
		isLoading.value = true;
		error.value = null;

		try {
			await api.delete(API_ENDPOINTS.BLOG.DETAIL(id));

			// Remove the post from the posts array
			blogPosts.value = blogPosts.value.filter((post) => post.id !== id);

			if (currentPost.value && currentPost.value.id === id) {
				currentPost.value = null;
			}

			return true;
		} catch (err: any) {
			error.value = err.message || 'Failed to delete blog post';
			console.error(error.value);
			throw error.value;
		} finally {
			isLoading.value = false;
		}
	};

	return {
		blogPosts,
		currentPost,
		isLoading,
		error,
		fetchBlogPosts,
		fetchRecentBlogPosts,
		fetchPopularBlogPosts,
		fetchDraftBlogPosts,
		fetchBlogPost,
		createBlogPost,
		updateBlogPost,
		deleteBlogPost,
	};
}
