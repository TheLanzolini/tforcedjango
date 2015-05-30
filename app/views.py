"""
Definition of views.
"""

import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.facebook import FacebookOAuth2
from social.backends.twitter import TwitterOAuth
from social.backends.reddit import RedditOAuth2
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa
from app.models import Show, Episode, Channel
from app.decorators import render_to

from django.template import RequestContext
from datetime import datetime


def logout(request):
    """Logs out user """
    auth_logout(request)
    return redirect('/')

def context(**extra):
    return dict({
            'facebook_id': getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', None),
            'facebook_scope': ''.join(FacebookOAuth2.DEFAULT_SCOPE),
            'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
        }, **extra)


@render_to('auth.html')
def authtest(request, backend):
    """ Test authorize view """
    if not request.user.is_authenticated():
        return context()
    return redirect('done')

@login_required
@render_to('authtest.html')
def done(request, backend):
    """Login complete view, displays user data"""
    return context()

@login_required
@render_to('home.html')
def complete_profile(request, **kwargs):
    backend = request.session['partial_pipeline']['backend']
    return context(missing_data=True, backend=backend)

@render_to('home.html')
def require_email(request):
    backend = request.session['partial_pipeline']['backend']
    return context(email_required=True, backend=backend)

@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token' : requst.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype="application/json")



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance=RequestContext(request,
            {
                'title':'Home Page',
                'year':datetime.now().year,
            })
    )



def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance=RequestContext(request,
            {
                'title':'Contact',
                'message':'Your contact page.',
                'year':datetime.now().year,
            })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance=RequestContext(request,
            {
                'title':'About',
                'message':'Your application description page.',
                'year':datetime.now().year,
            })
    )

#this is bad we should just have the names aligned between the back and front end
def convert_show_name_to_db_format(show_name):
    if(show_name == "wards"):
        return "four wards"
    elif(show_name == "lcs"):
        return "lcs rundown"
    elif(show_name == "proper"):
        return "trinity force podcast"
    elif(show_name == "ozlol"):
         return "ozlol"
    return show_name


def filter(request):
    response_data={}
    if request.method != 'POST':
        response_data['result']='failure'
        return

    filterOn = request.POST.get('categoryToFilter')
    key = request.POST.get('dbKey')
    response_data['categoryToFilter']= filterOn
    if filterOn == "show":
        result=Show.objects.filter(title__exact=convert_show_name_to_db_format(key))
        if(len(result) > 0):
            result=result[0].episodes.all() 

    if filterOn == "title":
        result=Show.objects.filter(title__exact=convert_show_name_to_db_format(key))
        if(len(result) > 0):
            result=result[0].episodes.all() 
        result=Episode.objects.filter(title=key).episodes.all() 

    if filterOn == "no_filter":
        result=Episode.objects.all()
        
    output_dictionary=[]
    i = 0

    for contentInstance in list(result):
        content_type = type(contentInstance)
        if content_type is Episode:
            output_dictionary.append(convert_episode_entry_to_dict(contentInstance))
        i+=1
    response_data['output']=output_dictionary

    response_data['result']='success'
    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    '''
    This is the expected dictionary to return to the client
    {
      result['title'] = "This is a Tforce proper podcast episode",
      result['content'] = "This is the new website and here is the place an excerpt would go to show the general details of this post!",
      result['show'] = "proper",
      result['hosts'] = ["pwnophobia", "declawd", "daysuntold", "chirajaeden", "punchinjello"],
      result['tags'] = ["patch 5.2", "mechanics", "wave manipulation", "mailbag", "top lane", "dyrus"],
      result['category'] ="podcast",
      result['video_url'] = "http://youtu.be/8x1oHRd46QM",
      result['image_url'] = "http://imgur.com/gallery/eRcR1fQ",
      result['stitcher_url'] = "http://app.stitcher.com/splayer/f/27428/36930238",
      result['itunes_url'] = "https://itunes.apple.com/us/podcast/trinity-force-podcast-league/id485769640"
      result['featured'] = True
      result['date_published'] = "5/19/15"
    },
    '''
def convert_episode_entry_to_dict(episode):
    result = {}
    result['title'] = episode.title
    result['content'] = episode.author_text
    result['show'] = episode.parents[0].show.title
    result['hosts'] = [profile.User.username for profile in episode.members.all()]
    result['tags'] = [tag.name for tag in episode.tags.all()]
    result['category'] ="podcast"
    result['video_url'] = "video_url"
    result['image_url'] = "image_url"
    result['stitcher_url'] = episode.url
    result['itunes_url'] = episode.url
    result['featured'] = (episode.status == 3)
    result['date_published'] = date_time_to_string(episode.published)
    return result

def date_time_to_string(date_time):
    if(date_time is None):
        return ""
    return str(date_time.month) + "/" + str(date_time.day) + "/" + str(date_time.year)
