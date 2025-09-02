<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      My Portfolios
      <v-spacer></v-spacer>
      <v-btn v-if="!manageMode" color="primary" variant="text" @click="manageMode = true">
        Manage
      </v-btn>
      <v-btn v-if="manageMode" color="primary" variant="text" @click="manageMode = false">
        Done
      </v-btn>
    </v-card-title>
    <v-card-subtitle>
      <v-btn color="primary" @click="goToCreatePortfolio" size="small" class="ml-n2">
        <v-icon left>mdi-plus</v-icon>
        Add Portfolio
      </v-btn>
    </v-card-subtitle>
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
          <v-btn
            v-if="manageMode"
            icon="mdi-delete-outline"
            variant="text"
            @click.stop="openDeleteDialog(portfolio)"
          ></v-btn>
          <v-icon v-else>mdi-chevron-right</v-icon>
        </template>
      </v-list-item>
      <v-list-item v-if="portfolioStore.portfolioList.length === 0">
        <v-list-item-title class="text-center text-grey">
          No portfolios found. Click "Add Portfolio" to get started.
        </v-list-item-title>
      </v-list-item>
    </v-list>

    <!-- Reusable Deletion Confirmation Dialog -->
    <ConfirmationDialog
      v-if="portfolioToDelete"
      v-model="isDeleteDialogOpen"
      title="Confirm Deletion"
      :message="`Are you sure you want to delete the portfolio '${portfolioToDelete.name}'? This action is irreversible.`"
      :loading="portfolioStore.loading"
      @confirm="handleDeleteConfirm"
      @cancel="handleDeleteCancel"
    />
  </v-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { usePortfolioStore } from '@/stores/portfolios';
import { useRouter } from 'vue-router';
import ConfirmationDialog from '@/components/ConfirmationDialog.vue';
import type { PortfolioSummary } from '@/api/models';

const portfolioStore = usePortfolioStore();
const router = useRouter();

const manageMode = ref(false);
const isDeleteDialogOpen = ref(false);
const portfolioToDelete = ref<PortfolioSummary | null>(null);

onMounted(() => {
  portfolioStore.fetchPortfolios();
});

const viewPortfolio = (id: string) => router.push({ name: 'portfolio-detail', params: { id } });
const goToCreatePortfolio = () => router.push({ name: 'portfolio-create' });

const openDeleteDialog = (portfolio: PortfolioSummary) => {
  portfolioToDelete.value = portfolio;
  isDeleteDialogOpen.value = true;
};

const handleDeleteConfirm = async () => {
  if (portfolioToDelete.value) {
    await portfolioStore.deletePortfolio(portfolioToDelete.value.portfolioId);
    isDeleteDialogOpen.value = false;
    portfolioToDelete.value = null;
  }
};

const handleDeleteCancel = () => {
  isDeleteDialogOpen.value = false;
  portfolioToDelete.value = null;
};

const formatCurrency = (value: number, currency: string) => new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value);
</script>
