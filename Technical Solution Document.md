# Technical Solution Document
The goal is to integrate my mini CRM with two existing applications used for OTA's sales and ﬁnance process.

Both applications integrate with REST API's.

## Overview

The CRM application will be the central hub for managing all customer records. The SA and PS applications will be responsible for managing client and invoice records respectively, but will rely on the CRM application for customer information.

# High-level considertations

## Syncing
Use a event-driven architecture with a message-broker like RabbitMQ, with event handlers to synchronize the data.

## Authentication
1) Use OAuth for token-based authentication. The CRM can act as the OAuth provider, where the SA and PS would be the clients.
The clients would register with the CRM app to get a client ID and client secret.

2) When a user in the SA or PS application needs to access data in the CRM application, the client would redirect the user to the CRM application's authorization endpoint. This endpoint would prompt the user to log in and authorize the client to access their data.

3) Once the user has authorized the client, the CRM application would generate an access token and send it back to the client. The access token would be a string that the client can use to authenticate with the CRM application's API.

4) The client would store the access token securely (e.g., in a database or encrypted file) and include it in each API request to the CRM application. The CRM application would verify the access token and grant or deny access based on the user's permissions.


### Backoff & Retry mechanism
A backoff and retry mechanism, could be useful if the SA or PS application sends too many requests to the CRM application's API in a short amount of time.

The CRM application could respond with an HTTP 429 status code (Too Many Requests) to indicate that the client should slow down. The SA or PS application could then wait a certain amount of time  and retry the request. This would prevent the client from overwhelming the CRM application's API and potentially causing performance issues.

The time-out should be increased each time up until a certain amount and the amount of total retries should be limited.