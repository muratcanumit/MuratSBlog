from celery.task import task
from blogArticles.models import Post
from PIL import Image


@task(ignore_result=True)
def resizePostImage(post_id):
    post = Post.objects.get(id=post_id)
    size = 128, 128
    name = str(post_id) + "_postimage.jpg"
    post = Post.objects.get(id=post_id)
    img = Image.open(post.post_image)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save('uploadedmedia/' + str(name), "JPEG")
    post.post_image = name
    post.save()
    return True
