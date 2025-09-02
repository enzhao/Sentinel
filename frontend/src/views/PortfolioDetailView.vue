<template>
  <v-container>
    <v-row v-if="portfolioStore.loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>
    <v-row v-else-if="portfolioStore.error">
      <v-col>
        <v-alert type="error">{{ portfolioStore.error }}</v-alert>
      </v-col>
    </v-row>
    <v-row v-else-if="portfolio">
      <v-col cols="12">
        <v-card>
          <v-card-title>{{ portfolio.name }}</v-card-title>
          <v-card-subtitle>{{ portfolio.description }}</v-card-subtitle>
          <v-card-text>
            <p><strong>Currency:</strong> {{ portfolio.defaultCurrency }}</p>
            <p><strong>Total Cash:</strong> {{ formatCurrency(portfolio.cashReserve.totalAmount, portfolio.defaultCurrency) }}</p>
            <p><strong>War Chest:</strong> {{ formatCurrency(portfolio.cashReserve.warChestAmount, portfolio.defaultCurrency) }}</p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="editPortfolio">Edit</v-btn>
            <v-btn color="error" @click="openDeleteDialog">Delete</v-btn>
          </v-card-actions>
        </v-card>

        <!-- Placeholder for the future Holdings List component -->
        <v-card class="mt-6">
          <v-card-title>Holdings</v-card-title>
          <v-divider></v-divider>
          <v-card-text class="text-center text-grey">Holdings list will be displayed here.</v-card-text>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePortfolioStore } from '@/stores/portfolios';

// References:
// - product_spec.md#3.1.2.2 (Single Retrieval)
// - docs/specs/views_spec.yaml (VIEW_PORTFOLIO_DETAIL)
// - docs/specs/ui_flows_spec.yaml (FLOW_VIEW_PORTFOLIO_DETAIL)

const route = useRoute();
const router = useRouter();
const portfolioStore = usePortfolioStore();

const portfolioId = computed(() => route.params.id as string);
const portfolio = computed(() => portfolioStore.currentPortfolio);

onMounted(() => {
  if (portfolioId.value) {
    portfolioStore.fetchPortfolioById(portfolioId.value);
  }
});

const editPortfolio = () => {
  router.push({ name: 'portfolio-edit', params: { id: portfolioId.value } });
};

const openDeleteDialog = () => {
  // This will be implemented with the delete modal component
  console.log('Open delete dialog for', portfolioId.value);
};

const formatCurrency = (value: number, currency: string) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value);
};
</script>