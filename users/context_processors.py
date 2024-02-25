from users.models import Feedback
from users.utilities import fb_topics


def feedbacks(request):
    user = request.user
    fb_queryset = Feedback.objects.filter(from_user=user) if user.is_authenticated else []
    for fb in fb_queryset:
        try:
            fb.topic = fb_topics()[fb.topic][1]
        except IndexError:
            fb.topic = fb_topics()[0][1]  # 'другая'
    return {'feedbacks': fb_queryset}
