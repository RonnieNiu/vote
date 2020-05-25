import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice
# Create your tests here.

#class QuestionModelTests(TestCase):
#    def test_was_published_recently_with_future_question(self):
#        time = timezone.now() + datetime.timedelta(days=20)
#        future_question = Question(pub_date=time)
#        '''was_published_recently return False for Questiona whose pub_date is 
#        in future'''
#        self.assertIs(future_question.was_published_recently(), False)
#
#    def test_was_published_recently_with_old_question(self):
#        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
#        old_question = Question(pub_date=time)
#        '''was_published_recently return False for Questiona whose pub_date is 
#        in old'''
#        self.assertIs(old_question.was_published_recently(), False)
#    
#    def test_was_published_recently_with_current_question(self):
#        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
#        current_question = Question(pub_date=time)
#        '''was_published_recently return False for Questiona whose pub_date within current 
#        '''
#        self.assertIs(current_question.was_published_recently(), True)
#        
#
def create_question(question_content,pub_date):
    time = timezone.now() + datetime.timedelta(days=pub_date)
    return Question.objects.create(question_text=question_content,pub_date=time)


class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    
    def test_past_questions(self):
        create_question(question_content="past question", pub_date=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context["latest_question_list"], ["<Question: past question>"])

    
    def test_future_questions(self):
        create_question(question_content="future question", pub_date=10)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    
    def test_future_questions_and_past_question(self):
        create_question(question_content="future question", pub_date=10)
        create_question(question_content="past question", pub_date=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context["latest_question_list"], ["<Question: past question>"])

    def test_two_past_question(self):
        create_question(question_content="past question1", pub_date=-15)
        create_question(question_content="past question2", pub_date=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context["latest_question_list"], ["<Question: past question2>", "<Question: past question1>"])


class QuestionDetailViewTests(TestCase):
    
    def test_future_questions(self):
        future_question = create_question(question_content="future question", pub_date=10)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        past_question = create_question(question_content="past question", pub_date=-10)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    
    def test_future_questions(self):
        future_question = create_question(question_content="future question", pub_date=10)
        response = self.client.get(reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        past_question = create_question(question_content="past question", pub_date=-10)
        past_choice = Choice.objects.create(question=past_question, choice_text="past choice")
        response = self.client.get(reverse('polls:results', args=(past_question.id,)))

        self.assertContains(response, past_choice.choice_text)
