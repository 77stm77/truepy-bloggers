from django import forms
from core.models import Post
from core.models import Comment

class CreateBlogPostForm(forms.ModelForm):
	class Meta:
		model = Post
		body = 'body'
		fields = ['name', body, 'img_1', 'img_2', 'img_3', 'img_4', 'img_5']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class UpdatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['name', 'body',]

	def save(self, commit=True):
		post = self.instance
		post.name = self.cleaned_data['name']
		post.body = self.cleaned_data['body']

		if commit:
			post.save()
		return post
