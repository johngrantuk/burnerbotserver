from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserDetail


def feed(request):
    """Gets the encrypted feed info. Also gets current Patron and Price of the feed from the smart contract."""
    # feed = Feed.objects.all()[0]

    # return render(request, 'feed.html', {'feed': feed, 'posts': posts, 'patron': patron, 'price': price_ether})
    return render(request, 'feed.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':                                                    # Confirm it is a POST

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body["username"]
        hash = body['hash']
        addressO = body['address']
        pk = body['privatekey']

        # If User already exists only update if hash is same
        # If hash not same then exit
        # If user doesn't exist then add but needs improvement - i.e. one time nonce

        user = UserDetail.objects.filter(username=username)
        if len(user) == 0:
            user = UserDetail(username=username, address=addressO, private_key=pk, hash=hash)
            user.save()
            responseData = {
                'status': 'user-added'
            }
        else:
            if user[0].hash == hash:
                user[0].address = addressO
                user[0].private_key = pk
                user[0].save()
                responseData = {
                    'status': 'user-updated'
                }
            else:
                responseData = {
                    'status': 'cheeky-monkey'
                }

        return JsonResponse(responseData)
    else:
        return HttpResponseNotFound()


def userInfo(request, username, hash):

    userinfo = UserDetail.objects.filter(username=username, hash=hash)

    if(len(userinfo) == 1):
        responseData = {
            'status': 'ok',
            'username': userinfo[0].username,
            'address': userinfo[0].address,
            'privatekey': userinfo[0].private_key
        }
    else:
        responseData = {
            'status': 'cheeky-monkey'
        }

    return JsonResponse(responseData)


def userAddress(request, username):

    print('Getting Address For User: ' + username)
    userinfo = UserDetail.objects.filter(username=username)

    if(len(userinfo) == 1):
        print('User Exists')
        responseData = {
            'status': 'ok',
            'username': userinfo[0].username,
            'address': userinfo[0].address
        }
    else:
        print('User Not Exists')
        responseData = {
            'status': 'no-user'
        }

    return JsonResponse(responseData)
