document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        let url = this.getAttribute('href');
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        }).then(response => {
            if (response.ok) {
                alert('Item added to cart!');
            }
        });
    });
});