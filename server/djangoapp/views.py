
import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .restapis import (
    get_request,
    analyze_review_sentiments,
    post_review
)

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else "/fetchDealers/" + state

    print("Endpoint:", endpoint)

    dealerships = get_request(endpoint)

    print("Received dealerships:", dealerships)

    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })
    print("Dealerships:", dealerships)

def get_dealer_details(request, dealer_id):
    endpoint = "/fetchDealer/" + str(dealer_id)
    dealer = get_request(endpoint)
    return JsonResponse(dealer, safe=False)


def get_dealer_reviews(request, dealer_id):
    endpoint = "/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)

    for review in reviews:
        try:
            sentiment = analyze_review_sentiments(review["review"])
            review["sentiment"] = sentiment["sentiment"]
        except Exception:
            review["sentiment"] = "Unavailable"

    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def login_request(request):
    if request.method != "POST":
        return JsonResponse({"status": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            return JsonResponse({
                "status": "Authenticated",
                "userName": user.username
            })

        return JsonResponse({
            "status": "Invalid",
            "message": "Invalid username or password"
        }, status=401)

    except Exception as error:
        print("Login error:", error)
        return JsonResponse({"status": "Error", "message": "Login failed"}, status=500)


@csrf_exempt
def register_request(request):
    if request.method != "POST":
        return JsonResponse({"status": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({
                "status": "Error",
                "message": "Username and password are required"
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": "Error",
                "message": "Username already exists"
            }, status=400)

        User.objects.create_user(username=username, password=password)

        return JsonResponse({
            "status": "Success",
            "message": "Registration successful"
        })

    except Exception as error:
        print("Registration error:", error)
        return JsonResponse({
            "status": "Error",
            "message": "Registration failed"
        }, status=500)


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "Invalid request method"}, status=405)

    if request.user.is_anonymous:
        return JsonResponse({
            "status": 403,
            "message": "Unauthorized. Please log in first."
        }, status=403)

    try:
        data = json.loads(request.body)
        post_review(data)
        return JsonResponse({"status": 200, "message": "Review posted successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"status": 400, "message": "Invalid JSON data"}, status=400)

    except Exception as error:
        print("Error posting review:", error)
        return JsonResponse({"status": 500, "message": "Error in posting review"}, status=500)


def analyze_review(request):
    if request.method == "POST":
        text = request.POST.get("review", "")
        sentiment = analyze_review_sentiments(text)
        return JsonResponse(sentiment, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)
