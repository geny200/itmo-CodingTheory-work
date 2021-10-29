module Decoder.TestPolar
  ( polarTest,
  )
where

import Decoder.Polar (evenTrim, oddTrim, s, sgn)
import Test.Hspec (SpecWith, describe, hspec, it, shouldBe)

-- | Function for running tests
polarTest :: IO ()
polarTest =
  do
    hspec $ do
      testS
      testSgn
      testOddEven

-- | Unit tests for S.
testS :: SpecWith ()
testS = describe "Task - S" $ do
  it "unit tests for 7" $ do
    s [False, False, False, False, False, False, False] 7 [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2] `shouldBe` (4.0 :: Double)
  it "unit tests for 0 (result)" $ do
    s [] 0 [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2] `shouldBe` (0.3 :: Float)
  it "unit tests for 1" $ do
    s [False] 1 [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2] `shouldBe` (-0.8 :: Rational)
  it "unit tests for 2" $ do
    s [False, False] 2 [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2] `shouldBe` (0.5 :: Double)
  it "unit tests for 3" $ do
    s [False, False, False] 3 [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2] `shouldBe` (1.2 :: Float)
  it "unit tests for 0 (tree)" $ do
    s [False] 0 (oddTrim [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2]) `shouldBe` (-0.3 :: Rational)
    s [False] 0 (evenTrim (evenTrim [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2])) `shouldBe` (1 :: Double)
    s [False] 0 (oddTrim (oddTrim (evenTrim [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2]))) `shouldBe` (-0.5 :: Float)
    s [False] 0 (evenTrim (oddTrim (evenTrim [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2]))) `shouldBe` (0.7 :: Rational)
    s [False] 0 (evenTrim [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2]) `shouldBe` (-0.5 :: Double)
    s [False] 0 (oddTrim (evenTrim [-0.5, 0.5, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0.3, -0.7, 1.5, -2])) `shouldBe` (-0.5 :: Float)

-- | Unit tests for sgn.
testSgn :: SpecWith ()
testSgn = describe "Task - sgn" $ do
  it "unit tests for sgn" $ do
    sgn 4.2 `shouldBe` (1 :: Double)
    sgn 0 `shouldBe` (1 :: Float)
    sgn (-1) `shouldBe` (-1 :: Int)
    sgn (-0.1) `shouldBe` (-1 :: Rational)

-- | Unit tests for Odd/Even.
testOddEven :: SpecWith ()
testOddEven = describe "Task - Odd/Even" $ do
  it "unit tests for odd" $ do
    oddTrim [3, 2, 1, 1, 2, 3, 4, 5 :: Int] `shouldBe` [3, 1, 2, 4]
    oddTrim [1 :: Int] `shouldBe` [1]
    oddTrim ([] :: [Int]) `shouldBe` []
  it "unit tests for even" $ do
    evenTrim [1, 2, 3, 4, 5 :: Int] `shouldBe` [2, 4]
    evenTrim [1 :: Int] `shouldBe` []
    evenTrim ([] :: [Int]) `shouldBe` []
