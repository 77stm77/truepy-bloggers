from core.models import Post, Comment, Subscribed
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import CreateBlogPostForm, CommentForm, UpdatePostForm
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
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()
        redirect("homepage")


	return render(request, 'post_publish.html', {"form" : form})

def post_view(request, id):
    template_name = 'post.html'
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    new_comment = None
    post_user_reaction = post.user_reaction.all()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            author = Account.objects.filter(email=request.user.email).first()
            new_comment.author = author
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm(data=request.POST, files=request.FILES)


    return render(request, template_name, {'post': post,'comments': comments, 'comment_form': comment_form})

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
    obj = get_object_or_404(Post, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('/')
    context = {
        "object": obj
    }
    return render(request, "post_confirm_delete.html", context)
