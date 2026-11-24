from django.db import migrations,models
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[migrations.CreateModel(name='Ticket',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=200,verbose_name='Тақырып')),('description',models.TextField(verbose_name='Сипаттама')),('priority',models.CharField(choices=[('low','Төмен'),('normal','Орташа'),('high','Жоғары')],default='normal',max_length=20,verbose_name='Басымдық')),('status',models.CharField(default='Жаңа',max_length=20,verbose_name='Мәртебе'))])]
