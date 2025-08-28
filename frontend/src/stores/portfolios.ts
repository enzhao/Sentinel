// frontend/src/stores/portfolios.ts
// This store manages the state for user portfolios.
// For the User Settings feature, it provides a minimal implementation
// to fetch a list of portfolios for the default portfolio selection.
// References: product_spec.md (Chapter 3)

import { defineStore } from 'pinia';
import axios from 'axios';
import { API_BASE_URL } from '@/config';
import type { Portfolio } from '@/api/models';

interface PortfoliosState {
  portfolios: Portfolio[];
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
      // The backend endpoint currently returns the full Portfolio object, not a summary.
      // We align the type here to match the actual API response.
      const response = await axios.get<Portfolio[]>(`${API_BASE_URL}/api/v1/users/me/portfolios`);
      this.portfolios = response.data;
      this.loading = false;
    },
  },
});