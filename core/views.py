from core.models import Post, Comment, Subscribed
from django.views.generic import ListView, DetailView, DeleteView, View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import CreateBlogPostForm, CommentForm, UpdatePostForm
from users.models import Account
from django.http import Http404, JsonResponse, HttpResponse

def homepage(request):
    posts = Post.objects.all()
    subs = Subscribed.objects.all()
    context = {
        "posts": posts,
        "subs": subs,
    }
    return render(request, "homepage.html", context)


def post_publish(request):
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

	context['form'] = form
	return render(request, "post_publish.html", context)

def post_view(request, id):
    template_name = 'post.html'
    post = get_object_or_404(Post, id=id)
    like = request.POST.get("like")
    dislike = request.POST.get("dislike")
    lk_reacted = post.user_like_react.all()
    dislk_reacted = post.user_dislike_react.all()

    if like == "1":
        if request.user in lk_reacted:
            post.lk_count -= 1
            post.user_like_react.remove(request.user)      
            post.save()
            return JsonResponse({'lk':post.lk_count, "userlk": "unreacted"})            
        else:    
            post.lk_count += 1
            post.user_like_react.add(request.user)      
            post.save()
            return JsonResponse({'lk': post.lk_count, "userlk": "reacted"})		        
    
    if dislike == "2":
        if request.user in dislk_reacted:
            post.dislk_count -= 1
            post.user_dislike_react.remove(request.user)      
            post.save()
            return JsonResponse({'dislk':post.dislk_count, "userdislk": "unreacted"})            
        else:    
            post.dislk_count += 1
            post.user_dislike_react.add(request.user)      
            post.save()
            return JsonResponse({'dislk': post.dislk_count, "userdislk": "reacted"})

    return render(request, template_name, {'post': post})		

def postdiscus(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(post=post)
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Post(text=post_text, author=request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
    context = {"post": post,"comments": comments}
    return render(request, "chatroom.html", context)

def edit_post(request, id):
	context = {}
	user = request.user

	if not user.is_authenticated:
		return redirect("must_auth")
	post = get_object_or_404(Post, id=id)

	if post.author != user:
		return HttpResponse('вы не являетесь автором этого поста')

	if request.POST:
		form = UpdatePostForm(request.POST or None, request.FILES or None, instance=post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			post = obj

	form = UpdatePostForm(
			initial = {
					"name": post.name,
					"body": post.body,
			}
		)
	context['form'] = form

	return render(request, 'edit_post.html', context)

def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.delete()
        return redirect("scses")

    context = {
        "post": post
    }
    return render(request, "post_confirm_delete.html", context)

def scses(request):
    return render(request, "scses.html", {})
