# **Lamoda Parser Backend**

Backend system for parsing data from various sources.

## **Description**

The project uses pipenv, the application architecture is divided into a fastapi application and a worker, in which Kafka
consumers work

## **Technical Stack**

    - FastAPI
    - MongoDB
    - BeautifulSoup
    - Requests
    - Kafka
    - Docker/Docker Compose
    - Pipenv
    - Pydantic


# Lamoda Parsing Project

A comprehensive backend system for parsing data from various sources, including Lamoda and Twitch.

## Overview

This project combines several powerful features to create a robust data parsing pipeline:

1. **Lamoda Parsing**: Utilizes BeautifulSoup to scrape product information from Lamoda website
   - Handles various product pages and categories

2. **Twitch API Integration**: Uses requests to fetch data from Twitch API
   - Supports various Twitch API endpoints

3. **Asynchronous Operations**: Leverages asyncio for efficient handling of concurrent operations
   - Improves performance when dealing with multiple API calls or web scraping tasks

4. **Database Support**: Includes drivers for Redis and MongoDB for data storage and caching
   - Allows for flexible data persistence options

5. **Kafka Integration**: Supports publishing parsed data to Kafka topics for further processing

6. **FastAPI Backend**: Provides RESTful APIs for accessing parsed data
   - Offers automatic interactive documentation via Swagger UI

## Key Features

- User-friendly API documentation with Swagger UI
- Real-time data processing through Kafka integration
- Modular design allowing easy addition of new parsing sources
- Flexible data storage options with Redis and MongoDB support

