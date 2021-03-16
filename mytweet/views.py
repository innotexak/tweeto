from django.shortcuts import render, redirect
from  django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet
from django.utils.http import is_safe_url
from django.conf import settings
import random
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    
    return render(request, 'pages/home.html', status = 200)


@api_view(['POST']) #method expected of client
@permission_classes([IsAuthenticated])
def tweet_form_view(request, *args,**Kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception = True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    """
        Rest_framework view  
    """
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request,tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"Message": "You cannot delete this post!"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"Deleted successfully "}, status=200)
    

@api_view(["DELETE", "POST"])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    """
    id required
    The actions expected are like, unlike and retweet 
    """
    serializer = TweetActionSerializer(request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if data == "like":
            obj.likes.add(request.user)
        elif data == "unlike":
            obj.likes.remove(request.user)
        elif data == "retweet":
            #next TODO
            pass
        
    # if request.user in obj.likes.all():
    #     obj.likes.remove(request.user)
    # else:
    #     obj.likes.add(request.user)
    return Response({"Deleted successfully "}, status=200)
    

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
        Rest_framework view  
    """
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj= qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)




def tweet_list_view_pure(request, *args, **kwargs):
    
    """
        Pure django view 
    """
    qs = Tweet.objects.all()
    tweet_list =[x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure(request, tweet_id, *args, **kwargs):
    data={
        "id":tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content 
    except:
        data["message"]= "Not Found"
        status = 404
    return JsonResponse(data, status=status)
    data = request.POST or None
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid():
        serializer.save(user=request.user)



def tweet_form_view_pure(request, *args, **Kwargs):
    print(request.user or None)
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        data = form.save(commit=False)
        data.user = user
        data.save()
        if request.is_ajax():
            return JsonResponse(data.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'pages/tweet_form.html', context={"form":form})