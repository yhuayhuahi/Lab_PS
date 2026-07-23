import { FormEvent, useEffect, useMemo, useState } from 'react';
import {
  createLocalGame,
  fetchLocalGames,
  fetchRawgGamesWithFilters,
  fetchRawgPlatforms,
  updateLocalStock,
} from './lib/api';
import type { LocalGame, RawgGame, RawgPlatform, RawgGameFilters } from './types';

const defaultForm = {
  title: '',
  genre: '',
  stock: 1,
};

type DetailSource = 'rawg' | 'local';

const ageRatingOptions = [
  { label: 'Todas las edades', value: '' },
  { label: 'Everyone', value: 'everyone' },
  { label: 'Teen', value: 'teen' },
  { label: 'Mature', value: 'mature' },
  { label: 'Adults Only', value: 'adults-only' },
];

function App() {
  const [rawgGames, setRawgGames] = useState<RawgGame[]>([]);
  const [rawgPlatforms, setRawgPlatforms] = useState<RawgPlatform[]>([]);
  const [localGames, setLocalGames] = useState<LocalGame[]>([]);
  const [loadingRawg, setLoadingRawg] = useState(true);
  const [loadingPlatforms, setLoadingPlatforms] = useState(true);
  const [loadingLocal, setLoadingLocal] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [search, setSearch] = useState('arcade');
  const [filters, setFilters] = useState<RawgGameFilters>({
    ordering: '-rating',
    search_precise: false,
    search_exact: false,
  });
  const [form, setForm] = useState(defaultForm);
  const [submitting, setSubmitting] = useState(false);
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [selectedRawgId, setSelectedRawgId] = useState<number | null>(null);
  const [selectedLocalId, setSelectedLocalId] = useState<string | null>(null);
  const [selectedSource, setSelectedSource] = useState<DetailSource | null>(null);

  useEffect(() => {
    void loadRawgGames('arcade');
    void loadRawgPlatforms();
    void loadLocalGames();
  }, []);

  async function loadRawgGames(query: string = search) {
    setLoadingRawg(true);
    setErrorMessage('');

    try {
      const dateFilter = filters.dates && filters.dates.includes(',') ? filters.dates : undefined;
      const response = await fetchRawgGamesWithFilters({
        search: query,
        dates: dateFilter,
        platforms: filters.platforms,
        parent_platforms: filters.parent_platforms,
        esrb_rating: filters.esrb_rating,
        metacritic: filters.metacritic,
        ordering: filters.ordering,
        search_precise: filters.search_precise,
        search_exact: filters.search_exact,
        page_size: filters.page_size ?? 12,
        page: filters.page,
      });
      setRawgGames(response.results);
      setSelectedRawgId((currentId) =>
        response.results.some((game) => game.id === currentId) ? currentId : response.results[0]?.id ?? null,
      );
      setSelectedSource((currentSource) =>
        response.results.length > 0 ? currentSource ?? 'rawg' : currentSource,
      );
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'No se pudo cargar RAWG.');
    } finally {
      setLoadingRawg(false);
    }
  }

  async function loadRawgPlatforms() {
    setLoadingPlatforms(true);

    try {
      const response = await fetchRawgPlatforms();
      setRawgPlatforms(response.results);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'No se pudieron cargar las plataformas RAWG.');
    } finally {
      setLoadingPlatforms(false);
    }
  }

  async function loadLocalGames() {
    setLoadingLocal(true);

    try {
      const response = await fetchLocalGames();
      setLocalGames(response);
      setSelectedLocalId((currentId) =>
        response.some((game) => game.id === currentId) ? currentId : response[0]?.id ?? null,
      );
      setSelectedSource((currentSource) =>
        response.length > 0 ? currentSource ?? 'local' : currentSource,
      );
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'No se pudo cargar el inventario local.');
    } finally {
      setLoadingLocal(false);
    }
  }

  async function handleCreateGame(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setErrorMessage('');

    try {
      const createdGame = await createLocalGame({
        title: form.title,
        genre: form.genre,
        stock: Number(form.stock),
      });

      setLocalGames((currentGames) => [createdGame, ...currentGames]);
      setSelectedLocalId(createdGame.id);
      setSelectedSource('local');
      setForm(defaultForm);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'No se pudo crear el juego.');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleStockChange(gameId: string, delta: number) {
    setUpdatingId(gameId);
    setErrorMessage('');

    try {
      const updatedGame = await updateLocalStock(gameId, { delta });
      setLocalGames((currentGames) =>
        currentGames.map((game) => (game.id === gameId ? updatedGame : game)),
      );
      setSelectedLocalId(gameId);
      setSelectedSource('local');
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'No se pudo actualizar el stock.');
    } finally {
      setUpdatingId(null);
    }
  }

  const localTotal = useMemo(
    () => localGames.reduce((total, game) => total + game.stock, 0),
    [localGames],
  );

  const selectedLocalGame = useMemo(
    () => localGames.find((game) => game.id === selectedLocalId) ?? null,
    [localGames, selectedLocalId],
  );

  const selectedRawgGame = useMemo(
    () => rawgGames.find((game) => game.id === selectedRawgId) ?? null,
    [rawgGames, selectedRawgId],
  );

  const featuredGame =
    selectedSource === 'local' && selectedLocalGame
      ? { kind: 'local' as const, game: selectedLocalGame }
      : selectedSource === 'rawg' && selectedRawgGame
        ? { kind: 'rawg' as const, game: selectedRawgGame }
        : selectedLocalGame
          ? { kind: 'local' as const, game: selectedLocalGame }
          : selectedRawgGame
            ? { kind: 'rawg' as const, game: selectedRawgGame }
            : null;

  return (
    <div className="app-shell">
      <div className="orb orb-one" />
      <div className="orb orb-two" />

      <main className="layout">
        <section className="hero card">
          <div className="hero-copy">
            <p className="eyebrow">Catálogo de videojuegos</p>
            <h1>Catálogo de videojuegos para arcade 2D y visual novels.</h1>
            <p className="lead">
              La vitrina pública toma datos de RAWG mediante el proxy del backend, mientras el
              inventario del laboratorio se gestiona con CRUD en memoria para pruebas y demos.
            </p>
            <div className="hero-stats">
              <div>
                <span className="stat-value">{rawgGames.length}</span>
                <span className="stat-label">juegos RAWG visibles</span>
              </div>
              <div>
                <span className="stat-value">{localGames.length}</span>
                <span className="stat-label">títulos locales</span>
              </div>
              <div>
                <span className="stat-value">{localTotal}</span>
                <span className="stat-label">stock total</span>
              </div>
            </div>
          </div>

          <form
            className="search-panel"
            onSubmit={(event) => {
              event.preventDefault();
              void loadRawgGames(search);
            }}
          >
            <label htmlFor="search">Buscar en RAWG</label>
            <div className="search-row">
              <input
                id="search"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="arcade, visual novel, fighting..."
              />
              <button type="submit">Explorar</button>
            </div>
            <p>Consulta los juegos populares sin exponer la API key.</p>
          </form>
        </section>

        <section className="detail-section card">
          <div className="section-header">
            <div>
              <p className="eyebrow">Vista detallada</p>
              <h2>Ficha del videojuego</h2>
            </div>
            <span className="muted">Selecciona un título desde RAWG o desde el inventario local</span>
          </div>

          {featuredGame ? (
            <div className="detail-layout">
              <div className="detail-art">
                {featuredGame.kind === 'rawg' && featuredGame.game.background_image ? (
                  <img src={featuredGame.game.background_image} alt={featuredGame.game.name} />
                ) : (
                  <div className="detail-placeholder">
                    <span>{featuredGame.kind === 'rawg' ? 'RAWG' : 'LOCAL'}</span>
                    <strong>
                      {featuredGame.kind === 'rawg' ? featuredGame.game.name : featuredGame.game.title}
                    </strong>
                  </div>
                )}
              </div>

              <div className="detail-copy">
                <div className="detail-head">
                  <div>
                    <p className="eyebrow">
                      {featuredGame.kind === 'rawg' ? 'Repositorio RAWG' : 'Inventario local'}
                    </p>
                    <h3>
                      {featuredGame.kind === 'rawg'
                        ? featuredGame.game.name
                        : featuredGame.game.title}
                    </h3>
                  </div>
                  <span className="source-pill">
                    {featuredGame.kind === 'rawg' ? 'Curado desde RAWG' : 'Registro del laboratorio'}
                  </span>
                </div>

                <p className="detail-summary">
                  {featuredGame.kind === 'rawg'
                    ? 'Ficha de referencia para explorar un título popular y comparar su presencia en el catálogo.'
                    : 'Ficha operativa del inventario local con control inmediato de stock y consulta por id.'}
                </p>

                <div className="detail-metrics">
                  {featuredGame.kind === 'rawg' ? (
                    <>
                      <div>
                        <span>Rating</span>
                        <strong>{featuredGame.game.rating.toFixed(1)}</strong>
                      </div>
                      <div>
                        <span>Fecha</span>
                        <strong>{featuredGame.game.released ?? 'No disponible'}</strong>
                      </div>
                      <div>
                        <span>Género</span>
                        <strong>{featuredGame.game.genres?.[0]?.name ?? 'Sin género'}</strong>
                      </div>
                    </>
                  ) : (
                    <>
                      <div>
                        <span>Stock</span>
                        <strong>{featuredGame.game.stock}</strong>
                      </div>
                      <div>
                        <span>Género</span>
                        <strong>{featuredGame.game.genre}</strong>
                      </div>
                      <div>
                        <span>Id</span>
                        <strong>{featuredGame.game.id.slice(0, 8)}…</strong>
                      </div>
                    </>
                  )}
                </div>

                {featuredGame.kind === 'rawg' ? (
                  <div className="genre-tags">
                    {featuredGame.game.genres.length > 0 ? (
                      featuredGame.game.genres.map((genre) => <span key={genre.name}>{genre.name}</span>)
                    ) : (
                      <span>Sin etiquetas</span>
                    )}
                  </div>
                ) : (
                  <div className="genre-tags">
                    <span>{featuredGame.game.genre}</span>
                    <span>Stock controlado</span>
                  </div>
                )}

                {featuredGame.kind === 'local' ? (
                  <div className="detail-actions">
                    <button
                      type="button"
                      onClick={() => void handleStockChange(featuredGame.game.id, -5)}
                      disabled={updatingId === featuredGame.game.id}
                    >
                      Reducir 5
                    </button>
                    <button
                      type="button"
                      className="ghost-button"
                      onClick={() => void handleStockChange(featuredGame.game.id, 5)}
                      disabled={updatingId === featuredGame.game.id}
                    >
                      Aumentar 5
                    </button>
                  </div>
                ) : null}
              </div>
            </div>
          ) : (
            <p className="empty-state">Todavía no hay un videojuego seleccionado.</p>
          )}
        </section>

        <section className="filter-section card">
          <div className="section-header">
            <div>
              <p className="eyebrow">Filtros RAWG</p>
              <h2>Fecha, plataforma, edad y metacritic</h2>
            </div>
            <button
              type="button"
              className="ghost-button"
              onClick={() => {
                setFilters({
                  ordering: '-rating',
                  search_precise: false,
                  search_exact: false,
                });
                void loadRawgGames(search);
              }}
            >
              Limpiar filtros
            </button>
          </div>

          <div className="filter-grid">
            <label>
              Plataforma
              <select
                value={filters.platforms ?? ''}
                onChange={(event) => setFilters((current) => ({ ...current, platforms: event.target.value }))}
                disabled={loadingPlatforms}
              >
                <option value="">Todas</option>
                {rawgPlatforms.map((platform) => (
                  <option key={platform.id} value={platform.id}>
                    {platform.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Clasificación de edad
              <select
                value={filters.esrb_rating ?? ''}
                onChange={(event) => setFilters((current) => ({ ...current, esrb_rating: event.target.value }))}
              >
                {ageRatingOptions.map((option) => (
                  <option key={option.value || 'all'} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Desde
              <input
                type="date"
                value={filters.dates?.split(',')[0] ?? ''}
                onChange={(event) =>
                  setFilters((current) => ({
                    ...current,
                    dates: event.target.value && current.dates?.split(',')[1]
                      ? `${event.target.value},${current.dates.split(',')[1]}`
                      : event.target.value || undefined,
                  }))
                }
              />
            </label>

            <label>
              Hasta
              <input
                type="date"
                value={filters.dates?.split(',')[1] ?? ''}
                onChange={(event) =>
                  setFilters((current) => ({
                    ...current,
                    dates: current.dates?.split(',')[0]
                      ? `${current.dates.split(',')[0]},${event.target.value}`
                      : event.target.value || undefined,
                  }))
                }
              />
            </label>

            <label>
              Metacritic
              <input
                value={filters.metacritic ?? ''}
                onChange={(event) => setFilters((current) => ({ ...current, metacritic: event.target.value }))}
                placeholder="80,100"
              />
            </label>

            <label>
              Ordenar por
              <select
                value={filters.ordering ?? '-rating'}
                onChange={(event) => setFilters((current) => ({ ...current, ordering: event.target.value }))}
              >
                <option value="-rating">Mejor valoración</option>
                <option value="-metacritic">Mejor Metacritic</option>
                <option value="-released">Más recientes</option>
                <option value="released">Más antiguos</option>
                <option value="name">Nombre A-Z</option>
              </select>
            </label>

            <label>
              <span>Preciso</span>
              <input
                type="checkbox"
                checked={Boolean(filters.search_precise)}
                onChange={(event) => setFilters((current) => ({ ...current, search_precise: event.target.checked }))}
              />
            </label>

            <label>
              <span>Exacto</span>
              <input
                type="checkbox"
                checked={Boolean(filters.search_exact)}
                onChange={(event) => setFilters((current) => ({ ...current, search_exact: event.target.checked }))}
              />
            </label>

            <button type="button" onClick={() => void loadRawgGames(search)}>
              Aplicar filtros
            </button>
          </div>
        </section>

        {errorMessage ? <div className="alert card">{errorMessage}</div> : null}

        <section className="grid-section">
          <div className="section-header">
            <div>
              <p className="eyebrow">Inventario local</p>
              <h2>Gestión de laboratorio</h2>
            </div>
            <button
              className="ghost-button"
              type="button"
              onClick={() => void loadLocalGames()}
            >
              Recargar inventario
            </button>
          </div>

          <div className="inventory-grid">
            <form className="card inventory-form" onSubmit={handleCreateGame}>
              <h3>Registrar juego</h3>
              <label>
                Título
                <input
                  value={form.title}
                  onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))}
                  placeholder="Neon Run"
                  required
                />
              </label>
              <label>
                Género
                <input
                  value={form.genre}
                  onChange={(event) => setForm((current) => ({ ...current, genre: event.target.value }))}
                  placeholder="Arcade 2D"
                  required
                />
              </label>
              <label>
                Stock
                <input
                  type="number"
                  min="0"
                  step="1"
                  value={form.stock}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, stock: Number(event.target.value) }))
                  }
                  required
                />
              </label>
              <button type="submit" disabled={submitting}>
                {submitting ? 'Guardando...' : 'Crear juego'}
              </button>
            </form>

            <div className="card inventory-list">
              <div className="section-header compact">
                <h3>Catálogo local</h3>
                <span>{loadingLocal ? 'Cargando...' : `${localGames.length} registros`}</span>
              </div>

              <div className="list-stack">
                {localGames.map((game) => (
                  <article className={`inventory-item${selectedLocalId === game.id ? ' is-selected' : ''}`} key={game.id}>
                    <div>
                      <h4>{game.title}</h4>
                      <p>{game.genre}</p>
                    </div>
                    <div className="inventory-meta">
                      <span>Stock: {game.stock}</span>
                      <div className="button-row">
                        <button
                          type="button"
                          className="ghost-button"
                          onClick={() => {
                            setSelectedLocalId(game.id);
                            setSelectedSource('local');
                          }}
                        >
                          Ver ficha
                        </button>
                        <button
                          type="button"
                          onClick={() => void handleStockChange(game.id, -5)}
                          disabled={updatingId === game.id}
                        >
                          -5
                        </button>
                        <button
                          type="button"
                          onClick={() => void handleStockChange(game.id, 5)}
                          disabled={updatingId === game.id}
                        >
                          +5
                        </button>
                      </div>
                    </div>
                  </article>
                ))}

                {!loadingLocal && localGames.length === 0 ? (
                  <p className="empty-state">Aún no hay títulos cargados en el inventario local.</p>
                ) : null}
              </div>
            </div>
          </div>
        </section>

        <section className="grid-section">
          <div className="section-header">
            <div>
              <p className="eyebrow">RAWG proxy</p>
              <h2>Juegos populares</h2>
            </div>
            <span className="muted">{loadingRawg ? 'Actualizando vitrina...' : 'Resultados listos'}</span>
          </div>

          <div className="rawg-grid">
            {rawgGames.map((game) => {
              const genreLabel = game.genres?.[0]?.name ?? 'Sin género';
              return (
                <article className={`card rawg-card${selectedRawgId === game.id ? ' is-selected' : ''}`} key={game.id}>
                  <div className="rawg-image-wrap">
                    {game.background_image ? (
                      <img src={game.background_image} alt={game.name} />
                    ) : (
                      <div className="placeholder-image">RAWG</div>
                    )}
                  </div>
                  <div className="rawg-content">
                    <div className="rawg-title-row">
                      <h3>{game.name}</h3>
                      <span>{game.rating.toFixed(1)}</span>
                    </div>
                    <p>{genreLabel}</p>
                    <p>{game.released ?? 'Fecha no disponible'}</p>
                    <button type="button" className="ghost-button detail-button" onClick={() => {
                      setSelectedRawgId(game.id);
                      setSelectedSource('rawg');
                    }}>
                      Ver detalle
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
