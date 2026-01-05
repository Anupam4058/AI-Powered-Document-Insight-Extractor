/**
 * API integration for backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const REQUEST_TIMEOUT = 300000; // 5 minutes for large file processing

export interface UploadResponse {
  success: boolean;
  filename: string;
  file_size: string;
  file_type: string;
  text_length: number;
  word_count: number;
  text: string;
  message: string;
}

export interface InsightsResponse {
  success: boolean;
  message: string;
  summary: string;
  document_type: {
    type: string;
    confidence: number;
  };
  creative_requirements: {
    dimensions: string[];
    formats: string[];
    file_sizes: string[];
    colors: string[];
    fonts: string[];
    tone: string[];
  };
  technical_specs: {
    dimensions: string[];
    formats: string[];
    file_sizes: string[];
    [key: string]: any;
  };
  brand_guidelines: {
    colors: string[];
    fonts: string[];
    tone: string[];
    [key: string]: any;
  };
  kpis: {
    [key: string]: any;
  };
  deadlines: Array<{
    date: string;
    type?: string;
    context?: string;
    description?: string;
  }>;
  action_items: Array<string | {
    task: string;
    priority?: string;
  }>;
  warnings: Array<{
    message?: string;
    text?: string;
    type?: string;
    severity?: string;
    keyword?: string;
  }>;
  file_metadata: {
    filename: string;
    file_size: string;
    file_type: string;
    text_length: number;
    word_count: number;
  };
  metadata: {
    [key: string]: any;
  };
}

export interface ApiErrorResponse {
  detail: string;
}

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
  statusCode?: number;
  isNetworkError: boolean;

  constructor(
    message: string,
    statusCode?: number,
    isNetworkError: boolean = false
  ) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
    this.isNetworkError = isNetworkError;
  }
}

/**
 * Fetch with timeout
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeout: number = REQUEST_TIMEOUT
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError('Request timeout. The file may be too large or the server is taking too long to respond.', 408, false);
    }
    throw error;
  }
}

/**
 * Handle API errors with user-friendly messages
 */
async function handleApiError(response: Response): Promise<never> {
  let errorMessage = 'An error occurred';
  let isNetworkError = false;

  // Check if it's a network error
  if (!response) {
    errorMessage = 'Unable to connect to the server. Please check if the backend is running on ' + API_BASE_URL;
    isNetworkError = true;
    throw new ApiError(errorMessage, 0, true);
  }

  // Try to parse error response
  try {
    const error: ApiErrorResponse = await response.json();
    errorMessage = error.detail || `Server error (${response.status})`;
  } catch {
    // If JSON parsing fails, use status text
    if (response.status === 0 || response.status >= 500) {
      errorMessage = 'Server error. Please try again later.';
      isNetworkError = response.status === 0;
    } else if (response.status === 404) {
      errorMessage = 'API endpoint not found. Please check the backend configuration.';
    } else if (response.status === 413) {
      errorMessage = 'File is too large. Maximum file size is 10MB.';
    } else {
      errorMessage = `Error: ${response.statusText || 'Unknown error'}`;
    }
  }

  throw new ApiError(errorMessage, response.status, isNetworkError);
}

/**
 * Upload a file to the backend for analysis
 */
export async function uploadFile(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      await handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network errors (connection refused, etc.)
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError(
        `Cannot connect to the backend server at ${API_BASE_URL}. Please ensure the backend is running.`,
        0,
        true
      );
    }
    throw new ApiError(
      error instanceof Error ? error.message : 'Failed to upload file',
      0,
      true
    );
  }
}

/**
 * Extract insights from a document
 */
export async function extractInsights(file: File): Promise<InsightsResponse> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/api/extract-insights`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      await handleApiError(response);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network errors (connection refused, etc.)
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError(
        `Cannot connect to the backend server at ${API_BASE_URL}. Please ensure the backend is running.`,
        0,
        true
      );
    }
    throw new ApiError(
      error instanceof Error ? error.message : 'Failed to extract insights',
      0,
      true
    );
  }
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<{ status: string }> {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/api/health`, {
      method: 'GET',
    }, 5000); // Shorter timeout for health check
    
    if (!response.ok) {
      throw new ApiError('API is not available', response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(
      `Cannot connect to the backend server at ${API_BASE_URL}. Please ensure the backend is running.`,
      0,
      true
    );
  }
}

