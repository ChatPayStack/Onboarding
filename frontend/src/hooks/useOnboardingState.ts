import { useState, useEffect, useCallback } from 'react';

export interface OnboardingState {
  userId: string | null;
  password: string | null;
  businessId: string | null;
  uploadBatchId: string | null;
  authMetadata: Record<string, unknown> | null;
}

type OnboardingStep = 'login' | 'ingestion' | 'testing';

const STORAGE_KEY = 'onboarding_state';

const getStoredState = (): OnboardingState => {
  try {
    const stored = sessionStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (e) {
    console.error('Failed to parse sessionStorage:', e);
  }
  return {
    userId: null,
    password: null,
    businessId: null,
    uploadBatchId: null,
    authMetadata: null,
  };
};

const saveState = (state: OnboardingState) => {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save to sessionStorage:', e);
  }
};

export const useOnboardingState = () => {
  const [state, setState] = useState<OnboardingState>(getStoredState);

  useEffect(() => {
    saveState(state);
  }, [state]);

  const getCurrentStep = useCallback((): OnboardingStep => {
    // No login credentials → show login
    if (!state.userId || !state.password) {
      return 'login';
    }
    
    // Logged in but no upload_batch_id → show ingestion
    if (!state.uploadBatchId) {
      return 'ingestion';
    }
    
    // Has everything → show testing
    return 'testing';
  }, [state]);

  const setLoginData = useCallback((data: {
    userId: string;
    password: string;
    businessId?: string;
    authMetadata?: Record<string, unknown>;
  }) => {
    setState(prev => ({
      ...prev,
      userId: data.userId,
      password: btoa(data.password), // Simple encoding for demo
      businessId: data.businessId || prev.businessId,
      authMetadata: data.authMetadata || prev.authMetadata,
    }));
  }, []);

  const setUploadBatchId = useCallback((uploadBatchId: string) => {
    setState(prev => ({
      ...prev,
      uploadBatchId,
    }));
  }, []);

  const setBusinessId = useCallback((businessId: string) => {
    setState(prev => ({
      ...prev,
      businessId,
    }));
  }, []);

  const logout = useCallback(() => {
    setState({
      userId: null,
      password: null,
      businessId: null,
      uploadBatchId: null,
      authMetadata: null,
    });
  }, []);

  const isLoggedIn = Boolean(state.userId && state.password);

  return {
    state,
    getCurrentStep,
    setLoginData,
    setUploadBatchId,
    setBusinessId,
    logout,
    isLoggedIn,
  };
};
