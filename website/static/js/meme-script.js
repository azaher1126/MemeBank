function like(id) {
    var http = new XMLHttpRequest();
    var url = '/like';
    var params = 'id=' + id;
    http.open('POST', url, true);

    var redirected = undefined;
    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function () {//Call a function when the state changes.
        if (http.readyState == XMLHttpRequest.HEADERS_RECEIVED) {
            redirected = http.responseURL;
        }
        else if (!redirected && http.readyState == 4 && http.status == 200) {
            const response = JSON.parse(http.responseText)
          document.getElementById('like_count'+id).innerHTML = response['likes'];
          const heartElem = document.getElementById('heart'+id);
          if (response['liked'] && heartElem.classList.contains('far')) {
            heartElem.classList.remove('far');
            heartElem.classList.add('fas');
            document.getElementById('like_button'+id).setAttribute('onclick', 'unlike('+id+')');
          }
        } else {
            window.history.pushState('','', redirected);
            document.querySelector('html').innerHTML = http.responseText;
        }
    }
    http.send(params);
  }
  function unlike(id) {
    var http = new XMLHttpRequest();
    var url = '/unlike';
    var params = 'id=' + id;
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function () {//Call a function when the state changes.
      if (http.readyState == 4 && http.status == 200) {
        const response = JSON.parse(http.responseText)
        document.getElementById('like_count'+id).innerHTML = response['likes'];
        const heartElem = document.getElementById('heart'+id);
        if (!response['liked'] && heartElem.classList.contains('fas')) {
            heartElem.classList.remove('fas');
            heartElem.classList.add('far');
            document.getElementById('like_button'+id).setAttribute('onclick', 'like('+id+')');
          }
        } else if (http.responseText == 'Login') {
            document.innerHTML = http.responseText;
            return;
        }
    }
    http.send(params);
  }