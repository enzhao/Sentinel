// frontend/src/stores/portfolios.ts
// This store manages the state for user portfolios.
// For the User Settings feature, it provides a minimal implementation
// to fetch a list of portfolios for the default portfolio selection.
// References: product_spec.md (Chapter 3)

import { defineStore } from 'pinia';
import axios from 'axios';
import { API_BASE_URL } from '@/config';

// As per product_spec.md section 3.3.2.2, the list view returns a summary.
export interface PortfolioSummary {
  portfolioId: string;
  name: string;
  description?: string;
  defaultCurrency: 'EUR' | 'USD' | 'GBP';
}

interface PortfoliosState {
  portfolios: PortfolioSummary[];
  loading: boolean;
  error: string | null;
}

export const usePortfolioStore = defineStore('portfolios', {
  state: (): PortfoliosState => ({
    portfolios: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchPortfolios() {
      // References: product_spec.md (P_2200: Portfolio List Retrieval)
      this.loading = true;
      this.error = null;
      const response = await axios.get<PortfolioSummary[]>(`${API_BASE_URL}/api/v1/users/me/portfolios`);
      this.portfolios = response.data;
      this.loading = false;
    },
  },
});