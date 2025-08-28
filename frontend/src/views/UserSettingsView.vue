<template>
  <StandardLayout>
    <template #body>
      <v-container>
        <ErrorMessage :message="userSettingsStore.error" />
        <v-progress-linear v-if="userSettingsStore.isLoading" indeterminate></v-progress-linear>

        <SettingsForm v-if="localUserSettings">
          <FormSection title="Portfolio Settings">
            <SelectField
              label="Default Portfolio on Login"
              :items="userSettingsStore.portfolios"
              item-title="name"
              item-value="portfolioId"
              v-model="localUserSettings.defaultPortfolioId"
            />
          </FormSection>

          <FormSection title="Notification Preferences">
            <MultiSelect
              label="Notification Channels"
              :options="['EMAIL', 'PUSH']"
              v-model="localUserSettings.notificationPreferences"
              @update:modelValue="(value) => handleNotificationPreferencesUpdate(value as ('EMAIL' | 'PUSH')[])"
            />
          </FormSection>
        </SettingsForm>
      </v-container>
    </template>

    <template #footer>
      <FormActions
        v-if="localUserSettings"
        :actions="[
          { label: 'Cancel', event: 'USER_CLICKS_CANCEL', variant: 'text' },
          { label: 'Save Changes', event: 'USER_CLICKS_SAVE', variant: 'contained', color: 'primary' },
        ]"
        @USER_CLICKS_CANCEL="handleCancel"
        @USER_CLICKS_SAVE="handleSave"
      />
    </template>
  </StandardLayout>
</template>

<script setup lang="ts">
// frontend/src/views/UserSettingsView.vue
// This view allows users to manage their application settings, such as default portfolio and notification preferences.
// References: product_spec.md Chapter 9, docs/specs/views_spec.yaml (VIEW_USER_SETTINGS), docs/specs/ui_flows_spec.yaml (FLOW_MANAGE_USER_SETTINGS)

import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useUserSettingsStore } from '@/stores/userSettings';
import { useAuthStore } from '@/stores/auth'; // Assuming an auth store exists for logout

// Components
import StandardLayout from '@/components/StandardLayout.vue';
import FormSection from '@/components/FormSection.vue';
import SelectField from '@/components/SelectField.vue';
import MultiSelect from '@/components/MultiSelect.vue';
import FormActions from '@/components/FormActions.vue';
import SettingsForm from '@/components/SettingsForm.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';

const userSettingsStore = useUserSettingsStore();
const authStore = useAuthStore();
const router = useRouter();

// Local state to hold form data, initialized from the store
const localUserSettings = ref<any>(null);

// Watch for changes in userSettingsStore.userSettings and update localUserSettings
watch(() => userSettingsStore.userSettings, (newSettings) => {
  if (newSettings) {
    localUserSettings.value = { ...newSettings };
  }
}, { immediate: true });

onMounted(() => {
  userSettingsStore.fetchUserSettings();
});

const handleNotificationPreferencesUpdate = (value: ('EMAIL' | 'PUSH')[]) => {
  if (localUserSettings.value) {
    localUserSettings.value.notificationPreferences = value;
  }
};

const handleSave = async () => {
  if (localUserSettings.value) {
    await userSettingsStore.updateUserSettings({
      defaultPortfolioId: localUserSettings.value.defaultPortfolioId,
      notificationPreferences: localUserSettings.value.notificationPreferences,
    });
    if (!userSettingsStore.error) {
      // On success, navigate back or show a success message
      router.back(); // FLOW_MANAGE_USER_SETTINGS -> Success -> NAVIGATE_BACK
    }
  }
};

const handleCancel = () => {
  router.back(); // FLOW_MANAGE_USER_SETTINGS -> USER_CLICKS_CANCEL -> (exit flow)
};
</script>
