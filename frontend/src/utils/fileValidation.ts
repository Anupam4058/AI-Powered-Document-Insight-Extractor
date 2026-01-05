/**
 * File validation utilities
 */

export const ALLOWED_FILE_TYPES = ['.pdf', '.docx'];
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export interface ValidationResult {
  valid: boolean;
  error?: string;
}

/**
 * Validate file type
 */
export function validateFileType(file: File): ValidationResult {
  const extension = '.' + file.name.split('.').pop()?.toLowerCase();
  
  if (!ALLOWED_FILE_TYPES.includes(extension)) {
    return {
      valid: false,
      error: `Unsupported file format. Please upload a PDF (.pdf) or DOCX (.docx) file.`,
    };
  }

  return { valid: true };
}

/**
 * Validate file size
 */
export function validateFileSize(file: File): ValidationResult {
  if (file.size === 0) {
    return {
      valid: false,
      error: 'Uploaded file is empty. Please upload a valid PDF or DOCX file.',
    };
  }

  if (file.size > MAX_FILE_SIZE) {
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    const maxSizeMB = (MAX_FILE_SIZE / (1024 * 1024)).toFixed(1);
    return {
      valid: false,
      error: `File size (${fileSizeMB}MB) exceeds maximum allowed size of ${maxSizeMB}MB. Please upload a smaller file.`,
    };
  }

  return { valid: true };
}

/**
 * Validate file (type and size)
 */
export function validateFile(file: File): ValidationResult {
  const typeValidation = validateFileType(file);
  if (!typeValidation.valid) {
    return typeValidation;
  }

  const sizeValidation = validateFileSize(file);
  if (!sizeValidation.valid) {
    return sizeValidation;
  }

  return { valid: true };
}

/**
 * Format file size for display
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

