from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapingJob, CoinData
from .serializers import CoinDataSerializer
from .tasks import start_scraping_task

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data
        #print(coins)
        job = ScrapingJob.objects.create()
        start_scraping_task.delay(job.job_id, coins)
        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        job = ScrapingJob.objects.get(job_id=job_id)
        coins = CoinData.objects.filter(job=job)
        serializer = CoinDataSerializer(coins, many=True)

        data = {
            'job_id': job_id,
            'tasks': serializer.data
        }
        return Response(data)