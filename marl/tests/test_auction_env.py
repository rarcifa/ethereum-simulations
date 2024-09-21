import unittest
from marl.auction_simulation import AuctionEnv

class TestAuctionEnv(unittest.TestCase):
    """
    Unit test class for the AuctionEnv environment.
    Contains tests to validate the functionality of the AuctionEnv class.
    """

    def setUp(self):
        """
        Initializes a new instance of AuctionEnv and resets it before each test case.
        """
        self.env = AuctionEnv()
        self.env.reset()

    def test_reset(self):
        """
        Tests the reset functionality of the environment.
        Ensures that the environment is initialized to a default state with 
        correct time remaining, highest bid, and personal funds.
        """
        state = self.env.reset()
        self.assertEqual(state['time_remaining'], 10)
        self.assertEqual(state['highest_bid'][0], 0)
        self.assertEqual(state['personal_funds'][0], 100)

    def test_no_bid_action(self):
        """
        Tests the environment behavior when no bid is placed (action 0).
        Ensures that the highest bid remains at 0, no reward is given, the time is decremented,
        and the auction is not yet finished.
        """
        state, reward, done, _ = self.env.step(0)
        self.assertEqual(state['highest_bid'][0], 0)
        self.assertEqual(reward, 0)
        self.assertFalse(done)
        self.assertEqual(state['time_remaining'], 9) 

    def test_small_bid_action(self):
        """
        Tests the environment behavior when a small bid is placed (action 1).
        Verifies that the highest bid is updated, the reward is negative (penalty for spending),
        and the time is decremented as expected.
        """
        state, reward, done, _ = self.env.step(1)
        self.assertEqual(state['highest_bid'][0], 5)
        self.assertEqual(reward, -1)  
        self.assertFalse(done)
        self.assertEqual(state['time_remaining'], 9)  

    def test_auction_end_by_time_exhaustion(self):
        """
        Simulates the auction environment until the time runs out.
        Ensures that the auction finishes when time is exhausted and 
        verifies the time remaining is 0 at the end.
        """
        done = False
        while not done:
            state, reward, done, _ = self.env.step(1)
        self.assertTrue(done)
        self.assertEqual(state['time_remaining'], 0)

if __name__ == '__main__':
    unittest.main()
