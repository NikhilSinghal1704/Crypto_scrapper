# Crypto Scrapper 

This Django project scrapes cryptocurrency data through Selenium using Celery for parallel processing. 

## Project Setup 

### Requirements 

All the requirements can be found in `requirements.txt`.

### Installation 

Follow these steps to install and run the project:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/NikhilSinghal1704/Crypto_scrapper.git
    cd Crypto_scrapper
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Django server:**
    ```bash
    python manage.py runserver
    ```

5. **Start the Celery worker:**
    ```bash
    celery -A myproject worker --loglevel=info
    ```

## Models

- **ScrapingJob:** Stores the job ID and timestamp.
- **CoinData:** Stores the scraped data for each coin related to a ScrapingJob.

## Celery Tasks

- **start_scraping_task:** Initiates the scraping process for the provided list of coins.
- **scrape_coin:** Scrapes data for a single coin.

## Screenshots

![Admin](https://github.com/NikhilSinghal1704/Crypto_scrapper/blob/main/Screenshots/admin.png)
![Postman Scrapping Status](https://github.com/NikhilSinghal1704/Crypto_scrapper/blob/main/Screenshots/postman_scrapping_status.png)
![Postman Start Scrapping](https://github.com/NikhilSinghal1704/Crypto_scrapper/blob/main/Screenshots/postman_start_scrapping.png)