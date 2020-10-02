# Inventory Management API

This is an Django app which can be integrated to any project.

## Data to send must be in JSON format

All data must be sent in the key **"jsonData"**  

```json
{
    "jsonData": {
        "YourData": "ex data"
    }
}
```

Response will be in the key **"responseData"**.
if data sent is invalid **"responseData.isError"** would return true together with **"responseData.errorInfo"** to show the error information

```json
{
    "responseData": {
        "the response": "ok"
    }
}
```

## Product API

**"/product/create/"** creates a new product. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "name": "your product name",  // required
        "stock": 0,                   // required
        "barcode": 123534535,         // optional
        "description": "your desc",   // optional
        "supplier": 1                 // optional (Must be a supplier id)
    }
}
```

if you want to create multiple products you can pass **isMass: true** together with the list of product information to create. example below.

```json
{
    "jsonData": [
        {
            "name": "product 1",
            "stock": 2
        },
        {
            "name": "product 2",
            "stock": 3
        }
    ],
    "isMass": true
}
```

**"/product/update/"** updates a product. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "productId": 2,                   // required (It must be a product id)
        "productInfo": {
            "name": "your product name",  // required
            "stock": 0,                   // required
            "barcode": 123534535,         // optional
            "description": "your desc",   // optional
            "supplier": 1                 // optional (It must be a supplier id if provided)
        }
    }
}
```

**"/product/read/"** reads a product. Data to send format must be like the example below.

* request method = get

```json
{
    "jsonData": {
        "productId": 2      // required
    }
}
```

**"/product/delete/"** deletes a product. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "productId": 2      // required
    }
}
```

## Supplier API

**"/supplier/create/"** creates a new supplier. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "name": "your supplier name",       // required
        "mobile_number": 63912332123,       // optional
        "address": "some st. some stat",    // optional
        "email": "someemail@email.com",     // optional
    }
}
```

**"/supplier/update/"** updates a supplier. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "supplierId": 2,                        // required (It must be a supplier id)
        "supplierInfo": {
            "name": "your supplier name",       // required
            "mobile_number": 63901231233,       // optional
            "address": "some st. some state",   // optional
            "email": "supplier@email.com",      // optional
        }
    }
}
```

**"/supplier/read/"** reads a supplier. Data to send format must be like the example below.

* request method = get

```json
{
    "jsonData": {
        "supplierId": 2      // required
    }
}
```

**"/supplier/delete/"** deletes a supplier. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "supplierId": 2      // required
    }
}
```

## Transaction API

**"/transaction/create/"** creates a new transaction. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "product": 1,           // required (must be a product id)
        "stock": 100,           // required
        "note": "some note",    // optional
    }
}
```

**"/transaction/update/"** updates a transaction. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "transactionId": 2,                     // required (It must be a supplier id)
        "transactionInfo": {
            "product": 1,                       // required (must be a product id)
            "stock": -100,                      // required
            "note": "some update note",         // optional
        }
    }
}
```

if you changed the product id your can pass **return_stocks:True** to return the stocks to the previous product. example below.

```json
{
    "jsonData": {
        "transactionId": 2,             // required
        "transactionInfo": {
            "product": 2,               // required
            "stock": 200,               // required
            "note": "some note"         // optional
        },
        "return_stocks": true           // optional
    }
}
```

**"/transaction/read/"** reads a transaction. Data to send format must be like the example below.

* request method = get

```json
{
    "jsonData": {
        "transactionId": 2      // required
    }
}
```

**"/transaction/delete/"** deletes a supplier. Data to send format must be like the example below.

* request method = post

```json
{
    "jsonData": {
        "transactionId": 2       // required
    }
}
```

if you want to return the stocks on product on the transaction you can pass **return_stocks: true**. example below.

```json
{
    "jsonData": {
        "transactionId": 5,        // required
        "return_stocks": true      // optional
    }
}
```

## Query API

**"/query/model_to_query/"** This will query a specific model. Method must always be get. The response will be in the key **"responseData"**.

### Product Query

**/query/product/** queries a product. Data sent should be like the format below.

```json
{
    "jsonData": {
        "query": "to query",                        // the query
        "query_by": "name, stock, id, description", // can either be the four.
        "order_by": "name, stock, id, description", // can either be the four.
        "query_limit": 100,                         // default is 100.
        "order_type": "ascn or desc",               // default is ascn (ascending). choose between the two.
    }
}
```

### Supplier Query

**/query/supplier/** queries a supplier. Data sent should be like the format below.

```json
{
    "jsonData": {
        "query": "to query",                                        // the query
        "query_by": "name, email, id, address, mobile_number",      // can either be the five.
        "order_by": "name, email, id, address, mobile_number",      // can either be the five.
        "query_limit": 100,                                         // default is 100.
        "order_type": "ascn or desc",                               // default is ascn (ascending). choose between the two.
    }
}
```

### Transaction Query

**/query/transaction/** queries a transaction. Data send should be like the format below.

```json
{
    "jsonData": {
        "query": "to _query",
        "query_by": "name, email, id, address, mobile_number",      // can either be the five.
        "query_by_suffix": "range, icontains, gt, lt"               // default is icontains refer to django docs about query.
        "order_by": "name, email, id, address, mobile_number",      // can either be the five.
        "query_limit": 100,                                         // default is 100.
        "order_type": "ascn or desc",                               // default is ascn (ascending). Can either be the two
    }
}
```
