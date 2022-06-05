import { createComponent } from "@wp/js/component-factory.js";
import { Button } from "./buttons.js";

/**
 * @typedef IPaginatorClientProps
 * @property { import("api/kemono/api.js").IPagination } pagination
 * @property {(page: number) => Promise<number>} onPageChange
 */

/**
 * This paginator is rendered client-only,
 * therefore no need for initialization
 * off a DOM element.
 * @param {IPaginatorClientProps} props
 */
export function PaginatorClient({ pagination, onPageChange }) {
  const { current_page, limit, total_count, total_pages } = pagination;
  const isFirstPage = current_page === 1;
  const isLastPage = current_page === total_pages;
  const currentMin = (current_page - 1) * limit;
  const currentMax = isLastPage ? total_count : currentMin + limit;
  const info = `Viewing ${currentMin}-${currentMax} out of ${total_count} items.`;

  /**
   * @type {HTMLDivElement}
   */
  const component = createComponent("paginator-client");
  /**
   * @type {HTMLParagraphElement}
   */
  const infoElement = component.querySelector(".paginator-client__info");
  /**
   * @type {HTMLUListElement}
   */
  const pages = component.querySelector(".paginator-client__pages");
  /**
   * @type {HTMLLIElement[]}
   */
  const [first, prev, current, next, last] = Array.from(pages.children);

  infoElement.textContent = info;

  if (isFirstPage) {
    first.textContent = String(1);
  } else {
    const button = Button({ textContent: String(1) });
    first.appendChild(button);
  }

  if (current_page - 1 > 1) {
    const button = Button({ textContent: String(current_page - 1) });
    prev.appendChild(button);
  } else {
    prev.textContent = "...";
  }

  current.textContent = String(current_page);

  if (current_page + 1 < total_pages) {
    const button = Button({ textContent: String(current_page + 1) });
    next.appendChild(button);
  } else {
    next.textContent = "...";
  }

  if (isLastPage) {
    last.textContent = String(total_pages);
  } else {
    const button = Button({ textContent: String(total_pages) });
    last.appendChild(button);
  }

  return component;
}
