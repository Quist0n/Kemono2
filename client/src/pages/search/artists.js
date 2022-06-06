import { kemonoAPI } from "@wp/api";
import { PaginatorClient, UserCard } from "@wp/components";
import { findFavouriteArtist } from "@wp/js/favorites";

/**
 * @typedef IRenderPageProps
 * @property {import("api/kemono/api.js").IArtistsAPIResponse["data"]} data
 * @property {HTMLUListElement} artistList
 */

/**
 * @param {HTMLElement} section
 */
export async function searchArtistsPage(section) {
  /**
   * @type {import("api/kemono/api.js").IArtistsAPIResponse}
   */
  const { data } = await kemonoAPI.api.artists();
  /**
   * @type {HTMLDivElement}
   */
  const cardList = section.querySelector(".card-list");
  /**
   * @type {HTMLUListElement}
   */
  const artistList = cardList.querySelector(".card-list__items");

  await renderPage({ data, artistList });
}

/**
 * @param {IRenderPageProps} props
 */
async function renderPage({ data, artistList }) {
  const { artists, pagination } = data;
  const paginatorTop = PaginatorClient({
    pagination,
    onPageChange: async (page) => {
      /**
       * @type {import("api/kemono/api.js").IArtistsAPIResponse}
       */
      const { data } = await kemonoAPI.api.artists(page);
      paginatorTop.remove();
      paginatorBottom.remove();
      renderPage({ data, artistList });
    }
  });
  const paginatorBottom = PaginatorClient({
    pagination,
    onPageChange: async (page) => {
      /**
       * @type {import("api/kemono/api.js").IArtistsAPIResponse}
       */
      const { data } = await kemonoAPI.api.artists(page);
      paginatorTop.remove();
      paginatorBottom.remove();
      const { left, top } = artistList.getBoundingClientRect()
      scrollTo({ left, top })
      renderPage({ data, artistList });
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
