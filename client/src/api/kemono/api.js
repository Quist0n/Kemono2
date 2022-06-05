import { KemonoError } from "@wp/utils";
import { kemonoFetch } from "./kemono-fetch";

export const api = {
  bans,
  bannedArtist,
  creators,
  logs,
  artists,
};

async function bans() {
  try {
    const response = await kemonoFetch('/api/bans', { method: "GET" });

    if (!response || !response.ok) {

      alert(new KemonoError(6));
      return null;
    }

    /**
     * @type {KemonoAPI.API.BanItem[]}
     */
    const banItems = await response.json();

    return banItems;

  } catch (error) {
    console.error(error);
  }
}

/**
 * @param {string} id
 * @param {string} service
 */
async function bannedArtist(id, service) {
  const params = new URLSearchParams([
    ["service", service],
  ]).toString();

  try {
    const response = await kemonoFetch(`/api/lookup/cache/${id}?${params}`);

    if (!response || !response.ok) {
      alert(new KemonoError(7));
      return null;
    }

    /**
     * @type {KemonoAPI.API.BannedArtist}
     */
    const artist = await response.json();

    return artist;

  } catch (error) {
    console.error(error);
  }
}

/**
 * @typedef IArtist
 * @property {string} id
 * @property {string} indexed
 * @property {string} name
 * @property {string} service
 * @property {string} updated
 */

/**
 * @param {number} [page]
 * @returns {IArtist[]}
 */
async function artists(page) {
  try {
    const url = page ? `/api/v1/artists/${page}` : "/api/v1/artists";
    const response = await kemonoFetch(url, { method: "GET" });
    if (!response || !response.ok) {

      alert(new KemonoError(8));
      return null;
    }

    const artists = await response.json();

    return artists;
  } catch (error) {

  }
}

async function creators() {
  try {
    const response = await kemonoFetch('/api/creators', { method: "GET" });

    if (!response || !response.ok) {

      alert(new KemonoError(8));
      return null;
    }

    /**
     * @type {KemonoAPI.Artist[]}
     */
    const artists = await response.json();

    return artists;

  } catch (error) {
    console.error(error);
  }
}

async function logs(importID) {
  try {
    const response = await kemonoFetch(`/api/logs/${importID}`, { method: "GET" });

    if (!response || !response.ok) {
      alert(new KemonoError(9));
      return null;
    }

    /**
     * @type {KemonoAPI.API.LogItem[]}
     */
    const logs = await response.json();

    return logs;

  } catch (error) {
    console.error(error);
  }
}
