<template>
  <StandardLayout>
    <template #body>
      <MarketDataTicker :tickers="['^GSPC', '^IXIC', '^GDAXI', '^VIX']" />
      <HeroSection
        title="Automate Your Investment Strategy."
        subtitle="Sentinel helps you follow your investment plan with discipline by monitoring the market for you. Define your rules, get notified, and stay in control."
      />
      <KeyFeaturesSection
        :features="[
          { icon: 'mdi-strategy', title: 'Define Your Strategy', description: 'Codify your investment philosophy into a set of clear, unemotional buy and sell rules.' },
          { icon: 'mdi-robot', title: 'Automated Monitoring', description: 'Let Sentinel watch the market for you 24/7, tracking prices and technical indicators.' },
          { icon: 'mdi-shield-check', title: 'Stay in Control', description: 'Receive timely, data-driven alerts, allowing you to execute your plan with discipline.' },
        ]"
      />
      <ProblemSolutionSection
        title="For the Busy, Hands-On Investor"
        :items="[
          { title: 'The Problem: No Time to Watch', description: 'You have a strategy, but work and family commitments prevent you from monitoring the market for the right entry and exit points.', icon: 'mdi-clock-outline' },
          { title: 'The Problem: High Management Fees', description: 'Professional wealth managers are expensive and often don\'t align perfectly with your personal investment philosophy.', icon: 'mdi-cash-remove' },
          { title: 'The Solution: Your Personal Sentinel', description: 'Sentinel automates your market surveillance. It\'s your always-on assistant, executing your strategy with precision so you can stay in control, save on fees, and invest with confidence.', icon: 'mdi-shield-account' },
        ]"
      />
      <TargetAudienceSection
        title="Is Sentinel Right For You?"
        :goodFit="{
          title: '✅ Yes, if you are a...', 
          items: [
            'Swing or Positional Trader',
            'Disciplined, rule-based investor',
            'Long-term thinker who still values good timing',
            'Busy professional who uses daily charts for decisions',
          ],
        }"
        :badFit="{
          title: '❌ Probably Not, if you are a...', 
          items: [
            'Day Trader who needs real-time, intraday data',
            'High-frequency trader',
            'Purely \'buy and hold forever\' investor',
            'Trader who relies on gut feeling over a defined strategy',
          ],
        }"
      />
    </template>
  </StandardLayout>
</template>

<script setup lang="ts">
// --- All this logic is no longer needed here! ---
// import AppBar from '@/components/AppBar.vue';
// import { useRouter } from 'vue-router';
// import { useAuthStore } from '@/stores/auth';

import StandardLayout from '@/components/StandardLayout.vue';
import MarketDataTicker from '@/components/MarketDataTicker.vue';
import HeroSection from '@/components/HeroSection.vue';
import KeyFeaturesSection from '@/components/KeyFeaturesSection.vue';
import ProblemSolutionSection from '@/components/ProblemSolutionSection.vue';
import TargetAudienceSection from '@/components/TargetAudienceSection.vue';

// The script is now clean and focused only on the components this page uses.
</script>

<style scoped>
/* Add any specific styles for the homepage here */
</style>