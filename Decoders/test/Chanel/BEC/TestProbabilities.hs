module Chanel.BEC.TestProbabilities
  ( probabilitiesTest,
  )
where

import Chanel.BEC.Probabilities (frozenBits, toProbability)
import Test.Hspec (SpecWith, describe, hspec, it, shouldBe)

-- | Function for running tests
probabilitiesTest :: IO ()
probabilitiesTest =
  do
    hspec $ do
      testFrozenBits

-- | Unit tests for frozenBits.
testFrozenBits :: SpecWith ()
testFrozenBits = describe "Task - frozenBits" $ do
  it "unit tests for frozenBits" $ do
    frozenBits (toProbability (0.5 :: Double)) 3 2 `shouldBe` [0, 1, 2, 4]
    frozenBits (toProbability (0.5 :: Double)) 4 3 `shouldBe` [0, 1, 2, 3, 4, 5, 6, 8]
