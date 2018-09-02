1. 首先我们使用了 `redirect` 函数。
这个函数位于 `django.shortcuts` 模块中，它的作用是对 HTTP 请求进行重定向（即用户访问的是某个 URL，但由于某些原因，服务器会将用户重定向到另外的 URL）。
`redirect` 既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数（例如这里的 post）。如果接收一个模型的实例，那么这个实例必须实现了`get_absolute_url` 方法，这样 `redirect` 会根据 `get_absolute_url` 方法返回的 URL 值进行重定向。

2. 另外我们使用了 `post.comment_set.all()` 来获取 `post` 对应的全部评论。 
`Comment` 和`Post` 是通过 `ForeignKey` 关联的，回顾一下我们当初获取某个分类 cate 下的全部文章时的代码：`Post.objects.filter(category=cate)`。
这里 `post.comment_set.all()` 也等价于 `Comment.objects.filter(post=post)`，即根据 `post` 来过滤该 `post` 下的全部评论。
但既然我们已经有了一个 `Post` 模型的实例 `post`（它对应的是 `Post` 在数据库中的一条记录），那么获取和 `post` 关联的评论列表有一个简单方法，即调用它的 `xxx_set `属性来获取一个类似于 `objects` 的模型管理器，然后调用其 `all` 方法来返回这个 `post` 关联的全部评论。 
其中 `xxx_set` 中的 `xxx` 为关联模型的类名（小写）。例如 `Post.objects.filter(category=cate)` 也可以等价写为 `cate.post_set.all()`。
3. `{% url %}` 标签中是根据`view.py`下的方法名字或者`urls.py`中的路径名称进行解析
例如：`{% url 'blog:detail' hot_post.pk %}` 中，是根据`url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail')`里的`name`值找到这条url

**TODO:**
1. 添加评论和统计功能
6. 添加分页和文章内部上下文翻页
