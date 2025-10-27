const upvotes = document.querySelectorAll('.upvote');

    upvotes.forEach(el => {
        el.addEventListener('click', function(e) {
            e.preventDefault();
            let ideaId = this.id;
            let type = this.type;
            let url = "/" + type + "/" + ideaId + "/up";
            let cookie_name = type + "_" + ideaId + "_up";
            if (!(document.cookie.includes(cookie_name))) {
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}),
                })
                .then(response => response.json())
                .then(data => {
                    this.innerHTML = "<i class=\"fa-solid fa-thumbs-up text-success\"></i> "+data.upvote;
                    document.cookie = cookie_name+"=true; path=/; max-age=" + (365 * 24 * 60 * 60);
                });
            }
        });

    });


    const downvotes = document.querySelectorAll('.downvote');

    downvotes.forEach(el => {
        el.addEventListener('click', function(e) {
            e.preventDefault();
            let ideaId = this.id;
            let type = this.type;
            let url = "/" +type + "/" + ideaId + "/down";
            let cookie_name = type + "_" + ideaId + "_down";
            if (!(document.cookie.includes(cookie_name))) {
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}),
                })
                .then(response => response.json())
                .then(data => {
                    this.innerHTML = "<i class=\"fa-solid fa-thumbs-down text-danger\"></i> "+data.downvote;
                    document.cookie = cookie_name+"=true; path=/; max-age=" + (365 * 24 * 60 * 60);
                });
            }
        });

    });