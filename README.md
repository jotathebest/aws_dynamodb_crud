# Porter Simple CRUD User

The following development is intended to show the abilities of AWS to create a simple CRUD Rest API using the Lambda
and chalice services

# Rest API

## User Schema

The user schema accepted for the requests is the following one:

```json
{
  "username": <username> [str, minimal length: 1, mandatory],
  "email": <email> [str, mandatory],
  "userId": <userId> [int, mandatory],
  "groupName": <groupName> [str, mandatory]
}
```

## Endpoints

Below the reader may find the relevant endpoints to consume the REST API. Bear in mind that all the requests' data 
should be sent as JSON type.

### Base Endpoint

The base endpoint is `https://43q597lncj.execute-api.us-east-2.amazonaws.com/api/`

### User Creation

```bash
POST /users/<user_id>
```

The user information must fit the user schema described previously.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "jose", "email": "test1@test.com", "userId": 1, "groupName": "Porter"}' "https://43q597lncj.execute-api.us-east-2.amazonaws.com/api//users/1"
```

*Response Upon Success*

status code: 201
```json
{"status":"ok","details":"user created"}
```

*Response errors status codes*

- 409: A request to an existing user
- 400: The userId in the JSON data does not fit with the one in the URL path or there is missing data to fit the user schema


### User Update

```bash
PUT /users/<user_id>
```

```bash
curl -X PUT -H "Content-Type: application/json" \
 -d '{"username": "jose", "email": "test2@test.com", "userId": 1, "groupName": "Porter"}' \
 "https://43q597lncj.execute-api.us-east-2.amazonaws.com/api/users/1"
```

*Response Upon Success*

status code: 200
```json
{"status":"ok","details":"user updated"}
```

*Response errors status codes*

- 409: A request to an existing user
- 400: The userId in the JSON data does not fit with the one in the URL path or there is missing data to fit the user schema
- 404: The userId does not exist


### User Retrieve

Retrieve the information from a user

```bash
GET /users/<user_id>
```

```bash
curl -X GET -H "Content-Type: application/json" "https://43q597lncj.execute-api.us-east-2.amazonaws.com/api/users/1"
```

*Response Upon Success*

status code: 200
```json
{
  "status":"ok",
  "details":"user retrieved properly",
  "user_data":[{"groupName":"Porter","username":"jose","email":"test1@test.com","userId":"1"}]
}
```

*Response errors status codes*

- 404: The userId does not exist

### User Delete

Deletes an existing user

```bash
DELETE /users/<user_id>
```

```bash
curl -X DELETE -H "Content-Type: application/json" "https://43q597lncj.execute-api.us-east-2.amazonaws.com/api/users/1"
```

*Response Upon Success*

status code: 204
```json
{
  "status":"ok",
  "details":"user deleted properly"
}
```

*Response errors status codes*

- 404: The userId does not exist

### Users with a common group

Obtains the list of usernames within the same group

```bash
GET /groups/<group_name>
```
*Response Upon Success*

status code: 200
```json
{"status":"ok","details":"group have members","users":[<username_1>, ..., <username_n>]}
```

*Response errors status codes*

- 404: The group does not exist

### Update Users' group in batch

Inserts the users in the list to the specified group from the url path 

```bash
PUT /groups/<group_name>
```

```bash
curl -X PUT -H "Content-Type: application/json" \
-d '{"users": [<username_1> , ... , <username_n>]}' "https://43q597lncj.execute-api.us-east-2.amazonaws.com/api/groups/<group_name>"
```

*Response Upon Success*

status code: 200
```json
{"status":"ok","details":"users' group updated"}
```

*Response errors status codes*

- 400: The users' list is empty
- 404: The group does not exist

### Delete Users in batch

Deletes the users within the same group 

```bash
DELETE /groups/<group_name>
```

```bash
curl -X DELETE "https://43q597lncj.execute-api.us-east-2.amazonaws.com/api/groups/<group_name>"
```

*Response Upon Success*

status code: 204
```json
{"status":"ok","details":"users deleted"}
```

*Response errors status codes*

- 404: The group does not exist or does not have members