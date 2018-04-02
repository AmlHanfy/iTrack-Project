from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Skill, Question, Answer
from django.core import serializers
from .utils import matrix
from django.views.decorators.csrf import csrf_protect

# Create your views here.
register_form = UserCreationForm()
login_form = AuthenticationForm()
context = {
    'register_form': register_form,
    'login_form': login_form
    }

def abet(request):
    from . import abet
    if request.method=='POST':
        answers_vector=request.POST['vector']
        best_subject=abet.get_track( answers_vector.split(','))
        #return render(request,'questionnaire/abet.html',{'subject':best_subject})
        context.update({'recommended':best_subject})
        return render(request, 'questionnaire/recommended.html', context)
    return render(request,'questionnaire/abet.html',context)

def welcome(request):
    return render(request,'questionnaire/welcome.html',context)

def index(request):
    return render(request, 'questionnaire/index.html', context)

def result(request):
    return render(request, 'questionnaire/result.html', context)


def question(request):
    global context
    question = Question.objects.order_by('pk').first()
    context.update({
        'question':question,
    })
    request.session['questions_meta'] ={
        'skills_vector':{
            'logic':0,
            'management':0,
            'interaction':0,
            'mechanical':0,
            'communication':0,
            'judment':0,
            'attention':0,
            'thinking':0,
        },
        'current_question_id':question.pk
    }
    return render(request, 'questionnaire/questions.html', context)
@csrf_protect
def question_fetch(request,answer = None):
    #get next object
    next_question = Question.objects.all().filter(pk__gt=request.session['questions_meta']['current_question_id']).order_by('pk')[0:1]
    next_question = Question.objects.get(pk=next_question[0].pk)
    # if(answer):
    #     pass
    # else:
    #     pass
    # json = [{'next_question' : Question.objects.all()}]
    # jsondata = serializers.serialize('json', next_question)
    return JsonResponse({'question':next_question.pk,'answers':serializers.serialize('json',next_question.answer_set.all())})
