const request = require('supertest');
const { app, resetGames } = require('../app');

describe('API de catálogo de videojuegos', () => {
  beforeEach(() => {
    resetGames();
    jest.restoreAllMocks();
  });

  // ==========================================
  // 1. FLUJO DE PERSISTENCIA CRUZADA
  // ==========================================
  describe('Flujo de Persistencia Cruzada', () => {
    test('crea un recurso con POST y lo recupera con GET usando el id dinámico', async () => {
      const createResponse = await request(app)
        .post('/api/games')
        .send({
          title: 'Arcade Rift',
          genre: 'Arcade 2D',
          stock: 12,
        });

      expect(createResponse.status).toBe(201);
      expect(createResponse.body).toEqual(
        expect.objectContaining({
          id: expect.any(String),
          title: 'Arcade Rift',
          genre: 'Arcade 2D',
          stock: 12,
        }),
      );

      const gameId = createResponse.body.id;
      const getResponse = await request(app).get(`/api/games/${gameId}`);

      expect(getResponse.status).toBe(200);
      expect(getResponse.body).toEqual({
        id: gameId,
        title: 'Arcade Rift',
        genre: 'Arcade 2D',
        stock: 12,
      });
    });

    test('crea múltiples recursos simultáneamente y verifica que se aíslan correctamente mediante sus IDs', async () => {
      const game1 = await request(app).post('/api/games').send({ title: 'Game A', genre: 'RPG', stock: 5 });
      const game2 = await request(app).post('/api/games').send({ title: 'Game B', genre: 'Action', stock: 10 });
      
      expect(game1.body.id).not.toBe(game2.body.id);

      const getGame1 = await request(app).get(`/api/games/${game1.body.id}`);
      const getGame2 = await request(app).get(`/api/games/${game2.body.id}`);

      expect(getGame1.body.title).toBe('Game A');
      expect(getGame2.body.title).toBe('Game B');
    });

    test('devuelve HTTP 404 al intentar recuperar (GET) un recurso con un ID que no existe', async () => {
      const response = await request(app).get('/api/games/id-falso-o-inexistente');
      expect(response.status).toBe(404);
      expect(response.body.message).toBeDefined();
    });

    test('actualiza un recurso completo con PUT y verifica la persistencia con un GET posterior', async () => {
      const createResponse = await request(app).post('/api/games').send({ title: 'Old Title', genre: 'Old Genre', stock: 1 });
      const gameId = createResponse.body.id;

      const putResponse = await request(app).put(`/api/games/${gameId}`).send({
        title: 'New Title',
        genre: 'New Genre',
        stock: 100
      });

      expect(putResponse.status).toBe(200);

      const getResponse = await request(app).get(`/api/games/${gameId}`);
      expect(getResponse.body.title).toBe('New Title');
      expect(getResponse.body.stock).toBe(100);
    });
  });

  // ==========================================
  // 2. SIMULACIÓN DE MODIFICACIÓN DE ESTADO
  // ==========================================
  describe('Simulación de Modificación de Estado', () => {
    test('aplica un cambio de stock negativo (resta) y consolida el nuevo valor en lectura posterior', async () => {
      const createResponse = await request(app).post('/api/games').send({ title: 'Visual Chronicle', genre: 'Visual Novel', stock: 20 });
      const gameId = createResponse.body.id;

      const patchResponse = await request(app).patch(`/api/games/${gameId}/stock`).send({ delta: -5 });
      
      expect(patchResponse.status).toBe(200);
      expect(patchResponse.body.stock).toBe(15);

      const getResponse = await request(app).get(`/api/games/${gameId}`);
      expect(getResponse.body.stock).toBe(15);
    });

    test('aplica un cambio de stock positivo (suma) y consolida el nuevo valor', async () => {
      const createResponse = await request(app).post('/api/games').send({ title: 'Restock Game', genre: 'FPS', stock: 2 });
      const gameId = createResponse.body.id;

      const patchResponse = await request(app).patch(`/api/games/${gameId}/stock`).send({ delta: 10 });
      
      expect(patchResponse.status).toBe(200);
      expect(patchResponse.body.stock).toBe(12);
    });

    test('rechaza la reducción de stock por debajo de cero con HTTP 400', async () => {
      const createResponse = await request(app).post('/api/games').send({ title: 'Low Stock Game', genre: 'Indie', stock: 3 });
      const gameId = createResponse.body.id;

      const patchResponse = await request(app).patch(`/api/games/${gameId}/stock`).send({ delta: -5 });
      
      expect(patchResponse.status).toBe(400);
      expect(patchResponse.body.message).toContain('El stock no puede ser negativo');
    });

    test('devuelve HTTP 404 al intentar modificar el estado de un recurso inexistente', async () => {
      const patchResponse = await request(app).patch('/api/games/un-id-que-no-existe/stock').send({ delta: 5 });
      expect(patchResponse.status).toBe(404);
    });
  });

  // ==========================================
  // 3. LISTADO, PAGINACIÓN Y BÚSQUEDA
  // ==========================================
  describe('Listado, Paginación y Búsqueda (Colecciones)', () => {
    test('devuelve una lista vacía cuando no hay juegos registrados', async () => {
      const response = await request(app).get('/api/games');
      expect(response.status).toBe(200);
      expect(response.body).toEqual([]);
    });

    test('devuelve una lista con todos los juegos creados', async () => {
      await request(app).post('/api/games').send({ title: 'Juego 1', genre: 'A', stock: 1 });
      await request(app).post('/api/games').send({ title: 'Juego 2', genre: 'B', stock: 2 });

      const response = await request(app).get('/api/games');
      expect(response.status).toBe(200);
      expect(response.body.length).toBe(2);
      expect(response.body).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ title: 'Juego 1' }),
          expect.objectContaining({ title: 'Juego 2' })
        ])
      );
    });

    test('filtra correctamente los resultados utilizando query parameters (ej. por género)', async () => {
      await request(app).post('/api/games').send({ title: 'Juego A', genre: 'RPG', stock: 10 });
      await request(app).post('/api/games').send({ title: 'Juego B', genre: 'Acción', stock: 5 });

      const response = await request(app).get('/api/games?genre=RPG');
      expect(response.status).toBe(200);
      expect(response.body.length).toBe(1);
      expect(response.body[0].title).toBe('Juego A');
    });
  });

  // ==========================================
  // 4. CICLO DE VIDA COMPLETO (DELETE)
  // ==========================================
  describe('Ciclo de Vida Completo (DELETE)', () => {
    test('elimina un recurso existente y devuelve 204 o 200, validando con GET que ya no existe (404)', async () => {
      const createResponse = await request(app)
        .post('/api/games')
        .send({ title: 'Juego a Eliminar', genre: 'Puzzle', stock: 5 });
      const gameId = createResponse.body.id;

      const deleteResponse = await request(app).delete(`/api/games/${gameId}`);
      expect([200, 204]).toContain(deleteResponse.status);

      const getResponse = await request(app).get(`/api/games/${gameId}`);
      expect(getResponse.status).toBe(404);
    });

    test('devuelve HTTP 404 al intentar eliminar un recurso con un ID inexistente', async () => {
      const response = await request(app).delete('/api/games/id-fantasma');
      expect(response.status).toBe(404);
    });
  });

  // ==========================================
  // 5. VALIDACIÓN DE ROBUSTEZ (EDGE CASES)
  // ==========================================
  describe('Validación de Robustez (Edge Cases)', () => {
    test('rechaza campos obligatorios vacíos con HTTP 400', async () => {
      const response = await request(app)
        .post('/api/games')
        .send({
          title: '',
          genre: '',
          stock: 10,
        });

      expect(response.status).toBe(400);
      expect(response.body.message).toContain('title es obligatorio');
      expect(response.body.message).toContain('genre es obligatorio');
    });

    test('rechaza una petición con body completamente vacío con HTTP 400', async () => {
      const response = await request(app).post('/api/games').send({});
      expect(response.status).toBe(400);
      expect(response.body.message).toBeDefined();
    });

    test('rechaza un stock de tipo texto con HTTP 400', async () => {
      const response = await request(app).post('/api/games').send({
        title: 'Broken Input',
        genre: 'Arcade',
        stock: 'cinco',
      });

      expect(response.status).toBe(400);
      expect(response.body.message).toContain('stock es obligatorio y debe ser un número válido');
    });

    test('rechaza la creación de un recurso si el stock inicial es un número negativo', async () => {
      const response = await request(app).post('/api/games').send({
        title: 'Debt Game',
        genre: 'Simulator',
        stock: -10,
      });

      expect(response.status).toBe(400);
      expect(response.body.message).toContain('stock no puede ser negativo');
    });

    test('rechaza tipos de datos incorrectos en propiedades de texto', async () => {
      const response = await request(app).post('/api/games').send({
        title: 12345,
        genre: true,
        stock: 5,
      });

      expect(response.status).toBe(400);
      expect(response.body.message).toContain('title debe ser una cadena de texto');
    });

    test('rechaza un payload de modificación de estado (PATCH) que no incluye la propiedad delta', async () => {
      const createResponse = await request(app).post('/api/games').send({ title: 'Game', genre: 'Test', stock: 10 });
      const gameId = createResponse.body.id;

      const patchResponse = await request(app).patch(`/api/games/${gameId}/stock`).send({ amount: 5 });
      
      expect(patchResponse.status).toBe(400);
      expect(patchResponse.body.message).toContain('delta es obligatorio');
    });
  });

  // ==========================================
  // 6. SEGURIDAD Y MALICIOUS INPUT
  // ==========================================
  describe('Seguridad y Casos Extremos de Validación (Malicious Input)', () => {
    test('rechaza la creación de un recurso con un título que excede la longitud máxima permitida', async () => {
      const hugeTitle = 'A'.repeat(300);
      const response = await request(app).post('/api/games').send({
        title: hugeTitle,
        genre: 'Aventura',
        stock: 10
      });

      expect(response.status).toBe(400);
      expect(response.body.message).toMatch(/longitud|máxima|caracteres/i);
    });

    test('ignora intentos de modificar campos protegidos/de solo lectura', async () => {
      const createResponse = await request(app).post('/api/games').send({ title: 'Hack Me', genre: 'Indie', stock: 5 });
      const originalId = createResponse.body.id;

      await request(app)
        .patch(`/api/games/${originalId}/stock`)
        .send({ delta: 5, id: 'id-malicioso-inyectado' });

      const getResponse = await request(app).get(`/api/games/${originalId}`);
      expect(getResponse.status).toBe(200);
      expect(getResponse.body.id).toBe(originalId);
    });

    test('maneja correctamente un payload con formato JSON inválido (ej. error de sintaxis)', async () => {
      const response = await request(app)
        .post('/api/games')
        .set('Content-Type', 'application/json')
        .send('{"title": "Juego Roto", "genre": "Fallo", "stock": 10, }'); // Coma extra (JSON inválido)

      expect(response.status).toBe(400);
    });
  });

  // ==========================================
  // 7. PROXY RAWG Y RESILIENCIA
  // ==========================================
  describe('Proxy RAWG', () => {
    test('expone resultados externos mediante el proxy del backend', async () => {
      const mockFetch = jest.spyOn(global, 'fetch').mockResolvedValue({
        ok: true,
        json: async () => ({
          count: 1,
          results: [
            {
              id: 777,
              name: 'Retro Blaze',
              background_image: 'https://example.com/retro-blaze.jpg',
              rating: 4.7,
              released: '2024-10-10',
              genres: [{ name: 'Arcade' }],
            },
          ],
        }),
      });

      const response = await request(app).get('/api/external/games?search=arcade&page_size=1');

      expect(mockFetch).toHaveBeenCalledTimes(1);
      expect(response.status).toBe(200);
      expect(response.body).toEqual({
        count: 1,
        results: [
          {
            id: 777,
            name: 'Retro Blaze',
            background_image: 'https://example.com/retro-blaze.jpg',
            rating: 4.7,
            released: '2024-10-10',
            genres: [{ name: 'Arcade' }],
          },
        ],
      });
    });

    test('reenvía filtros RAWG como fechas, plataforma, edad y metacritic', async () => {
      const mockFetch = jest.spyOn(global, 'fetch').mockResolvedValue({
        ok: true,
        json: async () => ({
          count: 0,
          results: [],
        }),
      });

      await request(app).get(
        '/api/external/games?search=arcade&dates=2024-01-01,2024-12-31&platforms=4&esrb_rating=teen&metacritic=80,100&ordering=-metacritic&search_precise=true&page_size=5',
      );

      expect(mockFetch).toHaveBeenCalledTimes(1);

      const calledUrl = mockFetch.mock.calls[0][0];
      expect(calledUrl).toContain('https://api.rawg.io/api/games?');
      expect(calledUrl).toContain('key=');
      expect(calledUrl).toContain('search=arcade');
      expect(calledUrl).toContain('dates=2024-01-01%2C2024-12-31');
      expect(calledUrl).toContain('platforms=4');
      expect(calledUrl).toContain('esrb_rating=teen');
      expect(calledUrl).toContain('metacritic=80%2C100');
      expect(calledUrl).toContain('ordering=-metacritic');
      expect(calledUrl).toContain('search_precise=true');
      expect(calledUrl).toContain('page_size=5');
    });

    test('proxy de plataformas RAWG devuelve resultados para poblar el frontend', async () => {
      const mockFetch = jest.spyOn(global, 'fetch').mockResolvedValue({
        ok: true,
        json: async () => ({
          count: 2,
          results: [
            { id: 4, name: 'PC', slug: 'pc' },
            { id: 187, name: 'PlayStation 5', slug: 'playstation5' },
          ],
        }),
      });

      const response = await request(app).get('/api/external/platforms?page_size=2');

      expect(mockFetch).toHaveBeenCalledTimes(1);
      expect(response.status).toBe(200);
      expect(response.body).toEqual({
        count: 2,
        results: [
          { id: 4, name: 'PC', slug: 'pc' },
          { id: 187, name: 'PlayStation 5', slug: 'playstation5' },
        ],
      });
    });

    describe('Resiliencia ante fallos del proveedor externo', () => {
      test('devuelve HTTP 502 (Bad Gateway) o 500 si la API de RAWG responde con un error de servidor', async () => {
        const mockFetch = jest.spyOn(global, 'fetch').mockResolvedValue({
          ok: false,
          status: 500,
          json: async () => ({ error: 'Internal Server Error' }),
        });

        const response = await request(app).get('/api/external/games?search=mario');

        expect(mockFetch).toHaveBeenCalledTimes(1);
        expect([500, 502]).toContain(response.status);
        expect(response.body.message).toBeDefined();
      });

      test('devuelve un error controlado si la petición a RAWG sufre un timeout o falla por red', async () => {
        const mockFetch = jest.spyOn(global, 'fetch').mockRejectedValue(new Error('Network Timeout'));

        const response = await request(app).get('/api/external/games?search=zelda');

        expect(mockFetch).toHaveBeenCalledTimes(1);
        expect([500, 503, 504]).toContain(response.status);
        expect(response.body.message).toContain('No se pudo conectar con el servicio externo');
      });

      test('devuelve HTTP 404 si la API de RAWG no encuentra resultados para un endpoint específico', async () => {
        const mockFetch = jest.spyOn(global, 'fetch').mockResolvedValue({
          ok: false,
          status: 404,
          json: async () => ({ detail: 'Not found.' }),
        });

        const response = await request(app).get('/api/external/games/9999999999');

        expect(mockFetch).toHaveBeenCalledTimes(1);
        expect(response.status).toBe(404);
      });
    });
  });
});