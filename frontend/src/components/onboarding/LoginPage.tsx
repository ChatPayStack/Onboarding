import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { api } from '@/lib/api';
import { Loader2, Sparkles } from 'lucide-react';

interface LoginPageProps {
  onSuccess: (data: {
    userId: string;
    password: string;
    businessId?: string;
    uploadBatchId?:string;
    authMetadata?: Record<string, unknown>;
  }) => void;
}

export const LoginPage = ({ onSuccess }: LoginPageProps) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await api.login({
        user_id: email,
        password: password,
      });

      if (response.user_id) {
        console.log(response)
        if(response.upload_batch_id)
        {
          console.log("Here")
            onSuccess({
            userId: email,
            password: password,
            businessId: response.business_id,
            uploadBatchId:response.upload_batch_id,
            authMetadata: response.auth_metadata,
          });
        }else{
          onSuccess({
            userId: email,
            password: password,
            businessId: response.business_id,
            authMetadata: response.auth_metadata,
          });
        }
      } else {
        setError(response.message || 'Login failed. Please try again.');
      }
    } catch {
      setError('Unable to connect. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fade-in flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md space-y-8">
        {/* Logo / Brand */}
        <div className="text-center">
          <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
            <Sparkles className="h-7 w-7 text-primary" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Welcome back</h1>
          <p className="mt-2 text-muted-foreground">
            Sign in to your agentic commerce platform
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="card-elevated space-y-6 rounded-2xl border border-border p-8">
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="input-glow h-12 border-border bg-secondary/50 transition-all focus:border-primary"
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-sm font-medium">
                Password
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="input-glow h-12 border-border bg-secondary/50 transition-all focus:border-primary"
                disabled={isLoading}
              />
            </div>
          </div>

          {error && (
            <div className="slide-up rounded-lg bg-destructive/10 p-3 text-sm text-destructive">
              {error}
            </div>
          )}

          <Button
            type="submit"
            disabled={isLoading || !email || !password}
            className="glow-button h-12 w-full bg-primary font-semibold text-primary-foreground hover:bg-primary/90"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Signing in...
              </>
            ) : (
              'Sign in'
            )}
          </Button>
        </form>

        <p className="text-center text-sm text-muted-foreground">
          By signing in, you agree to our Terms of Service
        </p>
      </div>
    </div>
  );
};
