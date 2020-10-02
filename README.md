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

* request method = post.

* **"name"** type: string, product name. (required)

* **"stock"** type: number, product stock. (required, default is 0)

* **"barcode"** type: string, product barcode. (optional)

* **"description"** type: string, product description. (optional)

* **"supplier"** type: number, product supplier id. (optional)

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

* **"jsonData"** type: list, list of product information. (required)
* **"isMass"** type: bool, set to true if creating multiple products. (optional)

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
* **"productId"** type: number, product id to update. (required)

* **"productInfo"** type: dict, updated product information.

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
* **"productId"** type: number, product id to be read. (required)

```json
{
    "jsonData": {
        "productId": 2      // required
    }
}
```

**"/product/delete/"** deletes a product. Data to send format must be like the example below.

* request method = post
* **"productId"** type: number, product id to be deleted. (required)

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

* **"name"** type: string, the suppliers name. (required)

* **"mobile_number"** type: number, the suppliers number. (optional)

* **"address"** type: string, the suppliers address. (optional)

* **"email"** type: string, the suppliers email. (optional)

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

* **"supplierId"** type: number, suppliers id to be updated. (required)

* **"supplierInfo"** type: dict, suppliers updated information.

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

* **"supplierId"** type: number, the suppliers id to be read.

```json
{
    "jsonData": {
        "supplierId": 2      // required
    }
}
```

**"/supplier/delete/"** deletes a supplier. Data to send format must be like the example below.

* request method = post

* **"supplierId"** type: number, the suppliers id to be deleted.

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

* **"product"** type: number, the product id in the transaction. (required)
* **"stock"** type: number, the stock in the supplier. (required)
* **"note"** type: string, note/description in the transaction. (optional)

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

* **"transactionId"** type: number, transaction id to be updated. (required)

* **"transactoinInfo"** type: dict, updated transaction information.

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

* **"return_stocks"** type: bool, true if you want to return stock from previous product. (optional)

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

* **"transactionId"** type: number, transaction id to be read. (required)

```json
{
    "jsonData": {
        "transactionId": 2      // required
    }
}
```

**"/transaction/delete/"** deletes a supplier. Data to send format must be like the example below.

* request method = post

* **"transcationId"** type: number, transaction id to be deleted. (required)

```json
{
    "jsonData": {
        "transactionId": 2       // required
    }
}
```

if you want to return the stocks on product on the transaction you can pass **return_stocks: true**. example below.
* **"return_stocks"** type: bool, set to true if you want to return the stocks of the product in the transaction.

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

* **"query"** type: string, the query. (optional if empty it will return all)

* **"query_by"** type: string, can be *name*, *description*, *id*, *stock*. (required)

* **"query_limit"** type: number, any number. (optional, default is 100)

* **"order_by"** type: string, can be *name*, *description*, *id*, *stock*. (required)

* **"order_type"** type: string, can be *ascn* or *desc*. (optional)

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

* **"query"** type: string, the query. (optional if empty it will return all)

* **"query_by"** type: string, can be *name*, *address*, *id*, *mobile_number*, *email*. (required)

* **"query_limit"** type: number, any number. (optional, default is 100)

* **"order_by"** type: string, can be *name*, *address*, *id*, *mobile_number*, *email*. (required)

* **"order_type"** type: string, can be *ascn* or *desc*. (optional)

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

* **"query"** type: string, the query. (optional if empty it will return all)

* **"query_by"** type: string, can be *id*, *note*, *product*, *stock*, *created_on*. (required)

* **"query_by_suffix"** type: string, can be *range*, *gt*, *lt*, *starts_with* etc. Refer to django docs about query. (optional, default is icontains)

* **"query_limit"** type: number, any number. (optional, default is 100)

* **"order_by"** type: string, can be *id*, *note*, *product*, *stock*, *created_on*. (required)

* **"order_type"** type: string, can be *ascn* or *desc*. (optional)

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
