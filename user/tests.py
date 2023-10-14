from django.test import TestCase
from user.models import User, Battle

# Battle Tests
class BattleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@example.com', 'testtest')
        Battle.objects.create(challenger="ditto", defender="gengar", winner="gengar", user=self.user)
        Battle.objects.create(challenger="gengar", defender="lucario", winner="lucario", user=self.user)
        Battle.objects.create(challenger="lucario", defender="ditto", winner="lucario", user=self.user)

    def test_user_has_battle_history(self):
        """User should have all previous battle he has done"""
        battles = Battle.objects.all()
        self.assertEqual(len(battles), 3)
        self.assertEqual(battles[0].user.username, "test")

    def test_battle_has_correct_properties(self):
        """User should have all previous battle he has done"""
        battle = Battle.objects.filter().last()
        self.assertNotEqual(battle.defender, None)
        self.assertNotEqual(battle.challenger, None)
        self.assertNotEqual(battle.winner, None)