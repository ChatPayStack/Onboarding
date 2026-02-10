import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
import { ArrowRight, Loader2, Store, Zap } from 'lucide-react';

interface ShopifyIngestionPageProps {
  businessId: string;
  onSuccess: (uploadBatchId: string) => void;
}

export const ShopifyIngestionPage = ({ businessId, onSuccess }: ShopifyIngestionPageProps) => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await api.ingest({
        url: url,
        business_id: businessId,
      });

      onSuccess(response.upload_batch_id);
    } catch {
      setError('Failed to ingest your store. Please check the URL and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const isValidUrl = url.includes('.myshopify.com') || url.includes('shopify');

  return (
    <div className="fade-in flex min-h-screen flex-col items-center justify-center px-4">
      <div className="w-full max-w-2xl space-y-12 text-center">
        {/* Hero Section */}
        <div className="space-y-6">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-primary/10">
            <Store className="h-10 w-10 text-primary" />
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Now get ready to sell
            <br />
            <span className="gradient-text">through Telegram</span>
          </h1>
          
          <p className="mx-auto max-w-lg text-lg text-muted-foreground">
            Connect your Shopify store and we'll create an AI-powered sales assistant 
            that can sell your products on Telegram
          </p>
        </div>

        {/* URL Input Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="card-elevated mx-auto max-w-xl rounded-2xl border border-border p-2">
            <div className="flex items-center gap-2">
              <Input
                type="url"
                placeholder="your-store.myshopify.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                className="h-14 flex-1 border-0 bg-transparent text-lg placeholder:text-muted-foreground/60 focus-visible:ring-0"
                disabled={isLoading}
              />
              <Button
                type="submit"
                disabled={isLoading || !url}
                size="lg"
                className="glow-button h-12 gap-2 bg-primary px-6 font-semibold text-primary-foreground hover:bg-primary/90"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Connecting...
                  </>
                ) : (
                  <>
                    Connect Store
                    <ArrowRight className="h-5 w-5" />
                  </>
                )}
              </Button>
            </div>
          </div>

          {error && (
            <div className="slide-up mx-auto max-w-xl rounded-lg bg-destructive/10 p-3 text-sm text-destructive">
              {error}
            </div>
          )}
        </form>

        {/* Features */}
        <div className="mx-auto grid max-w-lg gap-4 pt-8">
          <div className="flex items-center gap-4 rounded-xl bg-secondary/30 p-4 text-left">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <Zap className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="font-medium">Instant Product Sync</p>
              <p className="text-sm text-muted-foreground">
                All your products are automatically imported
              </p>
            </div>
          </div>
        </div>

        {/* URL Hint */}
        {url && !isValidUrl && (
          <p className="text-sm text-muted-foreground">
            Make sure to enter a valid Shopify URL (e.g., store.myshopify.com)
          </p>
        )}
      </div>
    </div>
  );
};
