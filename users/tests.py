from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

class UserViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')



    def test_register_view_post_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_view_post_valid(self):
        self.client.login(username='testuser', password='testpasswo34rd')
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'image': ''
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')

    def test_logout_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)