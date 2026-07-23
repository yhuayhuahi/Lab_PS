export interface RawgGenre {
  name: string;
}

export interface RawgEsrbRating {
  id: number;
  slug: string;
  name: string;
}

export interface RawgPlatformRef {
  platform: {
    id: number;
    name: string;
    slug: string;
  };
}

export interface RawgGame {
  id: number;
  name: string;
  background_image: string | null;
  rating: number;
  released: string | null;
  genres: RawgGenre[];
  metacritic?: number | null;
  esrb_rating?: RawgEsrbRating | null;
  platforms?: RawgPlatformRef[];
}

export interface RawgResponse {
  count: number;
  results: RawgGame[];
}

export interface RawgPlatform {
  id: number;
  name: string;
  slug: string;
}

export interface RawgPlatformResponse {
  count: number;
  results: RawgPlatform[];
}

export interface RawgGameFilters {
  search?: string;
  dates?: string;
  platforms?: string;
  parent_platforms?: string;
  esrb_rating?: string;
  metacritic?: string;
  ordering?: string;
  search_precise?: boolean;
  search_exact?: boolean;
  page_size?: number;
  page?: number;
}

export interface LocalGame {
  id: string;
  title: string;
  genre: string;
  stock: number;
}

export interface CreateGamePayload {
  title: string;
  genre: string;
  stock: number;
}

export interface StockUpdatePayload {
  delta: number;
}
