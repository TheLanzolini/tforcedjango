# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from tforce.models import Choice, Poll


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'tforce/detail.html', {
                'poll': p,
                'error_message': 'You didn\'t select a choice.'
            })

    else:
        selected_choice.votes += 1
        selected_choice.save()

        #Always return an HttpResponseRedirect after successfully dealing with
        # POST data. This prevents data from being posted twice if a user hits
        # the Back button

        return HttpResponseRedirect('polls:results', args=(p.id),)
