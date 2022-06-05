import { createComponent } from "@wp/js/component-factory.js";

/**
 * @typedef IButtonProps
 */

/**
 * @param {Partial<HTMLButtonElement> & IButtonProps} props
 */
export function Button({ ...buttonProps }) {
  /**
   * @type {HTMLButtonElement}
   */
  const component = createComponent("button");

  Object.assign(component, buttonProps);

  return component;
}
