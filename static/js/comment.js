/*global console*/
var likeIcon = document.getElementById("like"),
    likeCounter = likeIcon.nextElementSibling,
    loveIcon = document.getElementById("love"),
    loveCounter = loveIcon.nextElementSibling,
    comment = document.getElementById("comment"),
    addComment = comment.nextElementSibling,
    commentsContainer = document.getElementById("comments-container"),
    commentCounter = document.getElementById("comment-counter");

likeIcon.addEventListener("click", function () {
    this.classList.toggle("like");
    var numberOfLikes = Number(likeCounter.textContent);
    if (this.classList.contains("like")) {
        numberOfLikes++;

        $.getJSON('/background_like', {
				  proglang: '1',
                  nID : window.location.toString().split('/')[4],
                  nTitle: document.querySelector(".headline").textContent,
				}, function(data) {
				  $("#result").text(data.result);
				});
        likeCounter.textContent = numberOfLikes;
    } else {
        numberOfLikes--;
        $.getJSON('/background_dislike', {
				  proglang: '0',
                  nID : window.location.toString().split('/')[4],
				}, function(data) {
				  $("#result").text(data.result);
				});
        likeCounter.textContent = numberOfLikes;
    }
});

loveIcon.addEventListener("click", function () {
    this.classList.toggle("love");
    var numberOfLoves = Number(loveCounter.textContent);
    if (this.classList.contains("love")) {
        numberOfLoves++;

        $.getJSON('/background_love', {
				  proglang: '1',
            nID : window.location.toString().split('/')[4],
                  nTitle: document.querySelector(".headline").textContent,
				}, function(data) {
				  $("#result").text(data.result);
				});

        loveCounter.textContent = numberOfLoves;
    } else {
        numberOfLoves--;

        $.getJSON('/background_hate', {
				  proglang: '0',
				}, function(data) {
				  $("#result").text(data.result);
				});

        loveCounter.textContent = numberOfLoves;
    }
});

addComment.addEventListener("click", function () {

     if(comment.value!="") {
    var numberOfComments = Number(commentCounter.textContent),
        date = new Date();
    numberOfComments++;
    commentCounter.textContent = numberOfComments;
    commentsContainer.style.display = "block";
    commentsContainer.innerHTML +=
        `<div>${comment.value}
            <span>${date.toLocaleTimeString()} - ${date.toLocaleDateString()}</span>
            <i class="fa fa-trash"></i>
         </div>`;
    comment.value = "";
    var deleteIcons = document.querySelectorAll(".container .comments div i");
    for (let i = 0; i < deleteIcons.length; i++) {
        deleteIcons[i].addEventListener("click", function () {
            this.parentElement.style.display = "none";
            numberOfComments--;
            commentCounter.textContent = numberOfComments;
        });
    }

         }
    else
        {
            alert("Please enter your comment");
        }
});