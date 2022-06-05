import { kemonoAPI } from "@wp/api";
import { UserCard } from "@wp/components";
import { findFavouriteArtist } from "@wp/js/favorites";

const pageLimit = 25;

/**
 * @param {HTMLElement} section
 */
export async function searchArtistsPage(section) {
  const cardListElem = section.querySelector(".card-list");
  const cardList = cardListElem.querySelector(".card-list__items");

  const artists = await kemonoAPI.api.artists();
  const fragment = document.createDocumentFragment();

  for await (const artist of artists) {
    const card = UserCard(null, artist);
    const isFavArtist = await findFavouriteArtist(artist.id, artist.service);

    if (isFavArtist) {
      card.classList.add("user-card--fav");
    }

    fragment.appendChild(card);
  }

  cardList.appendChild(artistCards);

}
