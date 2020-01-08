from core.models import Post
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import CreateBlogPostForm, CommentForm, UpdatePostForm
from users.models import Account
from core.models import Comment

class homepage(ListView):
    model = Post
    template_name = 'homepage.html'
    ordering = ['-date_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.query = self.request.GET.get('q', "")
        if self.query:
            queryset = queryset.filter(name__contains=self.query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context

def post_publish(request):
	context = {}
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

	context['form'] = form

	return render(request, 'post_publish.html', context)

def post_view(request, id):
    template_name = 'post.html'
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            author = Account.objects.filter(email=request.user.email).first()
            new_comment.author = author
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

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
					"post_image": post.post_image,
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

def my_blog(request, id):
    posts = Entry.objects.filter(id=id)
    context = {
        "posts": posts
    }
    return render(request, "my_blog.html", context)    
