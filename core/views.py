from core.models import Post, Comment, Subscribed, Like
from django.views.generic import ListView, DetailView, DeleteView, View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import CreateBlogPostForm, CommentForm, UpdatePostForm, CreateLikeForm
from users.models import Account

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
	template_name = "post.html"
	post = get_object_or_404(Post, id=id)
	comments = post.comments.all()
	new_comment = None
	new_like = None
	if request.method == "POST":
		like_form = CreateLikeForm(data=request.POST)
		comment_form = CommentForm(data=request.POST)
		if like_form.is_valid():
			new_like = like_form.save(commit=False)
			lk_author = Account.objects.filter(email=request.user.email).first()
			new_like.lk_author = lk_author
			new_like.lk_post = post
			new_like.save()
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			author = Account.objects.filter(email=request.user.email).first()
			new_comment.author = author
			new_comment.post = post
			new_comment.save
	
	else:
		like_form = CreateLikeForm(data=request.POST, files=request.FILES)
		comment_form = CommentForm(data=request.POST, files=request.FILES)		
	
	context = {'post': post, 'like_form': like_form, 'comment_form': comment_form, 'comments': comments}
	return render(request, template_name, context)


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
