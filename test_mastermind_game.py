"""
    Kelly Lee
    CS 5001, Fall 2023
    Test Project

"""
import unittest
from mastermind_game import MasterMindGame

class TestMasterMindGame(unittest.TestCase):
    """
    TestMasterMindGame tests the game guesses against the secret code.
    """
    def setUp(self):
        """
        Method -- setUp
            initializes instance of the MasterMindGame and sets the
            first secret code and guesses
        Parameters
            self -- current object
        Returns
            None   
        """
        self.game = MasterMindGame()
        self.game.code = ["green",  "yellow", "red", "blue"] # secret code
        self.game.guesses = ["yellow", "red", "green", "blue"] # user guess
        
    def test_count_bulls_and_cows(self):
        """ 
        Method -- test_count_bulls_and_cows
            tests secret code against the user guesses for correct color/
            correct placement which is the first element of tuple and
            the correct color/incorrect placement which is the second element
        Parameters
            self -- current object
        Returns
            None
        """
        # 1 correct position, 3 correct colors
        outcome1 = self.game.count_bulls_and_cows()
        self.assertEqual(outcome1, (1, 3))

        # 4 correct position
        self.game.guesses = ["green", "yellow", "red", "blue"]
        outcome2 = self.game.count_bulls_and_cows()
        self.assertEqual(outcome2, (4, 0))
        
        # 3 correct positions
        self.game.code = ["purple", "black", "red", "green"]
        self.game.guesses = ["blue", "black", "red", "green"]
        outcome3 = self.game.count_bulls_and_cows()
        self.assertEqual(outcome3, (3, 0))

        # 2 correct colors
        self.game.code = ["blue", "red", "yellow", "green"]
        self.game.guesses = ["black", "purple", "red", "blue"]
        outcome4 = self.game.count_bulls_and_cows()
        self.assertEqual(outcome4, (0, 2))
        
    def test_win_or_lose(self):
        """
        Method -- test_win_or_lose
            tests whether the player wins or loses according to bulls
            and cows
        Parameters
            self -- current object
        Returns
            None
        """
        # does not win, bulls = 1 and cows = 3 (tests first outcome)
        self.assertEqual(self.game.win_or_lose(), False)

    def test_win_or_lose_winning(self):
        """
        Method -- test_win_or_lose_winning
            tests for win given code and guesses are the same
        Parameters
            self -- current object
        Returns
            None
        """
        # wins as bulls = 4
        self.game.code = ["red", "purple", "yellow", "black"]
        self.game.code = self.game.guesses
        self.game.count_bulls_and_cows()
        self.assertEqual(self.game.win_or_lose(), True)
        
if __name__ == "__main__":
    unittest.main(verbosity=3)
