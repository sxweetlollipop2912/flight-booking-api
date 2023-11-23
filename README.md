# flight-booking-api

## Description
This API supports the following operations:

1. Get the list of all flight tickets for sale
2. Get details of a single flight ticket 
3. Login/register a user
4. Add a flight ticket to cart
5. Get the list of all tickets in cart
6. Move a ticket from cart to history (i.e. the ticket is purchased)
7. Get the list of all purchased tickets (i.e. history)
8. Get details of a ticket in cart or history

## Usage
### Run the API locally
```commandline
docker run -dp 0.0.0.0:80:80 sxweetlollipop2912/flight-booking-api
```
Then, test the API at http://localhost:80/docs#

### Flow
1. View available tickets: `GET /api/tickets`
2. Login/Register a user: `POST /api/login/access-token`
3. Add ticket to cart: `POST /api/items/`, set `has_purchased` to `false`
4. Move ticket from cart to history: `PUT /api/items/{id}`, set `has_purchased` to `true`
5. View cart: `GET /api/items/cart`
6. View history: `GET /api/items/history`