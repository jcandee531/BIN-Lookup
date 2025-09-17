const axios = require("axios");
const dayjs = require("dayjs");

const RANGERS_TEAM_ID = 3;

async function fetchSeasonSchedule(season) {
  const url = `https://statsapi.web.nhl.com/api/v1/schedule?teamId=${RANGERS_TEAM_ID}&season=${season}`;
  const { data } = await axios.get(url);
  const dates = data.dates || [];
  const games = [];
  for (const d of dates) {
    for (const g of d.games) {
      const isRangersHome = g.teams.home.team.id === RANGERS_TEAM_ID;
      const opponentTeam = isRangersHome ? g.teams.away.team : g.teams.home.team;
      games.push({
        id: g.gamePk,
        date: dayjs(g.gameDate).toISOString(),
        opponent: opponentTeam.name,
        home: isRangersHome ? 1 : 0,
        status: g.status.detailedState,
        season
      });
    }
  }
  return games;
}

async function fetchGameFeed(gamePk) {
  const url = `https://statsapi.web.nhl.com/api/v1/game/${gamePk}/feed/live`;
  const { data } = await axios.get(url);
  return data;
}

function computeFirstScorerAndCounts(feed) {
  const allPlays = feed.liveData?.plays?.allPlays || [];
  let firstGoal = null;
  const counts = {};
  for (const play of allPlays) {
    if (play.result?.eventTypeId === 'GOAL') {
      const scorer = (play.players || []).find(p => p.playerType === 'Scorer');
      if (scorer) {
        const id = scorer.player?.id;
        const name = scorer.player?.fullName;
        if (id) {
          counts[id] = (counts[id] || 0) + 1;
          if (!firstGoal) {
            firstGoal = {
              player_id: id,
              player_name: name || '',
              team: play.team?.triCode || ''
            };
          }
        }
      }
    }
  }
  return { firstGoal, counts };
}

function extractRangersRosterFromFeed(feed) {
  const box = feed.liveData?.boxscore?.teams;
  if (!box) return [];
  const rangers = box.home?.team?.id === RANGERS_TEAM_ID ? box.home : box.away?.team?.id === RANGERS_TEAM_ID ? box.away : null;
  const teamBox = rangers ? (box.home?.team?.id === RANGERS_TEAM_ID ? feed.liveData.boxscore.teams.home : feed.liveData.boxscore.teams.away) : null;
  if (!teamBox) return [];
  const players = teamBox.players || {};
  const roster = [];
  for (const key of Object.keys(players)) {
    const p = players[key];
    roster.push({ id: p.person.id, name: p.person.fullName, position: p.position?.abbreviation || '' });
  }
  // Deduplicate by id
  const seen = new Set();
  return roster.filter(p => (seen.has(p.id) ? false : (seen.add(p.id), true)));
}

module.exports = { fetchSeasonSchedule, fetchGameFeed, computeFirstScorerAndCounts, extractRangersRosterFromFeed, RANGERS_TEAM_ID };

