var form = document.getElementById('tweet_form');

function createTweetForm(event) {
  event.preventDefault();
  const myForm = event.target;
  const myFormData = new FormData(myForm);
  const url = myForm.getAttribute('action');
  const method = myForm.getAttribute('method');
  const xhr = new XMLHttpRequest();
  //     const responseType ="json"
  // xhr.responseType = responseType
  xhr.open(method, url);
  xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.onload = function () {
    if (xhr.status === 201) {
      const newTweet = xhr.response;
      const newTweetJson = JSON.parse(newTweet);
      const tweetedElement = formatTweetElements(newTweetJson);
      const ogHTML = tweetsContainer.innerHTML;
      tweetsContainer.innerHTML = tweetedElement + ogHTML;
      myForm.reset();
    } else if (xhr.status === 400) {
      const errorJson = xhr.response;
      console.log(errorJson);
    } else if ((xhr.status = 500)) {
      const errorJson = xhr.response;
      alert('There was a server error, please try again');
    }
  };
  xhr.onerror = function () {
    alert('An error occurred, please try again!');
  };
  xhr.send(myFormData);
}

form.addEventListener('submit', createTweetForm);
var tweetsContainer = document.getElementById('tweets');
function loadTweets(tweetsElements) {
  const xhr = new XMLHttpRequest();
  const method = 'GET';
  const url = '/tweets';
  const responseType = 'json';
  xhr.responseType = responseType;
  xhr.open(method, url, true);
  xhr.onload = function () {
    var jsonResponse = xhr.response;
    serverResponse = xhr.response;
    listedItems = serverResponse.response;
    var finalTweets = '';
    var i;
    for (i = 0; i < listedItems.length; i++) {
      var tweetObj = listedItems[i];
      var currentItem = formatTweetElements(tweetObj);

      finalTweets += currentItem;
    }
    tweetsElements.innerHTML = finalTweets;
  };
  xhr.send();
}

loadTweets(tweetsContainer);

function likeHandler(tweet_id, currentCount) {
  console.log(tweet_id, currentCount);
}
function likeBtn(tweet) {
  return "<button class='btn btn-primary btn-sm' onclick='likeHandler(" + tweet.id + ',' + tweet.likes + ")'>" + tweet.likes + ' Like' + '</button>';
}
function formatTweetElements(tweet) {
  var formatedTweet =
    "<div class='col-12 border mb-3' tweet_id='" +
    tweet.id +
    "'>" +
    "<p class='m-2 br-3'>" +
    tweet.content +
    '</p>' +
    "<p class='btn-group m-3'>" +
    likeBtn(tweet) +
    '</p>' +
    '</div>';
  return formatedTweet;
}
