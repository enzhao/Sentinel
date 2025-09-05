<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card>
          <v-card-title>{{ isEditing ? 'Edit Portfolio' : 'Create Portfolio' }}</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="formData.name"
                :rules="[rules.required]"
                label="Portfolio Name"
                required
              ></v-text-field>
              <v-textarea
                v-model="formData.description"
                label="Description (Optional)"
              ></v-textarea>
              <v-select
                v-model="formData.defaultCurrency"
                :items="['USD', 'EUR', 'GBP']"
                :rules="[rules.required]"
                label="Default Currency"
                required
              ></v-select>
              <v-text-field
                v-model.number="formData.cashReserve.totalAmount"
                :rules="[rules.required, rules.nonNegative]"
                label="Total Cash Reserve"
                type="number"
                prefix="$"
              ></v-text-field>
              <v-text-field
                v-model.number="formData.cashReserve.warChestAmount"
                :rules="[rules.required, rules.nonNegative, warChestRule]"
                label="War Chest Amount"
                type="number"
                prefix="$"
                hint="Portion of cash for opportunistic buying"
                persistent-hint
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="cancel">Cancel</v-btn>
            <v-btn color="primary" :disabled="!valid" :loading="portfolioStore.loading" @click="save">
              Save Portfolio
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePortfolioStore } from '@/stores/portfolios';
import { Currency, type PortfolioCreationRequest, type PortfolioUpdateRequest } from '@/api/models';

// References:
// - product_spec.md#3.1.1 (Creation), #3.1.3 (Update)
// - docs/specs/views_spec.yaml (VIEW_PORTFOLIO_FORM)
// - docs/specs/ui_flows_spec.yaml (FLOW_CREATE_PORTFOLIO_MANUAL, FLOW_UPDATE_PORTFOLIO_MANUAL)

const route = useRoute();
const router = useRouter();
const portfolioStore = usePortfolioStore();

const form = ref<any>(null);
const valid = ref(false);

const isEditing = computed(() => !!route.params.id);
const portfolioId = computed(() => route.params.id as string | undefined);

const formData = ref<PortfolioCreationRequest | PortfolioUpdateRequest>({
  name: '',
  description: '',
  defaultCurrency: Currency.EUR,
  cashReserve: {
    totalAmount: 0,
    warChestAmount: 0,
  },
});

const rules = {
  required: (v: any) => !!v || 'This field is required',
  nonNegative: (v: number) => v >= 0 || 'Value cannot be negative',
};

const warChestRule = (v: number) =>
  v <= formData.value.cashReserve.totalAmount || 'War chest cannot exceed total cash';

onMounted(async () => {
  if (isEditing.value && portfolioId.value) {
    await portfolioStore.fetchPortfolioById(portfolioId.value);
    if (portfolioStore.currentPortfolio) {
      formData.value = { ...portfolioStore.currentPortfolio };
    }
  } else {
    portfolioStore.currentPortfolio = null;
  }
});

const save = async () => {
  await form.value?.validate();
  if (!valid.value) return;

  const result = isEditing.value && portfolioId.value
    ? await portfolioStore.updatePortfolio(portfolioId.value, formData.value as PortfolioUpdateRequest)
    : await portfolioStore.createPortfolio(formData.value as PortfolioCreationRequest);

  if (result) {
    router.push({ name: 'dashboard' });
  }
};

const cancel = () => {
  router.back();
};
</script>