from django.contrib import messages
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib import quote_plus
from django.utils import timezone
from django.db.models import Q

# Create your views here.

#CRUD stuff 
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		print form.cleaned_data.get("title")
		instance.save()
		#if sucesseed
		messages.success(request,"Sucessfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	#else:
	#	messages.error(request,"Problem occured while creation")
		
	#return HttpResponseRedirect(instance.get_absolute_url())

	#if request.method=="POST":
	#	print request.POST.get("content")
	#	print request.POST.get("title")
	context={
		"form":form,
	}
	return render(request,"post_form.html",context)

def post_detail(request, slug=None):#retrive
	#instance=Post.objects.get(id=11)
	today=timezone.now().date()
	instance = get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string=quote_plus(instance.content)
	context = {
		"title":instance.title,
		"instance":instance,
		"share_string":share_string,
		"today":today,
	}
	return render(request,"post_detail.html",context)

def post_list(request):
	today=timezone.now().date()
	queryset_list= Post.objects.active()#.filter(draft=False).filter(publish__lte=timezone.now())#.all()#.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list=Post.objects.all()
	
	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_request_var="page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context={
		"object_list":queryset,
		"title":"List ",
		"page_request_var":page_request_var,
		"today":today,
	}
	return render(request,"post_list.html",context)
	#if request.user.is_authenticated():
	#	context={
	#		"title": "auth user"
	#	}
	#else:
	#	context = {
	#		"title":"unauth user"
	#	}
	#return render(request,"index.html",context)
	#return HttpResponse("<h1>Hello list</h1>")





def post_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,slug=slug)
	form=PostForm(request.POST or None,request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user=request.user
		instance.save()
		messages.success(request,"<a href='#'>Saved Sucessfully</a>",extra_tags='html_safe')
		#message sucess
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title":instance.title,
		"instance":instance,
		"form":form,
	}

	return render(request,"post_form.html",context)
	#return HttpResponse("<h1>Hello update</h1>")

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,slug=slug)
	instance.delete()
	messages.success(request,"Sucessfully deleted")
	#message sucess
	return redirect("posts:list")