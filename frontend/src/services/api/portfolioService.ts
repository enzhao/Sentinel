// frontend/src/services/api/portfolioService.ts
// This service handles all API interactions related to portfolios.

import { apiService } from '@/services/apiService';
import type { Portfolio, PortfolioCreationRequest, PortfolioSummary, PortfolioUpdateRequest } from '@/api/models';

/**
 * Fetches a summary list of all portfolios for the current user.
 * Reference: product_spec.md#3.3.2.2 (P_2200)
 */
export const listPortfolios = (): Promise<PortfolioSummary[]> => {
  return apiService.get<PortfolioSummary[]>('/users/me/portfolios');
};

/**
 * Fetches the full details of a single portfolio.
 * Reference: product_spec.md#3.3.2.1 (P_2000)
 */
export const getPortfolioById = (portfolioId: string): Promise<Portfolio> => {
  return apiService.get<Portfolio>(`/users/me/portfolios/${portfolioId}`);
};

/**
 * Creates a new portfolio.
 * Reference: product_spec.md#3.3.1 (P_1000)
 */
export const createPortfolio = (portfolioData: PortfolioCreationRequest): Promise<Portfolio> => {
  return apiService.post<Portfolio>('/users/me/portfolios', portfolioData);
};

/**
 * Updates an existing portfolio.
 * Reference: product_spec.md#3.3.3.1 (P_3000)
 */
export const updatePortfolio = (portfolioId: string, portfolioData: PortfolioUpdateRequest): Promise<Portfolio> => {
  return apiService.put<Portfolio>(`/users/me/portfolios/${portfolioId}`, portfolioData);
};

/**
 * Deletes a portfolio.
 * Reference: product_spec.md#3.3.4.1 (P_4000)
 */
export const deletePortfolio = (portfolioId: string): Promise<void> => {
  // DELETE requests might not return a body, so the expected type is void.
  // The apiService will handle non-2xx responses as errors.
  return apiService.delete<void>(`/users/me/portfolios/${portfolioId}`);
};