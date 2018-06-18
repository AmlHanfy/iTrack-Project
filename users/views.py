'''
handles all the user registeration-authentication-profiling
'''
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from watch_course.models import Course


def current_profile(request):
	'''
	checks if the user is logged in, if he's logged in it redirects to his profile,
	if he's not logged in it redirects to the main page
	'''
	if not request.user.is_authenticated:
		return redirect('questionnaire:welcome')

	return redirect('user:profile',request.user.username)

def profile_view(request, username):
	'''
	updates the template context with the username, and displays his profile
	'''
	if not request.user.is_authenticated:
		return redirect('questionnaire:welcome')
	user = User.objects.get(username=username)
	context = {'user_profile':request.user.username == username,'profile':user,'current_course':user.profile.course}
	return render(request,'users/profile/profile.html', context)

def change_profile(request):
	# from PIL import Image
	# from django.core.files.images import ImageFile
	# im = Image.open(request.FILES.get('img_src'))
	# im = im.thumbnail((200,200), Image.ANTIALIAS)
	# # im = im.convert('RGB')
	# im = im.save('image.jpg')
	# im = ImageFile(im)
	user = request.user
	user.first_name = request.POST.get('first_name')
	user.last_name = request.POST.get('last_name')
	profile = user.profile
	profile.bio = request.POST.get('bio')
	if request.FILES.get('img_src') not None:
		profile.img_src = request.FILES.get('img_src')
	profile.save()
	user.save()
	return redirect('user:profile',request.user.username)

def change_security(request):
	user = request.user
	user.email = request.POST.get('email')
	if len(request.POST.get('password')) >6:
		user.set_password(request.POST.get('password'))
	user.save()
	login(request,user,backend='django.contrib.auth.backends.ModelBackend')
	return redirect('user:profile',user.username)
class SignupView(FormView):
	''' class-based view (Generic views)
	handles the user registeration, and initializes the course counter to 0
	'''
	template_name='users/register.html'
	form_class=UserCreationForm
	def form_valid(self,form):
		user=form.save()
		login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
		if 'result' in self.request.session:
			_course = Course.objects.get(title=self.request.session['result'])
			self.request.user.profile.course = _course
			self.request.user.profile.course_index=0
			self.request.user.profile.save()
			del self.request.session['result']
		return redirect('user:profile',user.username)

class LoginView(FormView):
	'''
    class-based view

    logs the user in if the information is correct
    '''
	template_name='users/login.html'
	form_class=AuthenticationForm
	def form_valid(self,form):
		user=form.get_user()
		login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
		return redirect('user:profile',user.username)


def logout_view(request):
	'''
    logs the user out
    '''
	logout(request)
	return redirect('questionnaire:welcome')
def setting(request):
	pass
