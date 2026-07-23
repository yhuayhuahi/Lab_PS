import type {
  CreateGamePayload,
  LocalGame,
  RawgGameFilters,
  RawgPlatformResponse,
  RawgResponse,
  StockUpdatePayload,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3001';

async function requestJson<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {}),
    },
    ...options,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'Se produjo un error inesperado.');
  }

  return data as T;
}

export function fetchRawgGames(search = 'arcade'): Promise<RawgResponse> {
  const params = new URLSearchParams();
  params.set('search', search);
  params.set('page_size', '12');
  return requestJson<RawgResponse>(`/api/external/games?${params.toString()}`);
}

export function fetchRawgGamesWithFilters(filters: RawgGameFilters): Promise<RawgResponse> {
  const params = new URLSearchParams();

  Object.entries(filters).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return;
    }

    params.set(key, String(value));
  });

  if (!params.has('page_size')) {
    params.set('page_size', '12');
  }

  if (!params.has('ordering')) {
    params.set('ordering', '-rating');
  }

  return requestJson<RawgResponse>(`/api/external/games?${params.toString()}`);
}

export function fetchRawgPlatforms(): Promise<RawgPlatformResponse> {
  return requestJson<RawgPlatformResponse>('/api/external/platforms?page_size=20');
}

export function fetchLocalGames(): Promise<LocalGame[]> {
  return requestJson<LocalGame[]>('/api/games');
}

export function createLocalGame(payload: CreateGamePayload): Promise<LocalGame> {
  return requestJson<LocalGame>('/api/games', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateLocalStock(id: string, payload: StockUpdatePayload): Promise<LocalGame> {
  return requestJson<LocalGame>(`/api/games/${id}/stock`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}
