$(document).ready(function() {
    const stripekey = Stripe("{{ STRIPE_PUBLIC_KEY|safe }}")
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var checkoutButton = document.getElementById('checkout-button');
    checkoutButton.addEventListener("click", function() {
        fetch("{% url 'order:create_checkout_session' product.pk %}", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(function(response) {
            return response.json()
        })
        .then(function(session) {
            return stripe.redirectToCheckout({sessionId: session.id})
        })
        .then(function(result) {
            alert(result.error.message)
        })
    })
})