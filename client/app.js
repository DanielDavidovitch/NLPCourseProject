
const controller = new Controller();
controller.start();




// const addMoviesToList = (data) => {
//     const ul = $('#movies-list');
//     data.reviewList.forEach(function(movie, index){
//         ul.append(`<li id=${movie.name}><a href = "#"> ${movie.name} </a></li>`)
//     })
// }

// const showRewives = (reviews) => {
//     const ul = $('#review_list');
//     ul.empty();
//     reviews.forEach(function(review, index){
//         ul.append(`<li class="' + ${review.rate} + '">' ${review.review} + '</li>`);
//     })   
// }

// addMoviesToList(data);

// let reviews = "";
// $("li").click(function(e){
//     reviews = "";
//     movieName = e.target.innerHTML;
//     $('#movie-selector').text(movieName);
//     reviews = data.reviewList.filter((movie => {return movie.name == movieName}))[0].reviews
//     showRewives(reviews);

// })

