import json
from django.shortcuts import render
from django.http import JsonResponse
from .restapis import get_request, analyze_review_sentiments, post_review


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    endpoint = "/fetchDealer/" + str(dealer_id)
    dealer = get_request(endpoint)
    return JsonResponse(dealer, safe=False)


def get_dealer_reviews(request, dealer_id):
    endpoint = "/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)

    for review in reviews:
        sentiment = analyze_review_sentiments(review["review"])
        review["sentiment"] = sentiment["sentiment"]

    return JsonResponse({"status": 200, "reviews": reviews})


def add_review(request):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


def analyze_review(request):
    if request.method == 'POST':
        text = request.POST.get('review', '')
        sentiment = analyze_review_sentiments(text)
        return JsonResponse(sentiment, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
