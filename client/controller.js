class Controller {
    constructor(){
        this.view = new View(this.getMovieById, this.addReviewToMovie);
        this.model = new Model();
    }



    getMovieById = (id) => {
        return this.model.getMovieById(id).then((movie) => {
            return movie;
        })
        // return this.model.getMovieById(id);
    }

    addReviewToMovie = (id,movie) => {
        return this.model.addReviewToMovie(id,movie).then((labelAndProb) => {
            return this.normalizedRate(labelAndProb.final_label, labelAndProb.final_prob);
        });
    }

    normalizedRate = (label,prob) => {
        if(label == 'POSITIVE'){
            return prob
        }else{
            return 1-prob;
        }
    }

    start = () => {
        this.model.getData().then((data) => {
            this.view.loadView(data);
        })   
    }
}