# QR Code Generator Telegram Bot

This project is a Telegram bot that generates QR codes for URLs, WIFI auto-connection, visit card (vcard) and more sent by users. The bot validates the data and returns a QR code image.

Bot deployment is currently on [Northflank](https://northflank.com), you can pay a visit directly in Telegram accessing the [qrcodegen-bot](https://t.me/qrcode_generator_jpizquierdo_bot).

## Features

- Data validation using [Pydantic](https://github.com/pydantic/pydantic).
- QR code generation using the [`qrcode`](https://github.com/lincolnloop/python-qrcode) library.
- Asynchronous handling of Telegram messages, thanks [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) people.
- Future features: different kind of QR codes with inlinekeyboard guidance.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation
#### 📦 Pull the Image from Docker Hub
1. Pull the image from Docker Hub:
To get the latest version of `qrcodegen`, pull it from Docker Hub:  
    ```sh
    docker pull jpizquierdo/qrcodegen:latest
    ```
2. Run the container:
    ```sh
    docker run --env TELEGRAM_TOKEN=yourGodFatherFancyToken -d jpizquierdo/qrcodegen:latest
    ```
3. Or run the container with docker compose:

    Create a `.env` file with your Telegram bot token (check `.env.example`):

    ```env
    TELEGRAM_TOKEN="your_telegram_bot_token"
    ```
    Execute:
    ```sh
    docker compose up -d
    ```
#### Build the image yourself
1. Clone the repository:

    ```sh
    git clone https://github.com/jpizquierdo/qrcodegen.git
    cd qrcodegen
    ```

2. Create a `.env` file with your Telegram bot token (check `.env.example`):

    ```env
    TELEGRAM_TOKEN="your_telegram_bot_token"
    ```

3. Build and run the Docker containers:

    ```sh
    docker compose up -d --build
    ```

4. Open Telegram and send a message to your bot clicking in any button like a URL. The bot will respond with a QR code image.

#### Usage - docker run
If you prefer to use docker run sentence and build the image yourself follow the these steps:
1. Build the image from Dockerfile:
    ```sh
    docker build -t qrcode_generator_bot .
    ```
2. Run the container with the environment variable:
    ```sh
    docker run --env TELEGRAM_TOKEN=your_secret_token -d qrcode_generator_bot
    ```
3. Open Telegram and send a message to your bot clicking in any button like a URL. The bot will respond with a QR code image.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).