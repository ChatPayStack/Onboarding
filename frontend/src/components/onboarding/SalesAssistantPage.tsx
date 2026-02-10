import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
import { Send, Loader2, Bot, User, Sparkles } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface SalesAssistantPageProps {
  businessId: string;
}

export const SalesAssistantPage = ({ businessId }: SalesAssistantPageProps) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
    };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setIsLoading(true);

    try {
      const response = await api.query({
        business_id: businessId,
        query: query,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fade-in flex min-h-screen flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
              <Sparkles className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h1 className="font-semibold">Sales Assistant</h1>
              <p className="text-sm text-muted-foreground">Test your AI-powered bot</p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded-full bg-primary/10 px-3 py-1.5">
            <span className="h-2 w-2 animate-pulse rounded-full bg-primary" />
            <span className="text-sm font-medium text-primary">Creating Telegram Bot...</span>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 overflow-hidden">
        <div className="mx-auto flex h-full max-w-4xl flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-6">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center">
                <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary/10">
                  <Bot className="h-10 w-10 text-primary" />
                </div>
                <h2 className="text-2xl font-bold">
                  Let's test your sales assistant
                </h2>
                <p className="mt-2 max-w-md text-muted-foreground">
                  While we create your Telegram bot, try asking questions about your products
                </p>
                <div className="mt-8 flex flex-wrap justify-center gap-2">
                  {[
                    'What products do you have?',
                    'What are your best sellers?',
                    'Tell me about shipping',
                  ].map((suggestion) => (
                    <button
                      key={suggestion}
                      onClick={() => setQuery(suggestion)}
                      className="rounded-full border border-border bg-secondary/50 px-4 py-2 text-sm transition-colors hover:bg-secondary"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`slide-up flex gap-4 ${
                      message.role === 'user' ? 'justify-end' : ''
                    }`}
                  >
                    {message.role === 'assistant' && (
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-primary/10">
                        <Bot className="h-5 w-5 text-primary" />
                      </div>
                    )}
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-secondary'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                    {message.role === 'user' && (
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-secondary">
                        <User className="h-5 w-5 text-muted-foreground" />
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className="slide-up flex gap-4">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-primary/10">
                      <Bot className="h-5 w-5 text-primary" />
                    </div>
                    <div className="flex items-center gap-2 rounded-2xl bg-secondary px-4 py-3">
                      <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                      <span className="text-muted-foreground">Thinking...</span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-border bg-card/50 p-4 backdrop-blur-sm">
            <form onSubmit={handleSubmit} className="mx-auto max-w-3xl">
              <div className="card-elevated flex items-center gap-2 rounded-2xl border border-border p-2">
                <Input
                  type="text"
                  placeholder="Ask a question about your products..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="h-12 flex-1 border-0 bg-transparent text-base placeholder:text-muted-foreground/60 focus-visible:ring-0"
                  disabled={isLoading}
                />
                <Button
                  type="submit"
                  disabled={isLoading || !query.trim()}
                  size="icon"
                  className="glow-button h-10 w-10 shrink-0 bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  {isLoading ? (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  ) : (
                    <Send className="h-5 w-5" />
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
