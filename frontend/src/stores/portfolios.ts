// frontend/src/stores/portfolios.ts
// This store manages the state for user portfolios, including the list of
// all portfolios and the currently selected/viewed portfolio.
// References: product_spec.md (Chapter 3)

import { defineStore } from 'pinia'
import type { Portfolio, PortfolioCreationRequest, PortfolioSummary, PortfolioUpdateRequest } from '@/api/models'
import * as portfolioService from '@/services/api/portfolioService';

interface PortfoliosState {
  portfolioList: PortfolioSummary[];
  currentPortfolio: Portfolio | null;
  loading: boolean;
  error: string | null;
}

export const usePortfolioStore = defineStore('portfolios', {
  state: (): PortfoliosState => ({
    portfolioList: [],
    currentPortfolio: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchPortfolios() {
      // References: product_spec.md (P_2200: Portfolio List Retrieval)
      this.loading = true;
      this.error = null;
      try {
        this.portfolioList = await portfolioService.listPortfolios();
      } catch (err: unknown) {
        if (err instanceof Error) {
          this.error = err.message;
        } else {
          this.error = 'An unexpected error occurred while fetching portfolios.';
        }
        this.portfolioList = [];
      } finally {
        this.loading = false;
      }
    },

    async fetchPortfolioById(id: string) {
      // References: product_spec.md (P_2000: Single Portfolio Retrieval)
      this.loading = true;
      this.error = null;
      try {
        this.currentPortfolio = await portfolioService.getPortfolioById(id);
      } catch (err: unknown) {
        if (err instanceof Error) {
          this.error = err.message;
        } else {
          this.error = `An unexpected error occurred while fetching portfolio ${id}.`;
        }
        this.currentPortfolio = null;
      } finally {
        this.loading = false;
      }
    },

    async createPortfolio(portfolioData: PortfolioCreationRequest) {
      // References: product_spec.md (P_1000: Portfolio Creation)
      this.loading = true;
      this.error = null;
      try {
        const newPortfolio = await portfolioService.createPortfolio(portfolioData);
        // After creating, refresh the list to include the new portfolio
        await this.fetchPortfolios();
        return newPortfolio;
      } catch (err: unknown) {
        if (err instanceof Error) {
          this.error = err.message;
        } else {
          this.error = 'An unexpected error occurred while creating the portfolio.';
        }
        return null;
      } finally {
        this.loading = false;
      }
    },

    async updatePortfolio(id: string, portfolioData: PortfolioUpdateRequest) {
      // References: product_spec.md (P_3000: Portfolio Update)
      this.loading = true;
      this.error = null;
      try {
        const updatedPortfolio = await portfolioService.updatePortfolio(id, portfolioData);
        this.currentPortfolio = updatedPortfolio;
        // After updating, refresh the list to reflect any name changes
        await this.fetchPortfolios();
        return updatedPortfolio;
      } catch (err: unknown) {
        if (err instanceof Error) {
          this.error = err.message;
        } else {
          this.error = 'An unexpected error occurred while updating the portfolio.';
        }
        return null;
      } finally {
        this.loading = false;
      }
    },

    async deletePortfolio(id: string) {
      // References: product_spec.md (P_4000: Portfolio Deletion)
      this.loading = true;
      this.error = null;
      try {
        await portfolioService.deletePortfolio(id);
        if (this.currentPortfolio?.portfolioId === id) {
          this.currentPortfolio = null;
        }
        // After deleting, refresh the list
        await this.fetchPortfolios();
        return true;
      } catch (err: unknown) {
        if (err instanceof Error) {
          this.error = err.message;
        } else {
          this.error = 'An unexpected error occurred while deleting the portfolio.';
        }
        return false;
      } finally {
        this.loading = false;
      }
    },
  },
});