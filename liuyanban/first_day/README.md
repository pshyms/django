
1. 创建一个新项目后，新建一个应用程序
python manager.py startapp message


2. 在message同级目录下创建3个目录static, log, media，apps目录，
static：存放静态文件，包括js,css,图片等
log：存放网站日志文件
media：存放用户上传的图片等资源
apps: 用于应用过多时，都放于这个目录下，然后将apps目录右键mark成Source Root


3.  存放静态文件
将message_form.html文件放在templates文件夹下
在static目录下新建css目录，并在css目录下新建stylesheet格式的style文件，将message_form.html文件中的<style>标签内容剪切到style.css文件中，首尾<style>去掉，shift+tab使css格式整齐


4. 配置django连接mysql

    4.1 在setting.py大概80行找到DATABASES代码段，默认是sqlites，我们修改为mysql如下，库名要事先写好
    ![image](https://github.com/pshyms/django/blob/master/liuyanban/first_day/images-folder/mysql.png)

    4.2 安装pymysql模块：
    pip install pymysql
    python3 pymysql就是MySQLdb,基本使用方法：import pymysql as MySQLdb
    django 中使用方法，在项目djangostart目录里的__init__.py中加入
    import pymysql
    pymysql.install_as_MySQLdb()

    4.3执行python manage.py migrate 首次执行，生成项目需要的一些基本数据库





5. 配置message_form.html页面展示出来

    5.1 message/views.py中添加如下代码：
		
    ![image](https://github.com/pshyms/django/blob/master/liuyanban/first_day/images-folder/views.png)

    5.2 djangostart/urls.py中添加代码
		
	
    ![image](https://github.com/pshyms/django/blob/master/liuyanban/first_day/images-folder/urls.png)

    5.3  DjangoGetStarted/settings.py 57行左右修templates代码块中的DIRS为如下，来指定模板位置
    ![image](https://github.com/pshyms/django/blob/master/liuyanban/first_day/images-folder/DIRS.png)

    5.4 页面出来后，没css样式，原因是css文件没找到，这是因为在settings.py中我们只是指定了静态文件目录名
    ![image](https://github.com/pshyms/django/blob/master/liuyanban/first_day/images-folder/DIRS.png)

    5.5 但是没指定静态文件查找的跟路径，所以还需添加如下代码
		
    ![image](https://github.com/pshyms/django/blob/master/liuyanban/first_day/images-folder/STATICFILES_DIRS.png)





