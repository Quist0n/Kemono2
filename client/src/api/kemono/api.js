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
 * @typedef IPagination
 * @property {number} total_count
 * @property {number} total_pages
 * @property {number} current_page
 * @property {number} limit
 */

/**
 * @typedef IArtist
 * @property {string} id
 * @property {string} indexed
 * @property {string} name
 * @property {string} service
 * @property {string} updated
 */

/**
 * @typedef IArtistsAPIBody
 * @property {IPagination} pagination
 * @property {IArtist[]} artists
 */

/**
 * @typedef IArtistsAPIResponse
 * @property {boolean} is_successful
 * @property {IArtistsAPIBody} data
 */

/**
 * @param {number} [page]
 * @param {string} [service]
 * @returns {Promise<IArtistsAPIResponse>}
 */
async function artists(page, service) {
  const path = page
    ? `/api/v1/artists/${page}`
    : "/api/v1/artists";

  const searchParams = new URLSearchParams();

  if (service) {
    searchParams.set("service", service);
  }

  const url = Array.from(searchParams.keys()).length
    ? `${path}?${searchParams.toString()}`
    : path;

  try {
    const response = await kemonoFetch(url, { method: "GET" });
    if (!response || !response.ok) {

      alert(new KemonoError(8));
      return null;
    }

    const apiResponse = await response.json();

    return apiResponse;
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
