import { kemonoAPI } from "@wp/api";
import { PaginatorClient, UserCard } from "@wp/components";
import { findFavouriteArtist } from "@wp/js/favorites";

/**
 * @param {HTMLElement} section
 */
export async function searchArtistsPage(section) {
  const cardListElem = section.querySelector(".card-list");
  const cardList = cardListElem.querySelector(".card-list__items");
  /**
   * @type {import("api/kemono/api.js").IArtistsAPIResponse}
   */
  const { data: { artists, pagination } } = await kemonoAPI.api.artists();
  const paginatorTop = PaginatorClient({ pagination });
  const paginatorBottom = PaginatorClient({ pagination });
  const artistCards = document.createDocumentFragment();

  for await (const artist of artists) {
    const card = UserCard(null, artist);
    const isFavArtist = await findFavouriteArtist(artist.id, artist.service);

    if (isFavArtist) {
      card.classList.add("user-card--fav");
    }

    artistCards.appendChild(card);
  }

  cardList.appendChild(artistCards);
  cardList.insertAdjacentElement("beforebegin", paginatorTop)
  cardList.insertAdjacentElement("afterend", paginatorBottom)
}
