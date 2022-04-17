function followUser(userToFollow) {
    fetch("/follow-user/", {
        method: 'POST',
        body: JSON.stringify({'userToFollow': userToFollow}),
        headers: {'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN}
    })
    .then(response => {
        console.log(response);
    });
}

function saveItinerary(itinerary) {
    fetch("/save-itinerary/", {
        method: 'POST',
        body: JSON.stringify({'itinerary': itinerary}),
        headers: {'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN}
    })
    .then(response => {
        console.log(response);
    });
}