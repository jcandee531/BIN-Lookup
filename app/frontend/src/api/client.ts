export type Participant = { id: number; name: string };
export type Game = { id: number; date: string; opponent: string; home: number; status: string; season: string; double_points?: number };
export type Pick = { id: number; game_id: number; participant_id: number; player_id: number; player_name: string };
export type Standing = { id: number; name: string; points: number };
export type RosterPlayer = { id: number; name: string; position: string };

async function http<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const res = await fetch(input, { headers: { 'Content-Type': 'application/json' }, ...init });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export const api = {
  listParticipants: (): Promise<Participant[]> => http('/api/participants'),
  addParticipant: (name: string): Promise<Participant> => http('/api/participants', { method: 'POST', body: JSON.stringify({ name }) }),

  importSeason: (season: string): Promise<{ imported: number }> => http('/api/games/import', { method: 'POST', body: JSON.stringify({ season }) }),
  listGames: (): Promise<Game[]> => http('/api/games'),
  getUpcomingGame: (): Promise<Game | null> => http('/api/games/upcoming'),
  getDraftOrder: (gameId: number): Promise<number[]> => http(`/api/games/${gameId}/draft-order`),
  getRoster: (gameId: number): Promise<RosterPlayer[]> => http(`/api/games/${gameId}/roster`),

  listPicks: (gameId: number): Promise<Pick[]> => http(`/api/picks?gameId=${gameId}`),
  createPick: (gameId: number, participantId: number, playerId: number, playerName: string): Promise<{ id: number }> =>
    http('/api/picks', { method: 'POST', body: JSON.stringify({ gameId, participantId, playerId, playerName }) }),

  computeGame: (gameId: number): Promise<{ ok: boolean }> => http(`/api/games/${gameId}/compute`, { method: 'POST' }),
  standings: (): Promise<Standing[]> => http('/api/standings'),
};

