import { createComponent } from "@wp/js/component-factory.js";

/**
 * @typedef IPaginatorClientProps
 * @property { import("api/kemono/api.js").IPagination } pagination
 */

/**
 * This paginator is rendered client-only,
 * therefore no need for initialization
 * off a DOM element.
 * @param {IPaginatorClientProps} props
 */
export function PaginatorClient({ pagination }) {
  const { current_page, limit, total_count, total_pages } = pagination;
  const isFinalPage = current_page === total_pages;
  const currentMin = (current_page - 1) * limit;
  const currentMax = isFinalPage ? total_count : currentMin + limit;
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
  first.textContent = String(1);
  prev.textContent = String(current_page - 1 > 1 ? current_page - 1 : "...");
  current.textContent = String(current_page);
  next.textContent = String(current_page + 1 < total_pages ? current_page : "..");
  last.textContent = String(total_pages);

  return component;
}
