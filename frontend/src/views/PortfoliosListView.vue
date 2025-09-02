<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      My Portfolios
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="goToCreatePortfolio">
        <v-icon left>mdi-plus</v-icon>
        Add Portfolio
      </v-btn>
    </v-card-title>
    <v-divider></v-divider>

    <v-progress-linear v-if="portfolioStore.loading" indeterminate></v-progress-linear>
    
    <v-alert v-if="portfolioStore.error" type="error" class="ma-4">
      {{ portfolioStore.error }}
    </v-alert>

    <v-list v-if="!portfolioStore.loading && !portfolioStore.error">
      <v-list-item
        v-for="portfolio in portfolioStore.portfolioList"
        :key="portfolio.portfolioId"
        @click="viewPortfolio(portfolio.portfolioId)"
        lines="two"
      >
        <v-list-item-title>{{ portfolio.name }}</v-list-item-title>
        <v-list-item-subtitle>
          Value: {{ formatCurrency(portfolio.currentValue, 'USD') }}
        </v-list-item-subtitle>
        <template v-slot:append>
          <v-icon>mdi-chevron-right</v-icon>
        </template>
      </v-list-item>
      <v-list-item v-if="portfolioStore.portfolioList.length === 0">
        <v-list-item-title class="text-center text-grey">
          No portfolios found. Click "Add Portfolio" to get started.
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { usePortfolioStore } from '@/stores/portfolios';
import { useRouter } from 'vue-router';

const portfolioStore = usePortfolioStore();
const router = useRouter();

onMounted(() => {
  portfolioStore.fetchPortfolios();
});

const viewPortfolio = (id: string) => router.push({ name: 'portfolio-detail', params: { id } });
const goToCreatePortfolio = () => router.push({ name: 'portfolio-create' });

const formatCurrency = (value: number, currency: string) => new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value);
</script>
