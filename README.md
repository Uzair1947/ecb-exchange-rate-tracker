# ECB Exchange Rate Tracker

The ECB Exchange Rate Tracker is a serverless currency exchange tracking application built on AWS Lambda. It allows users to access up-to-date exchange rate information for various currencies provided by the European Central Bank (ECB). The application fetches exchange rates daily and stores them in a secure and scalable database for easy retrieval.

## Key Features

- **Current Exchange Rates:** Get real-time exchange rate information for a wide range of currencies.
- **Rate Change Tracking:** View the rate change compared to the previous day for each currency.
- **Serverless Architecture:** Leverage AWS Lambda and API Gateway for cost-effectiveness and scalability.
- **Data Storage:** Exchange rate data securely stored in AWS DynamoDB for reliability.
- **Automatic Updates:** Daily updates from the ECB for accurate and up-to-date rates.
- **Public API Endpoint:** User-friendly REST API for easy access to exchange rate information.

## Setup and Usage

Follow the instructions in the [Setup Guide](/docs/setup.md) to deploy the application to your AWS account. Once deployed, access the API endpoint to retrieve the latest exchange rate information and changes.

## Technologies Used

- AWS Lambda
- AWS API Gateway
- AWS DynamoDB
- Python
- Docker
- SAM (Serverless Application Model)

## Contributing

Contributions to this project are welcome. Please check the [Contributing Guidelines](/CONTRIBUTING.md) for details on how to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for more information.

## Disclaimer

The ECB Exchange Rate Tracker is an assessment and educational project. It relies on exchange rate data sourced from the European Central Bank (ECB) and is intended for non-commercial use only. The creators of this repository are not liable for any financial transactions or decisions made based on the data provided by this application.
