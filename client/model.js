class Model{
    
    getData = () => {
        return fetch('http://localhost:8081', {
            method: 'GET',
            mode: 'cors'
        }).then(data => data.json())
    }

    getMovieById = (id) => {
        return fetch(`http://localhost:8081/?movie=${id}`, {
            method: 'GET',
            mode: 'cors'
        }).then(data => data.json())

        return this.data.reviewList.filter((movie => {return movie.id == id}))[0];
    }

    addReviewToMovie = (id,review) => {
        const dataBody = {
            "id": id,
            "review": review
        }
        return fetch(`http://localhost:8081`, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin', 
            headers: {
                'Content-Type': 'text/plain',
            },
            body: JSON.stringify(dataBody), 
            }).then(data => {
                return data.json();
            })


        // this.data.reviewList.filter((movie => {return movie.id == id}))[0].reviews.push({"review":review, "rate":5})
        // return 5;
    }
}
