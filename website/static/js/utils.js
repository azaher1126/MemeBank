/**
 * 
 * @param {*} callback - the function to call if delay has passed since last call 
 * @param {*} delay - delay to wait before allowing another call to callback
 * @returns a function with the throttle applied.
 */
export function throttle(callback, delay) {
  let lastCall = 0;
  return function (...args) {
    const now = new Date().getTime();
    if (now - lastCall >= delay) {
      lastCall = now;
      callback(...args);
    }
  };
}

/**
 * 
 * @param {HTMLElement} element - the element to check if is the viewport
 * @returns true if the element is in the viewport, false otherwise.
 */
export function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}