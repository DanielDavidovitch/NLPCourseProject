class View{
    constructor(getMovieById, addReviewToMovie){
        this.moviesList = $('#movies-list');
        this.reviewList = $('#review_list');
        this.addReviewButton = $('#add-review');
        this.newReview = $('#new-review')[0];
        this.movieSelector = $('#movie-selector');

        this.getMovieById = getMovieById;
        this.addReviewToMovie = addReviewToMovie
    }

    addMoviesToList = (moviesData) => {
        moviesData.reviewList.forEach((movie, index) => {
            this.moviesList.append(`<option class='movieSelector' data-movie-id=${movie.id}>${movie.name}</option>`)
        })
        this.movieSelector = $('.movieSelector');
    }

    loadReviewsToDom = (reviews) => {
        this.reviewList.empty();
        reviews.forEach((review, index) => {
            this.renderReview(review.review, review.rate);
        })   
    }

    renderReview = (review,rate) => {
        this.reviewList.append(`<li class="${rate}">${review}</li>`);
    }

    loadReviews = () => {
        this.selectedMovieId = this.moviesList.find(':selected').data('movieId');
            this.getMovieById(this.selectedMovieId).then((movie) => {
                this.loadReviewsToDom(movie.reviews)
            })
    }

    loadReviewsEvent = () => {
        this.moviesList.on('change',(e) => {
            this.loadReviews();
        });   
    }

    addReviewEvent = () => {
        const opacity = $("#opacity-div");
        this.addReviewButton.on('click', (e) => {
            opacity.removeClass("displaynone");
            opacity.addClass('opacitypage');
            this.addReviewToMovie(this.selectedMovieId,this.newReview.value).then((prob) => {
                this.renderReview(this.newReview.value, parseInt(prob*10));
                opacity.removeClass("opacitypage");
                opacity.addClass('displaynone');
            });
        })
    }


    loadView = (moviesData) => {
        this.addMoviesToList(moviesData);
        this.loadReviews();
        this.loadReviewsEvent();
        this.addReviewEvent();
    }

}