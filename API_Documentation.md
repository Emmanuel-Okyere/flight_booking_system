## Table of Contents
- [Table of Contents](#table-of-contents)
- [Registration](#registration)
  - [Request Information](#request-information)
  - [Header](#header)
  - [JSON Body](#json-body)
  - [Error Responses](#error-responses)
  - [Successful Response Example](#successful-response-example)
- [Verify Email](#verify-email)
  - [Request Information](#request-information-1)
  - [Header](#header-1)
  - [Params Body](#params-body)
  - [Error Responses](#error-responses-1)
  - [Successful Response Example](#successful-response-example-1)
- [Login](#login)
  - [Request Information](#request-information-2)
  - [Header](#header-2)
  - [JSON Body](#json-body-1)
  - [Error Responses](#error-responses-2)
  - [Successful Response Example](#successful-response-example-2)
- [Google Authentication](#google-authentication)
  - [Request Information](#request-information-3)
  - [Header](#header-3)
  - [JSON Body](#json-body-2)
  - [Error Responses](#error-responses-3)
  - [Successful Response Example](#successful-response-example-3)
- [Change Password](#change-password)
  - [Request Information](#request-information-4)
  - [Header](#header-4)
  - [JSON Body](#json-body-3)
  - [Error Responses](#error-responses-4)
  - [Successful Response Example](#successful-response-example-4)
- [Register Admin User](#register-admin-user)
  - [Request Information](#request-information-5)
  - [Header](#header-5)
  - [JSON Body](#json-body-4)
  - [Error Responses](#error-responses-5)
  - [Successful Response Example](#successful-response-example-5)
- [Reset Password](#reset-password)
  - [Request Information](#request-information-6)
  - [Header](#header-6)
  - [JSON Body](#json-body-5)
  - [Error Responses](#error-responses-6)
  - [Successful Response Example](#successful-response-example-6)
- [Verify Password Reset Link](#verify-password-reset-link)
  - [Request Information](#request-information-7)
  - [Header](#header-7)
  - [Params Body](#params-body-1)
  - [Error Responses](#error-responses-7)
  - [Successful Response Example](#successful-response-example-7)
- [Reset Forgotten Password](#reset-forgotten-password)
  - [Request Information](#request-information-8)
  - [Header](#header-8)
  - [JSON Body](#json-body-6)
  - [Error Responses](#error-responses-8)
  - [Successful Response Example](#successful-response-example-8)


<a name="registration"></a>

## Registration

The register API will accept user credentials:
first name, last name,username,phone number,email address and password and saves it to the database.

**Note** Until users verifies the email address using the link send to their email address provided during registrartion, they are not authenticated.

### Request Information

| Type | URL                 |
| ---- | ------------------- |
| POST | /accounts/register/ |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                   |
| ------------- | ------ | -------- | ----------------------------- |
| first_name    | String | false    | The first name of the user    |
| last_name     | String | false    | The last name of the user     |
| email_address | String | true     | email address of the user     |
| username      | String | true     | The username of the user      |
| phone_number  | String | false    | The phone number of the user  |
| password      | String | true     | Password for the user account |

### Error Responses

| Code | Message                                   |
| ---- | ----------------------------------------- |
| 400  | "users with this username already exists" |
| 400  | "users with this email already exists."   |
| 400  | "This field may not be blank."            |


### Successful Response Example

```
{
    "status": "sucess",
    "detail": "user created successfully",
    "data": {
        "first_name": "Emmanuel",
        "last_name": "Gyateng",
        "email_address": "emmanuel.gyaten@mail.com",
        "username": "EmmanuelGyateng"
    }
}
```
<a name="verify-email"></a>

## Verify Email
This endpoint is used to verify that verification emails are correct and not tempared with.

### Request Information

| Type | URL                     |
| ---- | ----------------------- |
| GET  | /accounts/verify-email/ |

### Header

| Type         | Property name |
| ------------ | ------------- |
| Allow        | GET, OPTIONS  |
| Content-Type | Param         |
| Vary         | Accept        |

### Params Body

| Property Name | type   | required | Description                          |
| ------------- | ------ | -------- | ------------------------------------ |
| iam           | string | true     | email address for user send the link |
| def           | string | true     | token sent to user to verify         |


### Error Responses

| Code | Message                               |
| ---- | ------------------------------------- |
| 400  | Link is invalid.                      |
| 404  | User with the email address not found |
| 403  | Email already verified                |

### Successful Response Example

```
{
    "status": "sucess",
    "detail": "email verified successful",
    "data": {
        "is_active": user.is_active
    }
}
```

<a name="login"></a>

## Login

This Api endpoint accepts user's email and password
and authenticates the user and return an access and refresh token.
The access token can be used by the user to authenticate their
identity.

**Note** If an account was registered by a manager and a password was generated, message would be returned requiring users who have not changed their generated password to do so. Until the generated password is changed, the user is not given access to the system.


### Request Information

| Type | URL              |
| ---- | ---------------- |
| POST | /accounts/login/ |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |


### JSON Body

| Property Name | type   | required | Description             |
| ------------- | ------ | -------- | ----------------------- |
| email_address | string | true     | email address for login |
| password      | string | true     | password for login      |

### Error Responses

| Code | Message                                |
| ---- | -------------------------------------- |
| 400  | email_address: This field is required. |
| 400  | password: This field is required.      |
| 401  | change password                        |

### Successful Response Example

```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1ODg3NTI4OCwiaWF0IjoxNjU4Nzg4ODg4LCJqdGkiOiIzZGFmODAzYmMzYzY0NTRmYTg5ZGNjMTAyMDgwMmQ2NSIsInVzZXJfaWQiOjh9.o4skxtda2LfgMBm2wQFZUGcR02xWr3oHY0HKFWNjoOc",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU4Nzg5MTg4LCJpYXQiOjE2NTg3ODg4ODgsImp0aSI6IjE1ZjZiYmEyMjVhODQyZGQ5ZDkzZDQyOTM2MDMwZDAyIiwidXNlcl9pZCI6OH0.UyBKDqydbWdpp-Pyvuq8uzZiMbOJz-YVOp-4u_7jxhw",
    "data": {
        "first_name": "Ernest",
        "last_name": "Nkrumah",
        "username": "ErnestNkrumah",
        "email_address": "engyateng@st.ug.edu.gh",
        "phone_number": null,
        "is_admin": true,
        "is_superuser": false
    }
}
```



<a name="google-authentication"></a>

## Google Authentication

This Api endpoint accepts token and authenticate users with google OAuth2.

**Note** This endpoint accepts only token generated after access is given by the user from OAuth 2.0.


### Request Information

| Type | URL               |
| ---- | ----------------- |
| POST | /accounts/google/ |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |


### JSON Body

| Property Name | type   | required | Description                                        |
| ------------- | ------ | -------- | -------------------------------------------------- |
| token         | string | true     | auth token to be authenticated with google systems |


### Error Responses

| Code | Message         |
| ---- | --------------- |
| 400  | token:required  |
| 400  | invalid token   |
| 400  | invalid expired |
| 408  | request timeout |

### Successful Response Example
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1ODg3NTkzMSwiaWF0IjoxNjU4Nzg5NTMxLCJqdGkiOiIyMjUyMzE1MDNmNjQ0ODllODY0YTlkMTVkMDcwYmZkZiIsInVzZXJfaWQiOjE2fQ.MjkC2G2k7H3DhKQWCaDhXc72WmbINeFdQ4fenPg401k",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU4Nzg5ODMxLCJpYXQiOjE2NTg3ODk1MzEsImp0aSI6IjE2NGQyOTcwZWVkMTRjZTk5OTNiNjIyMTMzODIyOTNjIiwidXNlcl9pZCI6MTZ9.esvK76dw9HA5UOFVWqmav9yYSgJ4AZXSNxu-y3Meu5o",
    "data": {
        "first_name": "Irene",
        "last_name": "Baidoo",
        "username": "IreneBaidoo",
        "email_address": "irene.banasko.baidoo@gmail.com",
        "phone_number": null,
        "is_admin": false,
        "is_superuser": false
    }
}
```
<a name="change-password"></a>

## Change Password

This endpoint allows user to change their password as they wish. They must be authenticated first before they can change their password.


### Request Information
| Type  | URL                        |
| ----- | -------------------------- |
| PATCH | /accounts/change-password/ |

### Header

| Type          | Property name         |
| ------------- | --------------------- |
| Allow         | PATCH                 |
| Content-Type  | application/json      |
| Authorization | Bearer {TOKEN.access} |

### JSON Body

| Property Name | type   | required | Description       |
| ------------- | ------ | -------- | ----------------- |
| old_password  | string | true     | old user Password |
| new_password  | string | true     | new User Password |

### Error Responses

| Code | Message                               |
| ---- | ------------------------------------- |
| 400  | Wrong old password                    |
| 401  | UNAUTHORIZED                          |
| 400  | BAD REQUEST                           |
| 400  | new_password: This field is required. |
| 400  | old_password: This field is required. |

### Successful Response Example
```
{
    "status": "success",
    "detail": "Password changed successfully",
    "data": {
        "username": "ErnestNkrumah",
        "email_address": "engyateng@st.ug.edu.gh",
        "is_admin": true,
        "is_superuser": false
    }
}
```
<a name="register-admin-user"></a>

## Register Admin User

This API endpoint is used to create admin users. Upon creation, email is sent to the admin user with the credentials created by the manager.
**Note** Only authenticated, manager users can access this endpoint. Passwords are generated for registered admins and required to change upon login.


### Request Information

| Type | URL                       |
| ---- | ------------------------- |
| POST | /accounts/register-admin/ |
### Header

| Type          | Property name         |
| ------------- | --------------------- |
| Allow         | POST                  |
| Content-Type  | application/json      |
| Authorization | Bearer {TOKEN.access} |

### JSON Body

| Property Name | type   | required | Description                   |
| ------------- | ------ | -------- | ----------------------------- |
| first_name    | string | false    | Should be Users first name    |
| last_name     | string | false    | Should be Users last name     |
| username      | string | false    | Should be Users username      |
| email_address | string | false    | Should be Users email address |

### Error Responses

| Code | Message        |
| ---- | -------------- |
| 400  | email required |
| 400  | BAD REQUEST    |
| 401  | UNAUTHORIZED   |
| 403  | FORBIDDEN      |

### Successful Response Example

```
{
    "status": "success",
    "detail": "Admin registered successfully",
    "data": {
        "first_name": "Ernest",
        "last_name": "Nkrumah",
        "username": "ErnestNkrumah",
        "email_address": "engyateng@st.ug.edu.gh"
    }
}
```


<a name="reset-password"></a>

## Reset Password

This API will let users forget their password by requesting for a password reset link with their email, registered with the account.

### Request Information

| Type | URL                       |
| ---- | ------------------------- |
| POST | /accounts/reset-password/ |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                   |
| ------------- | ------ | -------- | ----------------------------- |
| email_address | String | false    | The email address of the user |


### Error Responses

| Code | Message                                |
| ---- | -------------------------------------- |
| 404  | "users with this email does not exist" |


### Successful Response Example

```
{
    "status": "sucess",
    "detail": "reset email sent"
}
```

<a name="verify-password-reset-link"></a>

## Verify Password Reset Link
This endpoint is used to verify that password reset emails are correct and not tempared with.

### Request Information

| Type | URL                               |
| ---- | --------------------------------- |
| GET  | /accounts/reset-password/confirm/ |

### Header

| Type         | Property name |
| ------------ | ------------- |
| Allow        | GET, OPTIONS  |
| Content-Type | Param         |
| Vary         | Accept        |

### Params Body

| Property Name | type   | required | Description                          |
| ------------- | ------ | -------- | ------------------------------------ |
| iam           | string | true     | email address for user send the link |
| def           | string | true     | token sent to user to verify         |


### Error Responses

| Code | Message                               |
| ---- | ------------------------------------- |
| 400  | Link is invalid.                      |
| 404  | User with the email address not found |
| 403  | Email already verified                |

### Successful Response Example

```
{
    "status": "sucess",
    "detail": "link verified successful",
    "data": {
        "email_address": "engyateng@st.ug.edu.gh"
    }
}
```


<a name="reset-forgotten-password"></a>

## Reset Forgotten Password

This api will allow users to reset their passwords.

### Request Information

| Type | URL                           |
| ---- | ----------------------------- |
| POST | /accounts/reset-password/done |

### Header

| Type         | Property name    |
| ------------ | ---------------- |
| Allow        | POST, OPTIONS    |
| Content-Type | application/json |
| Vary         | Accept           |

### JSON Body

| Property Name | type   | required | Description                                    |
| ------------- | ------ | -------- | ---------------------------------------------- |
| password      | String | true     | The new password of the user                   |
| email_address | String | true     | The email address of the user                  |
| token         | String | true     | The token sent to the user through thier email |


### Error Responses

| Code | Message         |
| ---- | --------------- |
| 404  | "Token Invalid" |


### Successful Response Example

```
{
    "status": "success",
    "detail": "Password reset successful"
}
```
