from django.contrib.auth.models import User
from django.core.serializers import json
from django.test import TestCase, Client
from django.urls import reverse
import json

from Meeting.models import *

# Create your tests here.


class BaseTestCase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.client = Client()
        self.m = Meeting()
        self.m.save()
        self.old_ts = TokenSet(meeting=self.m)
        self.old_ts.save()
        self.ts = TokenSet(meeting=self.m)
        self.ts.save()
        self.admin = User()
        self.admin.is_superuser = True
        self.admin.save()


class ManagementInterfaceCases(BaseTestCase):
    def setUp(self):
        super(ManagementInterfaceCases, self).setUp()
        self.client.force_login(self.admin)
        pass

    def test_create_yna_vote(self):
        x = Vote.objects.count()
        result = self.client.post(reverse('meeting/new_vote', args=[self.m.id]), {'name': 'name',
                        'description':'description',
                        'method':Vote.YES_NO_ABS})
        self.assertEqual(x+1, Vote.objects.count())
        v = Vote.objects.first()
        self.assertEqual(v.name, 'name')
        self.assertEqual(v.description, 'description')
        self.assertEqual(v.method, Vote.YES_NO_ABS)
        self.assertEqual(v.state, Vote.READY)
        self.assertEqual(v.token_set, self.ts)
        self.assertListEqual(list(v.option_set.all().values_list('name', flat=True)), ['abs', 'no', 'yes'])

    def test_create_stv_vote(self):
        x = Vote.objects.count()
        result = self.client.post(reverse('meeting/new_vote', args=[self.m.id]), {'name': 'name',
                        'description':'description',
                        'method':Vote.STV})
        self.assertEqual(x+1, Vote.objects.count())
        v = Vote.objects.first()
        self.assertEqual(v.name, 'name')
        self.assertEqual(v.description, 'description')
        self.assertEqual(v.method, Vote.STV)
        self.assertEqual(v.state, Vote.READY)
        self.assertEqual(v.token_set, self.ts)
        self.assertEqual(v.option_set.count(), 0)

    def test_add_vote_option_YNA(self):
        v = Vote(name='name', token_set=self.ts, method=Vote.YES_NO_ABS)
        v.save()
        request_args = [reverse('meeting/add_vote_option', args=[self.m.id, v.id]),
                        {'name': 'name'}]
        result = self.client.post(*request_args)
        self.assertJSONEqual(result.content, json.dumps({'result': 'failure'}))
        self.assertEqual(3, v.option_set.count())

    def test_add_vote_option_non_ready_state(self):
        cant_add_option_states = [x[0] for x in Vote.states]
        cant_add_option_states.remove(Vote.READY)
        for s in cant_add_option_states:
            v = Vote(name='name', token_set=self.ts, method=Vote.STV, state=s)
            v.save()
            request_args = [reverse('meeting/add_vote_option', args=[self.m.id, v.id]),
                            {'name': 'name'}]
            result = self.client.post(*request_args)
            self.assertJSONEqual(result.content, json.dumps({'result': 'failure'}))
            self.assertEqual(0, v.option_set.count())

    def test_add_vote_option_predicted_success(self):
        v = Vote(name='name', token_set=self.ts, method=Vote.STV)
        v.save()
        request_args = [reverse('meeting/add_vote_option', args=[self.m.id, v.id]),
                        {'name': 'name'}]
        result = self.client.post(*request_args)
        self.assertJSONEqual(result.content, json.dumps({'result': 'success',
                                                         'id': v.option_set.first().id}))
        self.assertEqual(1, v.option_set.count())

    def test_remove_vote_option_YNA(self):
        v = Vote(name='name', token_set=self.ts, method=Vote.YES_NO_ABS)
        v.save()
        request_args = [reverse('meeting/remove_vote_option', args=[self.m.id, v.id]),
                        {'id': v.id}]
        result = self.client.post(*request_args)
        self.assertJSONEqual(result.content, json.dumps({'result': 'failure'}))
        self.assertEqual(3, v.option_set.count())

    def test_remove_vote_option_non_ready_state(self):
        cant_add_option_states = [x[0] for x in Vote.states]
        cant_add_option_states.remove(Vote.READY)
        for s in cant_add_option_states:
            v = Vote(name='name', token_set=self.ts, method=Vote.STV, state=s)
            v.save()
            Option(name='name', vote=v).save()
            self.assertEqual(1, v.option_set.count())
            request_args = [reverse('meeting/remove_vote_option', args=[self.m.id, v.id]),
                            {'id': v.option_set.first().id}]
            result = self.client.post(*request_args)
            self.assertJSONEqual(result.content, json.dumps({'result': 'failure'}))
            self.assertEqual(1, v.option_set.count())

    def test_remove_vote_option_predicted_success(self):
        v = Vote(name='name', token_set=self.ts, method=Vote.STV)
        v.save()
        Option(name='name', vote=v).save()
        self.assertEqual(1, v.option_set.count())
        request_args = [reverse('meeting/remove_vote_option', args=[self.m.id, v.id]),
                        {'id': v.option_set.first().id}]
        result = self.client.post(*request_args)
        self.assertJSONEqual(result.content, json.dumps({'result': 'success'}))
        self.assertEqual(0, v.option_set.count())



class TallyingYNACases(TestCase):
    def setUp(self):
        pass



class TallyingSTVCases(TestCase):
    def setUp(self):
        pass