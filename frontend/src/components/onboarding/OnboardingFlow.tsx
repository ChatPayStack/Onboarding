import { useOnboardingState } from '@/hooks/useOnboardingState';
import { LoginPage } from './LoginPage';
import { ShopifyIngestionPage } from './ShopifyIngestionPage';
import { SalesAssistantPage } from './SalesAssistantPage';

export const OnboardingFlow = () => {
  const {
    state,
    getCurrentStep,
    setLoginData,
    setUploadBatchId,
    setBusinessId,
  } = useOnboardingState();

  const currentStep = getCurrentStep();

  // Handle login success
  const handleLoginSuccess = (data: {
    userId: string;
    password: string;
    businessId?: string;
    authMetadata?: Record<string, unknown>;
  }) => {
    setLoginData(data);
    
    // If businessId is returned from login, set it
    if (data.businessId) {
      setBusinessId(data.businessId);
    }
    if (data.uploadBatchId) {
      setUploadBatchId(data.uploadBatchId);
    }
  };

  // Handle ingestion success
  const handleIngestionSuccess = (uploadBatchId: string) => {
    setUploadBatchId(uploadBatchId);
  };

  // Render based on current step
  switch (currentStep) {
    case 'login':
      return <LoginPage onSuccess={handleLoginSuccess} />;
    
    case 'ingestion':
      return (
        <ShopifyIngestionPage 
          businessId={state.businessId || ''} 
          onSuccess={handleIngestionSuccess} 
        />
      );
    
    case 'testing':
      return <SalesAssistantPage businessId={state.businessId || ''} />;
    
    default:
      return <LoginPage onSuccess={handleLoginSuccess} />;
  }
};
