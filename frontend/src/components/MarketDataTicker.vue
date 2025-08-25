<template>
  <v-container fluid class="market-data-ticker-container">
    <v-row justify="center">
      <v-col cols="12">
        <v-sheet class="pa-2 text-center" color="grey-lighten-3">
          <v-chip-group active-class="primary--text">
            <v-chip v-for="ticker in displayedTickers" :key="ticker.symbol">
              <strong>{{ ticker.symbol }}</strong>: {{ ticker.price }} ({{ ticker.change }})
            </v-chip>
          </v-chip-group>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

interface TickerData {
  symbol: string;
  price: string;
  change: string;
}

const props = defineProps({
  tickers: {
    type: Array as () => string[],
    required: true,
  },
});

const displayedTickers = ref<TickerData[]>([]);
let intervalId: number | undefined;

const fetchMarketData = async () => {
  // In a real application, this would call a backend API.
  // For now, we'll mock the data.
  const mockData: { [key: string]: TickerData } = {
    '^GSPC': { symbol: 'S&P 500', price: '5,200.12', change: '+0.5%' },
    '^IXIC': { symbol: 'NASDAQ', price: '16,300.45', change: '-0.2%' },
    '^GDAXI': { symbol: 'DAX', price: '18,200.78', change: '+1.1%' },
    '^VIX': { symbol: 'VIX', price: '14.50', change: '-1.5%' },
  };

  displayedTickers.value = props.tickers.map(symbol => mockData[symbol] || { symbol, price: 'N/A', change: 'N/A' });
};

onMounted(() => {
  fetchMarketData();
  intervalId = setInterval(fetchMarketData, 60000); // Refresh every minute
});

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});

watch(() => props.tickers, () => {
  fetchMarketData();
  if (intervalId) {
    clearInterval(intervalId);
  }
  intervalId = setInterval(fetchMarketData, 60000);
}, { deep: true });
</script>

<style scoped>
.market-data-ticker-container {
  padding: 8px 0;
  background-color: #f5f5f5; /* Light grey background */
}
</style>