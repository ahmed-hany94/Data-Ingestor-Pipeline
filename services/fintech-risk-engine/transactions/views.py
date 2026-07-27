from datetime import datetime, timedelta, timezone
 
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
 
from .models import Transaction
from .risk_rules import RiskContext, RiskEngine
from .serializers import ScoreRequestSerializer, TransactionSerializer

VELOCITY_WINDOW_MINUTES = 10

risk_engine = RiskEngine()

class ScoreTransactionView(APIView):
    def post(self, request):
        serializer = ScoreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
 
        timestamp = data.get("timestamp") or datetime.now(timezone.utc)
        window_start = timestamp - timedelta(minutes=VELOCITY_WINDOW_MINUTES)
        recent_count = Transaction.objects.filter(
            account_id=data["account_id"],
            created_at__gte=window_start,
        ).count()
 
        context = RiskContext(
            amount=float(data["tx_amount"]),
            timestamp=timestamp,
            recent_transaction_count=recent_count,
        )
        score, reasons = risk_engine.score(context)
        level = RiskEngine.classify(score)
 
        transaction = Transaction.objects.create(
            account_id=data["account_id"],
            amount=data["tx_amount"],
            currency=data.get("currency", "USD"),
            raw_payload=request.data,
            risk_score=score,
            risk_level=level,
            reasons=reasons,
        )
 
        return Response(TransactionSerializer(transaction).data, status=201)

class TransactionListView(APIView):
    def get(self, request):
        limit = min(int(request.query_params.get("limit", 50)), 200)
        risk_level = request.query_params.get("risk_level")
 
        queryset = Transaction.objects.all()
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
 
        transactions = queryset[:limit]
        return Response(TransactionSerializer(transactions, many=True).data)

def healthz(request):
    return JsonResponse({"status": "ok"})
