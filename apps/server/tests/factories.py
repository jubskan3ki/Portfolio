"""Factories factory_boy pour les tests."""

from datetime import UTC, date, datetime, timedelta

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.django import DjangoModelFactory

from core.articles.models import Article, Category, Tag
from core.audit.models import AuditLog
from core.contact.models import FAQ, Contact, ContactInfo
from core.experiences.models import Experience, ExperienceType
from core.projects.models import Project, ProjectCategory, ProjectStatus
from core.stacks.models import Stack, StackCategory, StackResource
from core.webhooks.models import Webhook, WebhookDelivery

User = get_user_model()


# ── User ──


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    is_active = True
    is_staff = False
    is_superuser = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "TestPassword123!")
        user = model_class(*args, **kwargs)
        user.set_password(password)
        user.save()
        return user


class AdminFactory(UserFactory):
    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    is_staff = True
    is_superuser = True


# ── Articles ──


class ArticleCategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))
    description = "Une categorie de test"


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f"Tag {n}")


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Sequence(lambda n: f"Article {n}")
    slug = factory.LazyAttribute(lambda o: o.title.lower().replace(" ", "-"))
    excerpt = "Un article de test"
    content = factory.LazyFunction(lambda: [{"type": "paragraph", "content": "Contenu de test"}])
    category = factory.SubFactory(ArticleCategoryFactory)
    read_time = 5
    is_published = True
    published_date = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def tags(self, create, extracted, **_kwargs):
        if not create or not extracted:
            return
        self.tags.add(*extracted)


# ── Projects ──


class ProjectCategoryFactory(DjangoModelFactory):
    class Meta:
        model = ProjectCategory

    name = factory.Sequence(lambda n: f"Project Category {n}")
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))


class ProjectStatusFactory(DjangoModelFactory):
    class Meta:
        model = ProjectStatus

    name = factory.Sequence(lambda n: f"Status {n}")


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Sequence(lambda n: f"Project {n}")
    slug = factory.LazyAttribute(lambda o: o.title.lower().replace(" ", "-"))
    description = "Un projet de test"
    category = factory.SubFactory(ProjectCategoryFactory)


# ── Stacks ──


class StackCategoryFactory(DjangoModelFactory):
    class Meta:
        model = StackCategory

    name = factory.Sequence(lambda n: f"Stack Category {n}")
    description = "Description test"


class StackFactory(DjangoModelFactory):
    class Meta:
        model = Stack

    name = factory.Sequence(lambda n: f"Stack {n}")
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))
    description = "Un stack de test"
    category = factory.SubFactory(StackCategoryFactory)
    level = 3.0
    started_date = factory.LazyFunction(
        lambda: datetime.now(tz=UTC).date() - timedelta(days=730),
    )


class StackResourceFactory(DjangoModelFactory):
    class Meta:
        model = StackResource

    stack = factory.SubFactory(StackFactory)
    title = factory.Sequence(lambda n: f"Resource {n}")
    description = "Une ressource de test"
    url = "https://example.com/resource"
    type = "documentation"


# ── Experiences ──


class ExperienceTypeFactory(DjangoModelFactory):
    class Meta:
        model = ExperienceType

    name = factory.Sequence(lambda n: f"Experience Type {n}")
    icon = "test-icon"


class ExperienceFactory(DjangoModelFactory):
    class Meta:
        model = Experience

    title = factory.Sequence(lambda n: f"Experience {n}")
    company = "Test Company"
    location = "Paris, France"
    type = factory.SubFactory(ExperienceTypeFactory)
    start_date = factory.LazyFunction(lambda: date(2023, 1, 1))
    end_date = factory.LazyFunction(lambda: date(2024, 1, 1))
    description = "Une experience de test"


# ── Contact ──


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = "Test User"
    email = factory.Sequence(lambda n: f"contact{n}@example.com")
    subject = "Test Subject"
    message = "Un message de test"
    reference_id = factory.Sequence(lambda n: f"REF-{n:06d}")


class FAQFactory(DjangoModelFactory):
    class Meta:
        model = FAQ

    question = factory.Sequence(lambda n: f"Question {n}?")
    answer = "Une reponse de test"
    is_published = True


class ContactInfoFactory(DjangoModelFactory):
    class Meta:
        model = ContactInfo

    email = "contact@example.com"


# ── Audit ──


class AuditLogFactory(DjangoModelFactory):
    class Meta:
        model = AuditLog

    action = "create"
    model_name = "Article"
    object_id = "1"
    object_repr = "Test Object"


# ── Webhooks ──


class WebhookFactory(DjangoModelFactory):
    class Meta:
        model = Webhook

    name = factory.Sequence(lambda n: f"Webhook {n}")
    url = "https://example.com/webhook"
    events = factory.LazyFunction(lambda: ["article.created", "project.created"])
    created_by = factory.SubFactory(AdminFactory)


class WebhookDeliveryFactory(DjangoModelFactory):
    class Meta:
        model = WebhookDelivery

    webhook = factory.SubFactory(WebhookFactory)
    event_type = "article.created"
    payload = factory.LazyFunction(lambda: {"test": "data"})
