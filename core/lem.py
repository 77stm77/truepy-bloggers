def post_view(request, id):
	template_name = 'post.html'
	post = get_object_or_404(Post, id=id)
	comments = post.comments.all()
	new_comment = None
	new_like = None
	if request.method == 'POST':
		like_form = CreateLikeForm(data=request.POST)
        comment_form = CommentForm(data=request.POST)
        if like_form.is_valid():
			new_like = like_form.save(commit=False)
			lk_author = Account.objects.filter(email=request.user.email).first()
			new_like.lk_author = lk_author
			new_like.lk_post = post
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			author = Account.objects.filter(email=request.user.email).first()
			new_comment.author = author
			new_comment.post = post
			new_comment.save()

	else:
		comment_form = CommentForm(data=request.POST, files=request.FILES)
		
	context = {'post': post,'comments': comments,'comment_form': comment_form}
	return render(request, template_name, context)