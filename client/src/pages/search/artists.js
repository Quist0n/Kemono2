import { kemonoAPI } from "@wp/api";
import { PaginatorClient, UserCard } from "@wp/components";
import { findFavouriteArtist } from "@wp/js/favorites";

/**
 * @typedef IState
 * @property {boolean} isLoading
 * @property {number} [currentPage]
 * @property {string} [service]
 * @property {string} [artist_name]
 */

/**
 * @typedef IRenderPageProps
 * @property {import("api/kemono/api.js").IArtistsAPIResponse["data"]} data
 * @property {HTMLUListElement} artistList
 * @property {IState} state
 */

/**
 * @param {HTMLElement} section
 */
export async function searchArtistsPage(section) {
  /**
   * @type {IState}
   */
  const state = {
    isLoading: false,
    currentPage: undefined,
    artist_name: undefined,
    service: undefined
  };
  /**
   * @type {HTMLFormElement}
   */
  const searchForm = document.forms["artist-search"];

  /**
   * @type {HTMLDivElement}
   */
  const cardList = section.querySelector(".card-list");
  /**
   * @type {HTMLUListElement}
   */
  const artistList = cardList.querySelector(".card-list__items");

  searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (state.isLoading) {
      return;
    }

    try {
      state.isLoading = true;

      /**
       * @type {HTMLFormElement}
       */
      const form = event.target;
      /**
       * @type {HTMLSelectElement}
       */
      const serviceSelect = form.elements["service"];
      const service = serviceSelect.value;

      /**
       * @type {HTMLInputElement}
       */
      const nameInput = form.elements["name"];
      const name = nameInput.value;

      /**
       * @type {import("api/kemono/api.js").IArtistsAPIResponse}
       */
      const { data } = await kemonoAPI.api.artists(state.currentPage, service, name);
      state.service = service;
      state.artist_name = name;

      await renderPage({ data, artistList, state });
    } catch (error) {
      alert(error);
    } finally {
      state.isLoading = false;
    }
  });
}

/**
 * @param {IRenderPageProps} props
 */
async function renderPage({ data, artistList, state }) {
  const { artists, pagination } = data;
  const paginatorTop = PaginatorClient({
    pagination,
    onPageChange: async (page) => {
      if (state.isLoading) {
        return;
      }

      try {
        state.isLoading = true;
        /**
       * @type {import("api/kemono/api.js").IArtistsAPIResponse}
       */
        const { data } = await kemonoAPI.api.artists(page, state.service, state.artist_name);
        paginatorTop.remove();
        paginatorBottom.remove();
        renderPage({ data, artistList, state });
      } catch (error) {
        alert(error);
      } finally {
        state.isLoading = false;
      }
    }
  });
  const paginatorBottom = PaginatorClient({
    pagination,
    onPageChange: async (page) => {
      if (state.isLoading) {
        return;
      }

      try {
        state.isLoading = true;
        /**
         * @type {import("api/kemono/api.js").IArtistsAPIResponse}
         */
        const { data } = await kemonoAPI.api.artists(page, state.service, state.artist_name);
        paginatorTop.remove();
        paginatorBottom.remove();
        const { left, top } = artistList.getBoundingClientRect();
        scrollTo({ left, top });
        renderPage({ data, artistList, state });
      } catch (error) {
        alert(error);
      } finally {
        state.isLoading = false;
      }

    }
  });
  const artistCards = document.createDocumentFragment();

  for await (const artist of artists) {
    const card = UserCard(null, artist);
    const isFavArtist = await findFavouriteArtist(artist.id, artist.service);

    if (isFavArtist) {
      card.classList.add("user-card--fav");
    }

    artistCards.appendChild(card);
  }

  artistList.replaceChildren(artistCards);
  artistList.insertAdjacentElement("beforebegin", paginatorTop);
  artistList.insertAdjacentElement("afterend", paginatorBottom);
}
