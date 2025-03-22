# QR Code Generator Telegram Bot

This project is a Telegram bot that generates QR codes from URLs sent by users. The bot validates the URLs and returns a QR code image.

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
    docker-compose up -d --build
    ```

## Usage - Docker Compose

1. Start the bot by running the Docker container:

    ```sh
    docker compose up -d --build
    ```

2. Open Telegram and send a message to your bot with a URL. The bot will respond with a QR code image.

## Usage - docker run
1. Build the image from Dockerfile:
    ```sh
    docker build -t qrcode_generator_bot .
    ```
2. Run the container with the environment variable:
    ```sh
    docker run --env TELEGRAM_TOKEN=your_secret_token -d qrcode_generator_bot
    ```
3. Open Telegram and send a message to your bot with a URL. The bot will respond with a QR code image.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.