from celery import shared_task, group
from .models import ScrapingJob, CoinData
from .utils import CoinMarketCap

@shared_task
def scrape_coin(job_id, coin):
    try:
        job = ScrapingJob.objects.get(job_id=job_id)
        coin_scraper = CoinMarketCap(coin)
        data = coin_scraper.fetch_data()
        CoinData.objects.create(job=job, coin=coin, output=data)
        return f"Successfully scraped data for {coin}"
    except Exception as e:
        return f"Failed to scrape data for {coin}: {str(e)}"

@shared_task
def start_scraping_task(job_id, coins):
    tasks = [scrape_coin.s(job_id, coin) for coin in coins]
    job = group(tasks).apply_async()
    return job.id

@shared_task
def debug_task():
    return "Celery is connected!"
