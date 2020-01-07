from django import forms
from core.models import Post
from core.models import Comment

class CreateBlogPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['name', 'body', 'post_image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class UpdatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['name', 'body', 'post_image']

	def save(self, commit=True):
		post = self.instance
		post.name = self.cleaned_data['name']
		post.body = self.cleaned_data['body']

		if self.cleaned_data['post_image']:
			post.post_image = self.cleaned_data['post_image']

		if commit:
			post.save()
		return post
