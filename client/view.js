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
            this.moviesList.append(`<li class='movieSelector' data-movie-id=${movie.id}>${movie.name}</a></li>`)
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

    loadReviews = (moviesData) => {
        this.movieSelector.on('click',(e) => {
            this.selectedMovieId = $(e.target).data('movieId');
            this.getMovieById(this.selectedMovieId).then((movie) => {
                this.loadReviewsToDom(movie.reviews)
            })
            // this.loadReviewsToDom(this.getMovieById(this.selectedMovieId).reviews);
        });   
    }

    addReviewEvent = () => {
        this.addReviewButton.on('click', (e) => {
            this.addReviewToMovie(this.selectedMovieId,this.newReview.value).then((prob) => {
                this.renderReview(this.newReview.value, parseInt(prob*10));
            });
        })
    }

    showUlWhenClick = () => {
        this.movieSelector.on('click', (e) => {
            this.moviesList.toggleClass('show-movies');
            this.moviesList.toggleClass('hide-movies');
        })
    }

    loadView = (moviesData) => {
        this.showUlWhenClick();
        this.addMoviesToList(moviesData);
        this.loadReviews(moviesData);
        this.addReviewEvent();
    }

}