const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { randomUUID } = require('node:crypto');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const RAWG_GAME_QUERY_KEYS = [
  'search',
  'search_precise',
  'search_exact',
  'parent_platforms',
  'platforms',
  'stores',
  'developers',
  'publishers',
  'genres',
  'tags',
  'creators',
  'dates',
  'updated',
  'platforms_count',
  'metacritic',
  'exclude_collection',
  'exclude_additions',
  'exclude_parents',
  'exclude_game_series',
  'exclude_stores',
  'ordering',
  'page',
  'page_size',
  'esrb_rating',
];

const games = [];
const MAX_TITLE_LENGTH = 120;

function resetGames() {
  games.splice(0, games.length);
}

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function isFiniteNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function validateTitle(payload, errors) {
  if (!Object.prototype.hasOwnProperty.call(payload, 'title')) {
    errors.push('title es obligatorio y debe ser una cadena de texto no vacía.');
    return;
  }

  if (typeof payload.title !== 'string') {
    errors.push('title debe ser una cadena de texto.');
    return;
  }

  if (payload.title.trim().length === 0) {
    errors.push('title es obligatorio y debe ser una cadena de texto no vacía.');
    return;
  }

  if (payload.title.trim().length > MAX_TITLE_LENGTH) {
    errors.push(`title excede la longitud máxima permitida de ${MAX_TITLE_LENGTH} caracteres.`);
  }
}

function validateGenre(payload, errors) {
  if (!Object.prototype.hasOwnProperty.call(payload, 'genre')) {
    errors.push('genre es obligatorio y debe ser una cadena de texto no vacía.');
    return;
  }

  if (typeof payload.genre !== 'string') {
    errors.push('genre debe ser una cadena de texto.');
    return;
  }

  if (payload.genre.trim().length === 0) {
    errors.push('genre es obligatorio y debe ser una cadena de texto no vacía.');
  }
}

function validateStock(payload, errors, allowNegative = false) {
  if (!Object.prototype.hasOwnProperty.call(payload, 'stock')) {
    errors.push('stock es obligatorio y debe ser un número válido.');
    return;
  }

  if (!isFiniteNumber(payload.stock)) {
    errors.push('stock es obligatorio y debe ser un número válido.');
    return;
  }

  if (!allowNegative && payload.stock < 0) {
    errors.push('stock no puede ser negativo.');
  }
}

function validateGamePayload(payload) {
  const errors = [];

  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    errors.push('El cuerpo de la solicitud debe ser un objeto JSON válido.');
    return errors;
  }

  validateTitle(payload, errors);
  validateGenre(payload, errors);
  validateStock(payload, errors);

  return errors;
}

function validateStockPatchPayload(payload) {
  const errors = [];

  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    errors.push('El cuerpo de la solicitud debe ser un objeto JSON válido.');
    return errors;
  }

  if (!Object.prototype.hasOwnProperty.call(payload, 'delta')) {
    errors.push('delta es obligatorio y debe ser un número válido.');
    return errors;
  }

  if (!isFiniteNumber(payload.delta)) {
    errors.push('delta debe ser un número válido.');
  }

  if (Object.prototype.hasOwnProperty.call(payload, 'stock') && !isFiniteNumber(payload.stock)) {
    errors.push('stock debe ser un número válido.');
  }

  return errors;
}

function findGameById(gameId) {
  return games.find((item) => item.id === gameId);
}

function normalizeGame(game) {
  return {
    id: game.id,
    title: game.title,
    genre: game.genre,
    stock: game.stock,
  };
}

function applyGameFilters(sourceGames, query) {
  let filteredGames = sourceGames;

  if (typeof query.genre === 'string' && query.genre.trim()) {
    const targetGenre = query.genre.trim().toLowerCase();
    filteredGames = filteredGames.filter((game) => game.genre.toLowerCase() === targetGenre);
  }

  return filteredGames;
}

app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok' });
});

app.get('/api/games', (_req, res) => {
  res.json(applyGameFilters(games, _req.query).map(normalizeGame));
});

function appendQueryParams(params, sourceQuery, keys) {
  keys.forEach((key) => {
    const value = sourceQuery[key];

    if (typeof value === 'string' && value.trim()) {
      params.set(key, value.trim());
    }
  });
}

app.get('/api/external/games', async (req, res) => {
  const apiKey = process.env.RAWG_API_KEY;

  if (!apiKey) {
    return res.status(500).json({ message: 'RAWG_API_KEY no está configurada.' });
  }

  const params = new URLSearchParams();
  params.set('key', apiKey);
  appendQueryParams(params, req.query, RAWG_GAME_QUERY_KEYS);

  if (!params.has('page_size')) {
    params.set('page_size', '12');
  }

  if (!params.has('ordering')) {
    params.set('ordering', '-rating');
  }

  try {
    const response = await fetch(`https://api.rawg.io/api/games?${params.toString()}`);
    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ message: 'No fue posible consultar RAWG.', details: data });
    }

    return res.json({
      count: data.count,
      results: data.results,
    });
  } catch (error) {
    return res.status(503).json({ message: 'No se pudo conectar con el servicio externo RAWG.', error: error.message });
  }
});

app.get('/api/external/games/:id', async (req, res) => {
  const apiKey = process.env.RAWG_API_KEY;

  if (!apiKey) {
    return res.status(500).json({ message: 'RAWG_API_KEY no está configurada.' });
  }

  const params = new URLSearchParams();
  params.set('key', apiKey);

  try {
    const response = await fetch(`https://api.rawg.io/api/games/${req.params.id}?${params.toString()}`);
    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ message: 'No fue posible consultar RAWG.', details: data });
    }

    return res.json(data);
  } catch (error) {
    return res.status(503).json({ message: 'No se pudo conectar con el servicio externo RAWG.', error: error.message });
  }
});

app.get('/api/external/platforms', async (req, res) => {
  const apiKey = process.env.RAWG_API_KEY;

  if (!apiKey) {
    return res.status(500).json({ message: 'RAWG_API_KEY no está configurada.' });
  }

  const params = new URLSearchParams();
  params.set('key', apiKey);
  appendQueryParams(params, req.query, ['ordering', 'page', 'page_size']);

  if (!params.has('page_size')) {
    params.set('page_size', '20');
  }

  try {
    const response = await fetch(`https://api.rawg.io/api/platforms?${params.toString()}`);
    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ message: 'No fue posible consultar plataformas RAWG.', details: data });
    }

    return res.json({
      count: data.count,
      results: data.results,
    });
  } catch (error) {
    return res.status(502).json({ message: 'Error al conectar con RAWG.', error: error.message });
  }
});

app.post('/api/games', (req, res) => {
  const errors = validateGamePayload(req.body);

  if (errors.length > 0) {
    return res.status(400).json({ message: errors.join(' ') });
  }

  const game = {
    id: randomUUID(),
    title: req.body.title.trim(),
    genre: req.body.genre.trim(),
    stock: req.body.stock,
  };

  games.push(game);
  return res.status(201).json(game);
});

app.get('/api/games/:id', (req, res) => {
  const game = findGameById(req.params.id);

  if (!game) {
    return res.status(404).json({ message: 'Juego no encontrado.' });
  }

  return res.json(game);
});

app.patch('/api/games/:id/stock', (req, res) => {
  const errors = validateStockPatchPayload(req.body);

  if (errors.length > 0) {
    return res.status(400).json({ message: errors.join(' ') });
  }

  const game = findGameById(req.params.id);

  if (!game) {
    return res.status(404).json({ message: 'Juego no encontrado.' });
  }

  const nextStock = game.stock + req.body.delta;

  if (nextStock < 0) {
    return res.status(400).json({ message: 'El stock no puede ser negativo.' });
  }

  game.stock = nextStock;
  return res.json(game);
});

app.put('/api/games/:id', (req, res) => {
  const errors = validateGamePayload(req.body);

  if (errors.length > 0) {
    return res.status(400).json({ message: errors.join(' ') });
  }

  const game = findGameById(req.params.id);

  if (!game) {
    return res.status(404).json({ message: 'Juego no encontrado.' });
  }

  game.title = req.body.title.trim();
  game.genre = req.body.genre.trim();
  game.stock = req.body.stock;

  return res.json(game);
});

app.delete('/api/games/:id', (req, res) => {
  const gameIndex = games.findIndex((item) => item.id === req.params.id);

  if (gameIndex === -1) {
    return res.status(404).json({ message: 'Juego no encontrado.' });
  }

  games.splice(gameIndex, 1);
  return res.status(204).send();
});

app.use((error, _req, res, next) => {
  if (error instanceof SyntaxError && 'body' in error) {
    return res.status(400).json({ message: 'JSON inválido en el cuerpo de la solicitud.' });
  }

  return next(error);
});

app.use((_req, res) => {
  res.status(404).json({ message: 'Ruta no encontrada.' });
});

module.exports = {
  app,
  games,
  resetGames,
};
