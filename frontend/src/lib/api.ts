 const API_BASE_URL = "http://localhost:8001";

interface LoginRequest {
  user_id: string;
  password: string;
}

interface LoginResponse {
  user_id: string;
  business_id: string;
  upload_batch_id: string | null;
}

interface IngestRequest {
  url: string;
  business_id: string;
}

interface IngestResponse {
  upload_batch_id: string;
  products: number;
  status: string;
}

interface QueryRequest {
  business_id: string;
  query: string;
}

interface QueryResponse {
  response: string;
  sources?: string[];
}

// Simulate network delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const api = {
  async login(data: LoginRequest): Promise<LoginResponse> {
  

    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }
    console.log(response)

    return response.json();
    
  },

  async ingest(data: IngestRequest): Promise<IngestResponse> {
    const response = await fetch(`${API_BASE_URL}/ingest`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Ingestion failed');
    }

    return response.json();
    
  },

  async query(data: QueryRequest): Promise<QueryResponse> {
    

    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Query failed');
    }

    return response.json();
    
  },
};
