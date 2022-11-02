import typing
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Choice, Question
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


def _get_past_questions():
    now = timezone.now()
    return Question.objects.filter(pub_date__lte=now).order_by("-pub_date")


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return _get_past_questions()[:5]


class DetailView(generic.DetailView):
    template_name = "polls/detail.html"

    def get_queryset(self):
        return _get_past_questions()


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def json_detail(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return JsonResponse(model_to_dict(question))


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(
            pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Please select a choice",
            },
        )
    else:
        selected_choice.vote()

        return HttpResponseRedirect(reverse("polls:results", args=(question.pk,)))


def results(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
