## Table of Contents
- [Table of Contents](#table-of-contents)
- [Registration](#registration)
- [Authentication - Login](#authentication---login)
- [Authentication Google Users](#authentication-google-users)
- [Change Password - ChangePassword](#change-password---changepassword)


<a name="registration"></a>

## Registration

The register API will accept user credentials:
username,email and password and saves it to the database.


<a name="login"></a>

## Authentication - Login

This Api endpoint accepts user's email and password
and authenticates the user and return a token.
The token can be used by the user to authenticate their
identity.


<a name="google_user"></a>

## Authentication Google Users

This Api endpoint accepts auth_token and authenticate users with google.

**Note** This endpoint accepts only auth_token from OAuth 2.0.


<a name="ChangePassword"></a>

## Change Password - ChangePassword

The Reset Password API makes helps users
to create a new password after they have provided they have beign authenticated. User must login before accessing the change password endpoint.