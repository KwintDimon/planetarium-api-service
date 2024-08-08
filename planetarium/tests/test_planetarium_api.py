from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import (
    AstronomyShow, ShowSession, PlanetariumDome, ShowTheme
)
from planetarium.serializers import (
    AstronomyShowListSerializer, AstronomyShowDetailSerializer
)

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")
SHOW_SESSION_URL = reverse("planetarium:showsession-list")


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample show",
        "description": "Sample description",
    }
    defaults.update(params)

    return AstronomyShow.objects.create(**defaults)


def sample_show_session(**params):
    dome = PlanetariumDome.objects.create(
        name="Main Dome", rows=10, seats_in_row=15
    )

    defaults = {
        "show_time": "2023-09-01 20:00:00",
        "astronomy_show": None,
        "planetarium_dome": dome,
    }
    defaults.update(params)

    return ShowSession.objects.create(**defaults)


def detail_url(astronomy_show_id):
    return reverse("planetarium:astronomyshow-detail", args=[astronomy_show_id])


class UnauthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_astronomy_shows(self):
        sample_astronomy_show()
        sample_astronomy_show()

        res = self.client.get(ASTRONOMY_SHOW_URL)

        astronomy_shows = AstronomyShow.objects.order_by("id")
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_astronomy_shows_by_themes(self):
        theme1 = ShowTheme.objects.create(name="Theme 1")
        theme2 = ShowTheme.objects.create(name="Theme 2")

        show1 = sample_astronomy_show(title="Show 1")
        show2 = sample_astronomy_show(title="Show 2")

        show1.themes.add(theme1)
        show2.themes.add(theme2)

        show3 = sample_astronomy_show(title="Show without themes")

        res = self.client.get(
            ASTRONOMY_SHOW_URL, {"themes": f"{theme1.id},{theme2.id}"}
        )

        serializer1 = AstronomyShowListSerializer(show1)
        serializer2 = AstronomyShowListSerializer(show2)
        serializer3 = AstronomyShowListSerializer(show3)

        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_filter_astronomy_shows_by_title(self):
        show1 = sample_astronomy_show(title="Show")
        show2 = sample_astronomy_show(title="Another Show")
        show3 = sample_astronomy_show(title="No match")

        res = self.client.get(ASTRONOMY_SHOW_URL, {"title": "show"})

        serializer1 = AstronomyShowListSerializer(show1)
        serializer2 = AstronomyShowListSerializer(show2)
        serializer3 = AstronomyShowListSerializer(show3)

        results_data = res.data["results"]

        self.assertTrue(any(item == serializer1.data for item in results_data))
        self.assertTrue(any(item == serializer2.data for item in results_data))
        self.assertFalse(any(item == serializer3.data for item in results_data))

    def test_retrieve_astronomy_show_detail(self):
        show = sample_astronomy_show()
        show.themes.add(ShowTheme.objects.create(name="Theme"))

        url = detail_url(show.id)
        res = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(show)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_astronomy_show_forbidden(self):
        payload = {
            "title": "Show",
            "description": "Description",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_astronomy_show(self):
        payload = {
            "title": "Show",
            "description": "Description",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        show = AstronomyShow.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(show, key))

    def test_create_astronomy_show_with_themes(self):
        theme1 = ShowTheme.objects.create(name="Educational")
        theme2 = ShowTheme.objects.create(name="Science Fiction")
        payload = {
            "title": "Space Odyssey",
            "themes": [theme1.id, theme2.id],
            "description": "A journey through the cosmos.",
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        show = AstronomyShow.objects.get(id=res.data["id"])
        themes = show.themes.all()
        self.assertEqual(themes.count(), 2)
        self.assertIn(theme1, themes)
        self.assertIn(theme2, themes)


class NotAdminAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.astronomy_show = sample_astronomy_show()
        self.show_session = sample_show_session(astronomy_show=self.astronomy_show)

    def test_put_astronomy_show_not_allowed(self):
        payload = {
            "title": "New show",
            "description": "New description",
        }

        show = sample_astronomy_show()
        url = detail_url(show.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_astronomy_show_not_allowed(self):
        show = sample_astronomy_show()
        url = detail_url(show.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
