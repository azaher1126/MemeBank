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