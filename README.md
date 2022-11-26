# powerplant-coding-challenge
## Challenge accepted!

I would like to express my gratitude for this opportunity.


I deeply hope that this implementation of the challenge satisfies the requirements of the documentation.

The algorithm, with which the problem has been solved, is explained in the comments of the code (main.py).

#

## Built the solution

When all the files are in place, let's build the container image.

Go to the project directory (in where the Dockerfile is, containing app directory).
Build the proyect image:

```bash
docker build -t productionplan .
```

Run a container based on this image:

```bash
docker run -d --name container -p 8888:8888 productionplan
```
#
## POST

The HTTP POST request method is used to send data to the server or create or update a resource. The POST request is usually used when submitting an HTML form or when uploading data to a server. The HTTP POST request may or may not contain data. The data is sent to the server in the body of the POST request message. The Content-Type header indicates the data type in the body of the POST request, and the data length is indicated with the Content-Length HTTP header.



## curl usage

For sending data with POST and PUT requests, these are common `curl` options:

 * request type

   * `-X POST`

 * content type header

   * `-H "Content-Type: application/json"`
 
* data
 
  * json: `-d '{{"load": 910,"fuels":{"gas(euro/MWh)": 13.4,"kerosine(euro/MWh)": 50.8,"co2(euro/ton)": 20,"wind(%)": 60},}` or `-d @payload.json`
  
## Examples

### POST application/json

explicit:

    curl -d "param1=value1&param2=value2" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8080/productionplan

with a data file
 
    curl -d "payload1.json" -X POST http://localhost:8080/productionplan

