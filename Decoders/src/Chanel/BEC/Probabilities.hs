module Chanel.BEC.Probabilities
  ( probability,
    toProbability,
    frozenBits,
  )
where

import Data.List (sort)

data Tree a
  = Branch (Tree a) (Tree a)
  | Leaf a

newtype Probability a = P a

-- | Wrap the value to @Probability@,
-- and check that the value is in the range [0, 1].
toProbability :: (Fractional a, Ord a) => a -> Probability a
toProbability v
  | (0 <= v) && (v <= 1) = P v
  | otherwise = error "Probability should be in the range [0, 1]"

growTree :: (Fractional a) => Tree a -> Tree a
growTree (Leaf v) = Branch (Leaf (v ^^ (2 :: Int))) (Leaf (2 * v - v ^^ (2 :: Int)))
growTree (Branch l r) = Branch (growTree l) (growTree r)

toList :: (Fractional a) => Tree a -> [a]
toList (Leaf v) = [v]
toList (Branch l r) = toList l ++ toList r

probabilityTree :: (Fractional a) => Int -> a -> Tree a
probabilityTree 0 = Leaf
probabilityTree n = growTree . probabilityTree (n - 1)

-- | Returns the erasure probabilities for each bit.
probability :: (Fractional a) => Probability a -> Int -> [a]
probability (P prob) n = toList (probabilityTree n prob)

getKMin :: (Ord a) => [a] -> Int -> [a]
getKMin list k = take k (reverse . sort $ list)

-- | Returns the numbers of frozen bits.
frozenBits ::
  (Ord a, Fractional a) =>
  Probability a -> -- Probability of erasure
  Int -> -- N - code length
  Int -> -- K - dimension
  [Int] --
frozenBits prob n k =
  let lengthFrozen = (2 ^ n - 2 ^ k)
      probabilities = reverse (probability prob n) `zip` ([0 ..] :: [Int])
      frozenNums = map snd (getKMin probabilities lengthFrozen)
   in sort frozenNums
