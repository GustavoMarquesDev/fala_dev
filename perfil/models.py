from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone

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
        ordering = ['-data_de_criacao']

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usuario_response")
    post = models.ForeignKey(
        PerguntasDoUsuario, on_delete=models.CASCADE, related_name="votos")
    resposta = models.TextField(blank=True, null=True)
    data_de_criacao = models.DateTimeField(default=timezone.now)
    imagem = models.ImageField(
        upload_to="respostas/fotos/%Y/%m/%d",
        verbose_name="Foto de resposta",
        blank=True, null=True,
        help_text='Foto de resposta a ser exibida para todos os usuários '
    )

    def __str__(self):
        return f"Resposta do usuário: {self.usuario.username}"

    @property
    def total_likes(self):
        """Retorna o total de likes da resposta"""
        return self.avaliacoes.filter(tipo_avaliacao=AvaliacaoResposta.LIKE).count()  # type: ignore

    @property
    def total_dislikes(self):
        """Retorna o total de dislikes da resposta"""
        return self.avaliacoes.filter(tipo_avaliacao=AvaliacaoResposta.DISLIKE).count()  # type: ignore

    @property
    def score_total(self):
        """Retorna o score total (likes - dislikes)"""
        return self.total_likes - self.total_dislikes


class AvaliacaoResposta(models.Model):
    class Meta:
        verbose_name = 'Avaliação de Resposta'
        verbose_name_plural = 'Avaliações de Respostas'
        unique_together = ("usuario", "resposta")

    LIKE = 1
    DISLIKE = -1

    TIPOS_AVALIACAO = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="avaliacoes_usuario")
    resposta = models.ForeignKey(
        RespostasDoUsuario, on_delete=models.CASCADE, related_name="avaliacoes")
    tipo_avaliacao = models.SmallIntegerField(
        choices=TIPOS_AVALIACAO, verbose_name="Tipo de Avaliação")
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tipo = "Like" if self.tipo_avaliacao == self.LIKE else "Dislike"
        return f"{tipo} de {self.usuario.username} em {self.resposta}"


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
            resize_image(self.foto, new_width=600)

    def __str__(self):
        return f"Foto do post: {self.post.titulo}"


class RespostaDaResposta(models.Model):
    class Meta:
        verbose_name = 'Resposta da Resposta'
        verbose_name_plural = 'Respostas da Resposta'
        unique_together = ("usuario", "resposta")
        ordering = ['-data_de_criacao']

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resposta_da_resposta_usuario")
    resposta = models.ForeignKey(
        RespostasDoUsuario, on_delete=models.CASCADE, related_name="resposta_da_resposta")
    texto_resposta = models.TextField(blank=True, null=True)
    data_de_criacao = models.DateTimeField(default=timezone.now)
    imagem = models.ImageField(
        upload_to="respostas/fotos/%Y/%m/%d",
        verbose_name="Foto de resposta",
        blank=True, null=True,
        help_text='Foto de resposta a ser exibida para todos os usuários '
    )

    @property
    def total_likes(self):
        """Retorna o total de likes da resposta"""
        return self.avaliacoes.filter(tipo_avaliacao=AvaliacaoResposta.LIKE).count()

    @property
    def total_dislikes(self):
        """Retorna o total de dislikes da resposta"""
        return self.avaliacoes.filter(tipo_avaliacao=AvaliacaoResposta.DISLIKE).count()

    @property
    def score_total(self):
        """Retorna o score total (likes - dislikes)"""
        return self.total_likes - self.total_dislikes

    def __str__(self):
        return f"Resposta da resposta: {self.usuario.username}"


class AvaliacaoRespostaDaResposta(models.Model):
    class Meta:
        verbose_name = 'Avaliação de Resposta da Resposta'
        verbose_name_plural = 'Avaliações de Respostas da Resposta'
        unique_together = ("usuario", "resposta")

    LIKE = 1
    DISLIKE = -1

    TIPOS_AVALIACAO = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usuario_avaliacao_resposta_da_resposta")
    resposta = models.ForeignKey(
        RespostaDaResposta, on_delete=models.CASCADE, related_name="avaliacoes")
    tipo_avaliacao = models.SmallIntegerField(
        choices=TIPOS_AVALIACAO, verbose_name="Tipo de Avaliação")
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tipo = "Like" if self.tipo_avaliacao == self.LIKE else "Dislike"
        return f"{tipo} de {self.usuario.username} em {self.resposta}"


class Notificacao(models.Model):
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-criado_em']

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notificacoes")
    pergunta = models.ForeignKey(
        PerguntasDoUsuario, on_delete=models.CASCADE, related_name="notificacoes")
    resposta = models.ForeignKey(
        RespostasDoUsuario, on_delete=models.CASCADE, related_name="notificacoes")
    lida = models.BooleanField(default=False, verbose_name='Lida')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario.username} - {self.pergunta.titulo[:50]}"
