import { throttle, isInViewport } from "./utils.js";

let csrfToken = null;
let last_meme_id = null;
let all_memes_loaded = false;

document.addEventListener("DOMContentLoaded", () => {
    styleMemeUsernames();
    const memes_container = document.getElementById("memes");
    if (memes_container !== null) {
        last_meme_id = retrieveLastMemeId(memes_container);
        const scroll_handler = throttle(load_new_page, 100);
        memes_container.addEventListener("scroll", scroll_handler, {passive: true });
    }

    csrfToken = document.querySelector('meta[name=csrf-token]').content;

    const like_buttons = document.querySelectorAll(".like-button");
    for (const like_button of like_buttons) {
        like_button.addEventListener("click", toggleLike)
    }
});

function styleMemeUsernames() {
    const memesUsername = document.querySelectorAll("[data-username-color]");
    for (const element of memesUsername) {
        element.style.color = element.getAttribute('data-username-color');
    }
}

/**
@param {HTMLElement} memes_container - meme container
*/
function retrieveLastMemeId(memes_container) {
    if (memes_container.childElementCount === 0) {
        return null;
    }
    const new_last_meme_id = Array.from(memes_container.children).reduce((min, child) => {
        const value = parseInt(child.getAttribute('data-meme-id'));
        return !isNaN(value) && value < min ? value : min;
    }, Infinity);
    if (new_last_meme_id === Infinity) {
        throw new Error("The retrieval of the last meme ID has resulted in Infinity. This should not happen.");
    }
    return new_last_meme_id;
}

/**
 * 
 * @param {HTMLElement} parent - the parent element to check
 */
function isAllChildrenAlerts(parent) {
    for (const child of parent.children) {
        if (child.role !== "alert") {
            return false;
        }
    }
    return true;
}

async function toggleLike() {
    if (csrfToken === null) {
        throw new Error("The CSRF token is null! This should never happen.");
    }

    const memeId = parseInt(this.getAttribute("data-meme-id"));
    if (memeId === NaN) {
        throw new Error("The element that triggered this function does not have the 'data-meme-id property set correctly.'");
    }

    const requestData = new FormData();
    requestData.append('id', memeId);

    const response = await fetch('/api/toggleLike', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrfToken
        },
        body: requestData
    });

    if (response.status === 401) {
        window.location.assign("/login");
    }

    const responseContent = await response.text();
    const newDoc = new DOMParser().parseFromString(responseContent, "text/html");
    if (!response.ok) {
        if (!isAllChildrenAlerts(newDoc.body)) {
            throw new Error("The call to the toggleLike API did not complete successfully and returned an unexpected result.");
        }
        const messagesContainer = document.getElementById("messages-container");
        messagesContainer.innerHTML += responseContent;
        return;
    }

    const newButton = newDoc.body.firstChild;
    newButton.addEventListener("click", toggleLike);
    this.replaceWith(newButton);
}

function load_new_page() {
    if (all_memes_loaded === true) {
        return;
    }

    if (last_meme_id === null) {
        throw new Error("The infinite scroll load_new_page function was called while the last_meme_id is null. This should never happen.");
    }

    const meme = document.querySelector(`#memes [data-meme-id='${last_meme_id}']`)
    if (isInViewport(meme) === false) {
        return;
    }

    let url = window.location.pathname;
    if (window.location.search !== undefined && window.location.search !== '') {
        url += window.location.search + '&last_id=' + last_meme_id;
    } else {
        url += '?last_id=' + last_meme_id;
    }

    fetch(url).then((response) => {
        if (!response.ok) {
            all_memes_loaded = true;
            throw new Error(`Failed to load a new page of memes. Error: ${response.statusText}`)
        }
        return response.text()
    }).then((response) => {
        if (response.trim() === '') {
            all_memes_loaded = true;
            return;
        }
        const newDoc = new DOMParser().parseFromString(response, "text/html");
        last_meme_id = retrieveLastMemeId(newDoc.body);
        const memes = document.getElementById('memes');
        memes.innerHTML += response;
    });
}