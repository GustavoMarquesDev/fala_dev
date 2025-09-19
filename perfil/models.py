from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

from utils import resize_image


class Perfil(models.Model):

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome',
        blank=False,
        null=False
    )
    sobrenome = models.CharField(
        max_length=100,
        verbose_name='Sobrenome',
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='Email',
        blank=False,
        null=False
    )
    profissao = models.CharField(
        max_length=100,
        verbose_name='Profissão',
        blank=False,
        null=False
    )
    foto = models.ImageField(
        upload_to='perfil/fotos/%Y/%m/%d',
        verbose_name='Foto de Perfil',
        blank=True, null=True,
        help_text='Foto de perfil a ser exibida para todos os usuários ')

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.foto:
            resize_image(self.foto)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'


class PerguntasDoUsuario(models.Model):

    class Meta:
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="perguntas")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(
        help_text='Selecione uma categoria para ajudar outros devs a encontrar sua pergunta.',
        blank=True,
        null=True,
        default=None,
        choices=(
            ('Javascript', 'Javascript'),
            ('Python', 'Python'),
            ('C#', 'C#'),
            ('HTML', 'HTML'),
            ('CSS', 'CSS'),
            ('Java', 'Java'),
            ('PHP', 'PHP'),
            ('C++', 'C++'),
            ('SQL', 'SQL'),
            ('Shell', 'Shell'),
            ('PowerShell', 'PowerShell'),
            ('Git', 'Git'),
            ('React', 'React'),
            ('Angular', 'Angular'),
            ('Vue', 'Vue'),
            ('NodeJS', 'NodeJS'),
            ('Express', 'Express'),
            ('MongoDB', 'MongoDB'),
            ('MySQL', 'MySQL'),
            ('PostgreSQL', 'PostgreSQL'),
            ('Firebase', 'Firebase'),
            ('AWS', 'AWS'),
            ('Azure', 'Azure'),
            ('Docker', 'Docker'),
            ('Kubernetes', 'Kubernetes'),
            ('Terraform', 'Terraform'),
            ('Ansible', 'Ansible'),
            ('Linux', 'Linux'),
            ('Windows', 'Windows'),
            ('MacOS', 'MacOS'),
            ('iOS', 'iOS'),
            ('Android', 'Android'),
            ('Flutter', 'Flutter'),
            ('Unity', 'Unity'),
            ('Unreal', 'Unreal'),
            ('Godot', 'Godot'),
            ('Blender', 'Blender'),
            ('Photoshop', 'Photoshop'),
            ('Illustrator', 'Illustrator'),
            ('Inkscape', 'Inkscape'),
            ('Figma', 'Figma'),
            ('Sketch', 'Sketch'),
            ('WebGL', 'WebGL'),
            ('ThreeJS', 'ThreeJS'),
            ('OpenGL', 'OpenGL'),
            ('DirectX', 'DirectX'),
            ('Vulkan', 'Vulkan'),
            ('AR', 'AR'),
            ('VR', 'VR'),
            ('XR', 'XR'),
            ('AI', 'AI'),
            ('ML', 'ML'),
            ('DL', 'DL'),
            ('IOT', 'IOT'),
            ('Blockchain', 'Blockchain'),
            ('Crypto', 'Crypto'),
            ('Blockchain', 'Blockchain'),
            ('Rust', 'Rust'),
            ('Go', 'Go'),
            ('Dart', 'Dart'),
            ('Kotlin', 'Kotlin'),
            ('Swift', 'Swift'),
            ('Objective-C', 'Objective-C'),
        )
    )

    def __str__(self):
        return self.titulo


class RespostasDoUsuario(models.Model):
    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        unique_together = ("usuario", "post", "resposta")

    LIKE = 1
    DISLIKE = -1
    NENHUM = 0

    OPCOES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="votos")
    post = models.ForeignKey(
        PerguntasDoUsuario, on_delete=models.CASCADE, related_name="votos")
    avaliacao = models.SmallIntegerField(choices=OPCOES)
    resposta = models.CharField(max_length=255, blank=True, null=True)


class FotoErro(models.Model):
    class Meta:
        verbose_name = 'Foto de Erro'
        verbose_name_plural = 'Fotos de Erro'

    post = models.ForeignKey(
        PerguntasDoUsuario, on_delete=models.CASCADE, related_name="fotos")
    foto = models.ImageField(
        upload_to="erros/fotos/%Y/%m/%d",
        verbose_name="Fotos do erro"
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.foto:
            resize_image(self.foto, new_width=800)

    def __str__(self):
        return f"Foto do post: {self.post.titulo}"
