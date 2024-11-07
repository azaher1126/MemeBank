function like(id) {
    const requestData = new FormData();
    requestData.append('id', id);

    fetch('/api/like', {
        method: 'POST',
        body: requestData,
    }).then((response) => {
        if (response.status === 401) {
            window.location.href = '/login?next=' + window.location.pathname + window.location.search;
        } else if (response.status != 200) {
            window.location.reload();
        } else {
            return response.json()
        }
    }).then((response) => {
        document.getElementById('like_count' + id).innerHTML = response['likes'];
        const heartElem = document.getElementById('heart' + id);
        if (response['liked'] && heartElem.classList.contains('far')) {
            heartElem.classList.remove('far');
            heartElem.classList.add('fas');
            document.getElementById('like_button' + id).setAttribute('onclick', 'unlike(' + id + ')');
        }
    });
}
function unlike(id) {
    const requestData = new FormData();
    requestData.append('id', id);

    fetch('/api/unlike', {
        method: 'POST',
        body: requestData,
    }).then((response) => {
        if (response.status === 401) {
            window.location.href = '/login?next=' + window.location.pathname + window.location.search;
        } else if (response.status != 200) {
            window.location.reload();
        } else {
            return response.json()
        }
    }).then((response) => {
        document.getElementById('like_count' + id).innerHTML = response['likes'];
        const heartElem = document.getElementById('heart' + id);
        if (!response['liked'] && heartElem.classList.contains('fas')) {
            heartElem.classList.remove('fas');
            heartElem.classList.add('far');
            document.getElementById('like_button' + id).setAttribute('onclick', 'like(' + id + ')');
        }
    });
}
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}
function load_new_page() {
    if (window.last_meme_id === undefined) {
        return;
    }
    const meme = document.getElementById('meme_' + window.last_meme_id);
    if (isInViewport(meme) === false) {
        return;
    }

    let url = window.location.pathname;
    if (window.location.search !== undefined && window.location.search !== '') {
        url += window.location.search + '&last_id=' + window.last_meme_id;
    } else {
        url += '?last_id=' + window.last_meme_id;
    }

    fetch(url).then((response) => {
        if (!response.ok) {
            last_meme_id = undefined;
            throw "Failed to load";
        }
        return response.text()
    }).then((response) => {
        if (response.trim() === '') {
            window.last_meme_id = undefined;
            return;
        }
        const newDoc = Document.parseHTMLUnsafe(response);
        const last_meme = Array.from(newDoc.getElementsByClassName('meme')).pop();
        window.last_meme_id = last_meme.id.substring(5)
        const memes = document.getElementById('memes');
        memes.innerHTML += response;
    });
}