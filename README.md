# Torima Demo

A simple web application demonstrating how to integrate [Torima](https://github.com/ochanoco/torima), an Identity-Aware Proxy (IAP), into an existing application.

This demo uses a lightweight Flask-based bulletin board called **N-chan** to demonstrate user authentication and identification through Torima.

## Features

- User authentication via LINE Login
- Create, view, update, and delete posts
- User identification using the `X-Torima-UserID` header
- Post ownership checks for updates and deletions
- Easy deployment with Docker Compose

## Architecture

Torima acts as a reverse proxy, authenticating users before forwarding requests to the Flask application.

```text
Browser
   |
   v
Torima Proxy (:8080)
   |
   | Authentication via LINE Login
   | X-Torima-UserID
   v
Flask App (:5000)
   |
   v
N-chan
```

The application receives the authenticated user's ID through the `X-Torima-UserID` HTTP header provided by Torima.

## Prerequisites

- Docker 
- A LINE Login channel (Channel ID and Channel Secret)

You can create a LINE Login channel in the [LINE Developers Console](https://developers.line.biz/console/).

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ochanoco/torima-demo.git
cd torima-demo
```

### 2. Configure authentication

Copy the environment variable template:

```bash
cp proxy/secret.env.template proxy/secret.env
```

Edit `proxy/secret.env` and provide your LINE Login credentials:

```dotenv
TORIMA_CLIENT_ID=YOUR_CHANNEL_ID
TORIMA_CLIENT_SECRET=YOUR_CHANNEL_SECRET
```

Do not commit your credentials to version control.

### 3. Configure LINE Login

Register the following callback URL in the LINE Developers Console:

```text
https://<YOUR_DOMAIN>/torima/auth/callback
```

Replace `<YOUR_DOMAIN>` with your application's domain.

For local development, make sure your callback URL and authentication settings meet LINE Login's requirements.

### 4. Start the application

```bash
docker compose up --build -d
```

Open your browser and navigate to:

```text
http://localhost:8080
```

Note that a working LINE Login flow requires a correctly configured callback URL.

To view the logs:

```bash
docker compose logs -f
```

To stop the application:

```bash
docker compose down
```


## How Authentication Works

1. Torima authenticates the user via LINE Login.
2. Torima forwards the request to the Flask application with the `X-Torima-UserID` header.
3. The application hashes the user ID with a randomly generated application token.
4. The hashed ID is associated with each new post.
5. When a user attempts to update or delete a post, the application compares the current user's ID with the post owner's ID.

This demonstrates how applications can use Torima to identify authenticated users without implementing the login flow themselves.

## HTTPS Deployment

The repository includes `compose.prod.yml`, which provides an example HTTPS configuration using [https-portal](https://github.com/SteveLTN/https-portal).

Before deploying:

1. Replace `example.ochano.co` in `compose.prod.yml` with your domain.
2. Configure DNS and allow incoming traffic on ports 80 and 443.
3. Set the `scheme` in `proxy/config.yaml` to `https`.
4. Register the corresponding LINE Login callback URL.

Start the application with:

```bash
docker compose -f compose.prod.yml up --build -d
```

This is an example deployment configuration, not a production-ready setup.

## Limitations

**This project is intended for demonstration purposes only.**

- Posts are stored in memory and are lost when the application restarts.
- Post IDs are based on list indices and may change after deletion.
- The application generates a new hashing token on every startup.
- Shared-secret verification between Torima and Flask is not enabled.
- The current `skip_auth_list` includes `/post/0`, allowing that path to bypass proxy authentication.
- The application uses Flask's development server.

For production use, review the authentication configuration, authorization checks, data persistence, and deployment security.

**Do not expose the Flask application directly to the internet.** All external requests should pass through Torima.

## Related Projects

- [Torima](https://github.com/ochanoco/torima)
