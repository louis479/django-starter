from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Course, Enrollment


class AuthAndCourseFlowTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student1', password='StrongPass123!')
        self.student.profile.role = 'student'
        self.student.profile.save()

        self.instructor = User.objects.create_user(username='instructor1', password='StrongPass123!')
        self.instructor.profile.role = 'instructor'
        self.instructor.profile.save()

        self.course = Course.objects.create(
            title='Intro to Swahili Tech',
            description='A starter course.',
            created_by=self.instructor,
        )

    def test_register_creates_user_with_selected_role(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newstudent',
                'password': 'StrongPass123!',
                'confirm_password': 'StrongPass123!',
                'role': 'student',
            },
        )

        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='newstudent')
        self.assertEqual(user.profile.role, 'student')

    def test_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'student1', 'password': 'StrongPass123!'},
        )

        self.assertRedirects(response, reverse('dashboard'))

    def test_student_can_enroll_in_course(self):
        self.client.login(username='student1', password='StrongPass123!')

        response = self.client.get(reverse('enroll', args=[self.course.id]))

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(
            Enrollment.objects.filter(user=self.student, course=self.course).exists()
        )

    def test_student_cannot_access_create_course(self):
        self.client.login(username='student1', password='StrongPass123!')

        response = self.client.get(reverse('create_course'))

        self.assertRedirects(response, reverse('dashboard'))

    def test_instructor_can_create_course(self):
        self.client.login(username='instructor1', password='StrongPass123!')

        response = self.client.post(
            reverse('create_course'),
            {
                'title': 'Advanced UI Design',
                'description': 'Make the platform feel polished.',
            },
        )

        self.assertRedirects(response, reverse('courses'))
        self.assertTrue(Course.objects.filter(title='Advanced UI Design').exists())
